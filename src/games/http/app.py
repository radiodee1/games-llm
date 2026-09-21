
from flask import Flask, render_template, jsonify, send_file
import subprocess
import threading
import queue
import os
import time
import signal
import io 

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

app = Flask(__name__)

#CSV_FILE = os.path.abspath('../pic/')
CSV_PATH = os.path.expanduser('~') + "/workspace/VJEPA2_FILES/demo/pic/"
PNG_FILE = os.path.abspath("../pic/figure_0.png")
PYTHON_APP = os.path.abspath("../main.py")  #"notebooks.vjepa2_demo_cpu" 
KEY_VALUE = 'vitl'
VIDEO_VALUE = '4'
PLUGIN_VALUE = 'ssv'
MODEL_VALUE = 'vjepa'
PYTHON_APP_ARRAY = [ i for i in ('uv run python -u ' + PYTHON_APP +' --model ' + MODEL_VALUE + ' --plugin ' + PLUGIN_VALUE + ' --inverse_size 4 --video ' + VIDEO_VALUE + ' --no_pic --key ' + KEY_VALUE).split(' ') ]
TARGET_DIR = os.path.abspath("..")

process = None
output_queue = queue.Queue()
process_lock = threading.Lock()


def read_output(proc):
    """Read output from the Python app and place it in a queue."""
    for line in iter(proc.stdout.readline, ''):
        output_queue.put(line)

    proc.stdout.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/image")
def image():
    """Return the current PNG file."""
    return send_file(PNG_FILE, mimetype="image/png")


@app.route("/start", methods=["POST"])
def start():
    global process

    with process_lock:
        if process is not None and process.poll() is None:
            return jsonify({"status": "already running"})

        process = subprocess.Popen(
            PYTHON_APP_ARRAY,
            cwd=TARGET_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        threading.Thread(
            target=read_output,
            args=(process,),
            daemon=True
        ).start()

    return jsonify({"status": "started"})

@app.route("/graph/<foldername>")
def graph(foldername):

    try:
        # Read CSV
        csv_path = CSV_PATH  + foldername + '/csv_' + KEY_VALUE + '_' + foldername + '.csv.1.csv'
        df = pd.read_csv(csv_path, header=None)

        if len(df.columns) < 2:
            return "CSV must contain at least two columns", 400

        y = df.iloc[0, :]

        x = [ i for i in range(len(y))]
        
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(
            x,
            y,
            marker="o",
            linewidth=2
        )

        ax.set_ylabel('Loss')
        ax.set_xlabel('Batches')

        ax.set_title("CSV Data - " + foldername)

        ax.grid(True)

        fig.tight_layout()

        # Write PNG into memory instead of creating a file
        image_data = io.BytesIO()

        fig.savefig(
            image_data,
            format="png",
            dpi=100
        )

        plt.close(fig)

        image_data.seek(0)

        return send_file(
            image_data,
            mimetype="image/png"
        )

    except FileNotFoundError:

        return "CSV file not found: " + csv_path, 404

    except Exception as e:

        return "Error creating graph: " + str(e), 500



@app.route("/stop", methods=["POST"])
def stop():
    global process

    with process_lock:
        if process is not None and process.poll() is None:
            process.terminate()

            try:
                process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                process.kill()

            output_queue.put("[Server] Python app stopped.\n")
            return jsonify({"status": "stopped"})

    return jsonify({"status": "not running"})


@app.route("/output")
def output():
    """Return any new output from the Python app."""
    lines = []

    while True:
        try:
            lines.append(output_queue.get_nowait())
        except queue.Empty:
            break

    return jsonify({
        "output": "".join(lines),
        "running": process is not None and process.poll() is None
    })

@app.route("/image_info")
def image_info():
    """Return the PNG modification time."""
    try:
        modified = os.path.getmtime(PNG_FILE)
        return jsonify({"modified": modified})
    except FileNotFoundError:
        return jsonify({"modified": 0})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
