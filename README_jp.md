# InfraCamControl

**他の言語版：[English](README.md) | [中文](README_zh.md) | [日本語](README_jp.md)**

---

## 目次

- [InfraCamControl](#infracamcontrol)
  - [目次](#目次)
  - [概要](#概要)
  - [特徴](#特徴)
  - [ハードウェア要件](#ハードウェア要件)
    - [PiCamera2モジュールのフィルター調整](#picamera2モジュールのフィルター調整)
  - [ソフトウェア要件](#ソフトウェア要件)
  - [インストールガイド](#インストールガイド)
  - [使用方法](#使用方法)
  - [システムアーキテクチャ](#システムアーキテクチャ)
  - [ハードウェア接続](#ハードウェア接続)
  - [貢献方法](#貢献方法)
  - [ライセンス](#ライセンス)
  - [トラブルシューティング](#トラブルシューティング)
  - [謝辞](#謝辞)

---

## 概要

InfraCamControlは、Raspberry Piをベースにした革新的なシステムで、赤外線リモコン機能とコンピュータビジョン技術を組み合わせて、自動化されたカメラ制御を実現します。このシステムは、Slackを通じて指令を受け取り、赤外線機器を制御し、環境光に応じて赤外線照明を自動調整します。また、Appleデバイスとの連携により、音声コントロールやその他のスマート機能を実現します。

---

## 特徴

- **リモート制御**：Slack統合を通じて効率的なリモート管理が可能。
- **赤外線学習と送信**：赤外線信号の学習と送信をサポート。
- **コンピュータビジョン**：顔認識などのターゲット識別機能を提供。
- **環境光管理**：照明条件に応じて赤外線照明を自動調整。
- **マルチタスク対応**：スレッド処理をサポートし、効率的な動作を実現。
- **プロトコル互換性**：NECや三菱の赤外線信号プロトコルをサポート。
- **Appleデバイス連携**：音声認識によるさらにスマートな制御を実現。

---

## ハードウェア要件

- **Raspberry Pi** (Model 4B)
- **PiCamera2**（OV5647 IR-CUT）
- **赤外線LED発光器**（OSI5FU5111C-40 940nm）×3
- **緑色LEDインジケータ**（OSG8HA3Z74A）
- **赤外線受信モジュール**（OSRB38C9AA）
- **NチャネルMOSFET**（2SK2232）
- **スライドスイッチ**
- **ボタン**
- **抵抗器**：
  - 100Ω（±5%）×4
  - 10kΩ（±5%）×1

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="ブレッドボード回路図" width="48%; height: auto;" />
  <img src="image/circuit_diagram.png" alt="回路図" width="48%; height: auto;" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi 実装図" width="48% height: auto;" />
  <img src="image/Tangent Diagram.jpg" alt="補助図" width="48% height: auto;" />
</div>

---

### PiCamera2モジュールのフィルター調整

**注意**：OV5647 IR-CUTモジュールは自動的に赤外線フィルターを切り替えません。手動でフィルターを取り外す必要があります。以下は無損傷での取り外し手順です。

1. **ネジとコネクタを外す**  
   赤色マークのネジを外し、青色マークのコネクタを抜きます。  
   <img src="image/Step1.png" alt="ステップ1" width="30%" />

2. **フィルターとレバーの調整**  
   青色マークのフィルターを所定の位置に移動し、赤色マークのレバーを少し上げた状態で固定します。コネクタを再接続する必要はありません。  
   <div style="display: flex; justify-content: space-between;">
   <img src="image/Step2.png" alt="ステップ2" style="width: 58%; height: auto;" />
   <img src="image/Step3.png" alt="ステップ3" style="width: 38%; height: auto;" />
   </div>

---

## ソフトウェア要件

- **Python 3.x**
- 必要なPythonパッケージ（pipでインストール）：
  - `picamera2`
  - `opencv-python`
  - `pigpio`
  - `slack-sdk`
  - `numpy`

---

## インストールガイド

1. **リポジトリをクローン**  
   ```bash
   git clone https://github.com/CC5103/InfraCamControl.git
   cd InfraCamControl
   ```

2. **依存パッケージをインストール**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Slack統合の設定**  
   `config.json`ファイルを作成し、Slackの認証情報を追加します：  
   ```json
   {
       "BOT_TOKEN": "your-slack-bot-token",
       "ID": "your-channel-id"
   }
   ```

---

## 使用方法

1. **pigpioデーモンを起動**  
   ```bash
   sudo pigpiod
   ```

2. **メインプログラムを実行**  
   ```bash
   python main.py
   ```

3. **赤外線信号を作成**  
   Slackで次のコマンドを入力して信号を録音します：  
   ```bash
   crate <save_type> <save_key> <save_name>
   ```
   - **ハードウェア操作**：スイッチを赤外線受信機に設定し、ボタンを押して信号を録音します。  
   - **信号プロトコル**：NECまたは三菱プロトコル（940nm）に対応。  
   - **ファイル管理**：システムは信号ファイルを自動生成し、`signal_list.json`に更新します。

4. **赤外線信号を送信**  
   Slackで`<save_key>`を入力して信号を送信します。  
   **ヒント**：回路ボタンを押して、ハードウェアの機能が正常かどうかをテストできます。

---

## システムアーキテクチャ

システムは主に2つのコアスレッドで構成されています：

1. **Slackメッセージスレッド**  
   - コマンドのリスニング  
   - 赤外線信号の録音と送信管理  

2. **カメラスレッド**  
   - 顔認識  
   - 環境光の監視と赤外線ライト調整  

---

## ハードウェア接続

主要GPIOインターフェースの説明：  
- **GPIO25**：赤外線LED発光器  
- **GPIO23**：赤外線受信モジュール  
- **CSIインターフェース**：カメラモジュール接続  
- **ステータスLED**：システムの動作状態を表示  

---

## 貢献方法

1. リポジトリをFork  
2. ブランチを作成  
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 変更をコミット  
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. ブランチをプッシュ  
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Pull Requestを送信  

---

## ライセンス

本プロジェクトはGNU一般公開ライセンス（GPL）に基づいて公開されています。詳細は`LICENSE`ファイルを参照してください。

---

## トラブルシューティング

- `pigpiod`サービスが起動しているか確認します。  
- Slack設定が正しいか確認します。  
- ハードウェア接続を確認します。  
- カメラモジュールが有効になっているか確認します。

---

## 謝辞

- **pigpio**と**OpenCV**の開発チームに感謝します。  
- 特別な謝辞：  
  - [yhotta240の赤外線チュートリアル](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b)  
  - [Casareal BSブログのエアコンリモコンチュートリアル](https://bsblog.casareal.co.jp/archives/5010)  

---