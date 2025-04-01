# YoloFormatterMOT17

This repository contains a Python script for preprocessing the MOT17 (Multiple Object Tracking 2017) dataset. The script resizes images, applies letterboxing, generates YOLO-format label files for training object detection models and generates the `*.yaml` configuration file.

## Description

The script processes the MOT17 dataset, which consists of image sequences with object bounding box annotations. It performs the following operations:

1.  **Image Resizing and Letterboxing:** Resizes images to a specified target size (either 640x640 or 480x480) while maintaining the aspect ratio using letterboxing. Letterboxing adds padding to the images to ensure they have the desired dimensions.
2.  **Label Generation:** Converts the bounding box annotations from the MOT17 format to the YOLO format, which represents bounding boxes as normalized center coordinates, width, and height.
3.  **Train/Validation Split:** Randomly splits the processed data into training and validation sets.
4.  **Directory Structure Creation:** Creates the necessary directory structure for storing the processed images and labels, organized by train and validation sets, and target image sizes.
5.  **Yaml Configuration:** The dataset configuration format for YOLO, the `path` feature might need to be adjusted manually.

The script is designed to prepare the MOT17 dataset for training object detection models using YOLO architectures.

## Functionality

* Resizes images to specified dimensions (640x640 or 480x480).
* Applies letterboxing to maintain aspect ratio during resizing.
* Converts MOT17 bounding box annotations to YOLO format.
* Generates separate label files for each image.
* Randomly splits the dataset into training and validation sets.
* Organizes processed data into a structured directory.
* Generates the dataset configuration format fo YOLO
* Supports command-line arguments for specifying the dataset directory and output image size.
* Checks existent output directory and encourage manual removal.

## Getting Started

### Prerequisites

* Python 3.x
* OpenCV (`cv2`)
* `tqdm`

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/ckevar/YoloFormatterMOT17.git
    ```

2.  Install the required packages:

    ```bash
    pip install opencv-python tqdm
    ```

### Usage

1.  Place the MOT17 dataset in a directory on your system.

2.  Run the script from the command line, providing the dataset directory and desired image size:

    ```bash
    python3 YoloFormatterMOT17.py <dataset_directory> <output directory> <image_size>
    ```
    
    * `<dataset_directory>`: The path to the root directory of the MOT17 dataset.
    * `<output directory>`: The path to the output directory where the processed images and labels will be saved.
    * `<image_size>`: The desired output image size, either `IMG_640x640` or `IMG_480x480`.

    **Example:**

    ```bash
    python3 YoloFormatterMOT17.py /path/to/MOT17/dataset /tmp IMG_640x640
    ```

    The processed images and labels will be saved in a new directory within the MOT17 root directory, named `letterbox_640x640` or `letterbox_480x480` depending on the selected image size.

### Directory Structure

The script creates the following directory structure:
```
[output directory]/
└─ letterbox_640x640/ (or letterbox_480x480)
   ├─ images/
   │  ├─ train/
   │  ├─ val/
   │  └─ test/   # under development
   └─ labels/
      ├─ train/
      ├─ val/
      └─ test/   # under development
```

## Contributing

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Create a new Pull Request.

## Acknowledgments

* The MOT17 dataset: [MOT17 Website](https://motchallenge.net/data/MOT17/)
* OpenCV: [OpenCV Website](https://opencv.org/)
* tqdm: [tqdm GitHub](https://github.com/tqdm/tqdm)
