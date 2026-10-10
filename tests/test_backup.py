import asyncio
from unittest.mock import MagicMock
from core.cloner import DiscordCloner
from core.models import GuildSnapshot

def test_create_backup_extracts_guild_data():
    cloner = DiscordCloner()

    # Mock Role
    mock_everyone_role = MagicMock()
    mock_everyone_role.id = 100
    mock_everyone_role.name = "@everyone"
    mock_everyone_role.color.value = 0
    mock_everyone_role.hoist = False
    mock_everyone_role.position = 0
    mock_everyone_role.permissions.value = 104324161
    mock_everyone_role.mentionable = False
    mock_everyone_role.is_default.return_value = True
    mock_everyone_role.managed = False

    mock_custom_role = MagicMock()
    mock_custom_role.id = 101
    mock_custom_role.name = "VIP"
    mock_custom_role.color.value = 0xFFD700
    mock_custom_role.hoist = True
    mock_custom_role.position = 1
    mock_custom_role.permissions.value = 8
    mock_custom_role.mentionable = True
    mock_custom_role.is_default.return_value = False
    mock_custom_role.managed = False

    mock_managed_bot_role = MagicMock()
    mock_managed_bot_role.id = 102
    mock_managed_bot_role.name = "Dyno"
    mock_managed_bot_role.managed = True

    # Mock Category
    mock_cat = MagicMock()
    mock_cat.id = 200
    mock_cat.name = "COMMUNITY"
    mock_cat.position = 0
    mock_cat.overwrites = {}

    # Mock Channel
    mock_ch = MagicMock()
    mock_ch.id = 300
    mock_ch.name = "general-chat"
    mock_ch.position = 0
    mock_ch.category = mock_cat
    mock_ch.category_id = 200
    mock_ch.topic = "Chit chat"
    mock_ch.nsfw = False
    mock_ch.slowmode_delay = 5
    mock_ch.type.name = "text"
    mock_ch.overwrites = {}

    # Mock Guild
    mock_guild = MagicMock()
    mock_guild.id = 99999
    mock_guild.name = "Test Guild"
    mock_guild.description = "A friendly server"
    mock_guild.icon = None
    mock_guild.banner = None
    mock_guild.verification_level.value = 1
    mock_guild.default_notifications.value = 0
    mock_guild.roles = [mock_everyone_role, mock_custom_role, mock_managed_bot_role]
    mock_guild.categories = [mock_cat]
    mock_guild.channels = [mock_ch]
    mock_guild.emojis = []

    snapshot = asyncio.run(cloner.create_backup(mock_guild))

    assert isinstance(snapshot, GuildSnapshot)
    assert snapshot.id == 99999
    assert snapshot.name == "Test Guild"
    # Managed bot role should be filtered out
    assert len(snapshot.roles) == 2
    assert snapshot.roles[1].name == "VIP"
    assert snapshot.roles[1].color == 0xFFD700
    assert len(snapshot.categories) == 1
    assert snapshot.categories[0].name == "COMMUNITY"
    assert len(snapshot.channels) == 1
    assert snapshot.channels[0].name == "general-chat"
    assert snapshot.channels[0].category_id == 200
