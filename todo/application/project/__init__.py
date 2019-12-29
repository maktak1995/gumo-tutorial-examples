import datetime

from injector import inject

from todo.application.project.repository import ProjectRepository
from todo.domain.project import Project, ProjectKey, ProjectName


class ProjectCreateService:
    @inject
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository

    def execute(self, project_name: str) -> Project:
        now = datetime.datetime.utcnow().astimezone(tz=datetime.timezone.utc)
        project = Project(
            key=ProjectKey.build_for_new(),
            name=ProjectName(project_name),
            created_at=now,
        )

        self.project_repository.save(project=project)

        return project
