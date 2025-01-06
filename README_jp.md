# InfraCamControl

**他の言語バージョン：[英語](README.md)、[中文](README_zh.md)、[日本語](README_jp.md)。**

## 概要

InfraCamControl は Raspberry Pi をベースにしたシステムで、赤外線リモコン機能とコンピュータビジョンを組み合わせ、自動化されたカメラ制御を実現します。このシステムは Slack を通じてコマンドを受信し、赤外線デバイスを制御するとともに、周囲の光条件に応じて赤外線照明を自動的に管理します。また、Apple デバイスとの連携を可能とし、音声認識やその他の情報を通じて自動化プロセスを実行し、よりスマートで便利な操作を提供します。

## 特徴

- Slack 連携によるリモート制御のサポート
- 赤外線信号の学習と送信をサポート
- コンピュータビジョンを使用した顔検出
- 周囲光に基づいた赤外線照明の自動制御
- マルチスレッド操作により並列タスクを実現
- NEC および三菱の赤外線プロトコルをサポート
- Apple デバイスとの連携をサポートし、音声認識とスマート制御を統合

## ハードウェア要件

- Raspberry Pi (Model 4B)
- PiCamera2
- 赤外線 LED 発射機 (OSI5FU5111C-40 940nm) x3
- 緑色 LED インジケーター (OSG8HA3Z74A)
- 赤外線受信モジュール (OSRB38C9AA)
- Nチャンネル MOSFET (2SK2232)
- ボタン
- 抵抗：
  - 100Ω（±5%）x4
  - 10kΩ（±5%）x1

<div style="display: flex; justify-content: space-between;">
  <img src="image/breadboard.png" alt="breadboard" width="48%" />
  <img src="image/circuit_diagram.png" alt="circuit_diagram" width="48%" />
</div>
<br>
<div style="display: flex; justify-content: space-between;">
  <img src="image/Raspberry Pi Implementation Diagram.jpg" alt="Raspberry Pi Implementation Diagram" width="48%" />
  <img src="image/Tangent Diagram.jpg" alt="Tangent Diagram" width="48%" />
</div>

## ソフトウェア要件

- Python 3.x
- 必須 Python パッケージ（pip を使用してインストール）：
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

3. Slack 連携を設定：
`config.json` ファイルを作成し、Slack の認証情報を追加：
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

3. Slack コマンドを使用して信号を登録：
   `crate <save_type> <save_key> <save_name>` コマンドを使用して赤外線信号を収録。  
   赤外線受信器に向けて送信機をセットし、ボタンを押して信号をキャプチャ。  
   NEC または三菱の赤外線信号プロトコル（940nm）に対応しています。
   自動的に信号ファイルを生成し、`<save_key>` と `<save_name>` の対応関係を記録した `singnal_list.json` ファイルが作成されます。

    ### Slack コマンド

    - 新しい赤外線信号マッピングを作成：
      ```
      crate <save_type> <save_key> <save_name>
      ```
      それぞれの項目：
      - `save_type`： "0" は NEC プロトコル、"1" は三菱プロトコルを示します。
      - `save_key`：コマンドキーワード。
      - `save_name`：信号データを保存するファイル名。

4. 特定の赤外線信号を送信：
   `singnal_list.json` に基づき、Slack 経由で該当する `<save_key>` を送信することでリモート制御を実現。  
   ボタンを押して回路が正しく動作しているか確認できます。

## システムアーキテクチャ

システムは以下の2つの主要スレッドを使用します：

1. Slack メッセージスレッド：
   - Slack チャンネルのコマンドを監視
   - 赤外線信号の学習リクエストを処理
   - コマンドに基づき赤外線信号を送信

2. カメラスレッド：
   - 顔検出を実行
   - 環境光レベルを監視
   - 赤外線照明を自動制御

## 回路図

ハードウェア部品は提供された回路図に基づいて接続してください。主な接続：
- GPIO25 に赤外線 LED（送信端）
- GPIO23 に赤外線受信器（受信端）
- CSI インターフェース経由で接続するカメラモジュール
- 状態 LED インジケーター

## コントリビューション

1. リポジトリを Fork
2. フィーチャーブランチを作成 (`git checkout -b feature/AmazingFeature`)
3. 変更をコミット (`git commit -m 'Add some AmazingFeature'`)
4. ブランチをプッシュ (`git push origin feature/AmazingFeature`)
5. Pull Request を作成

## ライセンス

このプロジェクトは GNU General Public License の下でライセンスされています - 詳細は LICENSE ファイルを参照してください。

## トラブルシューティング

- プログラムを開始する前に pigpio デーモンが実行されていることを確認
- Slack ボットの権限とトークンの有効性を確認
- 赤外線 LED と受信器の接続を検証
- カメラモジュールが正しく接続され、有効化されていることを確認

## 謝辞

- pigpio ライブラリの開発者に感謝
- OpenCV コミュニティによる顔検出機能に感謝
- Slack API チームによる Python SDK に感謝
- Qiita ユーザー yhotta240 による ESP32 赤外線リモコンチュートリアル [出典](https://qiita.com/yhotta240/items/df0f2f92b5dff1d9410b)
- Casareal の BS ブログによる Raspberry Pi でのエアコン電源制御チュートリアル [出典](https://bsblog.casareal.co.jp/archives/5010)