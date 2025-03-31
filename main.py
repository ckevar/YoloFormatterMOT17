import cv2 as cv
from tqdm import tqdm
import random
import time
import sys
import os

from datasetMOT17 import ImgStream
from datasetMOT17 import dataset_train as dataset

USER_INPUT_LEN = 3
CONFIG = {
    'IMG_640x640': {
        'dir' : 'letterbox_640x640/',
        'size' : 640
        },
    'IMG_480x480' : {
        'dir' : 'letterbox_480x480/',
        'size' : 480
        }
} 
ZERO_PADDING = [0, 0, 0]

def create_dest_path(src_path, tov, config):
    aux = src_path.split("/")
    aux[-1] = aux[-3] + aux[-1]
    aux[-3] = config['dir'] + tov
    img_path = "/".join(aux)

    aux[-2] = "labels"
    aux2 = aux[-1].split(".")
    aux2[-1] = "txt"
    aux[-1] = ".".join(aux2)
    label_path = "/".join(aux)

    return img_path, label_path

def letterbox(ratio, config):
    yolo_sz = config['size']
    new_hw = int(yolo_sz / ratio)

    padding_pixels = yolo_sz - new_hw
    x = padding_pixels // 2
    y = x + padding_pixels % 2

    return yolo_sz, new_hw, x, y
    
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
        xc = box[0] + box[2] / 2.
        yc = box[1] + box[3] / 2.
        
        line = str(int(box[-1])) + ' ' + \
               str(xc / w)       + ' ' + \
               str(yc / h)       + ' ' + \
               str(box[2] / w)   + ' ' + \
               str(box[3] / h)   + '\n'
        fd.write(line)
    fd.close()

def shuffle_train_validation(total, train_len=0.8):
    if random.random() < train_len:
        return "train"

    return "val"
    
def process_dataset(dataset_path, config):
    stream = ImgStream(dataset_path)

    for bbox, src_path in stream.streamPath():
        tov = shuffle_train_validation(stream.frame_count)
        img_path, label_path = create_dest_path(src_path, tov, config)

        h, w = process_image(img_path, src_path, config)
        process_bbox(label_path, bbox, h, w)
    
def main(root_dir, config):
    for ds in tqdm(dataset):
        process_dataset(root_dir + '/' + ds, config)
       
def mkdirs(root_dir, out_dir):
    target_dir = root_dir + '/train/' + out_dir
    
    try:
        os.makedirs(target_dir + 'train/labels/')
    except FileExistsError:
        pass
    except e:
        print("\n  Something went wrong when creating train/labels/.", e)
        exit()

    try:
        os.makedirs(target_dir + 'val/labels/')
    except FileExistsError:
        pass
    except e:
        print("\n  Something went wrong when creating val/labels/.", e)
        exit()
 
def init(root_dir, config):
    random.seed(time.time())
    mkdirs(root_dir, config['dir'])

def parse_user_input(argv):
    configs = list(CONFIG.keys())
    if (len(argv) < USER_INPUT_LEN) or (argv[2] not in configs):
        print("\nusage: python3 {} <dir> <imgsz>\n"\
              "  dir   : directory of MOT-17 dataset\n"\
              "  imgsz : {}".format(argv[0], configs))
        exit()

    return argv[1], CONFIG[argv[2]]

if "__main__" == __name__:
    root_dir, config = parse_user_input(sys.argv)

    init(root_dir, config)
    main(root_dir, config)

