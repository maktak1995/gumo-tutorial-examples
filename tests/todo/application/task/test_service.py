import main

from gumo.datastore.infrastructure.test_utils import DatastoreRepositoryMixinForTest
from todo.application.task.repository import TaskRepository
from todo.application.task import TaskCreateService, TaskUpdateService
from todo.domain import TaskKey


class TestTaskService(DatastoreRepositoryMixinForTest):
    KIND = TaskKey.KIND
    repository: TaskRepository = main.injector.get(TaskRepository)

    def test_create_service(self):
        self.cleanup_entities()
        assert self.count_entities() == 0

        task_name = "TaskName"
        service = main.injector.get(TaskCreateService)
        service.execute(task_name=task_name)

        assert self.count_entities() == 1

    def test_update_service(self):
        self.cleanup_entities()
        assert self.count_entities() == 0

        task_name = "TaskName"
        create_service = main.injector.get(TaskCreateService)
        task = create_service.execute(task_name=task_name)

        update_service = main.injector.get(TaskUpdateService)
        updated_task = update_service.execute(key=task.key, finished=True)

        assert updated_task.is_finished
