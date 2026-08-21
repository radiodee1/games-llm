# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import json
import os
import subprocess
import copy
import random
import glob

import numpy as np
import torch
import torch.nn.functional as F
from decord import VideoReader
from transformers import AutoModel, AutoVideoProcessor
import torch.nn as nn

import src.datasets.utils.video.transforms as video_transforms
import src.datasets.utils.video.volume_transforms as volume_transforms
from src.models.attentive_pooler import AttentiveClassifier
from src.models.vision_transformer import vit_giant_xformers_rope, vit_large_rope

from .vjepa2_classifier_cpu import  train_simple, show_shape, checkpoint_options, show_keys, eval_simple
import argparse

IMAGENET_DEFAULT_MEAN = (0.485, 0.456, 0.406)
IMAGENET_DEFAULT_STD = (0.229, 0.224, 0.225)

old_num_classes = 174 
num_classes =  6 ## 174 
out_classifier = None
classifier = None
hidden_dim = 0  
torch.set_default_device('cpu')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_pt = None
demo_weights = True
image_span = 1 #2 ## must be 1 or more 
video_list = []
image_batch_size = 2 #1  # 2 # 4 
choose_img = []
change_hidden_dim = True
args_foldername = 'train'
home_dir = os.path.expanduser('~')
LOCAL_FILE_STORE = 'workspace/VJEPA2_FILES/demo/'
output_path_filenumber = 0 
output_path = os.path.join(home_dir, LOCAL_FILE_STORE, "vjepa2_vitl_ckpt_classifier.pt")
output_path_list = glob.glob(output_path + '*')
if len(output_path_list) > 0:
    output_path_filenumber = len(output_path_list)
output_path_list.sort()  
VIDEO_PONG_CLASSES = {} # json.load(open(os.path.join(home_dir, LOCAL_FILE_STORE, "pic/" + args_foldername + "/video_image_label.json"), "r"))

encoder_flag = False
eval_flag = False
classifier_flag = False

#facebook/vjepa2-vitl-fpc64-256
PT_FILENAME = {
    'vitl': ['ssv2-vitl-16x2x3.pt',   'facebook/vjepa2-vitl-fpc16-256-ssv2', 'vitl.pt' ],
    'vitg': ['ssv2-vitg-384-64x2x3.pt', 'facebook/vjepa2-vitg-fpc64-384', 'vitg-384.pt' ]
}
pt_key = 'vitl'

def load_pretrained_vjepa_pt_weights_vitg(model, pretrained_weights):
    global encoder_flag 
    # Load weights of the VJEPA2 encoder
    # The PyTorch state_dict is already preprocessed to have the right key names
    if encoder_flag == True:
        print('model is not None')
        return
    pretrained_dict = torch.load(pretrained_weights, weights_only=True, map_location="cpu")["encoder"]
    #show_keys(pretrained_dict)
    print(pt_key)

    pretrained_dict = {k.replace("module.", ""): v for k, v in pretrained_dict.items()}
    pretrained_dict = {k.replace("backbone.", ""): v for k, v in pretrained_dict.items()}
    
    
    msg = model.load_state_dict(pretrained_dict, strict=False)
    #print(pretrained_dict, '\n-----')
    print("Pretrained weights found at {} and loaded with msg: {}".format(pretrained_weights, msg))
    encoder_flag = True

def load_pretrained_vjepa_pt_weights_vitl(model, model_path=''):
    global encoder_flag
    print(model_path, 'model_path')
    if encoder_flag == True:
        print('model not None')
        return
    pretrained_dict = torch.load(model_path, weights_only=True, map_location="cpu")["encoder"]
    pretrained_dict = {k.replace("module.", ""): v for k, v in pretrained_dict.items()}
    pretrained_dict = {k.replace("backbone.", ""): v for k, v in pretrained_dict.items()}
    msg = model.load_state_dict(pretrained_dict, strict=False)
    print(msg, 'msg vitl')
    #print(pretrained_dict, '\n-----')
    encoder_flag = True


def load_pretrained_vjepa_classifier_weights(classifier):
    global demo_weights, output_path_list, classifier_flag
    save_weights = False

    if classifier_flag == True:
        print('load classifier no')
        return classifier
    weight_path_custom = os.path.join(home_dir, LOCAL_FILE_STORE, 'vjepa2_' + pt_key + '_custom_classifier.pt')
    weight_path_pretrain = os.path.join(home_dir, LOCAL_FILE_STORE , PT_FILENAME[pt_key][0] )# 'ssv2-vitg-384-64x2x3.pt')
    weight_path_ckpt =  os.path.join(home_dir, LOCAL_FILE_STORE, "vjepa2_" + pt_key + "_ckpt_classifier.pt")

    if len(output_path_list) > 0:
        weight_path_ckpt = output_path_list[-1]

    weight_path_used = ''
    if os.path.exists(weight_path_ckpt):
        pretrained_dict = torch.load(weight_path_ckpt, weights_only=True, map_location="cpu")
        weight_path_used = weight_path_ckpt
        print('checkpoint', weight_path_ckpt)
    elif os.path.exists(weight_path_custom):
        pretrained_dict = torch.load(weight_path_custom, weights_only=True, map_location="cpu")
        weight_path_used = weight_path_custom
        print('not trained')
    else:
        pretrained_dict = torch.load(weight_path_pretrain, weights_only=True, map_location="cpu")["classifiers"][0]
        weight_path_used = weight_path_pretrain
        print('pretrained')

    pretrained_dict = edit_weights(pretrained_dict)
    print('before del')
    #show_keys(pretrained_dict)
    print(weight_path_used, 'weight_path_used')

    if 'linear.weight' not in  pretrained_dict or pretrained_dict['linear.weight'].shape[0] != num_classes:
        print('adjust num_classes')
        pretrained_dict_a = classifier.state_dict()
        pretrained_dict_a = edit_weights(pretrained_dict_a, True)
       
        msg = classifier.load_state_dict(pretrained_dict_a, strict=False)
        print('msg', msg)
        print('classifier.state_dict()')
        #show_keys(classifier.state_dict())
        pretrained_dict = classifier.state_dict()

        save_weights = True
    else:
        print('no adjust num_classes')

        #show_keys(pretrained_dict) 

        msg = classifier.load_state_dict(pretrained_dict, strict=False)

    if weight_path_used == weight_path_pretrain:# not os.path.exists(weight_path_ckpt) and not os.path.exists(weight_path_custom):

        in_features = classifier.linear.in_features

        #classifier = ModelWithLayer(classifier)
        pretrained_dict = classifier.state_dict()
        pretrained_dict = edit_weights(pretrained_dict, True)

        pretrained_dict['linear.weight'] = torch.zeros([num_classes , in_features])
        pretrained_dict['linear.bias'] = torch.zeros([num_classes])
        classifier.load_state_dict(pretrained_dict, strict=False)

        save_weights = True
    
    print("Pretrained weights loaded with msg: {}".format( msg))
    print('regular weights')

    if save_weights:
        save_classifier_weights(pretrained_dict)
    
    classifier_flag = True
    return classifier

def edit_weights(pretrained_dict, rm_linear=False):
    pretrained_dict = {k.replace("module.", ""): v for k, v in pretrained_dict.items()}
    pretrained_dict = {k.replace("model.", ""): v for k, v in pretrained_dict.items()}
    if rm_linear:
        pretrained_dict.pop('linear.bias', None)
        pretrained_dict.pop('linear.weight', None)

    return pretrained_dict

def save_classifier_weights(model_weights):
    global train_loss_past, output_path_filenumber
    output_path = os.path.join(home_dir, LOCAL_FILE_STORE, "vjepa2_" + pt_key + "_ckpt_classifier.pt")
    output_path_local = output_path
    if output_path_filenumber > 0:
        output_path_local = output_path + '.' + str(output_path_filenumber)
    torch.save(model_weights, output_path_local)
    print('save some model checkpoint')


def build_pt_video_transform(img_size):
    short_side_size = int(256.0 / 224 * img_size)
    # Eval transform has no random cropping nor flip
    #print(short_side_size, 'short_side_size',  img_size)
    eval_transform = video_transforms.Compose(
        [
            video_transforms.Resize(short_side_size, interpolation="bilinear"),
            video_transforms.CenterCrop(size=(img_size, img_size)),
            volume_transforms.ClipToTensor(),
            video_transforms.Normalize(mean=IMAGENET_DEFAULT_MEAN, std=IMAGENET_DEFAULT_STD),
        ]
    )
    return eval_transform

def prep_choose_img_list():
    global video_list, choose_img
    choose_img = []
    for i in video_list:
        j = i.split("_")[-1:]
        j = "".join(j)
        j = j.split('.')[0]
        choose_img.append(int(j))
    choose_img.sort()
    #print('choose_img', choose_img)


def get_filename(num):
    global video_list, args_foldername
    
    shortname = ''
    if num > 1 or len(video_list) > 1 :
        n = str('00000000' + str(num))[-5:]

        filename = os.path.join(home_dir, LOCAL_FILE_STORE, 'pic/' + args_foldername + '/output_' + n + '.mp4')
        shortname = os.path.join('output_' + n + '.mp4')
    else:
        num = 0 
        n = str(num)
        filename = os.path.join(os.getcwd(), 'pic/output_' + n + '.mp4')
    return filename, shortname

def get_video( num=0 ):
    global video_list
    filename, _ = get_filename(num)

    print(filename)
    if not os.path.exists(filename):
        print('filename not', filename)
        return None
    vr = VideoReader(filename)
    # choosing some frames here, you can define more complex sampling strategy
    frame_idx = np.arange(0, 4, 1) ## 0, 60, 1
    #frame_idx = np.arange(0, 128, 2)

    video = vr.get_batch(frame_idx).asnumpy()
    return video


def forward_vjepa_video(model_hf, model_pt, hf_transform, pt_transform ):
    global image_span, choose_img, args_foldername, VIDEO_PONG_CLASSES

    out_patch_features_pt = []
    out_patch_features_hf = []

    for _ in range(image_batch_size + 0):
        if len(choose_img) < 1:
            break
        i = random.choice(choose_img)
        choose_img.remove(i)

        video = get_video(i)  # T x H x W x C
        if video is None:
            print('skip image_span')
            continue
        filename, shortname = get_filename(i)
        #VIDEO_PONG_CLASSES = json.load(open(os.path.join(home_dir, LOCAL_FILE_STORE, "pic/" + args_foldername + "/video_image_label.json"), "r"))
        print(filename, 'filename', '( remaining', len(choose_img), ')')
        #print(shortname, 'shortname')
        if filename in VIDEO_PONG_CLASSES:
            x = VIDEO_PONG_CLASSES[filename]
        elif shortname in VIDEO_PONG_CLASSES:
            x = VIDEO_PONG_CLASSES[shortname]
        else:
            x = 0 
            print('no record')
        video = torch.from_numpy(video).permute(0, 3, 1, 2)  # T x C x H x W
        x_pt = pt_transform(video).cpu().unsqueeze(0)
        x_hf = hf_transform(video, return_tensors="pt")["pixel_values_videos"].to(device)
        # Extract the patch-wise features from the last layer
        out_patch_features_pt += [[model_pt(x_pt), torch.Tensor([int(x)])]]
        out_patch_features_hf += [model_hf.get_vision_features(x_hf)]

    if image_span <= 1:
        print(choose_img, 'choose_img')
        return out_patch_features_pt[0], out_patch_features_hf[0]
    return out_patch_features_hf, out_patch_features_pt


def get_vjepa_video_classification_results(classifier, out_patch_features_pt):
    #global out_classifier

    print('classification_results')

    SOMETHING_SOMETHING_V2_CLASSES = json.load(open(os.path.join(home_dir, LOCAL_FILE_STORE, "json/classes_pong.json"), "r"))
    #if True :
    with torch.inference_mode():
        out_classifier = classifier(out_patch_features_pt)

    print(f"Classifier output shape: {out_classifier.shape}")
    print("Top 6 predicted class names:\n-----\n")
    high_id = ""
    high_prob = 0 
    top5_indices = out_classifier.topk(num_classes).indices[0]
    top5_probs = F.softmax(out_classifier.topk(num_classes).values[0]) * 100.0  # convert to percentage
    for idx, prob in zip(top5_indices, top5_probs):
        str_idx = str(idx.item())
        print(f"{SOMETHING_SOMETHING_V2_CLASSES[str_idx]} ({prob}%)")
        if prob > high_prob: # or high_prob == 0:
            high_id = str_idx 
            high_prob = prob
    return SOMETHING_SOMETHING_V2_CLASSES[str(high_id)]


def run_sample_inference():
    global  demo_weights, video_list, choose_img, args_foldername, VIDEO_PONG_CLASSES

    VIDEO_PONG_CLASSES = json.load(open(os.path.join(home_dir, LOCAL_FILE_STORE, "pic/" + args_foldername + "/video_image_label.json"), "r"))
   
    batch_size = 64 
    hidden_dim = 1408
    if pt_key == 'vitl' and change_hidden_dim:
        hidden_dim = 1024 
    # HuggingFace model repo name
    hf_model_name = PT_FILENAME[pt_key][1] # "facebook/vjepa2-vitg-fpc64-384"  # Replace with your favored model, e.g. facebook/vjepa2-vitg-fpc64-384
    file_pattern = os.path.join(os.path.expanduser('~'), LOCAL_FILE_STORE, 'pic/' + args_foldername + '/output_00*.mp4')
   
    # Path to local PyTorch weights
    pt_model_path = os.path.join(home_dir, LOCAL_FILE_STORE, PT_FILENAME[pt_key][2] )# "vitg-384.pt")

    sample_video_path = os.path.join(os.getcwd(), "pic/output_0.mp4")
    if image_span == 1:
        print(image_span, 'image_span')
        file_pattern = sample_video_path
    video_list = glob.glob(file_pattern)
    prep_choose_img_list()
    num = 0 

    # Initialize the HuggingFace model, load pretrained weights
    model_hf = AutoModel.from_pretrained(hf_model_name, num_labels=num_classes, ignore_mismatched_sizes=True) 
    #model_hf.embed_dim = hidden_dim
    model_hf.to(device).eval()

    # Build HuggingFace preprocessing transform
    hf_transform = AutoVideoProcessor.from_pretrained(hf_model_name, hidden_size=hidden_dim)
    #hf_transform.embed_dim = hidden_dim

    img_size = hf_transform.crop_size["height"]  # E.g. 384, 256, etc.
    print(hf_transform.crop_size["height"], 'height')
    # Initialize the PyTorch model, load pretrained weights
    
    if pt_key == 'vitg':
        model_pt = vit_giant_xformers_rope(img_size=(img_size, img_size), num_frames=batch_size)
        #model_pt.embed_dim = hidden_dim
        model_pt.to(device).eval()
        load_pretrained_vjepa_pt_weights_vitg(model_pt, pt_model_path)

    elif pt_key == 'vitl':
        model_pt = vit_large_rope(img_size=(img_size, img_size), num_frames=batch_size)
        model_pt.to(device) #.eval()
        load_pretrained_vjepa_pt_weights_vitl(model_pt, pt_model_path)

    # Build PyTorch preprocessing transform
    pt_video_transform = build_pt_video_transform(img_size=img_size)

    while len(choose_img) > 0 and num < 1000:


        out_patch_features_hf, out_patch_features_pt = forward_vjepa_video(
            model_hf, model_pt, hf_transform, pt_video_transform
        )

        if image_span <= 1:
            print(
                f"""
                Inference results on video:
                HuggingFace output shape: {out_patch_features_hf[0].shape}
                PyTorch output shape:     {out_patch_features_pt[0].shape}
                """
                #Absolute difference sum:  {torch.abs(out_patch_features_pt[0] - out_patch_features_hf[0]).sum():.6f}
                #Close: {torch.allclose(out_patch_features_pt[0], out_patch_features_hf[0], atol=1e-3, rtol=1e-3)}

            )
        
        #print(model_pt.embed_dim, 'embed_dim')
        classifier = (
            AttentiveClassifier(embed_dim=hidden_dim, num_heads=16, depth=4, num_classes=num_classes).to(device).eval()
        )
        
        classifier = load_pretrained_vjepa_classifier_weights(classifier)

        if image_span > 1:
            if not eval_flag:
                print('must train here')
                classifier = train_simple(classifier, out_patch_features_pt)
            else:
                print('must eval here')
                eval_simple(classifier, out_patch_features_pt)
        num += 1
        
    if image_span > 1:
        exit() 

    # Download SSV2 classes if not already present
    ssv2_classes_path = os.path.join(home_dir, LOCAL_FILE_STORE , "json/classes_pong.json")
    if not os.path.exists(ssv2_classes_path):
        print("Download classes")

    x = get_vjepa_video_classification_results(classifier, out_patch_features_pt)
    return x 

if __name__ == "__main__":
    # Run with: `python -m notebooks.vjepa2_demo_cpu`
    parser = argparse.ArgumentParser( description='vjepa demo modified' )
    parser.add_argument('--single', action="store_true", help='Process one individual file. Takes precedence over others.')
    parser.add_argument('--image_span', type=int, default=-1, help='Process this number of files.')
    parser.add_argument('--load_checkpoint', action='store_true', help='Load checkpoint during train.')
    parser.add_argument('--save_checkpoint', action='store_true', help='Save checkpoint during train.')
    parser.add_argument('--foldername', type=str, default='train', help='Use "name" as folder for datasets.')
    parser.add_argument('--testset', action='store_true', help='use data for test set/evaluation.')
    parser.add_argument('--checkpoint', type=str, default='vjepa2.pt', help='choose from saved checkpoint files.')
    args = parser.parse_args()

    if args.single:
        image_span = 1
    else:
        if args.image_span > 0:
            image_span = args.image_span


    if args.foldername != 'train':
        args_foldername = args.foldername

    eval_flag = args.testset
    
    if args.checkpoint != 'vjepa2.pt':
        output_path_list = [args.checkpoint]

    checkpoint_options(args.load_checkpoint, args.save_checkpoint, pt_key, args_foldername)
    x = run_sample_inference()
    print(x)
