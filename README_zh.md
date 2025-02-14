# InfraCamControl

**Other Language Versions: [English](README.md) | [中文](README_zh.md) | [日本語](README_jp.md)**

---

## 目录

- [InfraCamControl](#infracamcontrol)
  - [目录](#目录)
  - [概述](#概述)
  - [特性](#特性)
  - [硬件需求](#硬件需求)
    - [硬件示意图](#硬件示意图)
    - [PiCamera2 模组滤镜调整](#picamera2-模组滤镜调整)
  - [软件需求](#软件需求)
  - [安装指南](#安装指南)
  - [使用说明](#使用说明)
  - [系统架构](#系统架构)
  - [面部检测方案](#面部检测方案)
    - [1. OpenCV Haar Cascade](#1-opencv-haar-cascade)
    - [2. YOLOv8](#2-yolov8)
    - [3. Ultra-Light-Fast](#3-ultra-light-fast)
    - [4. MediaPipe Face Mesh](#4-mediapipe-face-mesh)
  - [手部手势识别](#手部手势识别)
  - [硬件连接](#硬件连接)
  - [贡献方式](#贡献方式)
  - [许可证](#许可证)
  - [故障排除](#故障排除)
  - [致谢](#致谢)

---

## 概述

InfraCamControl 是一个基于 Raspberry Pi 的多功能智能相机控制系统，集成了红外遥控、计算机视觉和手势识别技术。通过 Slack 接收指令，支持红外设备控制、人脸和手势识别，并能根据环境光自动调整红外照明。同时，系统支持与苹果设备的语音联动，实现更智能的设备交互。

---

## 特性

- **远程控制**：通过 Slack 实现高效远程管理。
- **红外学习与发送**：支持红外信号的学习与发送。
- **计算机视觉**：
  - 支持多种人脸检测方案。
  - 实时手部手势识别。
- **环境光管理**：根据光照条件自动调节红外照明。
- **多任务并发**：支持多线程处理，提升运行效率。
- **协议兼容性**：支持 NEC 和三菱红外信号协议。
- **苹果设备联动**：通过语音识别实现更智能的控制。

---

## 硬件需求

- **Raspberry Pi** (Model 4B)
- **PiCamera2**（OV5647 IR-CUT）
- **红外 LED 发光器**（OSI5LA5A33A-B 940nm）×9
- **红色 LED 指示灯**（2.3V, 25mA）
- **二极管**（1N5819）
- **红外接收模块**（OSRB38C9AA）
- **N 沟道 MOSFET**（2SK2232）×2
- **滑动开关**
- **按钮**
- **电阻器**：
  - 2.2Ω (±5%) ×3
  - 10Ω (±5%) ×1
  - 100Ω（±5%）×1
  - 10kΩ（±5%）×2

### 硬件示意图

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="面包板电路图" width="48%; height: auto;" />
  <img src="image/circuit_diagram.png" alt="电路图" width="48%; height: auto;" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi 实现图" width="48%" height="auto;" />
  <img src="image/Tangent Diagram.jpg" alt="辅助图" width="48%" height="auto;" />
</div>

---

### PiCamera2 模组滤镜调整

**注意**：OV5647 IR-CUT 模组无法自动切换红外滤镜，需手动移除滤镜。以下为无损拆卸步骤：

1. **拆卸螺丝和插头**  
   卸下红色标记的螺丝，拔掉蓝色标记的插头。  
   <img src="image/Step1.png" alt="步骤1" width="30%" />

2. **调整滤镜和拨杆**  
   将蓝色标记的滤镜移至目标位置，并轻微翘起红色标记的拨杆，保持拨杆位置不变。重新固定螺丝，无需复位插头。
   <div style="display: flex; justify-content: space-between;">
     <img src="image/Step2.png" alt="步骤2" style="width: 58%; height: auto;" />
     <img src="image/Step3.png" alt="步骤3" style="width: 38%; height: auto;" />
   </div>

---

## 软件需求

- **Python 3.x**
- 必要 Python 包（通过 pip 安装）：
  - `picamera2`
  - `opencv-python`
  - `pigpio`
  - `slack-sdk`
  - `numpy`
  - `onnxruntime` (用于 Ultra-Light-Fast 模型)
  - `ultralytics` (用于 YOLOv8)
  - `mediapipe`

---

## 安装指南

1. **克隆仓库**

   ```bash
   git clone https://github.com/CC5103/InfraCamControl.git
   cd InfraCamControl
   ```

2. **安装依赖**

   ```bash
   pip install -r requirements.txt
   ```

3. **配置 Slack 集成**  
   创建 `config.json` 文件并添加 Slack 凭证：
   ```json
   {
     "BOT_TOKEN": "your-slack-bot-token",
     "ID": "your-channel-id"
   }
   ```

---

## 使用说明

1. **启动 pigpio 守护进程**

   ```bash
   sudo pigpiod
   ```

2. **运行主程序**

   ```bash
   python3 InfraCamControl/software/main_mediapipe.py
   ```

3. **创建红外信号**  
   在 Slack 中输入以下命令录入信号：

   ```bash
   crate <save_type> <save_key> <save_name>
   ```

   - **硬件操作**：将开关拨至红外接收器，按下按钮录制信号。
   - **信号协议**：支持 NEC 或三菱协议（940nm）。
   - **文件管理**：系统自动生成信号文件，并更新到 `signal_list.json`。

4. **发送红外信号**

   - **Slack 控制**：输入 `<save_key>` 触发信号发送（按下按钮点亮红灯可以确认系统是否正常）。
   - **手势控制**：通过手势识别发送绑定信号（5 指张开激活系统此时红灯自动点亮作为反馈，激活后比出对应手势）。

---

## 系统架构

系统包含两大核心线程：

1. **Slack 消息线程**

   - 监听命令
   - 管理红外信号录制与发送

2. **相机线程**
   - 人脸检测
   - 环境光监测与红外灯调节

---

## 面部检测方案

系统提供以下四种面部检测实现方案：

### 1. OpenCV Haar Cascade

- 优点：运行速度快，资源占用少。
- 缺点：准确率较低，对光照条件敏感。
- 适用场景：资源受限环境。

### 2. YOLOv8

- 优点：检测精度高，支持多目标检测。
- 缺点：资源占用较高。
- 适用场景：高精度应用。

### 3. Ultra-Light-Fast

- 优点：速度快，资源占用适中。
- 缺点：仅支持单人脸检测。
- 适用场景：平衡性能与资源需求。

### 4. MediaPipe Face Mesh

- 优点：高精度，支持多人检测。
- 缺点：对计算资源要求较高。
- 适用场景：需要精细特征分析的应用。

---

## 手部手势识别

系统通过 MediaPipe 实现实时手部手势识别功能，支持以下手势控制：

- **全手张开**：启动系统，此时红灯点亮。
- **食指**：开/关灯。
- **食指 + 中指**：开空调。
- **食指 + 中指 + 无名指**：关空调。

---

## 硬件连接

关键 GPIO 接口说明：

- **GPIO8**：红外 LED 发射器
- **GPIO25**：红外接收模块
- **GPIO23**：手势识别反馈（点亮红灯）
- **CSI 接口**：摄像头模块连接
- **状态 LED**：显示系统运行状态

---

## 贡献方式

1. Fork 仓库。
2. 创建分支。
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 提交更改。
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. 推送分支。
   ```bash
   git push origin feature/AmazingFeature
   ```
5. 提交 Pull Request。

---

## 许可证

本项目基于 GNU 通用公共许可证（GPL）发布。详情参见 `LICENSE` 文件。

---

## 故障排除

- 确保已启动 `pigpiod` 服务。
- 检查 Slack 配置是否正确。
- 验证硬件连接。
- 确认摄像头模块已启用。

---

## 致谢

- [yhotta240 的红外教程](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b)
- [Casareal BS 博客的空调遥控教程](https://bsblog.casareal.co.jp/archives/5010)
- [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [OpenCV](https://opencv.org/)
- [Google MediaPipe](https://github.com/google/mediapipe)

---
