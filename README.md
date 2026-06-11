# Academic Advisor

An academic decision-support system that recommends courses and academic paths based on completed courses, ratings, workload tolerance, interests, prerequisites, degree constraints, and career goals.

## Current Status

Early-stage development. The project currently contains a containerized FastAPI backend used for experimenting with API structure, validation, and backend architecture before implementing the main recommendation system. Students already use AI manually to research courses and plan their academic path. AcademicAdvisor turns that into a structured, data-driven advising system.

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

## Planned V1 Architecture

### Functional View

![image](docs/Architecture/FunctionalView.png)

The diagram above showcases the planned modules for V1 of this project. As this is web based, a mobile UI will be planned for a future version. The main purpose of V1 is to build the foundations for the main project and to learn the stack better. However this is subject to change in the future.

### Module Dependency View

![image](docs/Architecture/DependencyView.png)

This diagram showcases the dependencies between each module. The database arrow points only to the border of the logic tier to avoid bloat. It shows how each module read/writes on the DB.
