import flask.views

from gumo.core.injector import injector
from todo.application.project.repository import ProjectRepository
from todo.application.project import ProjectCreateService


class ProjectsView(flask.views.MethodView):
    def get(self):
        repository: ProjectRepository = injector.get(ProjectRepository)
        projects = repository.fetch_list()

        return flask.render_template("todo/projects.html", projects=projects)

    def post(self):
        project_name: str = flask.request.form.get("project_name", "")
        service: ProjectCreateService = injector.get(ProjectCreateService)
        service.execute(project_name=project_name)

        return flask.redirect("/projects")