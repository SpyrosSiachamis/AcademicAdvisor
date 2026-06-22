# Academic Advisor

An academic decision-support system that recommends courses and academic paths based on completed courses, ratings, workload tolerance, interests, prerequisites, degree constraints, and career goals.

## Current Status

Early-stage development. The project currently contains a containerized FastAPI backend used for experimenting with API structure, validation, and backend architecture before implementing the main recommendation system. Students already use AI manually to research courses and plan their academic path. AcademicAdvisor turns that into a structured, data-driven advising system.

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

The Academic Advisor recommendation and eligibility engine represents prerequisite rules as a nested collection, conceptually `list[list[str]]`.

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
