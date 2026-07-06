# Academic Advisor

An academic decision-support system that recommends courses and academic paths based on completed courses, ratings, workload tolerance, interests, prerequisites, degree constraints, and career goals.

## Table of Contents

- [Current Status](#current-status)
- [Current Scope](#current-scope)
- [API Documentation](#api-documentation)
- [Planned Stack for V1](#planned-stack-for-v1)
- [V1 Scope](#v1-scope)
- [Post-V1 / Pre-Production Scope](#post-v1--pre-production-scope)
- [Future Expansion: University Portal Data Sync](#future-expansion-university-portal-data-sync)
- [Planned V1 Architecture](#planned-v1-architecture)
- [ER Diagram](#er-diagram)
- [Prerequisite Rule Representation (V1)](#prerequisite-rule-representation-v1)
- [Eligibility Engine Status](#eligibility-engine-status)

## Current Status

Early-stage development. The project currently contains a containerized FastAPI backend used for experimenting with API structure, validation, and backend architecture before implementing the main recommendation system. Students already use AI manually to research courses and plan their academic path. AcademicAdvisor turns that into a structured, data-driven advising system.

## Current Scope

Eligibility evaluation currently supports a single department. The prerequisite adjacency list is built from all courses and prerequisite groups in storage, without filtering by department. Multi-department support (per-department adjacency lists, cross-department prerequisite resolution) is not yet implemented. Cross-department prerequisites may exist in real university data and are not handled.

## API Documentation

The current course catalog endpoints are documented in
[docs/api/courses.md](docs/api/courses.md).

When the backend is running, FastAPI also provides interactive documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Planned Stack for V1

- FastAPI
- PostgreSQL
- Docker
- Next.js

### Later

- Agentic tooling layer
- Redis

## V1 Scope

The first version focuses on the core academic planning engine:

- Course catalog
- Academic profile with completed/failed/in-progress courses
- User preferences and goals
- Course ratings
- Prerequisite and eligibility checks
- Deterministic course recommendations
- Rule-based recommendation explanations
- ECTS progress ring showing completed credits toward the overall degree target

The V1 progress ring is an ECTS-only progress indicator and does not perform full degree-audit validation.

Later versions will support multiple progress rings for requirement categories such as core courses and electives.

## Post-V1 / Pre-Production Scope

- Degree Constraints Module for validating program requirements, required courses, elective rules, ECTS requirements, category limits, thesis requirements, and graduation progress.

## Future Expansion: University Portal Data Sync

A read path for pulling a student's real grades/course history directly from the University of Crete's student portal has been prototyped, based on the `Options → University → Login → Scraper → Parser` pattern used by the open-source `unistudents-api` project. For UoC specifically, this means:

- Logging in through `sso.uoc.gr` (Apereo CAS: fetch a one-time `execution` token, then POST credentials).
- Fetching `eduportal.cict.uoc.gr`'s `GET /feign/student/grades/diploma` endpoint with the resulting session cookies.
- Flattening the nested JPA/Hibernate JSON response into a flat `Course` model based on the project's predefined one.

This would let a student's completed/passed courses be imported automatically instead of entered by hand, feeding directly into the eligibility and recommendation engine.

## Planned V1 Architecture

### Functional View

![image](docs/architecture/FunctionalView.png)

The diagram above showcases the planned modules for V1 of this project. As this is web based, a mobile UI will be planned for a future version. The main purpose of V1 is to build the foundations for the main project and to learn the stack better. However this is subject to change in the future.

### Module Dependency View

![image](docs/architecture/DependencyView.png)

This diagram showcases the dependencies between each module. The database arrow points only to the border of the logic tier to avoid bloat. It shows how each module read/writes on the DB.

## ER Diagram

![ER Diagram](docs/Database/ER.png)

The ER diagram above shows the current planned database schema for the project. It supports the course catalog, course ratings, user course attempts, recommendation-related data, and separate university/department modeling.

Prerequisites and suggested course relationships are modeled through dedicated relationship tables instead of raw fields on the course record.

## Prerequisite Rule Representation (V1)

The Academic Advisor recommendation and eligibility engine represents prerequisite rules as a nested collection, conceptually `list[list[int]]` (where each `int` is a course ID). Course codes are used below for readability.

The outer collection represents `AND` groups. Each inner collection represents an `OR` group. A prerequisite rule is satisfied when at least one course from every inner group has been completed.

Example:

```python
[
    ["HY240", "HY255"],
    ["HY118", "HY180"]
]
```

Interpretation:

```text
(HY240 OR HY255)
AND
(HY118 OR HY180)
```

Additional examples:

HY345:

```python
[
    ["HY240", "HY255"]
]
```

Meaning:

```text
HY240 OR HY255
```

HY380:

```python
[
    ["HY118", "HY280"],
    ["HY240"]
]
```

Meaning:

```text
(HY118 OR HY280)
AND
HY240
```

This structure was chosen as the V1 representation for prerequisite constraints and eligibility evaluation because university prerequisite rules naturally contain `AND` and `OR` relationships. The nested collection maps directly to the prerequisite graph design, is simple to validate and evaluate, and avoids large chains of hardcoded conditional logic.

### Design Reasoning

At first, prerequisite relationships seemed like a normal directed graph problem. For simple `OR` prerequisites, a plain graph works naturally. For example:

```text
HY100 -> HY252
HY150 -> HY252
```

This can be interpreted as `HY252` being reachable through either `HY100` or `HY150`, so the graph visually behaves like an `OR` condition.

However, this breaks down for mixed `AND`/`OR` prerequisite rules such as:

```text
(HY240 OR HY255) AND (HY118 OR HY180)
```

If all four courses are drawn as direct edges into `HY360`, the graph loses the distinction between:

- needing one course from each group
- needing all four courses
- needing any one of the four courses

This means plain graph edges alone are not expressive enough to preserve the real prerequisite logic.

The design therefore separates:

- course dependency relationships
- prerequisite logical rules

The V1 solution represents prerequisite logic as a nested collection:

- outer list = `AND` groups
- inner list = `OR` alternatives

Example:

```python
[
    ["HY240", "HY255"],
    ["HY118", "HY180"]
]
```

Meaning:

```text
(HY240 OR HY255) AND (HY118 OR HY180)
```

This idea came from trying to model the graph visually first, noticing that `OR` could be represented by multiple paths, but `AND` required a separate logical structure. The nested-list representation was chosen because it combines graph thinking, Boolean logic, and a simple data structure that can later be evaluated by the eligibility engine.

The same nested AND/OR representation may be reused for suggested-course rules, but suggested rules do not block eligibility. They only influence recommendation scoring and explanations.

## Eligibility Engine Status

The department-wide eligibility evaluation pipeline is implemented and tested:

- `get_passed_courses(user_id)` in `graph/service.py` — returns the set of course IDs the user has passed
- `build_department_prerequisite_adj_list()` in `graph/builder.py` — builds the full `{course_id: [[prereq_course_ids]]}` adjacency list by joining `Course_Prerequisite_Group` and `Course_Prerequisite` tables
- `get_course_prerequisites(course_id)` in `graph/service.py` — returns the AND-of-OR prerequisite groups for a single course from the adjacency list
- `get_all_course_eligibilities(user_id)` in `graph/service.py` — returns `{course_id: eligible}` for every course in the department
- `evaluate_prerequisite_rule(course_preq_rules, passed_courses)` in `eligibility/service.py` — evaluates a single course's prerequisite rules against the user's passed courses, returning `{"eligible": bool, "missing_groups": [[course_ids]]}` when prerequisites are not met
- The eligibility router (`eligibility/router.py`) wires these together: builds the adjacency list, looks up the course's prerequisite groups, fetches the user's passed courses, and delegates to `evaluate_prerequisite_rule`

Covered by tests in `tests/test_user_elibillity.py`.
