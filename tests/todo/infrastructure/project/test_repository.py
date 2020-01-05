import main
import datetime

from gumo.datastore.infrastructure.test_utils import DatastoreRepositoryMixinForTest
from todo.application.project.repository import ProjectRepository
from todo.domain.project import Project, ProjectKey, ProjectName


class TestProjectRepository(DatastoreRepositoryMixinForTest):
    KIND = ProjectKey.KIND
    repository: ProjectRepository = main.injector.get(ProjectRepository)

    def test_save(self):
        self.cleanup_entities()
        assert self.count_entities() == 0

        project = Project(
            key=ProjectKey.build_by_id(project_id=123),
            name=ProjectName("Project Name"),
            created_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
        )
        self.repository.save(project=project)
        assert self.count_entities() == 1

    def test_save_and_fetch(self):
        self.cleanup_entities()

        project = Project(
            key=ProjectKey.build_by_id(project_id=123),
            name=ProjectName("Project Name"),
            created_at=datetime.datetime(2019, 12, 1, tzinfo=datetime.timezone.utc),
        )
        self.repository.save(project=project)
        fetched_project = self.repository.fetch(key=project.key)
        assert fetched_project == project
