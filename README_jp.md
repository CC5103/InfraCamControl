# InfraCamControl

**Other Language Versions: [English](README.md) | [中文](README_zh.md) | [日本語](README_jp.md)**

---

## 目次

- [InfraCamControl](#infracamcontrol)
  - [目次](#目次)
  - [概要](#概要)
  - [特徴](#特徴)
  - [ハードウェア要件](#ハードウェア要件)
    - [PiCamera2 モジュールフィルタ調整](#picamera2モジュールフィルタ調整)
  - [ソフトウェア要件](#ソフトウェア要件)
  - [インストールガイド](#インストールガイド)
  - [使用方法](#使用方法)
  - [システムアーキテクチャ](#システムアーキテクチャ)
  - [顔検出ソリューション](#顔検出ソリューション)
  - [ハードウェア接続](#ハードウェア接続)
  - [貢献方法](#貢献方法)
  - [ライセンス](#ライセンス)
  - [トラブルシューティング](#トラブルシューティング)
  - [謝辞](#謝辞)

---

## 概要

InfraCamControl は、Raspberry Pi をベースにした革新的なシステムで、赤外線リモコン機能とコンピュータビジョン技術を組み合わせて、自動カメラ制御を実現します。システムは Slack を通じてコマンドを受信し、赤外線デバイスを制御するとともに、周囲の光に応じて赤外線照明を自動調整し、Apple デバイスと連携して音声制御やその他のスマート機能を実現します。

---

## 特徴

- **リモート制御**：Slack 統合を通じて効率的なリモート管理。
- **赤外線信号の学習と送信**：赤外線信号の学習と送信をサポート。
- **コンピュータビジョン**：
  - OpenCV Haar Cascade
  - YOLOv8
  - Ultra-Light-Fast
- **周囲光管理**：照明条件に応じて赤外線照明を自動調整。
- **マルチタスク対応**：マルチスレッド処理により、パフォーマンスを向上。
- **プロトコル互換性**：NEC および三菱赤外線信号プロトコルに対応。
- **Apple デバイスとの連携**：音声認識によるよりインテリジェントな制御。

---

## ハードウェア要件

- **Raspberry Pi**（モデル 4B）
- **PiCamera2**（OV5647 IR-CUT）
- **赤外線 LED エミッター**（OSI5FU5111C-40 940nm）×3
- **緑色 LED インジケーター**（OSG8HA3Z74A）
- **赤外線受信モジュール**（OSRB38C9AA）
- **N チャネル MOSFET**（2SK2232）
- **スライドスイッチ**
- **ボタン**
- **抵抗器**：
  - 100Ω（±5%）×4
  - 10kΩ（±5%）×1

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="ブレッドボード回路図" width="48%" height="auto" />
  <img src="image/circuit_diagram.png" alt="回路図" width="48%" height="auto" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi 実装図" width="48%" height="auto" />
  <img src="image/Tangent Diagram.jpg" alt="補助図" width="48%" height="auto" />
</div>

---

### PiCamera2 モジュールフィルタ調整

**注意**：OV5647 IR-CUT モジュールは自動的に赤外線フィルタを切り替えることができないため、手動でフィルタを取り外す必要があります。無損傷で取り外す手順は以下の通りです。

1. **ネジとコネクタを取り外す**  
   赤色のマークのネジを外し、青色のマークのコネクタを抜きます。  
   <img src="image/Step1.png" alt="ステップ1" width="30%" />

2. **フィルタとレバーの調整**  
   青色のマークのフィルタを目的の位置に移動させ、赤色のマークのレバーを軽く持ち上げて、その位置を維持します。ネジを再度締めてコネクタは戻さなくても構いません。
   <div style="display: flex; justify-content: space-between;">
   <img src="image/Step2.png" alt="ステップ2" style="width: 58%; height: auto;" />
   <img src="image/Step3.png" alt="ステップ3" style="width: 38%; height: auto;" />
   </div>

---

## ソフトウェア要件

- **Python 3.x**
- 必要な Python パッケージ（pip でインストール）：
  - `picamera2`
  - `opencv-python`
  - `pigpio`
  - `slack-sdk`
  - `numpy`
  - `onnxruntime`（Ultra-Light-Fast モデル用）
  - `ultralytics`（YOLOv8 用）

---

## インストールガイド

1. **リポジトリをクローンする**

   ```bash
   git clone https://github.com/CC5103/InfraCamControl.git
   cd InfraCamControl
   ```

2. **依存関係をインストールする**

   ```bash
   pip install -r requirements.txt
   ```

3. **Slack 統合の設定**  
   `config.json`ファイルを作成し、Slack の資格情報を追加します：

   ```json
   {
     "BOT_TOKEN": "your-slack-bot-token",
     "ID": "your-channel-id"
   }
   ```

---

## 使用方法

1. **pigpio デーモンを起動する**

   ```bash
   sudo pigpiod
   ```

2. **メインプログラムを実行する**

   ```bash
   python main.py
   ```

3. **赤外線信号を作成する**  
   以下のコマンドを Slack で入力して信号を録音します：

   ```bash
   crate <save_type> <save_key> <save_name>
   ```

   - **ハードウェア操作**：スイッチを赤外線受信機に設定し、ボタンを押して信号を録音します。
   - **信号プロトコル**：NEC または三菱プロトコル（940nm）に対応。
   - **ファイル管理**：システムは信号ファイルを自動的に生成し、`signal_list.json`に更新します。

4. **赤外線信号を送信する**  
   Slack で`<save_key>`を入力して信号送信をトリガーします。  
   **ヒント**：回路ボタンを押してハードウェア機能が正常かどうかをテストできます。

---

## システムアーキテクチャ

システムには 2 つの主要スレッドがあります：

1. **Slack メッセージスレッド**

   - コマンドをリッスン
   - 赤外線信号の録音と送信を管理

2. **カメラスレッド**
   - 顔検出
   - 周囲光監視と赤外線照明調整

---

## 顔検出ソリューション

システムは 3 つの異なる顔検出実装を提供しており、ニーズに応じて選択できます：

### 1. OpenCV Haar Cascade（main.py）

- 従来の Haar 特徴分類器に基づいています
- 利点：
  - 実行速度が速い
  - リソース消費が少ない
  - 追加依存関係が不要
- 欠点：
  - 精度が低い
  - 照明条件に敏感
- 使用例：リソースが制限された環境

### 2. YOLOv8（main_yolo.py）

- 最新の YOLOv8 深層学習モデルに基づいています
- 利点：
  - 高い検出精度
  - 高い堅牢性
  - 複数ターゲット検出に対応
- 欠点：
  - リソース消費が高い
  - モデルのダウンロードが必要
- 使用例：高精度が求められるアプリケーション

### 3. Ultra-Light-Fast（main_ultralight.py）

- 軽量のニューラルネットワークモデルに基づいています
- 利点：
  - 高速な検出
  - 適度なリソース消費
  - 良好な精度
- 欠点：
  - モデルのダウンロードが必要
  - 単一の顔検出のみ対応
- 使用例：パフォーマンスとリソースのバランスが求められる場合

---

## ハードウェア接続

主な GPIO インターフェースの説明：

- **GPIO25**：赤外線 LED エミッター
- **GPIO23**：赤外線受信モジュール
- **CSI インターフェース**：カメラモ

ジュール接続

- **ステータス LED**：システムの状態を表示

---

## 貢献方法

1. リポジトリをフォークする
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
5. プルリクエストを作成

---

## ライセンス

このプロジェクトは GNU General Public License（GPL）で公開されています。詳細は`LICENSE`ファイルを参照してください。

---

## トラブルシューティング

- `pigpiod`サービスが実行中であることを確認してください。
- Slack 設定が正しいか確認してください。
- ハードウェア接続を確認してください。
- カメラモジュールが有効になっているか確認してください。

---

## 謝辞

- **pigpio**および**OpenCV**の開発チームに感謝します。
- 特に以下の方々に感謝します：
  - [yhotta240 の赤外線チュートリアル](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b)
  - [Casareal BS ブログのエアコンリモコンチュートリアル](https://bsblog.casareal.co.jp/archives/5010)
  - [Ultra-Light-Fast-Generic-Face-Detector-1MB](https://github.com/Linzaer/Ultra-Light-Fast-Generic-Face-Detector-1MB)
  - [YOLOv8](https://github.com/ultralytics/ultralytics)
  - [OpenCV](https://opencv.org/)
