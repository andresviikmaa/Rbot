import subprocess
import time

  
def set_cam_settings_from_cli():
    # esmalt auto settingud
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'contrast=128'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'white_balance_temperature_auto=1'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'exposure_auto=3'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'focus_auto=1'])

    #time.sleep(2)  # ootame 2 sekki, et kaamera kohaneks valgusega, siis keerame auto seaded maha
def set_cam_settings_from_cli2():
    # auto whitebalance maha
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'white_balance_temperature_auto=0'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'gain=20'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'power_line_frequency=0'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'white_balance_temperature=3500'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'exposure_auto=1'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'exposure_absolute=250'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'focus_auto=0'])
    subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'focus_absolute=0'])
    #subprocess.check_call(['v4l2-ctl', '--set-ctrl', 'led1_mode=0'])
