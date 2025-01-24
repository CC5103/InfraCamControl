import time
import pigpio
import json

def signal_read(sender, save_type):
    """Read signal from IR receiver and save to csv file.
    Args:
        sender (Sender_class): Sender class instance.
        save_type (str): Type of signal to save. "0" for NEC signal, "1" for Mitsubishi signal.
        
    Returns:
        callback_instance (pigpio.callback): Callback instance.
    """
    if save_type == "0":
        sender.LEADER_PULSE_MIN, sender.LEADER_PULSE_MAX = 8500, 9500
        sender.ZERO_PULSE_MIN, sender.ZERO_PULSE_MAX = 500, 700
        sender.ONE_PULSE_MIN, sender.ONE_PULSE_MAX = 1500, 1800
    elif save_type == "1":
        sender.LEADER_PULSE_MIN, sender.LEADER_PULSE_MAX = 3000, 3500
        sender.ZERO_PULSE_MIN, sender.ZERO_PULSE_MAX = 300, 700
        sender.ONE_PULSE_MIN, sender.ONE_PULSE_MAX = 1000, 1500
    return sender.pi.callback(sender.pin_save, pigpio.EITHER_EDGE, (sender.pulse_callback))

def save_thread(sender, signal_map, save_type, save_key, save_name):
    """Save signal to csv file.
    Args:
        sender (Sender_class): Sender class instance.
        signal_map (dict): Signal map.
        save_type (str): Type of signal to save.
        save_key (str): Key to save signal.
        save_name (str): Name of signal to save.
    """
    callback_instance = signal_read(sender, save_type)
    while True:
        time.sleep(1)
        print("Waiting for signal")
        if not sender.save_bool:
            with open(f"../IR_signal/{save_name}.csv", "w") as f:
                f.write(" ".join(map(str, sender.pulse_list)))
            with open("../IR_signal/signal_list.json", "w") as f:
                signal_map[save_key] = f"{save_name}.csv"
                json.dump(signal_map, f)
            print("Signal saved")
            sender.leader_num = 0
            sender.pulse_list = []
            sender.save_bool = True
            callback_instance.cancel()
            break
