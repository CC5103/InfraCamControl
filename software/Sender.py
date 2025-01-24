import pigpio
import time
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class Sender_class:
    def __init__(self, pin_sender=25, pin_save=23, pin_hand=15):
        """Initialize the Sender class.
        
        Args:
            pin_sender (int): GPIO pin number for sending IR signal.
            pin_save (int): GPIO pin number for saving signal.
            
        Attributes:
            first (bool): True if the first message is received.
            save_bool (bool): True if the signal is saved.
            pulse_list (list): List of received pulses.
            leader_num (int): Number of leader pulses.
            SLACK_BOT_TOKEN (str): Slack bot token.
            CHANNEL_ID (str): Slack channel ID.
            client (WebClient): Slack client.
            pi (pigpio.pi): pigpio instance.
            pin_sender (int): GPIO pin number for sending IR signal.
            pin_save (int): GPIO pin number for saving signal.
            last_tick (int): Last tick time.
            LEADER_PULSE_MIN (int): Minimum leader pulse time.
            LEADER_PULSE_MAX (int): Maximum leader pulse time.
            ZERO_PULSE_MIN (int): Minimum zero pulse time.
            ZERO_PULSE_MAX (int): Maximum zero pulse time.
            ONE_PULSE_MIN (int): Minimum one pulse time.
            ONE_PULSE_MAX (int): Maximum one pulse time.
        """
        self.first = True
        self.save_bool = True
        self.pulse_list = []
        self.leader_num = 0

        # Slack API settings
        try:
            with open("../config.json") as f:
                config = json.load(f)
                self.SLACK_BOT_TOKEN = config["BOT_TOKEN"]
                self.CHANNEL_ID = config["ID"]
        except FileNotFoundError:
            print("Error: config.json not found")
            exit(1)

        self.client = WebClient(token=self.SLACK_BOT_TOKEN, timeout=30)

        # pigpio settings
        try:
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise RuntimeError("Cannot connect to pigpio")
            
            self.pin_sender = pin_sender
            self.pi.set_mode(self.pin_sender, pigpio.OUTPUT)
            self.pi.write(self.pin_sender, 0)
            
            self.pin_save = pin_save
            self.pi.set_mode(self.pin_save, pigpio.INPUT)
            
            self.pin_hand = pin_hand
            self.pi.set_mode(self.pin_hand, pigpio.OUTPUT)
            self.pi.write(self.pin_hand, 0)
            
            self.last_tick = self.pi.get_current_tick()
        except Exception as e:
            print(f"Error: {e}")
            exit(1)
            
    def fetch_slack_messages(self, last_timestamp):
        """Fetch slack messages.
        
        Args:
            last_timestamp (str): Last timestamp of fetched message.
            
        Returns:
            str: Received message.
            str: Last timestamp of fetched message.
            
        Raises:
            SlackApiError: If an error occurs while fetching messages.
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
            print(f"Error fetching messages: {e.response['error']}")
        return None
    
    def fetch_slack_messages_with_retry(self, last_timestamp, retries=10, delay=5):
        """Fetch slack messages with retry.
        
        Args:
            last_timestamp (str): Last timestamp of fetched message.
            retries (int): Number of retries.
            delay (int): Delay time between retries.
            
        Returns:
            str: Received message.
            str: Last timestamp of fetched message.
            
        Raises:
            SlackApiError: If an error occurs while fetching messages.
        """
        for attempt in range(retries):
            try:
                return self.fetch_slack_messages(last_timestamp)
            except SlackApiError as e:
                print(f"Slack API error on attempt {attempt + 1}: {e.response['error']}")
            except Exception as e:
                print(f"Unexpected error on attempt {attempt + 1}: {e}")
            time.sleep(delay)
        print("All attempts to fetch Slack messages failed.")
        return None, last_timestamp

    def send_signal_wave(self, singal_file):
        """Send signal wave.
        
        Args:
            singal_file (str): Signal file name.
            
        Raises:
            FileNotFoundError: If the signal file is not found.
        """
        pulses_base = [
            pigpio.pulse(1 << self.pin_sender, 0, 8),
            pigpio.pulse(0, 1 << self.pin_sender, 18),
        ]
        
        pulses = [pigpio.pulse(0, 1 << self.pin_sender, 4500)]
        
        data_bits = self.read_csv_data(singal_file)
        if len(data_bits) < 50:
            pulses.extend(pulses_base * int(9000 // 26))
            pulses.append(pigpio.pulse(0, 1 << self.pin_sender, 4500))
            for bit in data_bits:
                pulses.extend(pulses_base * int(560 // 26))
                pulses.append(pigpio.pulse(0, 1 << self.pin_sender, 1690) if bit == 1 else pigpio.pulse(0, 1 << self.pin_sender, 560))
            pulses.extend(pulses_base * int(560 // 26))
            pulses.append(pigpio.pulse(0, 1 << self.pin_sender, 0))
        else:
            pulses.extend(pulses_base * int(3190 // 26))
            pulses.append(pigpio.pulse(0, 1 << self.pin_sender, 1600))
            for bit in data_bits:
                pulses.extend(pulses_base * int(400 // 26))
                pulses.append(pigpio.pulse(0, 1 << self.pin_sender, 1200) if bit == 1 else pigpio.pulse(0, 1 << self.pin_sender, 450))
            pulses.extend(pulses_base * int(400 // 26))
            pulses.append(pigpio.pulse(0, 1 << self.pin_sender, 0))

        self.pi.wave_add_generic(pulses)
        wave_id = self.pi.wave_create()
        
        if wave_id >= 0:
            self.pi.wave_send_once(wave_id)
            while self.pi.wave_tx_busy():
                time.sleep(1)
            self.pi.wave_delete(wave_id)

    def read_csv_data(self, filename):
        """Read data from csv file.
        
        Args:
            filename (str): File name.
            
        Returns:
            list: List of data.
            
        Raises:
            FileNotFoundError: If the file is not found.
        """
        try:
            with open(f'../IR_signal/{filename}', 'r') as f:
                data = f.read().split()
                return list(map(int, data))
        except FileNotFoundError:
            print(f"Error {filename}")
            exit(1)
            
    def pulse_callback(self, gpio, level, tick):
        """Callback function for pulse.
        
        Args:
            gpio (int): GPIO pin number.
            level (int): GPIO level.
            tick (int): Tick time.
            
        Attributes:
            LEADER_PULSE_MIN (int): Minimum leader pulse time.
            LEADER_PULSE_MAX (int): Maximum leader pulse time.
            ZERO_PULSE_MIN (int): Minimum zero pulse time.
            ZERO_PULSE_MAX (int): Maximum zero pulse time.
            ONE_PULSE_MIN (int): Minimum one pulse time.
            ONE_PULSE_MAX (int): Maximum one pulse time
            
        Raises:
            ValueError: If the pulse is invalid.
        """
        if self.leader_num <= 1:
            print(f"GPIO{gpio}, level: {level}, time: {tick-self.last_tick}")
            if tick - self.last_tick > self.LEADER_PULSE_MIN and tick - self.last_tick < self.LEADER_PULSE_MAX:
                self.leader_num += 1
                print("Leader pulse")
            elif level == 0:
                if tick - self.last_tick > self.ZERO_PULSE_MIN and tick - self.last_tick < self.ZERO_PULSE_MAX:
                    self.pulse_list.append(0)
                    self.save_bool = False
                    print("Zero pulse")
                elif tick - self.last_tick > self.ONE_PULSE_MIN and tick - self.last_tick < self.ONE_PULSE_MAX:
                    self.pulse_list.append(1)
                    self.save_bool = False
                    print("One pulse")
                else:
                    self.leader_num = 0
                    self.pulse_list = []
                    self.save_bool = True
                    print("Invalid pulse")
            self.last_tick = tick
