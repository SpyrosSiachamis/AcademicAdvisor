from .schema import University
from typing import Any
from ..storage.memory import universities
def create_university(new_university: dict[str,Any]) -> dict[str, Any] | None:
    
    for university in universities:
        if(university.get("name") == new_university.get("name") or university.get("id") == new_university.get("id")):
            return None
    universities.append(new_university)
    print(new_university)
    return new_university

def get_all_universities() -> list[dict[str, Any]]:
    return universities

def get_university(university_id: int) -> dict[str,Any] | None:
    for university in universities:
        if(university.get("id") == university_id):
            return university
    return None

def delete_university(university_id: int) -> bool:
    for university in universities:
        if(university.get("id") == university_id):
            universities.remove(university)
            return True
    return False
