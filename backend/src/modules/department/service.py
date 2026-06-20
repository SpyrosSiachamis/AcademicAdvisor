from typing import Any
from .schema import DepartmentRead, DepartmentUpdate
from ..storage.memory import departments, universities
# TODO: - Rename flag to university_exists., - Make department name unique only within the same university., - Split duplicate department and missing university errors later.
def create_department(department_data: dict[str,Any]) -> DepartmentRead | None:
    if(not university_exists(department_data)):
        return None
    if(check_department(department_data)):
        return None
    departments.append(department_data)
    result = DepartmentRead(**department_data)
    return result

def get_departments() -> list[dict[str, Any]]:
    return [DepartmentRead.model_validate(department).model_dump() for department in departments]

def university_exists(department_data: dict[str,Any]) -> bool:
    for university in universities:
        if(university.get("id") == department_data["university_id"]):
            return True
    return False

def check_department(department_data: dict[str,Any]) -> bool:
    for department in departments:
        if(department.get("id") == department_data.get("id") or (department.get("name") == department_data.get("name") and department.get("university_id") == department_data.get("university_id"))):
            return True
    return False

def fetch_department(dep_id:int) -> DepartmentRead | None:
    """
    Fetches a department by its ID.
    Args:
        dep_id (int): The ID of the department to fetch.
    Returns:
        DepartmentRead | None: The department data if found, otherwise None.
    """
    for department in departments:
        if(department.get("id") == dep_id):
            result = DepartmentRead(**department)
            return result
    return None

def update_department(dep_id: int, department_update: DepartmentUpdate) -> DepartmentRead | None:
    update_data = department_update.model_dump(mode="json", exclude_unset=True)
    existing_department = fetch_department_record(dep_id)
    if existing_department is None:
        return None
    candidate_department = {**existing_department, **update_data}
    if not university_exists(candidate_department):
        return None
    for department in departments:
        if department.get("id") == dep_id:
            continue
        if (
            department.get("name") == candidate_department.get("name")
            and department.get("university_id") == candidate_department.get("university_id")
        ):
            return None
    existing_department.update(update_data)
    return DepartmentRead.model_validate(existing_department)

def delete_department(dep_id:int) -> bool:
    """
    Deletes a department by its ID.
    Args:
        dep_id (int): The ID of the department to delete.
    Returns:
        bool: True if the department was deleted, False if not found.
    """
    for department in departments:
        if(department.get("id") == dep_id):
            departments.remove(department)
            return True
    return False

def fetch_department_record(dep_id: int) -> dict[str, Any] | None:
    for department in departments:
        if department.get("id") == dep_id:
            return department
    return None
