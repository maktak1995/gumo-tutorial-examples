import flask

from todo.presentation.task import TasksView, TaskDeleteView, TaskStatusUpdateView, TaskNameUpdateView


def register_views(blueprint: flask.Blueprint):
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