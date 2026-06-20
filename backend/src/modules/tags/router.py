from fastapi import APIRouter, HTTPException

from .schema import Tag, TagUpdate
from .service import create_tag, delete_tag, get_tag, get_tags, update_tag


router = APIRouter(prefix="/tags", tags=["tags"])


@router.post("/")
async def add_tag(tag: Tag):
    result = create_tag(tag)
    if result is None:
        raise HTTPException(status_code=409, detail="Duplicate tag")
    return {"message": "Tag created successfully", "tag": result}


@router.get("/")
async def list_tags():
    return {"message": "Retrieved all tags", "tags": get_tags()}


@router.get("/{tag_id}")
async def get_tag_by_id(tag_id: int):
    result = get_tag(tag_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag found", "tag": result}


@router.put("/{tag_id}")
async def update_tag_by_id(tag_id: int, tag_update: TagUpdate):
    result = update_tag(tag_id, tag_update)
    if result is None:
        raise HTTPException(status_code=404, detail="Tag not found or duplicate name")
    return {"message": "Tag updated successfully", "tag": result}


@router.delete("/{tag_id}")
async def delete_tag_by_id(tag_id: int):
    result = delete_tag(tag_id)
    if not result:
        raise HTTPException(status_code=404, detail="Tag not found")
    return {"message": "Tag deleted successfully"}
