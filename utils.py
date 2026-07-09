class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    WHITE = '\033[97m'
    MAGENTA = '\033[95m'

def bold(text):
    return f"{Colors.BOLD}{text}{Colors.END}"

def green(text):
    return f"{Colors.GREEN}{text}{Colors.END}"

def red(text):
    return f"{Colors.RED}{text}{Colors.END}"

def yellow(text):
    return f"{Colors.YELLOW}{text}{Colors.END}"

def blue(text):
    return f"{Colors.BLUE}{text}{Colors.END}"

def cyan(text):
    return f"{Colors.CYAN}{text}{Colors.END}"

def magenta(text):
    return f"{Colors.MAGENTA}{text}{Colors.END}"

def get_status_color(status):
    if status == "Online":
        return green(status)
    elif status == "Offline":
        return red(status)
    elif status == "In-Game":
        return blue(status)
    elif status == "Lobby":
        return cyan(status)
    elif status == "Background":
        return yellow(status)
    else:
        return status

def get_ascii_art():
    return f"""
{Colors.CYAN}{Colors.BOLD}
   ██╗    ██╗ ██████╗ ███╗   ██╗██╗  ██╗██████╗ 
   ██║    ██║██╔═══██╗████╗  ██║╚██╗██╔╝██╔══██╗
   ██║ █╗ ██║██║   ██║██╔██╗ ██║ ╚███╔╝ ██║  ██║
   ██║███╗██║██║   ██║██║╚██╗██║ ██╔██╗ ██║  ██║
   ╚███╔███╔╝╚██████╔╝██║ ╚████║██╔╝ ██╗██████╔╝
    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═════╝ 
{Colors.END}                                                 
{Colors.MAGENTA}⚡ DELTA EXECUTOR AUTO TOOLS v2.0 ⚡{Colors.END}
{Colors.CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}
"""