from typing import Any
from .schema import DepartmentRead
from ..university.service import universities
from ..storage.memory import departments
# TODO: - Rename flag to university_exists., - Make department name unique only within the same university., - Split duplicate department and missing university errors later.
def create_department(department_data: dict[str,Any]) -> DepartmentRead | None:
    if(not verify_university(department_data)):
        return None
    if(check_department(department_data)):
        return None
    departments.append(department_data)
    result = DepartmentRead(**department_data)
    return result

def verify_university(department_data: dict[str,Any]) -> bool:
    for university in universities:
        if(university.get("university_id") == department_data["university_id"]):
            return False
    return True

def check_department(department_data: dict[str,Any]) -> bool:
    for department in departments:
        if(department.get("department_id") == department_data.get("department_id") or (department.get("name") == department_data.get("name") and department.get("university_id") == department_data.get("university_id"))):
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
        if(department.get("department_id") == dep_id):
            result = DepartmentRead(**department)
            return result
    return None

def delete_department(dep_id:int) -> bool:
    """
    Deletes a department by its ID.
    Args:
        dep_id (int): The ID of the department to delete.
    Returns:
        bool: True if the department was deleted, False if not found.
    """
    for department in departments:
        if(department.get("department_id") == dep_id):
            departments.remove(department)
            return True
    return False