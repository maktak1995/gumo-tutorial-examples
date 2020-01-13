import flask
import flask.views
from itertools import groupby


from todo.presentation.task import TasksView, TaskDeleteView, \
    TaskStatusUpdateView, TaskNameUpdateView, TaskProjectUpdateView
from todo.presentation.project import ProjectsView


from gumo.core.injector import injector
from todo.application.task.repository import TaskRepository
from todo.application.project.repository import ProjectRepository


class RootView(flask.views.MethodView):
    def get(self):
        task_repository: TaskRepository = injector.get(TaskRepository)
        project_repository: ProjectRepository = injector.get(ProjectRepository)
        tasks = task_repository.fetch_list()

        sorted_tasks = []
        for key, tasks in groupby(tasks, key=lambda task: task.project_key):
            project = project_repository.fetch(key) if key is not None else key
            if project is not None:
                project_name = project.name.value
            else:
                project_name = 'プロジェクト未指定'

            grouped_tasks = []
            for task in tasks:
                grouped_tasks.append(task)

            sorted_tasks.append({'project_name': project_name, 'tasks': grouped_tasks})

        sorted_tasks.sort(key=lambda task: task['project_name'], reverse=True)

        return flask.render_template('index.html', sorted_tasks=sorted_tasks)


def register_views(blueprint: flask.Blueprint):
    blueprint.add_url_rule(
        rule="/",
        view_func=RootView.as_view("index"),
        methods=["GET"]
    )

    blueprint.add_url_rule(
        rule="/tasks",
        view_func=TasksView.as_view("tasks"),
        methods=["GET", "POST"]
    )

    blueprint.add_url_rule(
        rule="/tasks/<task_id>/delete",
        view_func=TaskDeleteView.as_view("tasks/delete"),
        methods=["POST"]
    )

    blueprint.add_url_rule(
        rule="/tasks/<task_id>/update/status",
        view_func=TaskStatusUpdateView.as_view("tasks/update/status"),
        methods=["POST"]
    )

    blueprint.add_url_rule(
        rule="/tasks/<task_id>/update/name",
        view_func=TaskNameUpdateView.as_view("tasks/update/name"),
        methods=["POST"]
    )

    blueprint.add_url_rule(
        rule="/tasks/<task_id>/update/project",
        view_func=TaskProjectUpdateView.as_view("tasks/update/project"),
        methods=["POST"]
    )

    blueprint.add_url_rule(
        rule="/projects",
        view_func=ProjectsView.as_view("projects"),
        methods=["GET", "POST"]
    )
