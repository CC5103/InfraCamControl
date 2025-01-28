# InfraCamControl

**Other Language Versions: [English](README.md) | [中文](README_zh.md) | [日本語](README_jp.md)**

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Hardware Requirements](#hardware-requirements)
   - [PiCamera2 Module Filter Adjustment](#picamera2-module-filter-adjustment)
4. [Software Requirements](#software-requirements)
5. [Installation Guide](#installation-guide)
6. [Usage Instructions](#usage-instructions)
7. [System Architecture](#system-architecture)
8. [Face Detection Solutions](#face-detection-solutions)
9. [Hand Gesture Recognition](#hand-gesture-recognition)
10. [Hardware Connections](#hardware-connections)
11. [Contributing](#contributing)
12. [License](#license)
13. [Troubleshooting](#troubleshooting)
14. [Acknowledgments](#acknowledgments)

---

## Overview

InfraCamControl is a multifunctional smart camera control system based on Raspberry Pi, integrating infrared remote control, computer vision, and gesture recognition technologies. It receives instructions via Slack, supports infrared device control, face and gesture recognition, and automatically adjusts infrared lighting based on ambient light conditions. The system also supports voice interaction with Apple devices, enabling more intelligent device interaction.

---

## Features

- **Remote Control**: Efficient remote management via Slack.
- **Infrared Learning and Sending**: Supports learning and sending infrared signals.
- **Computer Vision**:
  - Supports multiple face detection methods.
  - Real-time hand gesture recognition.
- **Ambient Light Management**: Automatically adjusts infrared lighting based on light conditions.
- **Multitasking**: Supports multithreading for improved efficiency.
- **Protocol Compatibility**: Supports NEC and Mitsubishi infrared protocols.
- **Apple Device Integration**: Enables smarter control via voice recognition.

---

## Hardware Requirements

- **Raspberry Pi** (Model 4B)
- **PiCamera2** (OV5647 IR-CUT)
- **Infrared LED Emitters** (OSI5LA5A33A-B 940nm) ×3
- **Red LED Indicator Light** (2.3V, 25mA)
- **Infrared Receiver Module** (OSRB38C9AA)
- **N-channel MOSFETs** (2SK2232) ×2
- **Slide Switch**
- **Button**
- **Resistors**:
  - 47Ω (±5%) ×3
  - 100Ω (±5%) ×1
  - 10kΩ (±5%) ×2

### Hardware Diagram

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="Breadboard Diagram" width="48%; height: auto;" />
  <img src="image/circuit_diagram.png" alt="Circuit Diagram" width="48%; height: auto;" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi Implementation" width="48% height: auto;" />
  <img src="image/Tangent Diagram.jpg" alt="Tangent Diagram" width="48% height: auto;" />
</div>

---

### PiCamera2 Module Filter Adjustment

**Note**: The OV5647 IR-CUT module cannot automatically switch the infrared filter and needs to be manually removed. Follow these steps for non-destructive disassembly:

1. **Remove Screws and Connectors**  
   Unscrew the red-marked screws and unplug the blue-marked connector.  
   <img src="image/Step1.png" alt="Step 1" width="30%" />

2. **Adjust Filter and Lever**  
   Move the blue-marked filter to the target position, and gently lift the red-marked lever while keeping it in place. Reattach the screws without reconnecting the connector.
   <div style="display: flex; justify-content: space-between;">
   <img src="image/Step2.png" alt="Step 2" style="width: 58%; height: auto;" />
   <img src="image/Step3.png" alt="Step 3" style="width: 38%; height: auto;" />
   </div>

---

## Software Requirements

- **Python 3.x**
- Necessary Python Packages (install via pip):
  - `picamera2`
  - `opencv-python`
  - `pigpio`
  - `slack-sdk`
  - `numpy`
  - `onnxruntime` (for Ultra-Light-Fast model)
  - `ultralytics` (for YOLOv8)
  - `mediapipe`

---

## Installation Guide

1. **Clone the Repository**

   ```bash
   git clone https://github.com/CC5103/InfraCamControl.git
   cd InfraCamControl
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Slack Integration**  
   Create a `config.json` file and add your Slack credentials:
   ```json
   {
     "BOT_TOKEN": "your-slack-bot-token",
     "ID": "your-channel-id"
   }
   ```

---

## Usage Instructions

1. **Start the pigpio Daemon**

   ```bash
   sudo pigpiod
   ```

2. **Run the Main Program**

   ```bash
   python3 InfraCamControl/software/main_mediapipe.py
   ```

3. **Create Infrared Signals**  
   Input the following command in Slack to record a signal:

   ```bash
   crate <save_type> <save_key> <save_name>
   ```

   - **Hardware Operation**: Set the switch to the infrared receiver, press the button to record the signal.
   - **Signal Protocol**: Supports NEC or Mitsubishi protocols (940nm).
   - **File Management**: The system automatically generates signal files and updates them in `signal_list.json`.

4. **Send Infrared Signals**

   - **Slack Control**: Type `<save_key>` to trigger the signal (press the button to light up the red indicator for confirmation).
   - **Gesture Control**: Use hand gestures to send the bound signal (spread fingers to activate the system, then the red light automatically turns on as feedback. After activation, perform the corresponding gesture).

---

## System Architecture

The system consists of two main threads:

1. **Slack Message Thread**

   - Listens for commands
   - Manages infrared signal recording and sending

2. **Camera Thread**
   - Face detection
   - Ambient light monitoring and infrared light adjustment

---

## Face Detection Solutions

The system offers the following face detection methods:

### 1. OpenCV Haar Cascade

- **Advantages**: Fast, low resource usage.
- **Disadvantages**: Lower accuracy, sensitive to lighting conditions.
- **Use Case**: Resource-limited environments.

### 2. YOLOv8

- **Advantages**: High detection accuracy, supports multi-target detection.
- **Disadvantages**: Higher resource usage.
- **Use Case**: High-precision applications.

### 3. Ultra-Light-Fast

- **Advantages**: Fast, moderate resource usage.
- **Disadvantages**: Only supports single-face detection.
- **Use Case**: Balanced performance and resource demand.

### 4. MediaPipe Face Mesh

- **Advantages**: High accuracy, supports multi-person detection.
- **Disadvantages**: Requires significant computational resources.
- **Use Case**: Applications needing detailed feature analysis.

---

## Hand Gesture Recognition

The system uses MediaPipe for real-time hand gesture recognition. Supported gestures include:

- **Open Hand**: Activate the system, and the red light turns on.
- **Index Finger**: Turn the light on/off.
- **Index + Middle Finger**: Turn on the air conditioner.
- **Index + Middle + Ring Finger**: Turn off the air conditioner.

---

## Hardware Connections

Key GPIO Interface Descriptions:

- **GPIO8**: Infrared LED Emitters
- **GPIO24**: Infrared Receiver Module
- **GPIO18**: Gesture Recognition Feedback (lights up the red indicator)
- **CSI Interface**: Camera Module Connection
- **Status LED**: Displays system status

---

## Contributing

1. Fork the repository.
2. Create a branch.
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes.
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push the branch.
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Submit a Pull Request.

---

## License

This project is licensed under the GNU General Public License (GPL). See the `LICENSE` file for details.

---

## Troubleshooting

- Ensure the `pigpiod` service is running.
- Check if the Slack configuration is correct.
- Verify hardware connections.
- Confirm the camera module is enabled.

---

## Acknowledgments

- [yhotta240's Infrared Tutorial](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b)
- [Casareal BS Blog's Air Conditioner Remote Control Tutorial](https://bsblog.casareal.co.jp/archives/5010)
- [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [Google MediaPipe](https://github.com/google/mediapipe)

---
