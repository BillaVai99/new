#!/usr/bin/env python3
"""
Professional User Tool with colors and focused display
- Shows only SSH/V2RAY servers
- Selected server info focused
- Name & Country highlighted separately
- Other servers shown as a small reference line
- Config / Payload displayed line by line in a readable format
"""

import json, os, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent
DB_FILE = str(ROOT.joinpath("servers.json"))

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
WHITE = "\033[37m"

os.system('clear')
LOGO = f"""
{CYAN}{BOLD}=============================={RESET}
{GREEN}{BOLD}   ⚡ FREE SSH/V2RAY SERVER ⚡{RESET}
{YELLOW}           (HASIB HOSSEN){RESET}
{CYAN}{BOLD}=============================={RESET}
"""

def load_servers():
    if not os.path.exists(DB_FILE):
        print(f"{RED}servers.json not found. Ask admin to provide it.{RESET}")
        return []
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        print(f"{RED}Failed to parse servers.json{RESET}")
        return []

def save_servers(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def copy_to_clipboard(text):
    try:
        subprocess.run(["termux-clipboard-set"], input=text.encode("utf-8"), check=True)
        print(f"\n{GREEN}✅ Config copied to clipboard.{RESET}")
    except:
        print(f"\n{RED}⚠️ Could not copy automatically. Copy manually from screen.{RESET}")

def display_config_payload(config_text):
    if not config_text or config_text.strip() == "":
        print(f"{RED}(No Config / Payload found){RESET}")
        return
    lines = config_text.strip().splitlines()
    print(f"{MAGENTA}{BOLD}--- Config / Payload ---{RESET}\n")
    for idx, line in enumerate(lines, 1):
        if not line.strip():
            continue
        if "=" in line:
            key, value = map(str.strip, line.split("=", 1))
        else:
            parts = line.strip().split()
            if len(parts) >= 2:
                key, value = parts[0], " ".join(parts[1:])
            else:
                key, value = parts[0], ""
        print(f"{BOLD}{idx:02d}. {CYAN}{key:<12}{RESET}: {GREEN}{value}{RESET}")

def display_ssh_info(server):
    info_order = ["host", "port", "username", "password", "payload", "other"]
    print(f"{MAGENTA}{BOLD}--- SSH Server Info ---{RESET}\n")
    for key in info_order:
        value = server.get(key, "")
        if not value:
            continue
        color = CYAN if key in ["host", "port"] else GREEN if key=="username" else YELLOW if key=="password" else WHITE
        label = key.capitalize().replace("_"," ")
        print(f"{BOLD}{label:10}:{RESET} {color}{value}{RESET}")

def select_server(servers, stype):
    filtered = [s for s in servers if s.get("type","").upper()==stype.upper()]
    if not filtered:
        print(f"{RED}No {stype} servers available.{RESET}")
        return
    print(f"\n{BOLD}{MAGENTA}Available {stype} Servers:{RESET}")
    for s in filtered:
        print(f"{WHITE}- {s.get('name','-')} | {CYAN}{s.get('country','-')}{RESET}")
    country = input(f"\n{BOLD}Enter Country name to view server details: {RESET}").strip()
    if not country:
        return
    server = next((x for x in filtered if x.get('country','').lower() == country.lower()), None)
    if not server:
        print(f"{RED}No server found for country '{country}'.{RESET}")
        return
    os.system('clear')
    print(LOGO)
    print(f"{BOLD}{MAGENTA}=== Selected Server ==={RESET}\n")
    print(f"{BOLD}Server Name :{RESET} {GREEN}{server.get('name')}{RESET}")
    print(f"{BOLD}Country     :{RESET} {CYAN}{server.get('country')}{RESET}")
    print(f"{BOLD}Type        :{RESET} {YELLOW}{server.get('type')}{RESET}\n")
    if server.get("type","").upper() == "SSH":
        display_ssh_info(server)
        print()
        display_config_payload(server.get("config",""))
    else:
        print(f"{WHITE}{server.get('config') or '(no config)'}{RESET}")
    if input(f"\n{BOLD}Copy config to clipboard? (y/N): {RESET}").strip().lower() == "y":
        copy_to_clipboard(server.get("config") or "")
    for s in servers:
        if s.get("id") == server.get("id"):
            s["usage"] = s.get("usage",0) + 1
            s["last_used"] = datetime.utcnow().isoformat()
            break
    save_servers(servers)

def main():
    print(LOGO)
    servers = load_servers()
    if not servers:
        return
    print(f"{BOLD}Select server :{RESET}")
    print(f"{BLUE}1) SSH servers{RESET}")
    print(f"{BLUE}2) V2RAY servers{RESET}")
    choice = input(f"{BOLD}Choice: {RESET}").strip()
    if choice == "1":
        select_server(servers, "SSH")
    elif choice == "2":
        select_server(servers, "V2RAY")
    else:
        print(f"{RED}Invalid choice.{RESET}")

if __name__ == "__main__":
    main()