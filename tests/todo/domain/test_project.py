import datetime
import pytest

from gumo.core import EntityKeyFactory
from dataclass_type_validator import TypeValidationError

from todo.domain.project import Project, ProjectKey, ProjectName


class TestProjectKey:
    def test_equal(self):
        key1 = ProjectKey.build_by_id(project_id=1)
        key2 = ProjectKey.build_by_id(project_id=1)
        assert key1 == key2
        assert key1.task_id == 1

    def test_build_from_key(self):
        entity_key = EntityKeyFactory().build(kind="Project", name=1,)
        project_key = ProjectKey.build_from_key(key=entity_key)
        assert entity_key != project_key
        assert entity_key.key_literal() == project_key.key_literal()


class TestProject:
    def test_build_successful(self):
        project = Project(
            key=ProjectKey.build_by_id(project_id=1),
            name=ProjectName("Project Name"),
            created_at=datetime.datetime(
                2019, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )
        assert isinstance(project, Project)

    def test_build_failure(self):
        with pytest.raises(expected_exception=TypeValidationError):
            Project(
                key=ProjectKey.build_by_id(project_id=1),
                name='project name',
                created_at=datetime.datetime(
                    2019, 12, 1, 0, 0, 0, tzinfo=datetime.timezone.utc
                ),
            )