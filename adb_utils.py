import subprocess
import time
import re

def run(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            return result.stdout.strip()
        result2 = subprocess.run(f"su -c '{cmd}'", shell=True, capture_output=True, text=True)
        return result2.stdout.strip()
    except:
        return ""

def run_root(cmd):
    try:
        result = subprocess.run(f"su -c '{cmd}'", shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except:
        return ""

def tap(x, y):
    run(f"input tap {x} {y}")

def input_text(text):
    text = text.replace(" ", "%s")
    run(f"input text '{text}'")

def press_keycode(keycode):
    run(f"input keyevent {keycode}")

def get_clipboard():
    out = run("service call clipboard 1")
    match = re.search(r"'(.*?)'", out)
    if match:
        return match.group(1)
    return ""

def set_clipboard(text):
    text_escaped = text.replace("'", "\\'")
    run(f"service call clipboard 2 i32 0 s16 '{text_escaped}'")

def dump_ui():
    run("uiautomator dump /data/local/tmp/ui.xml")
    return run("cat /data/local/tmp/ui.xml")

def is_running(pkg):
    out = run_root(f"ps -A | grep {pkg}")
    if pkg in out:
        return True
    out2 = run_root(f"pidof {pkg}")
    if out2:
        return True
    ui = dump_ui()
    if "ZETSU DELTA" in ui or "LITE" in ui:
        return True
    return False

def is_foreground(pkg):
    out = run_root("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'")
    if pkg in out:
        return True
    out2 = run_root("dumpsys activity activities | grep -E 'mFocusedApp|mResumedActivity'")
    if pkg in out2:
        return True
    return False

def get_foreground_app():
    out = run_root("dumpsys window windows | grep -E 'mCurrentFocus|mFocusedApp'")
    match = re.search(r'([a-zA-Z0-9._]+)/(?:[a-zA-Z0-9._]+)', out)
    if match:
        return match.group(1)
    return None

def start_app(pkg):
    run(f"am start -p {pkg}")

def wait_app(pkg, timeout=10):
    for i in range(timeout):
        if is_running(pkg):
            return True
        time.sleep(1)
    return False

def get_username_from_prefs(pkg):
    pref_file = f"/data/data/{pkg}/shared_prefs/com.roblox.client.preferences.xml"
    out = run_root(f"cat {pref_file} 2>/dev/null | grep -E 'username|UserName'")
    match = re.search(r'<string name="(?:username|UserName)">([^<]+)</string>', out)
    if match:
        return match.group(1)
    return None