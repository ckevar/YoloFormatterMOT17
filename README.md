# YoloFormatterMOT17
# MOT17 Dataset Preprocessing

This repository contains a Python script for preprocessing the MOT17 (Multiple Object Tracking 2017) dataset. The script resizes images, applies letterboxing, and generates YOLO-format label files for training object detection models.

## Description

The script processes the MOT17 dataset, which consists of image sequences with object bounding box annotations. It performs the following operations:

1.  **Image Resizing and Letterboxing:** Resizes images to a specified target size (either 640x640 or 480x480) while maintaining the aspect ratio using letterboxing. Letterboxing adds padding to the images to ensure they have the desired dimensions.
2.  **Label Generation:** Converts the bounding box annotations from the MOT17 format to the YOLO format, which represents bounding boxes as normalized center coordinates, width, and height.
3.  **Train/Validation Split:** Randomly splits the processed data into training and validation sets.
4.  **Directory Structure Creation:** Creates the necessary directory structure for storing the processed images and labels, organized by train and validation sets, and target image sizes.

The script is designed to prepare the MOT17 dataset for training object detection models using YOLO architectures.

## Functionality

* Resizes images to specified dimensions (640x640 or 480x480).
* Applies letterboxing to maintain aspect ratio during resizing.
* Converts MOT17 bounding box annotations to YOLO format.
* Generates separate label files for each image.
* Randomly splits the dataset into training and validation sets.
* Organizes processed data into a structured directory.
* Supports command-line arguments for specifying the dataset directory and output image size.

## Getting Started

### Prerequisites

* Python 3.x
* OpenCV (`cv2`)
* `tqdm`

### Installation

1.  Clone the repository:

    ```bash
    git clone [repository URL]
    ```

2.  Install the required packages:

    ```bash
    pip install opencv-python tqdm
    ```

### Usage

1.  Place the MOT17 dataset in a directory on your system.

2.  Run the script from the command line, providing the dataset directory and desired image size:

    ```bash
    python3 main.py <dataset_directory> <image_size>
    ```
MOT17/
└── train/
└── letterbox_640x640/ (or letterbox_480x480)
├── train/
│   ├── images/
│   └── labels/
└── val/
│   ├── images/
│   └── labels/

    * `<dataset_directory>`: The path to the root directory of the MOT17 dataset.
    * `<image_size>`: The desired output image size, either `IMG_640x640` or `IMG_480x480`.

    **Example:**

    ```bash
    python3 main.py /path/to/MOT17/dataset IMG_640x640
    ```

    The processed images and labels will be saved in a new directory within the MOT17 root directory, named `letterbox_640x640` or `letterbox_480x480` depending on the selected image size.

### Directory Structure

The script creates the following directory structure:

MOT17/
└── train/
└── letterbox_640x640/ (or letterbox_480x480)
├── train/
│   ├── images/
│   └── labels/
└── val/
│   ├── images/
│   └── labels/


## Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

* The MOT17 dataset: [MOT17 Website](https://motchallenge.net/data/MOT17/)
* OpenCV: [OpenCV Website](https://opencv.org/)
* tqdm: [tqdm GitHub](https://github.com/tqdm/tqdm)
