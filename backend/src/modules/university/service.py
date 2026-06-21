from .schema import UniversityUpdate
from typing import Any
from ..storage.memory import universities
def create_university(new_university: dict[str,Any]) -> dict[str, Any] | None:
    for university in universities:
        if(university.get("name") == new_university.get("name") or university.get("id") == new_university.get("id")):
            return None
    universities.append(new_university)
    return new_university

def get_all_universities() -> list[dict[str, Any]]:
    return universities

def get_university(university_id: int) -> dict[str,Any] | None:
    for university in universities:
        if(university.get("id") == university_id):
            return university
    return None

def update_university(university_id: int, university_update: UniversityUpdate) -> dict[str, Any] | None:
    update_data = university_update.model_dump(mode="json", exclude_unset=True)
    existing_university = get_university(university_id)
    if existing_university is None:
        return None
    if "name" in update_data:
        for university in universities:
            if university.get("id") != university_id and university.get("name") == update_data["name"]:
                return None
    existing_university.update(update_data)
    return existing_university

def delete_university(university_id: int) -> bool:
    for university in universities:
        if(university.get("id") == university_id):
            universities.remove(university)
            return True
    return False
