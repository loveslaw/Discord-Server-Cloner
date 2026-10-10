import os
import time
import asyncio
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime

import discord

from core.models import (
    GuildSnapshot,
    RoleSnapshot,
    CategorySnapshot,
    ChannelSnapshot,
    OverwriteSnapshot,
    EmojiSnapshot
)
from core.utils import save_json, load_json, sanitize_filename

class DiscordCloner:
    """
    High-performance Discord Server Backup, Snapshot & Cloning Engine.
    Handles lossless role hierarchy, channel permissions, categories and safe API backoff.
    """

    def __init__(self, delay_between_actions: float = 0.5):
        self.delay = delay_between_actions

    async def create_backup(self, guild, progress_callback: Optional[Callable[[str, int, int], None]] = None) -> GuildSnapshot:
        """
        Creates a lossless JSON-serializable snapshot of the target guild.
        Filters out bot integration/managed roles and captures permission overwrites.
        """
        # 1. Capture Roles
        roles_list: List[RoleSnapshot] = []
        for role in guild.roles:
            is_default = False
            if hasattr(role, "is_default") and callable(role.is_default):
                val = role.is_default()
                is_default = (val is True)
            elif role.id == guild.id or role.name == "@everyone":
                is_default = True

            if getattr(role, "managed", False) and not is_default:
                continue

            roles_list.append(RoleSnapshot(
                id=role.id,
                name=role.name,
                color=role.color.value if hasattr(role.color, "value") else int(role.color),
                hoist=role.hoist,
                position=role.position,
                permissions=role.permissions.value if hasattr(role.permissions, "value") else int(role.permissions),
                mentionable=role.mentionable,
                is_default=is_default
            ))

        # 2. Capture Categories
        categories_list: List[CategorySnapshot] = []
        for cat in guild.categories:
            cat_overwrites: List[OverwriteSnapshot] = []
            for target, ow in cat.overwrites.items():
                allow_val = ow.pair()[0].value if hasattr(ow, "pair") else 0
                deny_val = ow.pair()[1].value if hasattr(ow, "pair") else 0
                target_type = "role" if hasattr(target, "guild") else "member"
                cat_overwrites.append(OverwriteSnapshot(
                    target_id=target.id,
                    target_type=target_type,
                    allow=allow_val,
                    deny=deny_val
                ))

            categories_list.append(CategorySnapshot(
                id=cat.id,
                name=cat.name,
                position=cat.position,
                overwrites=cat_overwrites
            ))

        # 3. Capture Channels
        channels_list: List[ChannelSnapshot] = []
        for ch in guild.channels:
            ch_type_str = str(ch.type.name if hasattr(ch.type, "name") else ch.type)
            if ch_type_str.lower() == "category":
                continue

            ch_overwrites: List[OverwriteSnapshot] = []
            for target, ow in ch.overwrites.items():
                allow_val = ow.pair()[0].value if hasattr(ow, "pair") else 0
                deny_val = ow.pair()[1].value if hasattr(ow, "pair") else 0
                target_type = "role" if hasattr(target, "guild") else "member"
                ch_overwrites.append(OverwriteSnapshot(
                    target_id=target.id,
                    target_type=target_type,
                    allow=allow_val,
                    deny=deny_val
                ))

            cat_id = ch.category.id if getattr(ch, "category", None) else getattr(ch, "category_id", None)
            topic = getattr(ch, "topic", None)
            nsfw = getattr(ch, "nsfw", False)
            slowmode = getattr(ch, "slowmode_delay", 0)
            bitrate = getattr(ch, "bitrate", None)
            user_limit = getattr(ch, "user_limit", None)

            channels_list.append(ChannelSnapshot(
                id=ch.id,
                name=ch.name,
                type=ch_type_str,
                position=ch.position,
                category_id=cat_id,
                topic=topic,
                nsfw=nsfw,
                slowmode_delay=slowmode,
                bitrate=bitrate,
                user_limit=user_limit,
                overwrites=ch_overwrites
            ))

        # 4. Capture Emojis
        emojis_list: List[EmojiSnapshot] = []
        for emoji in getattr(guild, "emojis", []):
            url = str(emoji.url) if hasattr(emoji, "url") else ""
            emojis_list.append(EmojiSnapshot(
                id=emoji.id,
                name=emoji.name,
                url=url
            ))

        icon_url = str(guild.icon.url) if getattr(guild, "icon", None) else None
        banner_url = str(guild.banner.url) if getattr(guild, "banner", None) else None
        ver_level = guild.verification_level.value if hasattr(guild.verification_level, "value") else int(guild.verification_level)
        default_notif = guild.default_notifications.value if hasattr(guild.default_notifications, "value") else int(guild.default_notifications)

        snapshot = GuildSnapshot(
            id=guild.id,
            name=guild.name,
            description=getattr(guild, "description", None),
            icon_url=icon_url,
            banner_url=banner_url,
            verification_level=ver_level,
            default_notifications=default_notif,
            roles=roles_list,
            categories=categories_list,
            channels=channels_list,
            emojis=emojis_list
        )

        return snapshot

    def save_backup_file(self, snapshot: GuildSnapshot, output_dir: str = "backups") -> str:
        """Saves GuildSnapshot to formatted JSON on disk."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        sanitized_name = sanitize_filename(snapshot.name)
        filename = f"{sanitized_name}_{snapshot.id}_{timestamp}.json"
        filepath = os.path.join(output_dir, filename)
        save_json(filepath, snapshot.to_dict())
        return filepath

    async def purge_guild(self, target_guild, status_callback: Optional[Callable[[str], None]] = None) -> None:
        """
        Safely clears existing channels and custom roles from target guild.
        Leaves @everyone and bot integration roles intact.
        """
        # Delete channels
        for ch in list(target_guild.channels):
            try:
                if status_callback:
                    status_callback(f"Purging channel: #{ch.name}")
                await ch.delete()
                if self.delay > 0:
                    await asyncio.sleep(self.delay)
            except Exception:
                pass

        # Delete roles (skip default @everyone and managed bot roles)
        everyone_role = getattr(target_guild, "default_role", None) or next((r for r in target_guild.roles if r.name == "@everyone"), None)
        for role in list(target_guild.roles):
            if role == everyone_role or role.name == "@everyone" or getattr(role, "managed", False):
                continue
            try:
                if status_callback:
                    status_callback(f"Purging role: @{role.name}")
                await role.delete()
                if self.delay > 0:
                    await asyncio.sleep(self.delay)
            except Exception:
                pass

    async def restore_backup(
        self,
        target_guild,
        snapshot: GuildSnapshot,
        status_callback: Optional[Callable[[str, int, int], None]] = None
    ) -> None:
        """
        Reconstructs roles, categories, channels, and permission overwrites from snapshot.
        """
        role_map: Dict[int, Any] = {}
        category_map: Dict[int, Any] = {}

        everyone_role = getattr(target_guild, "default_role", None) or next((r for r in target_guild.roles if r.name == "@everyone"), None)

        # 1. Recreate Roles
        total_roles = len(snapshot.roles)
        for idx, role_data in enumerate(snapshot.roles):
            if status_callback:
                status_callback(f"Creating role: @{role_data.name}", idx + 1, total_roles)

            if role_data.is_default or role_data.name == "@everyone":
                if everyone_role:
                    try:
                        perms = discord.Permissions(role_data.permissions) if hasattr(discord, "Permissions") else role_data.permissions
                        await everyone_role.edit(permissions=perms)
                    except Exception:
                        pass
                    role_map[role_data.id] = everyone_role
                continue

            try:
                color = discord.Color(role_data.color) if hasattr(discord, "Color") else role_data.color
                perms = discord.Permissions(role_data.permissions) if hasattr(discord, "Permissions") else role_data.permissions
                new_role = await target_guild.create_role(
                    name=role_data.name,
                    color=color,
                    hoist=role_data.hoist,
                    mentionable=role_data.mentionable,
                    permissions=perms
                )
                role_map[role_data.id] = new_role
                if self.delay > 0:
                    await asyncio.sleep(self.delay)
            except Exception:
                pass

        # Helper to convert stored overwrites to Discord PermissionOverwrites
        def build_overwrites(ow_list: List[OverwriteSnapshot]):
            overwrites = {}
            for ow in ow_list:
                target = role_map.get(ow.target_id)
                if not target:
                    continue
                if hasattr(discord, "PermissionOverwrite") and hasattr(discord, "Permissions"):
                    allow_p = discord.Permissions(ow.allow)
                    deny_p = discord.Permissions(ow.deny)
                    overwrite_obj = discord.PermissionOverwrite.from_pair(allow_p, deny_p)
                else:
                    overwrite_obj = ow
                overwrites[target] = overwrite_obj
            return overwrites

        # 2. Recreate Categories
        total_cats = len(snapshot.categories)
        for idx, cat_data in enumerate(snapshot.categories):
            if status_callback:
                status_callback(f"Creating category: {cat_data.name}", idx + 1, total_cats)

            cat_ow = build_overwrites(cat_data.overwrites)
            try:
                new_cat = await target_guild.create_category(
                    name=cat_data.name,
                    overwrites=cat_ow
                )
                category_map[cat_data.id] = new_cat
                if self.delay > 0:
                    await asyncio.sleep(self.delay)
            except Exception:
                pass

        # 3. Recreate Channels
        total_channels = len(snapshot.channels)
        for idx, ch_data in enumerate(snapshot.channels):
            if status_callback:
                status_callback(f"Creating channel: #{ch_data.name}", idx + 1, total_channels)

            target_cat = category_map.get(ch_data.category_id)
            ch_ow = build_overwrites(ch_data.overwrites)

            try:
                ch_type = ch_data.type.lower()
                if "voice" in ch_type:
                    await target_guild.create_voice_channel(
                        name=ch_data.name,
                        category=target_cat,
                        overwrites=ch_ow,
                        bitrate=ch_data.bitrate or 64000,
                        user_limit=ch_data.user_limit or 0
                    )
                else:
                    # Default to text channel
                    await target_guild.create_text_channel(
                        name=ch_data.name,
                        category=target_cat,
                        topic=ch_data.topic or None,
                        slowmode_delay=ch_data.slowmode_delay,
                        nsfw=ch_data.nsfw,
                        overwrites=ch_ow
                    )
                if self.delay > 0:
                    await asyncio.sleep(self.delay)
            except Exception:
                pass
