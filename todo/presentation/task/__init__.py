import flask.views

from gumo.core.injector import injector
from todo.application.task.repository import TaskRepository
from todo.application.project.repository import ProjectRepository
from todo.application.task import TaskCreateService, TaskStatusUpdateService,\
     TaskNameUpdateService, TaskProjectUpdateService
from todo.domain.task import TaskKey


class TasksView(flask.views.MethodView):
    def get(self):
        task_repository: TaskRepository = injector.get(TaskRepository)
        project_repository: ProjectRepository = injector.get(ProjectRepository)
        tasks = task_repository.fetch_list()
        projects = project_repository.fetch_list()

        return flask.render_template("todo/tasks.html", tasks=tasks, projects=projects)

    def post(self):
        task_name: str = flask.request.form.get("task_name", "")
        service: TaskCreateService = injector.get(TaskCreateService)
        service.execute(task_name=task_name)

        return flask.redirect("/tasks")


class TaskDeleteView(flask.views.MethodView):
    def post(self, task_id):
        task_key = TaskKey.build_by_id(task_id=task_id)
        repository: TaskRepository = injector.get(TaskRepository)
        repository.delete(key=task_key)

        return flask.redirect("/tasks")


class TaskStatusUpdateView(flask.views.MethodView):
    def post(self, task_id):
        task_key = TaskKey.build_by_id(task_id=task_id)
        finished = flask.request.form.get("finished", "false") == "true"
        redirect_to = flask.request.form.get("redirectTo", "/tasks")
        if not redirect_to.startswith("/"):
            redirect_to = "/tasks"

        service: TaskStatusUpdateService = injector.get(TaskStatusUpdateService)
        service.execute(key=task_key, finished=finished)

        return flask.redirect(redirect_to)


class TaskNameUpdateView(flask.views.MethodView):
    def post(self, task_id):
        task_key = TaskKey.build_by_id(task_id=task_id)
        task_name: str = flask.request.form.get("new_task_name", "")
        service: TaskNameUpdateService = injector.get(TaskNameUpdateService)
        service.execute(key=task_key, task_name=task_name)

        return flask.redirect("/tasks")


class TaskProjectUpdateView(flask.views.MethodView):
    def post(self, task_id):
        task_key = TaskKey.build_by_id(task_id=task_id)
        project_id: str = flask.request.form.get("project_id", "")
        service: TaskProjectUpdateService = injector.get(TaskProjectUpdateService)
        service.execute(key=task_key, project_id=project_id)

        return flask.redirect("/tasks")
