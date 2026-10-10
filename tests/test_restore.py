import asyncio
from unittest.mock import MagicMock, AsyncMock
from core.cloner import DiscordCloner
from core.models import (
    GuildSnapshot,
    RoleSnapshot,
    CategorySnapshot,
    ChannelSnapshot,
    OverwriteSnapshot
)

def test_purge_guild():
    cloner = DiscordCloner(delay_between_actions=0)

    mock_ch1 = MagicMock()
    mock_ch1.delete = AsyncMock()
    mock_ch2 = MagicMock()
    mock_ch2.delete = AsyncMock()

    mock_everyone_role = MagicMock()
    mock_everyone_role.id = 100
    mock_everyone_role.name = "@everyone"
    mock_everyone_role.managed = False

    mock_bot_role = MagicMock()
    mock_bot_role.id = 101
    mock_bot_role.name = "MyBot"
    mock_bot_role.managed = True
    mock_bot_role.delete = AsyncMock()

    mock_custom_role = MagicMock()
    mock_custom_role.id = 102
    mock_custom_role.name = "Member"
    mock_custom_role.managed = False
    mock_custom_role.delete = AsyncMock()

    mock_guild = MagicMock()
    mock_guild.id = 100
    mock_guild.channels = [mock_ch1, mock_ch2]
    mock_guild.categories = []
    mock_guild.roles = [mock_everyone_role, mock_bot_role, mock_custom_role]

    asyncio.run(cloner.purge_guild(mock_guild))

    mock_ch1.delete.assert_called_once()
    mock_ch2.delete.assert_called_once()
    # Bot role & @everyone should NOT be deleted
    mock_bot_role.delete.assert_not_called()
    mock_custom_role.delete.assert_called_once()

def test_restore_backup_creates_and_maps_hierarchy():
    cloner = DiscordCloner(delay_between_actions=0)

    # Backup data with 1 custom role, 1 category, 1 text channel with overwrite
    role_snap = RoleSnapshot(
        id=555,
        name="VIP",
        color=0xFF0000,
        hoist=True,
        position=1,
        permissions=8,
        mentionable=True
    )
    ow_snap = OverwriteSnapshot(
        target_id=555,
        target_type="role",
        allow=1024,
        deny=0
    )
    cat_snap = CategorySnapshot(
        id=777,
        name="LOUNGE",
        position=0,
        overwrites=[ow_snap]
    )
    ch_snap = ChannelSnapshot(
        id=888,
        name="vip-chat",
        type="text",
        position=0,
        category_id=777,
        topic="VIPs only",
        nsfw=False,
        slowmode_delay=0,
        bitrate=None,
        user_limit=None,
        overwrites=[ow_snap]
    )
    snapshot = GuildSnapshot(
        id=999,
        name="Restored Server",
        description=None,
        icon_url=None,
        banner_url=None,
        verification_level=1,
        default_notifications=0,
        roles=[role_snap],
        categories=[cat_snap],
        channels=[ch_snap],
        emojis=[]
    )

    # Target Guild Mock
    mock_everyone = MagicMock()
    mock_everyone.id = 1000
    mock_everyone.name = "@everyone"
    mock_everyone.edit = AsyncMock()

    new_role_created = MagicMock()
    new_role_created.id = 666
    new_role_created.name = "VIP"

    new_cat_created = MagicMock()
    new_cat_created.id = 7770
    new_cat_created.name = "LOUNGE"

    new_ch_created = MagicMock()
    new_ch_created.id = 8880
    new_ch_created.name = "vip-chat"

    mock_target = MagicMock()
    mock_target.id = 1000
    mock_target.roles = [mock_everyone]
    mock_target.edit = AsyncMock()
    mock_target.create_role = AsyncMock(return_value=new_role_created)
    mock_target.create_category = AsyncMock(return_value=new_cat_created)
    mock_target.create_text_channel = AsyncMock(return_value=new_ch_created)

    asyncio.run(cloner.restore_backup(mock_target, snapshot))

    # Verification
    mock_target.create_role.assert_called_once()
    mock_target.create_category.assert_called_once()
    mock_target.create_text_channel.assert_called_once()
