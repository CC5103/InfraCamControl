# InfraCamControl

**Other language versions: [English](README.md) | [中文](README_zh.md) | [日本語](README_jp.md)**

---

## Table of Contents

- [InfraCamControl](#infracamcontrol)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Hardware Requirements](#hardware-requirements)
    - [PiCamera2 Module Filter Adjustment](#picamera2-module-filter-adjustment)
  - [Software Requirements](#software-requirements)
  - [Installation Guide](#installation-guide)
  - [Usage Instructions](#usage-instructions)
  - [System Architecture](#system-architecture)
  - [Hardware Connections](#hardware-connections)
  - [Contribution Guidelines](#contribution-guidelines)
  - [License](#license)
  - [Troubleshooting](#troubleshooting)
  - [Acknowledgments](#acknowledgments)

---

## Overview

InfraCamControl is an innovative system based on Raspberry Pi that combines infrared remote control functionality with computer vision technology for automated camera control. The system receives commands via Slack, controls infrared devices, automatically adjusts infrared lighting according to ambient light, and integrates with Apple devices for voice control and other smart features.

---

## Features

- **Remote Control**: Efficient remote management through Slack integration.
- **Infrared Learning and Sending**: Supports learning and sending infrared signals.
- **Computer Vision**: Provides target recognition (e.g., face detection).
- **Ambient Light Management**: Automatically adjusts infrared lighting based on lighting conditions.
- **Multitasking**: Supports multithreaded processing for enhanced efficiency.
- **Protocol Compatibility**: Supports NEC and Mitsubishi infrared signal protocols.
- **Apple Device Integration**: Enables smart control via voice recognition.

---

## Hardware Requirements

- **Raspberry Pi** (Model 4B)
- **PiCamera2** (OV5647 IR-CUT)
- **Infrared LED Emitters** (OSI5FU5111C-40 940nm) ×3
- **Green LED Indicator** (OSG8HA3Z74A)
- **Infrared Receiver Module** (OSRB38C9AA)
- **N-channel MOSFET** (2SK2232)
- **Slide Switch**
- **Button**
- **Resistors**:
  - 100Ω (±5%) ×4
  - 10kΩ (±5%) ×1

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="Breadboard Circuit Diagram" width="48%; height: auto;" />
  <img src="image/circuit_diagram.png" alt="Circuit Diagram" width="48%; height: auto;" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi Implementation Diagram" width="48% height: auto;" />
  <img src="image/Tangent Diagram.jpg" alt="Supplementary Diagram" width="48% height: auto;" />
</div>

---

### PiCamera2 Module Filter Adjustment

**Note**: The OV5647 IR-CUT module does not automatically switch infrared filters, and the filter must be manually removed. Below are the steps for non-destructive removal:

1. **Remove Screws and Connectors**  
   Unscrew the red-marked screws and unplug the blue-marked connector.  
   <img src="image/Step1.png" alt="Step 1" width="30%" />

2. **Adjust the Filter and Lever**  
   Move the blue-marked filter to the target position, and gently lift the red-marked lever while keeping it in place. Screw everything back without reconnecting the plug.  
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

---

## Installation Guide

1. **Clone the repository**  
   ```bash
   git clone https://github.com/CC5103/InfraCamControl.git
   cd InfraCamControl
   ```

2. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Slack integration**  
   Create a `config.json` file and add your Slack credentials:  
   ```json
   {
       "BOT_TOKEN": "your-slack-bot-token",
       "ID": "your-channel-id"
   }
   ```

---

## Usage Instructions

1. **Start the pigpio daemon**  
   ```bash
   sudo pigpiod
   ```

2. **Run the main program**  
   ```bash
   python main.py
   ```

3. **Create infrared signals**  
   In Slack, enter the following command to record a signal:  
   ```bash
   crate <save_type> <save_key> <save_name>
   ```
   - **Hardware operation**: Set the switch to the infrared receiver and press the button to record the signal.
   - **Signal protocol**: Supports NEC or Mitsubishi protocol (940nm).
   - **File management**: The system will automatically generate a signal file and update it in `signal_list.json`.

4. **Send infrared signals**  
   In Slack, input `<save_key>` to trigger the signal.  
   **Tip**: Press the circuit button to test whether the hardware is functioning properly.

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

## Hardware Connections

Key GPIO interface descriptions:  
- **GPIO25**: Infrared LED emitter  
- **GPIO23**: Infrared receiver module  
- **CSI Interface**: Camera module connection  
- **Status LED**: Displays system status  

---

## Contribution Guidelines

1. Fork the repository  
2. Create a new branch  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit changes  
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push the branch  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Submit a Pull Request  

---

## License

This project is licensed under the GNU General Public License (GPL). See the `LICENSE` file for details.

---

## Troubleshooting

- Ensure the `pigpiod` service is running.  
- Check that the Slack configuration is correct.  
- Verify hardware connections.  
- Confirm that the camera module is enabled.

---

## Acknowledgments

- Thanks to the development teams of **pigpio** and **OpenCV**.
- Special thanks to:  
  - [yhotta240's infrared tutorial](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b)  
  - [Casareal BS blog's air conditioner remote tutorial](https://bsblog.casareal.co.jp/archives/5010)

---