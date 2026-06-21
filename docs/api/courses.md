# Courses API

The courses API supports creating, listing, retrieving, and deleting course
records.

## Running the API

Start the backend from the repository root:

```bash
docker compose up --build backend
```

The API is then available at `http://localhost:8000`. Interactive OpenAPI
documentation is available at `http://localhost:8000/docs`.

## Data Storage

Course data is currently stored in memory. Records are lost whenever the
backend process restarts, and the storage is not suitable for concurrent or
production use.

## Course Model

| Field | Type | Constraints |
| --- | --- | --- |
| `id` | integer | At least `1`; must be unique |
| `department_id` | integer | At least `1` |
| `ects` | integer | Greater than `0` and less than `40` |
| `code` | string | 2-20 characters; format `AA-000` or `AAA-000` |
| `name` | string | 2-50 characters |
| `contact_email` | string or null | Valid email address; defaults to `null` |
| `difficulty_estimate` | number | Between `1` and `5`, inclusive |
| `workload_estimate` | number | Between `1` and `5`, inclusive |

Example request body:

```json
{
  "id": 1,
  "department_id": 1,
  "ects": 6,
  "code": "CS-101",
  "name": "Introduction to Computer Science",
  "contact_email": "lecturer@example.edu",
  "difficulty_estimate": 2.5,
  "workload_estimate": 3
}
```

## Course Prerequisite Model

| Field | Type | Constraints |
| --- | --- | --- |
| `id` | integer | Greater than `0`; must be unique |
| `course_id` | integer | Greater than `0`; must reference an existing course |
| `prerequisite_course_id` | integer | Greater than `0`; must reference an existing course |

## Course Suggested Model

| Field | Type | Constraints |
| --- | --- | --- |
| `id` | integer | Greater than `0`; must be unique |
| `course_id` | integer | Greater than `0`; must reference an existing course |
| `suggested_course_id` | integer | Greater than `0`; must reference an existing course |

## Endpoints

### Create a course

`POST /courses/add`

Creates a course from the JSON request body.

- `200 OK`: Returns the created course.
- `409 Conflict`: A course with the same `id` already exists.
- `422 Unprocessable Entity`: The request does not satisfy the course model.

### List courses

`GET /courses/`

Returns all courses currently stored in memory. The `courses` field is an empty
array when no courses have been created.

### Get a course by ID

`GET /courses/{course_id}`

Returns the course whose numeric `id` matches `course_id`.

- `200 OK`: Returns the matching course.
- `404 Not Found`: No course has the requested ID.
- `422 Unprocessable Entity`: `course_id` is not an integer.

### Get a course by code

`GET /courses/code/{course_code}`

Returns the course whose `code` matches `course_code`. Matching is
case-sensitive.

- `200 OK`: Returns the matching course.
- `404 Not Found`: No course has the requested code.

### Delete a course by ID

`DELETE /courses/{course_id}`

Deletes the course whose numeric `id` matches `course_id`.

- `200 OK`: The course was deleted.
- `404 Not Found`: No course has the requested ID.
- `422 Unprocessable Entity`: `course_id` is not an integer.

### Delete a course by code

`DELETE /courses/code/{course_code}`

Deletes the course whose `code` matches `course_code`.

- `200 OK`: The course was deleted.
- `404 Not Found`: No course has the requested code.

### Course prerequisites

`POST /course-prerequisites/`
`GET /course-prerequisites/`
`GET /course-prerequisites/{prerequisite_id}`
`PUT /course-prerequisites/{prerequisite_id}`
`DELETE /course-prerequisites/{prerequisite_id}`

Creates and manages normalized prerequisite relationships between courses.

### Course suggested

`POST /course-suggested/`
`GET /course-suggested/`
`GET /course-suggested/{suggested_id}`
`PUT /course-suggested/{suggested_id}`
`DELETE /course-suggested/{suggested_id}`

Creates and manages normalized suggested-course relationships between courses.

## Example

```bash
curl -X POST http://localhost:8000/courses/add \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 1,
    "department_id": 1,
    "ects": 8,
    "code": "HY-100",
    "name": "Intro to CS",
    "contact_email": "hy100@example.com",
    "difficulty_estimate": 5,
    "workload_estimate": 5
}'

curl -X POST http://localhost:8000/courses/add \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 2,
    "department_id": 1,
    "ects": 6,
    "code": "HY-101",
    "name": "Data Structures"
}'

curl -X POST http://localhost:8000/course-prerequisites/ \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 1,
    "course_id": 2,
    "prerequisite_course_id": 1
}'

curl -X POST http://localhost:8000/course-suggested/ \
  -H 'Content-Type: application/json' \
  -d '{
    "id": 1,
    "course_id": 1,
    "suggested_course_id": 2
}'

curl http://localhost:8000/courses/
curl http://localhost:8000/courses/1
curl http://localhost:8000/courses/code/HY-100
curl -X DELETE http://localhost:8000/courses/1
curl -X DELETE http://localhost:8000/courses/code/HY-100
```
