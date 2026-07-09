import time
from adb_utils import start_app, tap, input_text, press_keycode, get_clipboard, set_clipboard, run, run_root, wait_app, is_running, is_foreground, get_foreground_app, dump_ui, get_username_from_prefs
from ui_automator import find, find_edit, find_btn, get_username_from_ui, is_in_game, is_in_lobby, is_delta_visible
from key_fetcher import get_key

def wait_delta(pkg, timeout=30):
    for _ in range(timeout // 2):
        if is_delta_visible():
            return True
        time.sleep(2)
    return False

def get_shortlink(pkg):
    btn = find("Receive Key") or find("Get Key")
    if not btn:
        return None
    tap(btn[0], btn[1])
    time.sleep(2)
    s = get_clipboard()
    if s and s.startswith("http"):
        return s
    return None

def input_key(pkg, key):
    e = find_edit()
    if not e:
        return False
    tap(e[0], e[1])
    time.sleep(0.5)
    input_text(key)
    time.sleep(0.5)
    c = find_btn("Continue")
    if c:
        tap(c[0], c[1])
        return True
    return False

def get_status(pkg):
    if not is_running(pkg):
        return "Offline"
    if is_foreground(pkg):
        if is_in_game():
            return "In-Game"
        if is_in_lobby():
            return "Lobby"
        return "Online"
    return "Background"

def get_username(pkg):
    uname = get_username_from_prefs(pkg)
    if uname:
        return uname
    uname2 = get_username_from_ui()
    if uname2:
        return uname2
    return "Unknown"

def full_process(pkg, place_id, bot_token, channel_id):
    print(f"\n[Delta] === {pkg} ===")
    start_app(pkg)
    time.sleep(3)
    wait_app(pkg, 10)
    username = get_username(pkg)
    print(f"[Delta] Username: {username}")
    run(f"am start -a android.intent.action.VIEW -d 'roblox://placeId={place_id}' {pkg}")
    time.sleep(5)
    if not wait_delta(pkg, 30):
        print(f"[Delta] Delta tidak muncul untuk {pkg}")
        return username
    short = get_shortlink(pkg)
    if not short:
        return username
    key = get_key(bot_token, channel_id, short)
    if not key:
        return username
    if not input_key(pkg, key):
        return username
    time.sleep(2)
    return username