# InfraCamControl

**Read in other languages: [English](README.md), [中文](README_zh.md), [日本語](README_jp.md).**

## Overview

InfraCamControl is a Raspberry Pi-based system that combines infrared remote control functionality with computer vision for automated camera control. It can receive commands via Slack to control infrared devices, automatically manage infrared lighting based on ambient light levels, and integrate with iPhones for voice recognition and other automation features, enhancing intelligence and convenience.

## Features

- **Remote control**: Integrated with Slack for remote control
- **Infrared learning and sending**: Supports recording and sending infrared signals
- **Face detection**: Uses computer vision for target identification
- **Ambient light management**: Automatically adjusts infrared lighting based on environmental conditions
- **Multithreading**: Enables concurrent task execution for improved performance
- **Protocol support**: Supports NEC and Mitsubishi infrared protocols
- **Apple integration**: Includes support for voice recognition and intelligent control via iPhone

## Hardware Requirements

- **Raspberry Pi** (Model 4B)  
- **PiCamera2** (OV5647 IR-CUT)  
- **Infrared LED Emitter** (OSI5FU5111C-40 940nm) x3  
- **Green LED Indicator** (OSG8HA3Z74A)  
- **Infrared Receiver Module** (OSRB38C9AA)  
- **N-Channel MOSFET** (2SK2232)  
- **Slide Switch**  
- **Button**  
- **Resistors**:  
  - 100Ω (±5%) x4  
  - 10kΩ (±5%) x1  

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="Breadboard circuit diagram" width="48%" />
  <img src="image/circuit_diagram.png" alt="Circuit diagram" width="48%" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi implementation diagram" width="48%" />
  <img src="image/Tangent Diagram.jpg" alt="Auxiliary diagram" width="48%" />
</div>

## Software Requirements

- Python 3.x
- Required Python packages (install via pip):
  - picamera2
  - opencv-python
  - pigpio
  - slack-sdk
  - numpy

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/CC5103/InfraCamControl.git
   cd InfraCamControl
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure Slack integration:
   Create a `config.json` file and add your Slack credentials:
   ```json
   {
       "BOT_TOKEN": "your-slack-bot-token",
       "ID": "your-channel-id"
   }
   ```

## Usage

1. Start the pigpio daemon:
   ```bash
   sudo pigpiod
   ```

2. Run the main program:
   ```bash
   python main.py
   ```

3. **Record infrared signals**:
   Use the following Slack command to record a signal:
   ```bash
   crate <save_type> <save_key> <save_name>
   ```
   Instructions:
   - Point the switch to the infrared receiver and press the button to record the signal.
   - Supports NEC or Mitsubishi 940nm infrared signal protocols.
   - Automatically generates signal files and updates the mapping between `<save_key>` and `<save_name>` in the `signal_list.json` file.

4. **Send infrared signals**:
   Enter the saved `<save_key>` in Slack to send the corresponding infrared signal for remote control.

   **Tip**: Press the hardware button to confirm that the circuit is functioning correctly.

## System Architecture

The system operates with two primary threads:

1. **Slack Message Thread**:
   - Monitors commands in the Slack channel
   - Handles infrared signal learning and sending tasks

2. **Camera Thread**:
   - Performs face detection
   - Monitors ambient light levels
   - Automatically adjusts infrared lighting

## Circuit Diagram

Hardware components should be connected as follows:
- **GPIO25**: Connect to the infrared LED transmitter
- **GPIO23**: Connect to the infrared receiver module
- **CSI interface**: Used to connect the camera module
- **Status LED**: Indicates system state

## Contribution

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. Push the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License (GPL). See the LICENSE file for more details.

## Troubleshooting

- Ensure the pigpio daemon is running before starting the program.
- Verify Slack bot permissions and token validity.
- Check the connections of the infrared LED and receiver module.
- Ensure the camera module is properly connected and enabled.

## Acknowledgments

- Thanks to the pigpio development team.
- Thanks to the OpenCV community for providing robust face detection functionality.
- Thanks to the Slack API development team for the Python SDK.
- Special thanks to Qiita user yhotta240 for the infrared remote control tutorial [Source](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b).
- Thanks to Casareal's BS Blog for the air conditioner control tutorial using Raspberry Pi [Source](https://bsblog.casareal.co.jp/archives/5010).