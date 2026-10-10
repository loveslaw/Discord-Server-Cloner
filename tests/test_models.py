import pytest
from core.models import RoleSnapshot, ChannelSnapshot, OverwriteSnapshot, GuildSnapshot

def test_role_snapshot_serialization():
    role = RoleSnapshot(
        id=123456789,
        name="Moderator",
        color=0x3498DB,
        hoist=True,
        position=4,
        permissions=268435456,
        mentionable=True
    )
    data = role.to_dict()
    assert data["name"] == "Moderator"
    assert data["color"] == 0x3498DB
    assert data["permissions"] == 268435456

    restored = RoleSnapshot.from_dict(data)
    assert restored.id == 123456789
    assert restored.name == role.name
    assert restored.color == role.color
    assert restored.hoist is True
    assert restored.permissions == 268435456

def test_channel_snapshot_serialization():
    overwrite = OverwriteSnapshot(
        target_id=123456789,
        target_type="role",
        allow=1024,
        deny=2048
    )
    channel = ChannelSnapshot(
        id=987654321,
        name="announcements",
        type="text",
        position=1,
        category_id=1122334455,
        topic="Important server news",
        nsfw=False,
        slowmode_delay=0,
        bitrate=None,
        user_limit=None,
        overwrites=[overwrite]
    )
    data = channel.to_dict()
    assert data["name"] == "announcements"
    assert data["type"] == "text"
    assert len(data["overwrites"]) == 1
    assert data["overwrites"][0]["allow"] == 1024

    restored = ChannelSnapshot.from_dict(data)
    assert restored.id == 987654321
    assert restored.topic == "Important server news"
    assert len(restored.overwrites) == 1
    assert restored.overwrites[0].deny == 2048

def test_guild_snapshot_roundtrip():
    role = RoleSnapshot(id=1, name="Admin", color=0xFF0000, hoist=True, position=1, permissions=8, mentionable=False)
    channel = ChannelSnapshot(id=2, name="general", type="text", position=0, category_id=None, topic="", nsfw=False, slowmode_delay=0, bitrate=None, user_limit=None, overwrites=[])
    
    guild = GuildSnapshot(
        id=1001,
        name="Cyber Fortress",
        description="Official Community Hub",
        icon_url=None,
        banner_url=None,
        verification_level=2,
        default_notifications=1,
        roles=[role],
        categories=[],
        channels=[channel],
        emojis=[]
    )
    
    data = guild.to_dict()
    assert data["name"] == "Cyber Fortress"
    assert len(data["roles"]) == 1
    assert len(data["channels"]) == 1
    
    restored = GuildSnapshot.from_dict(data)
    assert restored.id == 1001
    assert restored.name == "Cyber Fortress"
    assert restored.roles[0].name == "Admin"
    assert restored.channels[0].name == "general"
