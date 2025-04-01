import cv2 as cv
from tqdm import tqdm
import threading
import random
import time
import sys
import os

from datasetMOT17 import ImgStream
from datasetMOT17 import dataset_train as dataset

USER_INPUT_LEN = 4
CONFIG = {
    'IMG_640x640': {
        'dir' : 'letterbox_640x640',
        'size' : 640
        },
    'IMG_480x480' : {
        'dir' : 'letterbox_480x480',
        'size' : 480
        }
} 

YOLO_DIRS = ['train', 'val', 'test']
ZERO_PADDING = [0, 0, 0]

def create_target_path(src_file, target_path, tov, config):
    
    aux = src_file.split("/")
    file_name = aux[-3] + aux[-1]

    root_dir = target_path + '/' + config['dir']

    img_path = root_dir + '/images/' + tov + '/'  + file_name
    label_path = root_dir + '/labels/' + tov + '/' + file_name.split(".")[0] + '.txt'

    return img_path, label_path

def letterbox(ratio, config):
    yolo_sz = config['size']

    new_hw = int(yolo_sz / ratio)
    padding_pixels = int(yolo_sz - new_hw)

    margin0 = padding_pixels // 2
    margin1 = margin0 + (padding_pixels & 1)

    return yolo_sz, new_hw, margin0, margin1
    
def process_image(dst, src, config):
    img = cv.imread(src, cv.IMREAD_COLOR)
    
    h, w = img.shape[:2]
    ratio = w/h
    top = bottom = left = right = 0

    if ratio > 1:
        new_width, new_height, top, bottom = letterbox(ratio, config)
    else:
        new_height, new_width, left, right = letterbox(ratio, config)

    new_img = cv.resize(img, (new_width, new_height))
    new_img = cv.copyMakeBorder(new_img, 
                                top, 
                                bottom,
                                left, 
                                right, 
                                cv.BORDER_CONSTANT, 
                                value=ZERO_PADDING)
    cv.imwrite(dst, new_img)
    return h, w

def process_bbox(path, bbox, h, w):
    fd = open(path, 'w')

    for box in bbox:
        xc = (box[0] + box[2] / 2.) / w
        yc = (box[1] + box[3] / 2.) / h

        if xc > 1: 
            xc = 1.0
            box[2] = w - box[0]

        elif xc < 0:
            box[2] += box[0]
            xc = 0.0
        
        if yc > 1: 
            yc = 1.0
            box[3] = h - box[1]

        elif yc < 0: 
            box[3] += box[1]
            yc = 0.0
    
        if box[2] > w: box[2] = w
        if box[3] > h: box[3] = h
        
        line = str(int(box[-1])) + ' ' + \
               str(xc)           + ' ' + \
               str(yc)           + ' ' + \
               str(box[2] / w)   + ' ' + \
               str(box[3] / h)   + '\n'

        fd.write(line)
    fd.close()

def flip_train_validation(total, train_len=0.8):
    if random.random() < train_len:
        return "train"

    return "val"


def process_dataset(dataset_path, new_path, config):
    stream = ImgStream(dataset_path)

    for bbox, src_path in stream.streamPath():
        tov = flip_train_validation(stream.frame_count)
        img_path, label_path = create_target_path(src_path, new_path, tov, config)
        h, w = process_image(img_path, src_path, config)
        process_bbox(label_path, bbox, h, w)

def create_yaml(root_dir, config):
    path = root_dir + '/' + config['dir']

    yaml_content = \
"# YOLO Dataset Configuration for MOT17\n" \
"# Auto-generated by YoloFormatterMOT17\n" \
"# Author: C. Alvarado @ https://github.com/ckevar\n" \
"# Date: " + time.asctime() + '\n' \
"#\n"\
"# Configuration:\n"\
"#   image_size: " + str(config['size']) + 'x' + str(config['size']) + '\n' \
"#   nc: 12\n"\
"\n"\
"path: " + path + '\n' + \
YOLO_DIRS[0] + ": images/" + YOLO_DIRS[0] + '\n' + \
YOLO_DIRS[1] + ": images/" + YOLO_DIRS[1] + '\n' + \
YOLO_DIRS[2] + ": images/" + YOLO_DIRS[2] + '\n' + \
"\n" \
"names:\n" \
"    0: _background_\n" \
"    1: Pedestrian\n" \
"    2: Person on vehicle\n" \
"    3: Car\n" \
"    4: Bicycle\n" \
"    5: Motorbike\n" \
"    6: Non motorized vehicle\n" \
"    7: Static person\n" \
"    8: Distractor\n" \
"    9: Occluder\n" \
"    10: Occluder on the ground\n" \
"    11: Occluder full\n" \
"    12: Reflection\n"

    fd = open(path + '/data.yaml', 'w')
    fd.write(yaml_content)
    fd.close()
    
def main(root_dir, dest_dir, config):

    for ds in tqdm(dataset):
        process_dataset(root_dir + '/' + ds, dest_dir, config)

    create_yaml(dest_dir, config)

def _make_directory_(target_dir):
    try:
        os.makedirs(target_dir)
    except FileExistsError:
        pass
    except Exception as e:
        print("\n  Something went wrong when creating images dir.", e)
        exit()

def mkdirs(root_dir, out_dir):
    base_dir = root_dir + '/' + out_dir

    if os.path.exists(base_dir):
        '''
        For security reasons, we aren't removing the output directory
        automatically.
        '''
        print("\n"\
              "  Warning: Remove the output directory to avoid data\n" \
              "           duplication {}, run:\n"\
              "\n"\
              "           rm -r {}\n".format(base_dir, base_dir))
        exit()

    images_dir = base_dir + '/images'
    labels_dir = base_dir + '/labels'

    for yd in YOLO_DIRS:
        _make_directory_(images_dir + '/' + yd)
        _make_directory_(labels_dir + '/' + yd)
 
def init(root_dir, config):
    random.seed(time.time())
    mkdirs(root_dir, config['dir'])

def parse_user_input(argv):
    configs = list(CONFIG.keys())
    args = int(len(argv))
    
    if (args < USER_INPUT_LEN) or (argv[3] not in configs):
        print("\nusage: python3 {} <src dir> <dst dir> <imgsz>\n"\
              "  src dir : directory of MOT-17 dataset\n"\
              "  dst dir : directory for the YOLO format dataset\n"\
              "  imgsz   : {}\n".format(argv[0], configs))
        exit()
    
    return argv[1], argv[2], CONFIG[argv[3]]

if "__main__" == __name__:
    src_dir, dest_dir, config = parse_user_input(sys.argv)

    init(dest_dir, config)
    main(src_dir, dest_dir, config)

