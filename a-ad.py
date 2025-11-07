#!/usr/bin/env python3
"""
Admin Panel (admin_panel.py)
• Password protected
• Add / List / Delete SSH & V2RAY servers separately
• Saves everything into servers.json
"""

import json, os, getpass
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
DB_FILE = str(ROOT.joinpath("servers.json"))
ADMIN_PASS = "admin123"  # <-- change this to a strong password

def load_servers():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []

def save_servers(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def next_id(servers):
    if not servers:
        return 1
    return max(s.get("id", 0) for s in servers) + 1

def add_server():
    servers = load_servers()
    stype = input("Type (SSH / V2RAY): ").strip().upper()
    if stype not in ("SSH", "V2RAY"):
        print("Invalid type, defaulting to SSH")
        stype = "SSH"

    country = input("Country (e.g. Singapore, India) [optional]: ").strip()
    name = input("Server Name/Label [optional]: ").strip() or f"{stype.lower()}-server"

    print("\nPaste full server config/payload. Type 'END' on a new line when done.\n")
    lines = []
    while True:
        try:
            l = input()
        except EOFError:
            break
        if l.strip().upper() == "END":
            break
        lines.append(l)
    config_text = "\n".join(lines).strip()

    entry = {
        "id": next_id(servers),
        "type": stype,
        "country": country,
        "name": name,
        "config": config_text,
        "created_at": datetime.utcnow().isoformat(),
        "usage": 0,
        "last_used": None,
    }

    servers.append(entry)
    save_servers(servers)
    print(f"\n✅ Added {stype} server id={entry['id']}")

def list_servers(filter_type=None):
    servers = load_servers()
    if not servers:
        print("No servers found.")
        return []

    filtered = [s for s in servers if not filter_type or s["type"] == filter_type]
    if not filtered:
        print(f"No {filter_type or 'any'} servers found.")
        return []

    print("\n=== SERVER LIST ===")
    for s in filtered:
        print(f"[{s['id']}] {s['type']} | {s.get('country','-')} | {s.get('name','-')} | used:{s.get('usage',0)}")

    return filtered

def delete_server():
    stype = input("Delete which type? (SSH / V2RAY): ").strip().upper()
    if stype not in ("SSH", "V2RAY"):
        print("Invalid type.")
        return

    servers = load_servers()
    filtered = [s for s in servers if s["type"] == stype]
    if not filtered:
        print(f"No {stype} servers to delete.")
        return

    print(f"\n=== {stype} SERVERS ===")
    for s in filtered:
        print(f"[{s['id']}] {s['name']} | {s.get('country','-')}")

    sid = input(f"Enter {stype} server ID to delete: ").strip()
    if not sid:
        print("Cancelled.")
        return

    new = [s for s in servers if not (str(s.get("id")) == sid and s["type"] == stype)]
    save_servers(new)
    print(f"✅ Deleted {stype} server ID {sid} (if existed).")

def admin_menu():
    while True:
        print("\n=== ADMIN PANEL ===")
        print("1) Add server")
        print("2) List all servers")
        print("3) Delete server (choose type)")
        print("0) Exit")
        c = input("Choice: ").strip()
        if c == "1":
            add_server()
        elif c == "2":
            list_servers()
        elif c == "3":
            delete_server()
        elif c == "0":
            break
        else:
            print("Invalid choice.")

def main():
    pw = getpass.getpass("Admin password: ")
    if pw != ADMIN_PASS:
        print("Wrong password.")
        return
    admin_menu()

if __name__ == "__main__":
    main()