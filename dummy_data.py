from Backend.schemas import Task

### Pydantic Task Data for API
dummy_data: list[Task] = [
    Task(
        id=1,
        name="Write project proposal",
        description="Draft the initial proposal document outlining goals, timeline, and budget for the new project.",
        is_completed=True,
    ),
    Task(
        id=2,
        name="Review pull requests",
        description="Go through pending pull requests from the team and leave feedback or approve them.",
        is_completed=False,
    ),
    Task(
        id=3,
        name="Update documentation",
        description="Revise the API documentation to reflect the latest endpoint changes.",
        is_completed=False,
    ),
]


### JSON Dummy Tasks
dummy_tasks_key = [
    {
        "id": 1,
        "name": "Write project proposal",
        "description": "Draft the initial proposal document outlining goals, timeline, and budget for the new project.",
        "is_completed": True,
    },
    {
        "id": 2,
        "name": "Update documentation",
        "description": "Revise the API documentation to reflect the latest endpoint changes.",
        "is_completed": False,
    },
    {
        "id": 3,
        "name": "Review pull requests",
        "description": "Go through pending pull requests from the team and leave feedback or approve them.",
        "is_completed": False,
    },
    {
        "id": 4,
        "name": "Review pull requests",
        "description": "Go through pending pull requests from the team and leave feedback or approve them.",
        "is_completed": True,
    },
]