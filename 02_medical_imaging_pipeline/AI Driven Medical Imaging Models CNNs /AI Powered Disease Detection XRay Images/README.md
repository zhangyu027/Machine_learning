# AI-Powered Disease Detection in X-Ray Images

## Overview

This project leverages deep learning techniques, particularly Convolutional Neural Networks (CNNs), to detect diseases in X-ray images. With a focus on improving medical diagnostics, the project provides a framework for training and evaluating models to identify conditions like pneumonia from medical imaging. The model aims to assist healthcare professionals in early disease detection and enhance diagnostic accuracy. Made in 2022-2023

---

## Features

- **Deep Learning with CNN**: Utilizes convolutional neural networks for image processing and feature extraction.
- **Disease Detection**: Trained to identify diseases such as pneumonia in chest X-rays.
- **Customizable Model**: Flexible to adapt to different diseases or imaging data by retraining the model.
- **Evaluation Metrics**: Includes accuracy, precision, recall, and AUC score for model performance assessment.

---

## Table of Contents

1. [Installation](#installation)
2. [Dataset](#dataset)
3. [Model Architecture](#model-architecture)
4. [Usage](#usage)
5. [Training and Evaluation](#training-and-evaluation)
6. [Results](#results)
7. [OpenVINO](#optimizing-tensorflow-models-with-openvino)
8. [Contributing](#contributing)
9. [License](#license)

---

## Installation

### Prerequisites

Make sure you have the following installed on your machine:

- Python 3.7 or higher
- TensorFlow/Keras
- Numpy
- Matplotlib
- OpenCV
- Scikit-learn
- Pandas

You can install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

## Dataset

For this project, we used the [Kaggle Pneumonia Dataset](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia). This dataset contains labeled chest X-ray images divided into two categories: normal and pneumonia cases.

### Directory Structure

- **train/**: Training data
- **test/**: Testing data
- **val/**: Validation data

You can modify the dataset paths in the code if you are using a different dataset.

---

## Model Architecture

The project employs a Convolutional Neural Network (CNN) model with the following architecture:

- **Input Layer**: X-ray image (e.g., 224x224 pixels)
- **Convolutional Layers**: Several convolutional layers for feature extraction
- **Pooling Layers**: Max pooling to reduce dimensionality
- **Fully Connected Layers**: Dense layers for final classification
- **Output Layer**: Softmax activation for disease classification (e.g., pneumonia vs. normal)

The architecture can be easily modified within the code to experiment with different model configurations.

---

## Usage

### Running the Model

1. Clone the repository:

   ```bash
   git clone https://github.com/osu/AI-Powered-Disease-Detection-in-X-Ray-Images.git
   ```

2. Navigate into the directory:

   ```bash
   cd AI-Powered-Disease-Detection-in-X-Ray-Images
   ```

3. Start the training:

   ```bash
   python train_model.py
   ```

4. Evaluate the model:

   ```bash
   python evaluate_model.py
   ```

### Customization

- **Data Augmentation**: You can apply transformations like rotation, scaling, or flipping to augment the training data.
- **Hyperparameters**: Adjust the learning rate, batch size, or number of epochs in `config.py`.
- **Transfer Learning**: You can integrate pre-trained models (like ResNet or DenseNet) to improve performance on small datasets.

---

## Training and Evaluation

The model is trained using categorical cross-entropy loss and Adam optimizer. Key evaluation metrics include:

- **Accuracy**: Measures the overall correctness of predictions.
- **Precision**: Measures the proportion of positive predictions that were correct.
- **Recall**: Measures how well the model captures true positives.
- **AUC (Area Under the Curve)**: Evaluates the ability of the model to differentiate between classes.

Training logs, validation accuracy, and loss graphs are generated and saved for monitoring the model's performance.

---

## Results

After training, the model achieved the following performance metrics on the test set:

- **Accuracy**: 93.5%
- **Precision**: 91.2%
- **Recall**: 90.7%
- **AUC**: 0.95

Sample results (X-ray images and predictions) are saved in the `results/` folder for visual inspection.

## Optimizing TensorFlow Models with OpenVINO

To further enhance the performance of the model, I am currently trying to integrate Intel's **OpenVINO™ Toolkit**. OpenVINO allows us to optimize and accelerate TensorFlow models, especially on Intel hardware (CPUs, integrated GPUs, VPUs, and FPGAs).

### Why OpenVINO?

- **Faster Inference**: OpenVINO accelerates inference performance by optimizing TensorFlow models for Intel hardware.
- **Reduced Latency**: It reduces model latency, making predictions faster.
- **Ease of Use**: OpenVINO works seamlessly with TensorFlow, converting trained models and providing a simple API for optimized inference.

### Installation of OpenVINO

To install the OpenVINO toolkit, follow the steps below:

1. Install OpenVINO Toolkit:

   ```bash
   pip install openvino-dev[tensorflow2]
   ```

2. Set up the OpenVINO environment (on Linux or MacOS):

   ```bash
   source /opt/intel/openvino/bin/setupvars.sh
   ```

   On Windows, use the **Command Prompt** or **PowerShell** to run the `setupvars.bat` file:

   ```bash
   "C:\Program Files (x86)\Intel\openvino\bin\setupvars.bat"
   ```

3. Convert the TensorFlow model to an OpenVINO IR format:

   ```bash
   mo --input_model model.pb --framework tf --data_type FP16 --output_dir optimized_model
   ```

   This converts the TensorFlow model into an Intermediate Representation (IR) that OpenVINO can run efficiently.

4. Load and run the model using OpenVINO Inference Engine:

   ```python
   from openvino.runtime import Core

   core = Core()
   model = core.read_model(model="optimized_model/model.xml")
   compiled_model = core.compile_model(model, "CPU")

   # Run inference
   output = compiled_model([input_image])
   ```

### Performance Gains

By using OpenVINO, you can expect a significant improvement in inference times, especially when running on Intel CPUs. This allows the model to make predictions faster, enabling near real-time diagnostics in healthcare applications.

---

### Future Plans

The integration of OpenVINO is currently in progress, and upcoming updates will provide benchmark results comparing TensorFlow's native performance with OpenVINO-optimized performance on Intel hardware.

---

## Contributing

We welcome contributions to improve the project! Here's how you can help:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request to the `main` branch.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

Special thanks to the following open-source projects and datasets:

- [Kaggle Pneumonia Dataset](https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia)
- TensorFlow and Keras for the deep learning frameworks.

---
