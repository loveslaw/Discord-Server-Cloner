"""
Discord-Server-Cloner
Full Server Backup, Archiver & 1-Click Restore Suite
Author: loveslaw
"""

import os
import sys
import json
import asyncio
import argparse
from datetime import datetime

import discord
from dotenv import load_dotenv

from core.ui import console, print_banner, print_panel, print_menu, print_backups_table
from core.cloner import DiscordCloner
from core.models import GuildSnapshot
from core.utils import load_json

load_dotenv()

def get_saved_backups(backup_dir: str = "backups"):
    if not os.path.exists(backup_dir):
        return []
    result = []
    for f in os.listdir(backup_dir):
        if f.endswith(".json"):
            path = os.path.join(backup_dir, f)
            try:
                data = load_json(path)
                size_kb = os.path.getsize(path) / 1024
                mtime = os.path.getmtime(path)
                date_str = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
                result.append({
                    "filename": f,
                    "filepath": path,
                    "name": data.get("name", "Unknown"),
                    "size_kb": size_kb,
                    "date": date_str
                })
            except Exception:
                pass
    return sorted(result, key=lambda x: x["date"], reverse=True)

class ClonerBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloner = DiscordCloner(delay_between_actions=0.4)
        self.is_ready_event = asyncio.Event()

    async def on_ready(self):
        console.print(f"[bold green]✔ Authenticated as:[/bold green] {self.user.name} ({self.user.id})")
        console.print(f"[bold green]✔ Connected to {len(self.guilds)} guilds.[/bold green]")
        self.is_ready_event.set()

async def interactive_cli(bot: ClonerBot):
    await bot.is_ready_event.wait()
    print_banner()

    while True:
        print_menu()
        choice = console.input("\n[bold cyan]Select operation (1-5): [/bold cyan]").strip()

        if choice == "1":
            # Backup
            console.print("\n[bold yellow]--- Available Guilds ---[/bold yellow]")
            for g in bot.guilds:
                console.print(f"• [cyan]{g.name}[/cyan] (ID: [bold white]{g.id}[/bold white])")
            guild_id_str = console.input("\n[cyan]Enter Guild ID to Backup: [/cyan]").strip()
            try:
                guild = bot.get_guild(int(guild_id_str))
                if not guild:
                    console.print(f"[red]Error: Bot is not in guild with ID {guild_id_str}.[/red]")
                    continue
                console.print(f"[yellow]Snapshotting '{guild.name}'... Please wait.[/yellow]")
                snapshot = await bot.cloner.create_backup(guild)
                saved_path = bot.cloner.save_backup_file(snapshot)
                print_panel(f"Backup created successfully!\nFile: [bold green]{saved_path}[/bold green]", "SUCCESS", "green")
            except Exception as e:
                console.print(f"[red]Error creating backup: {e}[/red]")

        elif choice == "2":
            # Restore
            backups = get_saved_backups()
            print_backups_table(backups)
            if not backups:
                continue
            b_idx_str = console.input("\n[cyan]Select backup number to restore: [/cyan]").strip()
            try:
                b_idx = int(b_idx_str) - 1
                if b_idx < 0 or b_idx >= len(backups):
                    console.print("[red]Invalid selection.[/red]")
                    continue
                selected_backup = backups[b_idx]
                target_id_str = console.input("[cyan]Enter Target Guild ID to clone onto: [/cyan]").strip()
                target_guild = bot.get_guild(int(target_id_str))
                if not target_guild:
                    console.print(f"[red]Error: Bot is not in guild with ID {target_id_str}.[/red]")
                    continue

                confirm = console.input(f"[bold red]WARNING: This will reconstruct template onto '{target_guild.name}'. Proceed? (y/n): [/bold red]").strip().lower()
                if confirm != "y":
                    console.print("[yellow]Restoration cancelled.[/yellow]")
                    continue

                snapshot_data = load_json(selected_backup["filepath"])
                snapshot = GuildSnapshot.from_dict(snapshot_data)

                def log_status(msg, cur=0, tot=0):
                    console.print(f"[blue][{cur}/{tot}][/blue] {msg}")

                console.print(f"[yellow]Restoring '{snapshot.name}' template onto '{target_guild.name}'...[/yellow]")
                await bot.cloner.restore_backup(target_guild, snapshot, log_status)
                print_panel(f"Server cloned successfully onto '{target_guild.name}'!", "RESTORE COMPLETE", "green")
            except Exception as e:
                console.print(f"[red]Error during restore: {e}[/red]")

        elif choice == "3":
            # Purge
            target_id_str = console.input("\n[bold red]Enter Guild ID to purge (DELETE all channels/roles): [/bold red]").strip()
            try:
                target_guild = bot.get_guild(int(target_id_str))
                if not target_guild:
                    console.print(f"[red]Guild {target_id_str} not found.[/red]")
                    continue
                confirm = console.input(f"[bold red]Are you ABSOLUTELY sure you want to purge '{target_guild.name}'? (yes/no): [/bold red]").strip().lower()
                if confirm != "yes":
                    console.print("[yellow]Purge cancelled.[/yellow]")
                    continue

                def purge_log(msg):
                    console.print(f"[dim]{msg}[/dim]")

                await bot.cloner.purge_guild(target_guild, purge_log)
                print_panel(f"Purge complete on '{target_guild.name}'. Canvas is now clear.", "PURGED", "yellow")
            except Exception as e:
                console.print(f"[red]Error during purge: {e}[/red]")

        elif choice == "4":
            # List backups
            backups = get_saved_backups()
            print_backups_table(backups)

        elif choice == "5":
            console.print("[bold cyan]Exiting Discord Server Cloner. Goodbye![/bold cyan]")
            await bot.close()
            break

def main():
    parser = argparse.ArgumentParser(description="Discord-Server-Cloner CLI by loveslaw")
    parser.add_argument("--token", help="Discord bot token", default=None)
    parser.add_argument("--backup", help="Guild ID to backup (headless mode)", default=None)
    parser.add_argument("--restore", help="Backup JSON path (headless mode)", default=None)
    parser.add_argument("--target", help="Target Guild ID for restore/purge", default=None)
    parser.add_argument("--purge", help="Guild ID to purge (headless mode)", default=None)

    args = parser.parse_args()

    token = args.token or os.getenv("DISCORD_TOKEN")
    if not token:
        print_banner()
        token = console.input("[bold cyan]Enter Discord Bot Token: [/bold cyan]").strip()
        if not token:
            console.print("[red]Token is required. Exiting.[/red]")
            sys.exit(1)

    intents = discord.Intents.default()
    intents.guilds = True
    intents.emojis = True

    bot = ClonerBot(intents=intents)

    async def runner():
        asyncio.create_task(interactive_cli(bot))
        try:
            await bot.start(token)
        except discord.LoginFailure:
            console.print("[bold red]Invalid Discord Token provided.[/bold red]")
            sys.exit(1)

    try:
        asyncio.run(runner())
    except (KeyboardInterrupt, SystemExit):
        pass

if __name__ == "__main__":
    main()
