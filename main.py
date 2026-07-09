import time
from config import PACKAGES_FILE, CHANNEL_ID, PLACE_ID, PRIVATE_SERVER_CODE, DELAY, INTERVAL
from delta_control import full_process, get_username
from monitor import monitor, show_loading
from utils import get_ascii_art, Colors, bold, green, red, yellow, cyan

def main():
    print(get_ascii_art())
    print()
    
    # Baca token dari file atau input manual
    try:
        with open("token.txt", "r") as f:
            bot_token = f.read().strip()
            if not bot_token:
                raise Exception("Token kosong")
    except:
        bot_token = input(f"{bold('Bot Token')}: ").strip()
    
    if not bot_token:
        print(red("[!] Token tidak boleh kosong!"))
        return
    
    show_loading("Reading package list...", 1)
    with open(PACKAGES_FILE, "r") as f:
        packages = [line.strip() for line in f if line.strip()]
    if not packages:
        print(red("[!] packages.txt kosong!"))
        return
    
    print(f"\n{cyan('[*]')} Found {bold(str(len(packages)))} packages to process")
    print(f"{cyan('[*]')} Place ID: {bold(PLACE_ID)}")
    print()
    
    username_map = {}
    print(f"{bold('Starting up instances...')}\n")
    for i, pkg in enumerate(packages):
        print(f"[{i+1}/{len(packages)}] Processing {bold(pkg)}...")
        show_loading(f"Opening {pkg}...", 1.5)
        uname = full_process(pkg, PLACE_ID, bot_token, CHANNEL_ID)
        if uname and uname != "Unknown":
            username_map[pkg] = uname
            print(f"    {green('✓')} Username: {bold(uname)}")
        else:
            username_map[pkg] = f"Akun {i+1}"
            print(f"    {yellow('⚠')} Username: {yellow('Unknown')}")
        time.sleep(DELAY)
    
    print(f"\n{green(bold('✓ Startup completed!'))}")
    show_loading("Starting monitoring...", 1)
    monitor(packages, PLACE_ID, bot_token, CHANNEL_ID, INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{red(bold('[!] Interrupted by user'))}")
    except Exception as e:
        print(f"\n{red(bold('[!] Error:'))} {e}")