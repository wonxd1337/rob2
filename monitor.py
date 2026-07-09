import time
import os
import sys
from config import PRIVATE_SERVER_CODE
from adb_utils import is_running, dump_ui
from delta_control import full_process, get_status, get_username
from utils import Colors, bold, green, red, yellow, blue, cyan, magenta, get_status_color, get_ascii_art

last_status = {}
last_username = {}
table_dirty = True

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_loading(message, duration=1.5):
    chars = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{Colors.CYAN}{chars[i % len(chars)]}{Colors.END} {message}')
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 60 + '\r')
    sys.stdout.flush()

def print_table(packages, status, username_map, start_time, force=False):
    global table_dirty
    if not force and not table_dirty:
        return
    clear_screen()
    print(get_ascii_art())
    print()
    print(f"{bold('USERNAME')}  {bold('PACKAGE')}  {bold('TIME')}  {bold('STATUS')}")
    print("=" * 75)
    for i, pkg in enumerate(packages, 1):
        elapsed = int(time.time() - start_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        time_str = f"{h}h{m:02d}m{s:02d}s"
        username = username_map.get(pkg, f"Akun {i}")
        stat = status.get(pkg, "Unknown")
        colored_status = get_status_color(stat)
        print(f"{bold(username):<15} {pkg:<20} {bold(time_str):<12} {colored_status}")
    print("=" * 75)
    print(f"{Colors.WHITE}⏱ Last Update: {time.strftime('%H:%M:%S')}{Colors.END}")
    print(f"{Colors.CYAN}📡 Monitoring {len(packages)} instances...{Colors.END}")
    table_dirty = False

def monitor(packages, place_id, bot_token, channel_id, interval=10):
    global last_status, last_username, table_dirty
    start_time = time.time()
    status = {}
    username_map = {}
    show_loading("Initializing monitoring system...", 1.5)
    for i, pkg in enumerate(packages):
        show_loading(f"Checking {pkg}...", 0.8)
        status[pkg] = get_status(pkg)
        uname = get_username(pkg)
        if uname and uname != "Unknown":
            username_map[pkg] = uname
        else:
            username_map[pkg] = f"Akun {i+1}"
    last_status = status.copy()
    last_username = username_map.copy()
    table_dirty = True
    print_table(packages, status, username_map, start_time, force=True)
    while True:
        changed = False
        for pkg in packages:
            new_status = get_status(pkg)
            if new_status != status.get(pkg):
                status[pkg] = new_status
                changed = True
                if new_status == "Offline":
                    print(f"\n{red(bold('[!]'))} {bold(pkg)} {red('offline, restarting...')}")
                    show_loading(f"Restarting {pkg}...", 1.5)
                    uname = full_process(pkg, place_id, bot_token, channel_id, PRIVATE_SERVER_CODE)
                    if uname and uname != "Unknown":
                        username_map[pkg] = uname
                    status[pkg] = get_status(pkg)
                    changed = True
            new_uname = get_username(pkg)
            if new_uname and new_uname != "Unknown" and new_uname != username_map.get(pkg):
                username_map[pkg] = new_uname
                changed = True
        if changed:
            table_dirty = True
            print_table(packages, status, username_map, start_time, force=True)
        time.sleep(interval)