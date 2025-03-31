import numpy as np

base_path_train = "train"
base_path_test = "test"

dataset_train = [base_path_train + "/MOT17-02",
                 base_path_train + "/MOT17-04",
                 base_path_train + "/MOT17-05",
                 base_path_train + "/MOT17-09",
                 base_path_train + "/MOT17-10",
                 base_path_train + "/MOT17-11",
                 base_path_train + "/MOT17-13"]

dataset_test = [base_path_test + "/MOT17-01",
                base_path_test + "/MOT17-03",
                base_path_test + "/MOT17-06",
                base_path_test + "/MOT17-07",
                base_path_test + "/MOT17-08",
                base_path_test + "/MOT17-12",
                base_path_test + "/MOT17-14"]

class ImgStream:
    def __init__(self, ds_path):
        self.path = ds_path
        self._load_det_(ds_path)
        self._touch_output_(ds_path)
    
    def _touch_output_(self, some_path):
        self.est_file = some_path + "/det/det.txt"
        f = open(self.est_file, 'w')
        f.close()

    def _load_det_(self, ds_path):
        self.dets = np.loadtxt(ds_path + "/gt/gt.txt", delimiter=',')
        self.frame_count = int(self.dets[:,0].max())

    def _load_frame_(self):
        path = self.path + "/img1/" + format(self.frame_i + 1, '06d') + ".jpg" 
        img = cv.imread(path, cv.IMREAD_COLOR)
        return img

    def stream(self, subset=1):
        for self.frame_i in range(int(self.frame_count * subset)):
            frame_id = self.frame_i + 1
            yield self.dets[self.dets[:, 0] == frame_id, 2:7], self._load_frame_()

    def streamPath(self, subset=1):
        for self.frame_i in range(int(self.frame_count * subset)):
            frame_id = self.frame_i + 1
            path = self.path + "/img1/" + format(frame_id, '06d') + ".jpg" 
            yield self.dets[self.dets[:, 0] == frame_id, 2:8], path


    def saveTrackers(self, tracks):
        with open(self.est_file, 'a') as f:
            for j in range(len(tracks)):
                w = tracks[j][2] - tracks[j][0]
                h = tracks[j][3] - tracks[j][1]

                f.write(str(int(self.frame_i + 1)) + ',' +
                        str(tracks[j][4]) + ',' +
                        str(tracks[j][0]) + ',' +
                        str(tracks[j][1]) + ',' + 
                        str(w) + ',' +
                        str(h) + ',' + 
                        '-1\n')

