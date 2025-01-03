import pigpio
import time
import sys
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class NECSender:
    def __init__(self, pin=12, slack_token=None, channel_id=None):
        """
        初期化 NEC 赤外線信号送信機
        
        param pin: GPIO ピン番号 (デフォルトは12)
        param slack_token: Slack Bot Token
        param channel_id: Slack チャンネルID
        """
        # Slackの設定
        if not slack_token or not channel_id:
            raise ValueError("Slack token and channel ID must be provided.")
        
        self.SLACK_BOT_TOKEN = slack_token
        self.CHANNEL_ID = channel_id
        self.client = WebClient(token=self.SLACK_BOT_TOKEN, timeout=30)
        self.first = True

        # pigpioの初期化
        try:
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise RuntimeError("Cannot connect to pigpio.")
            
            self.pin = pin
            self.pi.set_mode(self.pin, pigpio.OUTPUT)
        except Exception as e:
            print(f"Error initializing NECSender: {e}")
            sys.exit(1)
    
    def fetch_slack_messages(self, last_timestamp):
        """
        Slackメッセージを取得
        
        param last_timestamp: 最後に取得したメッセージのタイムスタンプ
        return: メッセージ内容と新しいタイムスタンプ
        """
        try:
            response = self.client.conversations_history(channel=self.CHANNEL_ID, limit=1)
            if response["messages"]:
                last_message = response["messages"][0]
                timestamp = last_message["ts"]
                if timestamp == last_timestamp:
                    return None, last_timestamp
                else:
                    last_timestamp = timestamp
                    if self.first:
                        self.first = False
                        return None, last_timestamp
                    return last_message["text"], last_timestamp
        except SlackApiError as e:
            print(f"Slack API error: {e.response['error']}")
        return None, last_timestamp
    
    def send_nec_signal_wave(self, message):
        """
        NEC信号を送信
        
        param message: Slackから受け取ったメッセージ
        """
        try:
            data_bits = self.read_csv_data(f"data_{message}.csv")
            pulses = self.generate_pulses(data_bits)
            self.pi.wave_add_generic(pulses)
            wave_id = self.pi.wave_create()

            if wave_id >= 0:
                self.pi.wave_send_once(wave_id)
                while self.pi.wave_tx_busy():
                    time.sleep(0.1)
                self.pi.wave_delete(wave_id)
        except Exception as e:
            print(f"Error sending NEC signal: {e}")
    
    def read_csv_data(self, filename):
        """
        CSVファイルからデータを読み込む
        
        param filename: ファイル名
        return: データのリスト
        """
        try:
            with open(filename, 'r') as f:
                data = list(map(int, f.read().split()))
                return data
        except FileNotFoundError:
            print(f"File not found: {filename}")
            sys.exit(1)
    
    def generate_pulses(self, data_bits):
        """
        信号のパルスを生成
        
        param data_bits: データのビット列
        return: パルスのリスト
        """
        base_pulse = [pigpio.pulse(1 << self.pin, 0, 560), pigpio.pulse(0, 1 << self.pin, 560)]
        pulses = [pigpio.pulse(1 << self.pin, 0, 9000), pigpio.pulse(0, 1 << self.pin, 4500)]
        
        for bit in data_bits:
            pulses.extend(base_pulse)
            if bit == 1:
                pulses.append(pigpio.pulse(0, 1 << self.pin, 1690))
            else:
                pulses.append(pigpio.pulse(0, 1 << self.pin, 560))
        
        pulses.extend(base_pulse)
        return pulses

if __name__ == '__main__':
    # セキュリティのため、環境変数からSlackのトークンを取得する
    import os
    SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

    sender = NECSender(pin=12, slack_token=SLACK_TOKEN, channel_id=CHANNEL_ID)
    try:
        last_timestamp = None
        while True:
            message, last_timestamp = sender.fetch_slack_messages(last_timestamp)
            if message in ["0", "on", "off"]:
                print(f"Received valid message: {message}")
                sender.send_nec_signal_wave(message)
            elif message:
                print(f"Invalid message received: {message}")
                sender.client.chat_postMessage(channel=sender.CHANNEL_ID, text=f"Invalid message: {message}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        sender.pi.write(sender.pin, 0)
        sender.pi.stop()
        print("Program terminated.")