import datetime

from injector import inject

from todo.application.task.repository import TaskRepository
from todo.domain.task import Task, TaskKey, TaskName
from todo.domain.project import ProjectKey


class TaskCreateService:
    @inject
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, task_name: str) -> Task:
        now = datetime.datetime.utcnow().astimezone(tz=datetime.timezone.utc)
        task = Task(
            key=TaskKey.build_for_new(),
            name=TaskName(task_name),
            project_key=None,
            finished_at=None,
            created_at=now,
            updated_at=now,
        )

        self.task_repository.save(task=task)

        return task


class TaskStatusUpdateService:
    @inject
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, key: TaskKey, finished: bool) -> "Task":
        task = self.task_repository.fetch(key=key)

        if finished:
            modified_task = task.to_finished_now()
        else:
            modified_task = task.to_canceled_finish()

        self.task_repository.save(task=modified_task)

        return modified_task


class TaskNameUpdateService:
    @inject
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, key: TaskKey, task_name: str) -> "Task":
        task = self.task_repository.fetch(key=key)
        modified_task = task.to_changed_task_name(task_name=TaskName(task_name))

        self.task_repository.save(task=modified_task)

        return modified_task


class TaskProjectUpdateService:
    @inject
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def execute(self, key: TaskKey, project_id: str) -> "Task":
        task = self.task_repository.fetch(key=key)

        if project_id != "None":
            project_key = ProjectKey.build_by_id(int(project_id))
        else:
            project_key = None

        modified_task = task.with_project_key(project_key=project_key)

        self.task_repository.save(task=modified_task)

        return modified_task
