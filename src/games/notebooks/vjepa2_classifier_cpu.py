from re import T
import torchvision
import torchvision.transforms as transforms
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms
import os 
import glob

from peft import LoraConfig, get_peft_model, PeftModel 

model = None
home_dir = os.path.expanduser('~')
LOCAL_FILE_STORE = 'workspace/VJEPA2_FILES/demo/'
train_loss = 0.0
train_loss_past = []
test_loss = 0.0 
test_loss_past = []
pt_key = 'vitl'

output_path = os.path.join(home_dir, LOCAL_FILE_STORE, "vjepa2_vitl_ckpt_classifier.pt")
output_path_filenumber = 0
csv_output_pic_folder = 'train'
csv_output_pic_filenumber = 0 
load_checkpoint = False
save_checkpoint = False
model = None
model_peft = None
use_lora = True

criterion = None
optimizer = None
optimizer_flag = False

def checkpoint_options(load_checkpoint_in=False, save_checkpoint_in=False, size_key='vitl', foldername='train'):
    global load_checkpoint, save_checkpoint, output_path, csv_output_pic_folder, csv_output_pic_filenumber
    global output_path_filenumber, pt_key

    pt_key = size_key
    csv_output_pic_folder = foldername
    i = glob.glob(os.path.join(home_dir, LOCAL_FILE_STORE, 'pic', csv_output_pic_folder , 'csv_' +  pt_key + '_' + foldername + '.csv*'))
    if len(i) > 0:
        csv_output_pic_filenumber = len(i)
    output_path = os.path.join(home_dir, LOCAL_FILE_STORE, "vjepa2_" + size_key + "_ckpt_classifier.pt")
    i = glob.glob(output_path + '*')
    i.sort() 
    #print('output_path', i)
    if len(i) > 0:
        output_path_filenumber = highest_number(output_path) + 1  # len(i)
    output_path = os.path.join(home_dir, LOCAL_FILE_STORE, "vjepa2_" + size_key + "_ckpt_classifier.pt")
    load_checkpoint = load_checkpoint_in
    save_checkpoint = save_checkpoint_in
    #print(output_path, 'path set')

def highest_number(search_name):
    j = glob.glob(search_name + "*")
    x_list = []
    for i in j:
        j = i.split('/')[-1]
        try:
            ii = j.split('.')[-1]
            j = float(ii)
            x_list.append( int(j) )
        except ValueError:
            pass 
    x_list.sort()
    if len(x_list) < 1:
        x_list = [0]
    return x_list[-1]

def show_shape(in_dict, key):
    print('-----')
    if key in in_dict:
        print(key, in_dict[key])
        print(in_dict[key].shape)
    else:
        print('no key', key)
    print('-----')

def show_keys(in_dict):
    print('-----')
    print_dict = [k for k, v in in_dict.items()] 
    print(print_dict)
    print('from classifier file')
    print('-----')


def train_simple(model_input, out_patch_features_pt):
    global train_loss, train_loss_past, criterion, optimizer, optimizer_flag, model_peft, model

    print('train_simple')
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   
    if not optimizer_flag:

        model = model_input

        show_keys(model.state_dict())

        # Run this to look at the exact names of your linear layers
        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Linear):
                print(name)

        if use_lora:

            lora_path = load_lora_path()
            if (lora_path is not None) :
                model_peft = PeftModel.from_pretrained(model, lora_path, is_trainable=True)
            
            else:

                peft_config = LoraConfig(
                    r=8,  # LoRA rank
                    lora_alpha=16,  # Scaling parameter
                    target_modules=r".*pooler\.blocks\.\d+\.attn\.(qkv|q|kv|query|key|value|proj)$",
                    #target_modules=r".*encoder\.layer\.\d+\.attention\.(query|key|value|proj)$", #["query", "value"],  # Modules to inject adapters into
                    #modules_to_save=["classifier", "pooler"], 
                    lora_dropout=0.1,
                    bias="none",
                    #task_type="SEQ_CLS",  # Sequence classification task type
                )

                model_peft = get_peft_model(model, peft_config)
            
            #model_peft.print_trainable_parameters()
            model = model_peft

        for name, param in model.named_parameters():
            if 'linear.weight' in name or 'linear.bias' in name:
                param.requires_grad = True
                print('requires_grad', name)
            else:
                pass 
                #param.requires_grad = False
                #print('not requires_grad', name)

        model.print_trainable_parameters()

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.AdamW(
            #model.parameters()
            filter(lambda p: p.requires_grad, model.parameters())
            , lr=1e-1, weight_decay=0.1) ## lr=1e-3

        print('optimizer init')
        
        optimizer_flag = True
    else:
        print('not optimizer init')

    for name, param in model.named_parameters():
        if 'linear.weight' in name or 'linear.bias' in name:
            param.requires_grad = True
            print('requires_grad', name)
        else:
            #param.requires_grad = False
            pass 

    #pretrained_dict = model.state_dict()

    #model.load_state_dict(pretrained_dict, strict=False)

    #show_shape(pretrained_dict, 'linear.weight')
    #show_shape(pretrained_dict, 'linear.bias')

    model.train()
    train_loss = 0.0
    for inputs, labels in  out_patch_features_pt  : ## test values
        inputs, labels = inputs.to(device), labels.to(device)
        
        #print(inputs.shape, labels.shape, 'inputs, labels')
        optimizer.zero_grad()
        outputs = model(inputs)
        print(labels)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        train_loss += loss.item() * inputs.size(0)
        
    epoch_train_loss = train_loss / len(out_patch_features_pt[0])
    print(f"Train Loss: {epoch_train_loss:.4f} len out_patch_features_pt = {len(out_patch_features_pt)}")
    train_loss_past.append(round(epoch_train_loss, 3))

    print('past train_loss', train_loss_past )
    if save_checkpoint:
        save_simple(model.state_dict())
        save_lora(model)

    return model

def eval_simple(model, out_patch_features_pt):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    criterion = nn.CrossEntropyLoss()

    for _, param in model.named_parameters():
        param.requires_grad = False

    model.eval()
    test_loss = 0.0

    with torch.no_grad():
        for inputs, labels in out_patch_features_pt:
            inputs, labels = inputs.to(device), labels.to(device)
            
            outputs = model(inputs)
            print(labels)
            
            loss = criterion(outputs, labels)
            test_loss += loss.item() * inputs.size(0)

    epoch_test_loss = test_loss / len(out_patch_features_pt[0])
    print(f"Train Loss: {epoch_test_loss:.4f} len(out_patch_features_pt) = {len(out_patch_features_pt)}")
    test_loss_past.append(round(epoch_test_loss, 3))
    csv_simple(test_loss_past, 'test')
    print('past test_loss', test_loss_past)


def load_lora_path(path=None):
    global use_lora, output_path, output_path_filenumber
    if use_lora:
        if path is not None:
            output_path_local = path
        else:
            output_path_local = output_path
        if output_path_filenumber > 0:
            xstring = '0000000000'
            ystring = (xstring + str(highest_number(output_path_local)))[-5:]

            output_path_local = output_path + '.' + str( ystring ) # + str(output_path_filenumber)
        i = output_path_local.split('/')[-1]
        j = output_path_local.split('/')[:-1]
        output_path_local = '/'.join(j)  + '/lora.' + i 
        g = glob.glob(output_path_local + '*')
        if len(g) < 1:
            return None
        g.sort()
        if g[-1].endswith(str(highest_number(output_path_local))) :
            return g[-1]
    return None


def save_lora(peft_modal):
    global use_lora, output_path
    if not use_lora:
        return
    else:
        output_path_local = output_path
        if output_path_filenumber > 0:
            xstring = '0000000000'
            ystring = (xstring + str(highest_number(output_path_local)))[-5:]

            output_path_local = output_path + '.' + str(ystring)
        i = output_path_local.split('/')[-1]
        j = output_path_local.split('/')[:-1]
        output_path_local = '/'.join(j)  + '/lora.' + i 
        peft_modal.save_pretrained(output_path_local)
        return

def save_simple(model_weights):
    global train_loss_past, output_path_filenumber, output_path
    output_path_local = output_path
    if output_path_filenumber > 0:
        xstring = '0000000000'
        ystring = (xstring + str(output_path_filenumber))[-5:]
        output_path_local = output_path + '.' +  ystring # str(output_path_filenumber)
    torch.save(model_weights, output_path_local)
    print('save some model checkpoint')
    csv_simple(train_loss_past, 'train')
    
def load_simple(model):
    if  os.path.exists(output_path):
        pretrained_dict = torch.load(output_path, weights_only=True, map_location="cpu")    
        model.load_state_dict(pretrained_dict, strict=False)
        print('load checkpoint')
        return model

def csv_simple(loss_past, csv_name=None):
    global pt_key, csv_output_pic_filenumber
    if csv_name != None:
        tag = csv_name
    else: 
        tag = 'train'
       #if csv_output_pic_filenumber > 0:
    csv_output_path = os.path.join(home_dir, LOCAL_FILE_STORE, 'pic', csv_output_pic_folder , 'csv_' +  pt_key + '_' + tag + '.csv')
    csv_output_path = csv_output_path + '.' + str(csv_output_pic_filenumber + 1) + '.csv'
    with open(csv_output_path, 'w') as w:
        for i in loss_past:
            w.write(str(i) + ',')
    print('save some cvs train data', csv_output_path)


