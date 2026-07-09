import time
import re
from config import PACKAGES_FILE, CHANNEL_ID, DELAY, INTERVAL
from delta_control import full_process, get_username
from monitor import monitor, show_loading
from utils import get_ascii_art, Colors, bold, green, red, yellow, cyan

def extract_private_code(link):
    """Ekstrak parameter 'code' dari link private server Roblox."""
    match = re.search(r'[?&]code=([^&]+)', link)
    if match:
        return match.group(1)
    return None

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
    
    # ===== Konfigurasi Join =====
    print(f"\n{cyan('[*]')} Join Configuration")
    use_private = input(f"{bold('Use Private Server? (y/n)')}: ").strip().lower()
    place_id = None
    private_code = None
    
    if use_private == 'y':
        link = input(f"{bold('Private Server Link')}: ").strip()
        private_code = extract_private_code(link)
        if not private_code:
            print(red("[!] Gagal mengekstrak kode dari link private server."))
            return
        print(f"{green('[✓]')} Private server code: {private_code}")
    else:
        place_id = input(f"{bold('Enter Place ID')}: ").strip()
        if not place_id.isdigit():
            print(red("[!] Place ID harus angka."))
            return
        print(f"{green('[✓]')} Place ID: {place_id}")
    
    # Baca daftar package
    show_loading("Reading package list...", 1)
    with open(PACKAGES_FILE, "r") as f:
        packages = [line.strip() for line in f if line.strip()]
    if not packages:
        print(red("[!] packages.txt kosong!"))
        return
    
    # Tampilkan informasi
    print(f"\n{cyan('[*]')} Found {bold(str(len(packages)))} packages to process")
    if private_code:
        print(f"{cyan('[*]')} Mode: Private Server (code: {private_code})")
    else:
        print(f"{cyan('[*]')} Mode: Public Game (Place ID: {place_id})")
    print()
    
    # Proses startup semua instance
    username_map = {}
    print(f"{bold('Starting up instances...')}\n")
    for i, pkg in enumerate(packages):
        print(f"[{i+1}/{len(packages)}] Processing {bold(pkg)}...")
        show_loading(f"Opening {pkg}...", 1.5)
        uname = full_process(pkg, place_id, bot_token, CHANNEL_ID, private_code)
        if uname and uname != "Unknown":
            username_map[pkg] = uname
            print(f"    {green('✓')} Username: {bold(uname)}")
        else:
            username_map[pkg] = f"Akun {i+1}"
            print(f"    {yellow('⚠')} Username: {yellow('Unknown')}")
        time.sleep(DELAY)
    
    print(f"\n{green(bold('✓ Startup completed!'))}")
    show_loading("Starting monitoring...", 1)
    # Jalankan monitor dengan parameter join yang sama
    monitor(packages, place_id, bot_token, CHANNEL_ID, private_code, INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{red(bold('[!] Interrupted by user'))}")
    except Exception as e:
        print(f"\n{red(bold('[!] Error:'))} {e}")