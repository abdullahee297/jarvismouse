# Virtual Mouse using Hand Gesture Recognition

A Python-based virtual mouse that allows users to control the computer cursor using hand gestures captured through a webcam. The project utilizes computer vision and real-time hand landmark detection to perform mouse operations such as cursor movement, left-click, and drag-and-drop without requiring any physical mouse.

---

## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [System Workflow](#system-workflow)
* [Gesture Controls](#gesture-controls)
* [Project Structure](#project-structure)
* [Technologies Used](#technologies-used)
* [Installation](#installation)
* [Requirements](#requirements)
* [Usage](#usage)
* [Future Improvements](#future-improvements)
* [Author](#author)
* [License](#license)

---

## Overview

The Virtual Mouse project demonstrates how computer vision and hand tracking can replace traditional mouse interactions. A webcam continuously captures video frames, detects the user's hand, identifies finger positions, and translates specific gestures into mouse actions.

The application provides a natural and touch-free way to interact with a computer, making it useful for gesture-based interfaces, accessibility applications, and human-computer interaction research.

---

## Features

* Real-time hand detection
* Cursor movement using the index finger
* Left-click using the index and middle fingers
* Drag and drop using the thumb and index finger
* Smooth cursor movement
* Live hand landmark visualization
* Real-time FPS display

---

## System Workflow

```text
Webcam Input
      │
      ▼
Frame Capture
      │
      ▼
Hand Detection
      │
      ▼
Landmark Extraction
      │
      ▼
Gesture Recognition
      │
      ▼
Mouse Action
      │
      ├── Cursor Movement
      ├── Left Click
      └── Drag & Drop
```

---

## Gesture Controls

| Gesture                              | Action        |
| ------------------------------------ | ------------- |
| Index Finger Up                      | Move Cursor   |
| Index + Middle Finger Close Together | Left Click    |
| Thumb + Index Finger Pinch           | Drag and Drop |
| Index + Middle + Ring                | Right Click   |

---

## Project Structure

```text
Virtual-Mouse/
│
├── main.py
├── hand_landmarker.task
├── requirements.txt
├── README.md
└── assets/
    └── screenshots/
```

---

## Technologies Used

### Programming Language

* Python

### Computer Vision

* OpenCV
* MediaPipe

### Mouse Automation

* Autopy

### Numerical Computation

* NumPy

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/virtual-mouse.git

cd virtual-mouse
```

---

### 2. Create a Virtual Environment

**Windows**

```bash
python -m venv venv

venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv

source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Download MediaPipe Hand Landmark Model

Download the model file:

```
hand_landmarker.task
```

Place it in the project root directory beside `main.py`.

---

### 5. Run the Project

```bash
python main.py
```

---

## Requirements

The project depends on the following libraries:

* OpenCV
* MediaPipe
* NumPy
* Autopy

Install them using:

```bash
pip install -r requirements.txt
```

---

## Usage

1. Launch the application.
2. Allow the webcam to access your hand.
3. Keep your hand inside the camera frame.
4. Perform the supported gestures to control the mouse.
5. Press **Esc** to exit the application.

---

## How It Works

### Hand Detection

The webcam continuously captures frames which are processed using the MediaPipe Hand Landmarker model. The model identifies 21 landmarks representing different joints of the hand.

### Cursor Movement

The position of the index fingertip is mapped from the camera frame to the computer screen coordinates. A smoothing algorithm reduces cursor jitter and provides stable movement.

### Left Click

When the index and middle fingertips come close together, the application interprets the gesture as a mouse click and performs a left-click action.

### Drag and Drop

When the thumb and index fingertip are pinched together, the left mouse button is held down. Releasing the fingers releases the mouse button, enabling drag-and-drop functionality.

---

## Future Improvements

* Right-click gesture
* Double-click gesture
* Scroll using finger gestures
* Multi-hand support
* Custom gesture configuration
* Gesture calibration
* Improved gesture stability
* Cross-platform optimization

---

## Author

**Muhammad Abdullah**

Python | OpenCV | MediaPipe | Computer Vision

---

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this project for educational and research purposes.
