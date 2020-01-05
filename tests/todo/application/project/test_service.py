import main

from gumo.datastore.infrastructure.test_utils import DatastoreRepositoryMixinForTest
from todo.application.project.repository import ProjectRepository
from todo.application.project import ProjectCreateService
from todo.domain.project import ProjectKey


class TestProjectService(DatastoreRepositoryMixinForTest):
    KIND = ProjectKey.KIND
    repository: ProjectRepository = main.injector.get(ProjectRepository)

    def test_create_service(self):
        self.cleanup_entities()
        self.cleanup_entities()
        assert self.count_entities() == 0

        project_name = "ProjectName"
        service = main.injector.get(ProjectCreateService)
        service.execute(project_name=project_name)

        assert self.count_entities() == 1
