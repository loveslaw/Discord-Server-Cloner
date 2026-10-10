# Discord-Server-Cloner Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a robust, modular, asynchronous Discord Server Backup, Archiver & 1-Click Cloner CLI in Python, fully tested and deployed to GitHub.

**Architecture:** Async Python application leveraging `discord.py` for API interaction, custom serializable dataclass models for lossless snapshotting, and `rich` for an interactive terminal interface.

**Tech Stack:** Python 3.10+, `discord.py` (v2.3+), `rich`, `colorama`, `pytest`, `pytest-asyncio`.

**Spec:** `docs/superpowers/specs/2026-10-11-discord-server-cloner-design.md`

## Global Constraints
- Target user and Git author identity: `loveslaw` (<loveslaw@users.noreply.github.com>).
- Zero references to previous identities anywhere in code, comments, logs, or commit history.
- Pure zero-clutter workspace: clean `.gitignore` excluding `.env`, cache, and exported backups.
- Clean rate-limit mitigation with automatic exponential backoff.

## Review Focus
1. Managed & integrated bot roles cannot be created via API — must be filtered out gracefully.
2. Discord burst rate limit on channel and role creation — must throttle with configured delays.
3. Permission overwrite role mapping — must map old guild role IDs to newly generated role IDs.
4. Channel hierarchy preservation — categories must be created before child channels.
5. `@everyone` role cannot be deleted or re-created, only its permissions updated.

---

### Task 1: Core Snapshot Data Models & Serialization
**Files:**
- Create: `core/models.py`
- Create: `core/utils.py`
- Create: `tests/test_models.py`

**Interfaces:**
- Produces: `GuildSnapshot`, `RoleSnapshot`, `ChannelSnapshot`, `OverwriteSnapshot`, `sanitize_filename()`.

- [ ] **Step 1: Write failing tests for data models**
```python
# tests/test_models.py
from core.models import RoleSnapshot, ChannelSnapshot, GuildSnapshot

def test_role_snapshot_serialization():
    role = RoleSnapshot(
        id=123456,
        name="Admin",
        color=0xFF0000,
        hoist=True,
        position=5,
        permissions=8,
        mentionable=True
    )
    data = role.to_dict()
    assert data["name"] == "Admin"
    assert data["permissions"] == 8
    
    restored = RoleSnapshot.from_dict(data)
    assert restored.name == role.name
    assert restored.color == 0xFF0000
```
- [ ] **Step 2: Run pytest to verify failure**
Run: `pytest tests/test_models.py` (Expected: ModuleNotFoundError / ImportError)
- [ ] **Step 3: Implement data models in `core/models.py` & `core/utils.py`**
- [ ] **Step 4: Run pytest to verify all tests pass**
- [ ] **Step 5: Git commit task 1**

---

### Task 2: Backup & Export Engine
**Files:**
- Create: `core/cloner.py`
- Create: `tests/test_backup.py`

**Interfaces:**
- Consumes: `GuildSnapshot`, `RoleSnapshot`, `ChannelSnapshot`
- Produces: `DiscordCloner.create_backup(guild) -> GuildSnapshot`

- [ ] **Step 1: Write failing tests for backup generator using mock objects**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `create_backup` in `core/cloner.py`**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Git commit task 2**

---

### Task 3: Restore & Purge Engine
**Files:**
- Modify: `core/cloner.py`
- Create: `tests/test_restore.py`

**Interfaces:**
- Consumes: `GuildSnapshot`
- Produces: `DiscordCloner.restore_backup(target_guild, snapshot, status_callback)`, `DiscordCloner.purge_guild(target_guild)`

- [ ] **Step 1: Write failing tests for role ID remapping & channel hierarchy mapping**
- [ ] **Step 2: Run pytest to verify failure**
- [ ] **Step 3: Implement `restore_backup` and `purge_guild` with rate-limit throttling**
- [ ] **Step 4: Run pytest to verify pass**
- [ ] **Step 5: Git commit task 3**

---

### Task 4: Interactive Rich UI & CLI Entrypoint
**Files:**
- Create: `core/ui.py`
- Create: `main.py`
- Create: `config/config.json`
- Create: `config/.env.example`
- Create: `requirements.txt`
- Create: `.gitignore`
- Create: `LICENSE`

**Interfaces:**
- Consumes: `DiscordCloner`, `ui.show_banner()`, `ui.prompt_menu()`

- [ ] **Step 1: Implement `core/ui.py` with Rich ASCII banners and tables**
- [ ] **Step 2: Implement `main.py` entrypoint connecting discord.Client event loop with CLI menu**
- [ ] **Step 3: Add `requirements.txt`, `.gitignore`, `LICENSE`, and default configs**
- [ ] **Step 4: Verify CLI starts cleanly with `--help` flag**
- [ ] **Step 5: Git commit task 4**

---

### Task 5: Detailed README, GitHub Remote & Live Push
**Files:**
- Create: `README.md`

- [x] **Step 1: Write comprehensive project documentation in `README.md`**
- [x] **Step 2: Check all repository files for any identity references**
- [ ] **Step 3: Create public repository `loveslaw/Discord-Server-Cloner` on GitHub**
- [ ] **Step 4: Push to GitHub origin main**
- [ ] **Step 5: Verify repository via GitHub API audit**
