from typing import Any
from .schema import DepartmentCreate,DepartmentRead
from ..university.service import universities
departments: list[dict[str,Any]] = []
def create_department(department_data: dict[str,Any]) -> DepartmentRead | None:
    flag:bool = False
    for department in departments:
        if((department.get("department_id") == department_data.get("department_id")) or department.get("name") == department_data.get("name")):
            return None
    for university in universities:
        if(university.get("university_id") == department_data.get("university_id")):
            flag = True
    if(not flag):
        return None
    departments.append(department_data)
    result = DepartmentRead(**department_data)
    return result

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