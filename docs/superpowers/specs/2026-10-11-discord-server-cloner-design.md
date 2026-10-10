# Design Spec: Discord-Server-Cloner

**Date:** 2026-10-11  
**Author:** loveslaw  
**Status:** Approved  
**Topic:** Discord Full Server Backup, Archiver & 1-Click Template Cloner Suite  

---

## 1. Executive Summary
Discord-Server-Cloner is an asynchronous Python CLI automation tool built on `discord.py` and `rich`. It enables server owners and administrators to take full, lossless snapshots of their Discord guilds (roles, categories, channels, permission overwrites, emojis, and server metadata) and seamlessly clone/restore them to any new or existing target server with intelligent rate-limit throttling.

---

## 2. Core Functional Requirements

### 2.1 Server Backup & Snapshotting
- Authenticate via bot token or user token (with explicit rate-limit safety).
- Extract guild properties:
  - Name, icon URL, splash, banner, verification level, default notification settings.
- Extract role hierarchy:
  - Role name, hex color, permissions bitfield, hoist status, mentionable flag, position hierarchy.
- Extract category and channel structures:
  - Categories with exact ordering.
  - Text channels, Voice channels, Announcement channels, Forum channels, Stage channels.
  - Channel topic, NSFW flag, slowmode delay, bitrate, user limit.
- Extract permission overwrites:
  - Specific permission flags (`view_channel`, `send_messages`, `connect`, etc.) per role.
- Output: Export clean, portable JSON format saved to `backups/<guild_id>_<timestamp>.json`.

### 2.2 Server Restoration & Cloning
- Read selected JSON snapshot from `backups/`.
- Validate target guild ID and bot administrative permissions.
- Optional wipe/purge mode: Delete existing default channels and roles (except `@everyone` and managed bot roles).
- Recreate role hierarchy:
  - Map old role IDs to new created role IDs.
- Recreate categories and channels:
  - Apply corresponding permission overwrites mapped to the newly created role IDs.
- Rate-limit mitigation:
  - Implement dynamic backoff upon encountering HTTP 429 (`retry_after`).
  - Introduce artificial delays between channel/role creations to remain safely under Discord's burst limits.

### 2.3 Interactive Terminal CLI
- Beautiful ASCII art banner using `rich`.
- Interactive prompts for:
  1. Full Server Backup
  2. Restore / Clone from Backup
  3. Purge Target Guild
  4. List Available Backups
  5. Exit
- Live progress bars indicating role, category, and channel creation progress.

---

## 3. Architecture & File Layout

```
Discord-Server-Cloner/
├── backups/               # Directory for exported backup JSON files
├── core/
│   ├── __init__.py
│   ├── cloner.py          # Core async backup & restore logic
│   ├── ui.py              # Rich terminal interface & banners
│   └── utils.py           # Rate limiting, logging, helper functions
├── config/
│   ├── config.json        # User configurations (delays, backup paths)
│   └── .env.example       # Example environment variables
├── .gitignore             # Standard git exclusions (backups, .env, __pycache__)
├── LICENSE                # MIT License
├── README.md              # Detailed documentation with setup and badges
├── main.py                # CLI entry point
└── requirements.txt       # Python dependencies (discord.py, rich, colorama)
```

---

## 4. Privacy & Anonymization
- **Author Identity:** Exclusively identified as `loveslaw`.
- **Zero Personal Data:** No local file paths, personal usernames, or tokens committed.
- **Git Commit Author:** `loveslaw <loveslaw@users.noreply.github.com>`.

---

## 5. Error Handling & Edge Cases
- **Missing Permissions:** Warn user if bot lacks `Administrator` or `Manage Roles` / `Manage Channels`.
- **Managed Roles:** Skip bot-specific integrated roles and Nitro booster role during role creation.
- **Role Hierarchy Bounds:** Only assign roles lower than the bot's highest role.
- **Rate Limits:** Automatic exponential backoff and retry logic.
