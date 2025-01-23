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

InfraCamControl is a multifunctional smart camera control system based on Raspberry Pi, integrating infrared remote control, computer vision, and gesture recognition technology. It receives commands via Slack, supports infrared device control, face and gesture recognition, and automatically adjusts infrared illumination based on environmental light. The system also supports voice interaction with Apple devices for smarter device control.

---

## Features

- **Remote Control**: Efficient remote management through Slack.
- **Infrared Learning and Transmission**: Supports learning and sending infrared signals.
- **Computer Vision**:
  - Supports multiple face detection solutions.
  - Real-time hand gesture recognition.
- **Ambient Light Management**: Automatically adjusts infrared lighting based on light conditions.
- **Multitasking Concurrency**: Supports multithreading for better performance.
- **Protocol Compatibility**: Supports NEC and Mitsubishi infrared signal protocols.
- **Apple Device Integration**: Voice recognition for smarter control.

---

## Hardware Requirements

- **Raspberry Pi** (Model 4B)
- **PiCamera2** (OV5647 IR-CUT)
- **Infrared LED Emitters** (OSI5FU5111C-40 940nm) ×3
- **Green LED Indicator** (OSG8HA3Z74A)
- **Infrared Receiver Module** (OSRB38C9AA)
- **N-Channel MOSFET** (2SK2232)
- **Slide Switch**
- **Buttons**
- **Resistors**:
  - 100Ω (±5%) ×4
  - 10kΩ (±5%) ×1

### Hardware Diagram

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="Breadboard Circuit Diagram" width="48%" height="auto" />
  <img src="image/circuit_diagram.png" alt="Circuit Diagram" width="48%" height="auto" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi Implementation Diagram" width="48%" height="auto" />
  <img src="image/Tangent Diagram.jpg" alt="Tangent Diagram" width="48%" height="auto" />
</div>

---

### PiCamera2 Module Filter Adjustment

**Note**: The OV5647 IR-CUT module cannot automatically switch filters and requires manual removal. Below are the steps for safe disassembly:

1. **Remove Screws and Connector**  
   Unscrew the red-marked screws and unplug the blue-marked connector.  
   <img src="image/Step1.png" alt="Step 1" width="30%" />

2. **Adjust Filter and Lever**  
   Move the blue-marked filter to the target position, gently lift the red-marked lever, and keep the lever in place. Reattach the screws without resetting the connector.
   <div style="display: flex; justify-content: space-between;">
   <img src="image/Step2.png" alt="Step 2" style="width: 58%; height: auto;" />
   <img src="image/Step3.png" alt="Step 3" style="width: 38%; height: auto;" />
   </div>

---

## Software Requirements

- **Python 3.x**
- Required Python packages (install via pip):
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
   python main_mediapipe.py
   ```

3. **Create Infrared Signal**  
   To record a signal in Slack, type the following command:

   ```bash
   crate <save_type> <save_key> <save_name>
   ```

   - **Hardware Action**: Switch to the infrared receiver, press the button to record the signal.
   - **Signal Protocol**: Supports NEC or Mitsubishi protocol (940nm).
   - **File Management**: The system automatically generates signal files and updates them in `signal_list.json`.

4. **Send Infrared Signal**

   - **Slack Control**: Type `<save_key>` to trigger the signal.
   - **Gesture Control**: Send the bound signal by performing the corresponding gesture (e.g., 5 fingers to activate recognition).

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

The system provides the following face detection methods:

### 1. OpenCV Haar Cascade

- Pros: Fast, low resource usage.
- Cons: Lower accuracy, sensitive to lighting conditions.
- Suitable for: Resource-limited environments.

### 2. YOLOv8

- Pros: High detection accuracy, supports multi-object detection.
- Cons: Higher resource usage.
- Suitable for: High-accuracy applications.

### 3. Ultra-Light-Fast

- Pros: Fast, moderate resource usage.
- Cons: Single face detection only.
- Suitable for: Balancing performance and resource demands.

### 4. MediaPipe Face Mesh

- Pros: High accuracy, supports multiple face detection.
- Cons: High computational resource requirements.
- Suitable for: Applications requiring fine feature analysis.

---

## Hand Gesture Recognition

The system uses MediaPipe for real-time hand gesture recognition, supporting the following gestures:

- **Index Finger**: Switch to "0" state.
- **Index + Middle Finger**: Turn on the device ("on").
- **Index + Middle + Ring Finger**: Turn off the device ("off").
- **Open Hand**: Start the system ("start").

---

## Hardware Connections

Key GPIO Interface Description:

- **GPIO25**: Infrared LED Emitters
- **GPIO23**: Infrared Receiver Module
- **CSI Interface**: Camera Module connection
- **Status LED**: Displays system operational status

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
4. Push your branch.
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Submit a Pull Request.

---

## License

This project is licensed under the GNU General Public License (GPL). See the `LICENSE` file for more details.

---

## Troubleshooting

- Ensure the `pigpiod` service is running.
- Check Slack configuration.
- Verify hardware connections.
- Confirm the camera module is enabled.

---

## Acknowledgments

- [yhotta240's infrared tutorial](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b)
- [Casareal BS blog air conditioner remote tutorial](https://bsblog.casareal.co.jp/archives/5010)
- [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [Google MediaPipe](https://github.com/google/mediapipe)

---
