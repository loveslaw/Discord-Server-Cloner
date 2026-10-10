from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any

@dataclass
class RoleSnapshot:
    id: int
    name: str
    color: int
    hoist: bool
    position: int
    permissions: int
    mentionable: bool
    is_default: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoleSnapshot":
        return cls(**data)

@dataclass
class OverwriteSnapshot:
    target_id: int
    target_type: str  # "role" or "member"
    allow: int
    deny: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "OverwriteSnapshot":
        return cls(**data)

@dataclass
class ChannelSnapshot:
    id: int
    name: str
    type: str  # "text", "voice", "category", "news", "stage"
    position: int
    category_id: Optional[int] = None
    topic: Optional[str] = None
    nsfw: bool = False
    slowmode_delay: int = 0
    bitrate: Optional[int] = None
    user_limit: Optional[int] = None
    overwrites: List[OverwriteSnapshot] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["overwrites"] = [o.to_dict() if isinstance(o, OverwriteSnapshot) else o for o in self.overwrites]
        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChannelSnapshot":
        raw_ow = data.pop("overwrites", [])
        overwrites = [OverwriteSnapshot.from_dict(o) if isinstance(o, dict) else o for o in raw_ow]
        return cls(overwrites=overwrites, **data)

@dataclass
class CategorySnapshot:
    id: int
    name: str
    position: int
    overwrites: List[OverwriteSnapshot] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["overwrites"] = [o.to_dict() if isinstance(o, OverwriteSnapshot) else o for o in self.overwrites]
        return res

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CategorySnapshot":
        raw_ow = data.pop("overwrites", [])
        overwrites = [OverwriteSnapshot.from_dict(o) if isinstance(o, dict) else o for o in raw_ow]
        return cls(overwrites=overwrites, **data)

@dataclass
class EmojiSnapshot:
    id: int
    name: str
    url: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmojiSnapshot":
        return cls(**data)

@dataclass
class GuildSnapshot:
    id: int
    name: str
    description: Optional[str] = None
    icon_url: Optional[str] = None
    banner_url: Optional[str] = None
    verification_level: int = 0
    default_notifications: int = 0
    roles: List[RoleSnapshot] = field(default_factory=list)
    categories: List[CategorySnapshot] = field(default_factory=list)
    channels: List[ChannelSnapshot] = field(default_factory=list)
    emojis: List[EmojiSnapshot] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon_url": self.icon_url,
            "banner_url": self.banner_url,
            "verification_level": self.verification_level,
            "default_notifications": self.default_notifications,
            "roles": [r.to_dict() for r in self.roles],
            "categories": [c.to_dict() for c in self.categories],
            "channels": [ch.to_dict() for ch in self.channels],
            "emojis": [e.to_dict() for e in self.emojis]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GuildSnapshot":
        roles = [RoleSnapshot.from_dict(r) for r in data.get("roles", [])]
        categories = [CategorySnapshot.from_dict(c) for c in data.get("categories", [])]
        channels = [ChannelSnapshot.from_dict(ch) for ch in data.get("channels", [])]
        emojis = [EmojiSnapshot.from_dict(e) for e in data.get("emojis", [])]
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description"),
            icon_url=data.get("icon_url"),
            banner_url=data.get("banner_url"),
            verification_level=data.get("verification_level", 0),
            default_notifications=data.get("default_notifications", 0),
            roles=roles,
            categories=categories,
            channels=channels,
            emojis=emojis
        )
