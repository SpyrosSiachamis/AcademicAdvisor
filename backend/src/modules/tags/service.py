from typing import Any

from .schema import Tag, TagUpdate
from ..storage.memory import tags


def create_tag(tag: Tag) -> dict[str, Any] | None:
    tag_data = tag.model_dump(mode="json")
    for existing_tag in tags:
        if existing_tag.get("id") == tag_data["id"] or existing_tag.get("name") == tag_data["name"]:
            return None
    tags.append(tag_data)
    return tag_data


def get_tags() -> list[dict[str, Any]]:
    return tags


def get_tag(tag_id: int) -> dict[str, Any] | None:
    for tag in tags:
        if tag.get("id") == tag_id:
            return tag
    return None


def update_tag(tag_id: int, tag_update: TagUpdate) -> dict[str, Any] | None:
    update_data = tag_update.model_dump(mode="json", exclude_unset=True)
    existing_tag = get_tag(tag_id)
    if existing_tag is None:
        return None
    if "name" in update_data:
        for tag in tags:
            if tag.get("id") != tag_id and tag.get("name") == update_data["name"]:
                return None
    existing_tag.update(update_data)
    return existing_tag


def delete_tag(tag_id: int) -> bool:
    for tag in tags:
        if tag.get("id") == tag_id:
            tags.remove(tag)
            return True
    return False
