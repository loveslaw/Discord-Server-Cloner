# 🚀 Discord Server Cloner & Backup Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square&logo=python)](https://python.org)
[![Discord.py](https://img.shields.io/badge/discord.py-v2.3%2B-5865F2.svg?style=flat-square&logo=discord)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=flat-square)]()

A high-performance, asynchronous Discord server cloning, backup, and template replication suite built in Python. Effortlessly export entire Discord communities—including role hierarchies, permission overwrites, channel structures, categories, and server metadata—into portable JSON snapshots and restore them onto fresh target guilds in seconds.

---

## 📸 Terminal Interface Preview

```
██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗     ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗ 
██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗   ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗
██║  ██║██║███████╗██║     ██║   ██║██████╔╝   ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝
██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗   ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗
██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║   ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║
╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                       Full Discord Server Backup, Archiver & 1-Click Restore Suite
                                          Developed by loveslaw
```

---

## ✨ Features

- **⚡ Full Lossless Snapshots**:
  - **Role Hierarchy**: Color values, hoist state, mentionability, position order, and permission bitfields.
  - **Category Organization**: Channel group order and nested permission inheritances.
  - **Channel Types**: Full support for Text Channels, Voice Channels, Announcement/News Channels, and Stage Channels.
  - **Channel Attributes**: Topics, slowmode delays, NSFW flags, bitrates, and user capacity limits.
  - **Permission Overwrites**: Granular allow/deny bitfield mappings mapped to newly created roles.
- **🔄 Intelligent Hierarchy Remapping**: Automatically maps old role IDs to newly generated Discord role IDs during restoration, preserving complex permission matrixes.
- **🛡️ Rate-Limit Throttling**: Built-in dynamic delays between Discord REST actions with automatic exponential backoff on HTTP 429 (`retry_after`).
- **🧹 Canvas Purge Mode**: One-click wipe tool to clean out default Discord channels and dummy roles on fresh target servers before restoration.
- **💻 Dual Interface**:
  - **Interactive TUI**: Styled terminal dashboard powered by `rich` with colored tables and live step counters.
  - **Headless CLI**: Command-line flags for automated scripting and CI/CD operations.
- **🔒 Zero Leak Architecture**: Strictly decoupled configuration via `.env` with no hardcoded credentials.

---

## 📁 Repository Structure

```
Discord-Server-Cloner/
├── core/
│   ├── __init__.py       # Package definition
│   ├── cloner.py         # Async backup, restore, and purge engine
│   ├── models.py         # Type-safe dataclass snapshot models
│   ├── ui.py             # Rich terminal banners and tables
│   └── utils.py          # JSON serialization & filesystem sanitizers
├── config/
│   ├── config.json       # Throttling delays and directory settings
│   └── .env.example      # Example environment configuration
├── tests/
│   ├── test_models.py    # Unit tests for data serialization
│   ├── test_backup.py    # Unit tests for backup extraction
│   └── test_restore.py   # Unit tests for restore & purge engine
├── .gitignore            # Git exclusion rules
├── LICENSE               # MIT License
├── main.py               # CLI entry point
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10** or higher installed on your system.
- A **Discord Bot** created via the [Discord Developer Portal](https://discord.com/developers/applications).

### Required Bot Permissions
Ensure your bot is invited to both source and target servers with the following permissions:
- `Administrator` *(recommended for full channel & role reconstruction)*
- Or at minimum:
  - `Manage Server`
  - `Manage Roles`
  - `Manage Channels`
  - `View Channels`

> ⚠️ **Note:** To clone role hierarchies, place the Bot's role at the very top of the role list in Server Settings.

---

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/loveslaw/Discord-Server-Cloner.git
   cd Discord-Server-Cloner
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your Token**:
   Copy `.env.example` to `.env`:
   ```bash
   cp config/.env.example .env
   ```
   Edit `.env` and insert your Discord Bot token:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ```

---

## 🛠️ Usage

### 1. Interactive Menu Mode
Run without arguments to launch the interactive terminal:
```bash
python main.py
```
From the interactive menu, choose:
1. `1`: **Full Server Backup** — Select any guild the bot is in and create a timestamped JSON snapshot.
2. `2`: **Restore / Clone Server** — Pick a saved snapshot from the list and replicate it onto a target server.
3. `3`: **Purge Target Server** — Wipe existing channels and custom roles to start with a blank canvas.
4. `4`: **List Available Backups** — View existing backup files with file sizes and export dates.
5. `5`: **Exit** — Safely disconnect the bot.

---

### 2. Headless CLI Mode (Automation / Scripting)

- **Create a Backup**:
  ```bash
  python main.py --token "YOUR_TOKEN" --backup 123456789012345678
  ```

- **Purge a Target Guild**:
  ```bash
  python main.py --token "YOUR_TOKEN" --purge 987654321098765432
  ```

- **Restore / Clone onto Target Guild**:
  ```bash
  python main.py --token "YOUR_TOKEN" --restore "backups/MyServer_123_20261011_000000.json" --target 987654321098765432
  ```

---

## 🧪 Running Unit Tests

The test suite validates data models, backup generation, and hierarchy restoration:
```bash
python -m pytest -v
```

---

## ⚙️ Configuration (`config/config.json`)

You can fine-tune operation delays to match your network latency:
```json
{
  "delays": {
    "channel_creation_seconds": 0.4,
    "role_creation_seconds": 0.3,
    "purge_action_seconds": 0.2
  },
  "storage": {
    "backup_dir": "backups"
  }
}
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ⚠️ Disclaimer

This tool is created for server backup, archiving, administrative migration, and template management purposes. Ensure you have appropriate administrative permissions from the respective server owners before taking backups or restoring layouts. Adhere to [Discord's Terms of Service](https://discord.com/terms).
