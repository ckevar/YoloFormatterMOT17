import numpy as np
from PIL import Image

from letterbox import letterbox_sz
from dataset import dataset_train

DIR_FORMAT = ['MOT17', 'KITTI']

KITTI_CLASS = dataset_train['KITTI']['meta']['names']

def default_rearrange(bbox):
    return bbox

def KITTI_rearrange(bbox):
    '''
    Standardises the bounding box, which in case of KITTI is,
    left, top, right, bottom to left, top, width, height
    '''

    bbox[:, 2] = bbox[:, 2] - bbox[:, 0]
    bbox[:, 3] = bbox[:, 3] - bbox[:, 1]
    return bbox;


class ImgStream:
    def __init__(self, ds_path, dir_format):
        self.__initDatasetConfig__(ds_path, dir_format)

    def __init_mot17__(self, path):
        gt_path = path + "/gt/gt.txt"
        self.dets = np.loadtxt(gt_path, delimiter=',')

        self.frame_count = int(self.dets[:,0].max())
        self.base_path = f"{path}/img1/%06d.jpg"
        self.col_frame_id = 0
        # bbox(left, top, width, height), valid flag, class
        self.cols_of_interest = [2, 3, 4, 5, 6, 7]
        self.callback = default_rearrange

    def __init_kitti__(self):
        gt_path = path.split('/')
        gt_path[-2] = 'label_02'
        gt_path = '/'.join(gt_path) + '.txt'

        self.dets = np.loadtxt(
                gt_path, 
                delimiter=' ', 
                converters={2 : lambda x: KITTI_CLASS[x]}
        )


        self.frame_count = int(self.dets[:,0].max())
        self.base_path = f"{path}/%06d.png"
        self.col_frame_id = 0
        #bbox(left, top, right, bottom, score, type/class)
        self.cols_of_interest = [6, 7, 8, 9, 16, 2]
        self.callback = KITTI_rearrange

    def __initDatasetConfig__(self, ds_path, dir_format):

        if 'MOT17' == dir_format:
            self.__init_mot17__(ds_path)
        elif 'KITTI' == dir_format:
            self.__init_kitti__(ds_path)

        else:
            print(f"\nThis directory format {dir_format} is unknown. Available formats are:\n"\
                  f"{DIR_FORMAT}")
            exit()

    def imgalloc(self, req_sz, stride=31):
        img_tmp = Image.open(self.base_path % 1)
        w, h = img_tmp.size
        new_shape, top, bottom, left, right = letterbox_sz((h,w), req_sz, stride)
        
        canvas = 114 * np.ones(
            (
                new_shape[1] + top + bottom, 
                new_shape[0] + left + right, 
                3
            ),
            dtype=np.uint8
        )
        
        artwork = canvas[
           top:(top + new_shape[1]), 
           left:(left + new_shape[0])
        ]

        return canvas, artwork, (left, top, h, w, new_shape[0], new_shape[1])


    def framePath(self, subset=1):
        
        base_path = self.base_path
        col_frame_id = self.col_frame_id
        cols_of_interest = self.cols_of_interest
        dets = self.dets
        callback = self.callback

        for self.frame_i in range(int(self.frame_count * subset)):
            frame_id = self.frame_i + 1
            path = base_path % frame_id 

            tmp = dets[:, col_frame_id] == frame_id
            tmp = dets[np.ix_(tmp, cols_of_interest)]
            tmp = callback(tmp)

            yield tmp, path
