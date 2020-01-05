import flask
import os
from itertools import groupby

from gumo.core.injector import injector
from todo.bind import bind_todo
from todo.presentation import register_views

from todo.application.task.repository import TaskRepository
from todo.application.project.repository import ProjectRepository


injector.binder.install(bind_todo)

app = flask.Flask(__name__)
blueprint = flask.Blueprint("blueprint", __name__)
register_views(blueprint=blueprint)
app.register_blueprint(blueprint=blueprint)


@app.route('/')
def root():
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


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=os.environ.get("SERVER_PORT", 8080), debug=True)
