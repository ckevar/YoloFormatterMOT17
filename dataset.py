base_path_train_mot17 = "train"
base_path_test_mot17 = "test"

base_path_train_kitti = "training"
base_path_test_kitti = "testing"


dataset_train = {
        'MOT17': {
            'paths' : [
                base_path_train_mot17 + "/MOT17-02-DPM",
                base_path_train_mot17 + "/MOT17-04-DPM",
                base_path_train_mot17 + "/MOT17-05-DPM",
                base_path_train_mot17 + "/MOT17-09-DPM",
                base_path_train_mot17 + "/MOT17-10-DPM",
                base_path_train_mot17 + "/MOT17-11-DPM",
                base_path_train_mot17 + "/MOT17-13-DPM"
            ],
            'meta' : {
                'dataset': 'MOT17',
                'nc': 12,
                'names': {
                    b'__background__': 0,
                    b'Pedestrian': 1,
                    b'Person on Vehicle': 2,
                    b'Car': 3,
                    b'Bicycle': 4,
                    b'Motorbike': 5,
                    b'Non motorized vehicle': 6,
                    b'Static person': 7,
                    b'Distractor': 8,
                    b'Occluder': 9,
                    b'Occluder on the ground' : 10,
                    b'Occluder full': 11,
                    b'Reflection': 12
                },
            }
        },
        'KITTI': {
            'paths' : [
                base_path_train_kitti + "/image_02/0000",
                base_path_train_kitti + "/image_02/0001",
                base_path_train_kitti + "/image_02/0002",
                base_path_train_kitti + "/image_02/0003",
                base_path_train_kitti + "/image_02/0004",
                base_path_train_kitti + "/image_02/0005",
                base_path_train_kitti + "/image_02/0006",
                base_path_train_kitti + "/image_02/0007",
                base_path_train_kitti + "/image_02/0008",
                base_path_train_kitti + "/image_02/0009",
                base_path_train_kitti + "/image_02/0010",
                base_path_train_kitti + "/image_02/0011",
                base_path_train_kitti + "/image_02/0012",
                base_path_train_kitti + "/image_02/0013",
                base_path_train_kitti + "/image_02/0014",
                base_path_train_kitti + "/image_02/0015",
                base_path_train_kitti + "/image_02/0016",
                base_path_train_kitti + "/image_02/0017",
                base_path_train_kitti + "/image_02/0018",
                base_path_train_kitti + "/image_02/0019",
                base_path_train_kitti + "/image_02/0020"
            ],
            'meta': {
                'dataset': 'KITTI',
                'nc': 9,
                'names': {
                    b'__background__': 0,
                    b'Car': 1,
                    b'Van': 2,
                    b'Truck': 3,
                    b'Pedestrian': 4,
                    b'Person': 5,
                    b'Cyclist': 6,
                    b'Tram': 7,
                    b'Misc': 8,
                    b'DontCare': 9
                }

            }
        }
}


