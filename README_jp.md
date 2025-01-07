# InfraCamControl

**他の言語バージョンを読む：[English](README.md), [中文](README_zh.md), [日本語](README_jp.md).**

## 概要

InfraCamControl は、Raspberry Pi を基盤としたシステムで、赤外線リモコン機能とコンピュータビジョンを組み合わせ、自動化されたカメラ制御を実現します。Slack を通じてコマンドを受信し、赤外線デバイスを制御するとともに、環境の明るさに応じて赤外線照明を自動的に管理します。また、Apple デバイスと連携し、音声認識やその他の情報に基づいて自動処理を行うことで、さらに高度な利便性を提供します。

## 特徴

- **リモートコントロール**：Slack 統合を介したリモート操作
- **赤外線の学習と送信**：赤外線信号の学習および送信機能に対応
- **顔検出**：コンピュータビジョン技術を用いてターゲットを識別
- **環境光の管理**：赤外線照明を自動調整し、環境光に適応
- **マルチスレッド対応**：複数タスクを並列処理し、効率を向上
- **プロトコル対応**：NEC および三菱の赤外線信号プロトコルをサポート
- **Apple 連携**：Apple デバイスを通じた音声認識とスマートコントロールに対応

## ハードウェア要件

- **Raspberry Pi** (Model 4B)
- **PiCamera2**（OV5647 IR-CUT）
- **赤外線 LED 発光器**（OSI5FU5111C-40 940nm）x3
- **緑色 LED インジケータ**（OSG8HA3Z74A）
- **赤外線受信モジュール**（OSRB38C9AA）
- **N チャンネル MOSFET**（2SK2232）
- **スライドスイッチ**
- **ボタン**
- **抵抗器**：
  - 100Ω（±5%）x4
  - 10kΩ（±5%）x1

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="ブレッドボード配線図" width="48%" />
  <img src="image/circuit_diagram.png" alt="回路図" width="48%" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi 実装図" width="48%" />
  <img src="image/Tangent Diagram.jpg" alt="補助図" width="48%" />
</div>

## ソフトウェア要件

- Python 3.x
- 必要な Python パッケージ（pip でインストール可能）：
  - picamera2
  - opencv-python
  - pigpio
  - slack-sdk
  - numpy

## インストール

1. リポジトリをクローン：

   ```bash
   git clone https://github.com/CC5103/InfraCamControl.git
   cd InfraCamControl
   ```

2. 依存関係をインストール：

   ```bash
   pip install -r requirements.txt
   ```

3. Slack 統合を設定：  
   `config.json` ファイルを作成し、Slack 資格情報を追加：
   ```json
   {
     "BOT_TOKEN": "your-slack-bot-token",
     "ID": "your-channel-id"
   }
   ```

## 使用方法

1. pigpio デーモンを起動：

   ```bash
   sudo pigpiod
   ```

2. メインプログラムを実行：

   ```bash
   python main.py
   ```

3. **赤外線信号の作成**：  
   Slack コマンドを使用して信号を記録：

   ```bash
   crate <save_type> <save_key> <save_name>
   ```

   説明：

   - スイッチを赤外線受信モジュールに向け、ボタンを押して信号を記録します。
   - NEC または三菱プロトコルの 940nm 赤外線信号に対応。
   - システムは信号ファイルを自動生成し、`<save_key>` と `<save_name>` のマッピングを `signal_list.json` ファイルに更新します。

4. **赤外線信号の送信**：  
   Slack に保存済みの `<save_key>` を入力して信号送信をトリガーし、リモート操作を実現。

   **ヒント**：回路のボタンを押してハードウェアが正常に動作しているか確認できます。

## システムアーキテクチャ

システムは主に 2 つのスレッドで構成されています：

1. **Slack メッセージスレッド**：

   - Slack チャンネルでコマンドを監視
   - 赤外線信号の学習および送信タスクを処理

2. **カメラスレッド**：
   - 顔検出を実行
   - 環境光レベルを監視
   - 赤外線照明を自動調整

## 回路図

ハードウェアは次の主要な接続方式に従う必要があります：

- **GPIO25**：赤外線 LED 発光器に接続
- **GPIO23**：赤外線受信モジュールに接続
- **CSI インターフェース**：カメラモジュール用
- **ステータス LED インジケータ**：システムステータスを表示

## コントリビューション

1. リポジトリをフォーク
2. フィーチャーブランチを作成：
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. 変更をコミット：
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. ブランチをプッシュ：
   ```bash
   git push origin feature/AmazingFeature
   ```
5. プルリクエストを送信

## ライセンス

このプロジェクトは GNU 一般公衆利用許諾契約書（GPL）の下でライセンスされています。詳細については LICENSE ファイルを参照してください。

## トラブルシューティング

- プログラムを実行する前に pigpio デーモンを起動していることを確認してください。
- Slack ボットの権限とトークンが有効であることを確認してください。
- 赤外線 LED および受信モジュールの接続が正しいか確認してください。
- カメラモジュールが有効で、正しく接続されているか確認してください。

## 感謝

- pigpio 開発チームに感謝いたします。
- 強力な顔検出機能を提供する OpenCV に感謝します。
- Slack API 開発チームの Python SDK に感謝します。
- 特に Qiita ユーザー yhotta240 の赤外線リモコンチュートリアル [出典](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b) に感謝します。
- Casareal BS ブログのエアコンリモコンチュートリアル [出典](https://bsblog.casareal.co.jp/archives/5010) に感謝します。
