# 🐍 Telegram Controlled Cross-Platform Agent

A cross-platform remote agent built in Python that enables authorized users to control a system via a Telegram bot. It supports file operations, command execution, screenshots, uploads, and more.

> ⚠️ **This project is for educational and authorized use only. Do not use this software on any system without explicit permission.**

---

## 🚀 Features

- ✅ Windows & Linux support
- 🔐 Telegram bot controlled (send commands, receive output)
- 📁 Grab files, read text, list directories
- 📤 Upload files via bot and execute remotely
- 🗑️ Delete files and folders (no prompts)
- 📸 Take screenshots from remote system
- 🧠 Built-in `--help`, `close`, `commands` support
- 🤫 Stealth mode (no console popup on Windows)

---

## 🧠 How it Works

1. Start the `agent.py` (or compiled `agent.exe`) on the target system.
2. Control the agent from your Telegram bot using plain text commands.
3. Receive responses, files, or screenshots directly in Telegram.

---

## ⚙️ Commands List

| Command                   | Description                             |
|----------------------------|-----------------------------------------|
| `dir` / `ls`              | List files                              |
| `cd <path>`              | Change directory                        |
| `grab "file"`            | Download file                           |
| `type "file.txt"`        | View .txt file content                  |
| `upload <filename>`      | Upload from bot                         |
| `exec <filename>`        | Execute uploaded file                   |
| `del "target"`           | Delete file/folder silently             |
| `screenshot`             | Take screenshot                         |
| `--help`                 | Show command list                       |
| `commands`               | Show command count                      |
| `close`                  | End agent session                       |

---

## 📦 Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/yourname/your-repo-name.git
   cd your-repo-name
2. next step file to convert .exe file
   pip install requests pyautogui
     Install PyInstaller:

pip install pyinstaller
Generate a stealth .exe (no console window):

pyinstaller --onefile --noconsole agent.py
Output will be available in the dist/ folder:

dist/agent.exe
