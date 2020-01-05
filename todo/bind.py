from todo.application.task.repository import TaskRepository
from todo.infrastructure.task.repository import DatastoreTaskRepository
from todo.application.project.repository import ProjectRepository
from todo.infrastructure.project.repository import DatastoreProjectRepository


def bind_todo(binder):
    binder.bind(TaskRepository, to=DatastoreTaskRepository)
    binder.bind(ProjectRepository, to=DatastoreProjectRepository)
