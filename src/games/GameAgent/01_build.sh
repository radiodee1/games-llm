## you may need to remove the .venv folder and run this script again.
## this could help with issues like installing python 3.10
## rm .venv -fr

## or try
## uv venv --python 3.10

uv init
uv sync
uv build
