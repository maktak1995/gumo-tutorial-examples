import main

from gumo.datastore.infrastructure.test_utils import DatastoreRepositoryMixinForTest
from todo.application.task.repository import TaskRepository
from todo.application.task import TaskCreateService, TaskStatusUpdateService, TaskNameUpdateService
from todo.domain.task import TaskKey


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

    def test_status_update_service(self):
        task_name = "TaskName"
        create_service = main.injector.get(TaskCreateService)
        task = create_service.execute(task_name=task_name)

        status_update_service = main.injector.get(TaskStatusUpdateService)
        updated_task = status_update_service.execute(key=task.key, finished=True)

        assert updated_task.is_finished

    def test_task_name_update_service(self):
        task_name = "TaskName"
        create_service = main.injector.get(TaskCreateService)
        task = create_service.execute(task_name=task_name)

        task_name_update_service = main.injector.get(TaskNameUpdateService)
        updated_task = task_name_update_service.execute(key=task.key, task_name="NewTaskName")

        assert updated_task.name.value == "NewTaskName"
