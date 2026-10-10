import os
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

BANNER = """
[bold cyan]██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗     ██████╗██╗      ██████╗ ███╗   ██╗███████╗██████╗ [/bold cyan]
[bold cyan]██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗   ██╔════╝██║     ██╔═══██╗████╗  ██║██╔════╝██╔══██╗[/bold cyan]
[bold blue]██║  ██║██║███████╗██║     ██║   ██║██████╔╝   ██║     ██║     ██║   ██║██╔██╗ ██║█████╗  ██████╔╝[/bold blue]
[bold blue]██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗   ██║     ██║     ██║   ██║██║╚██╗██║██╔══╝  ██╔══██╗[/bold blue]
[bold magenta]██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║   ╚██████╗███████╗╚██████╔╝██║ ╚████║███████╗██║  ██║[/bold magenta]
[bold magenta]╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝[/bold magenta]
[dim]                       Full Discord Server Backup, Archiver & 1-Click Restore Suite[/dim]
[dim]                                          Developed by loveslaw[/dim]
"""

def print_banner():
    console.print(BANNER)

def print_panel(text: str, title: str = "INFO", style: str = "cyan"):
    console.print(Panel(text, title=f"[{style}]{title}[/{style}]", border_style=style))

def print_menu():
    table = Table(title="[bold yellow]Available Operations[/bold yellow]", border_style="bright_blue")
    table.add_column("Key", justify="center", style="bold green")
    table.add_column("Action", style="white")
    table.add_column("Description", style="dim")

    table.add_row("1", "Full Server Backup", "Export roles, channels, categories & permissions to JSON")
    table.add_row("2", "Restore / Clone Server", "Replicate an exported snapshot onto a target server")
    table.add_row("3", "Purge Target Server", "Clean slate: wipe existing channels and custom roles")
    table.add_row("4", "List Available Backups", "View snapshot files saved in backups/ directory")
    table.add_row("5", "Exit", "Close Discord Server Cloner")

    console.print(table)

def print_backups_table(backups: List[Dict[str, Any]]):
    if not backups:
        console.print("[yellow]No backups found in backups/ directory.[/yellow]")
        return

    table = Table(title="[bold green]Saved Snapshots[/bold green]", border_style="cyan")
    table.add_column("#", justify="center", style="bold yellow")
    table.add_column("Filename", style="white")
    table.add_column("Server Name", style="bold cyan")
    table.add_column("Size (KB)", justify="right", style="magenta")
    table.add_column("Date", style="dim")

    for idx, b in enumerate(backups):
        table.add_row(str(idx + 1), b["filename"], b["name"], f"{b['size_kb']:.1f}", b["date"])

    console.print(table)
