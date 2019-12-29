import typing
from gumo.datastore.infrastructure import DatastoreRepositoryMixin
from gumo.datastore.infrastructure import DatastoreEntity

from todo.application.project.repository import ProjectRepository
from todo.domain.project import Project, ProjectKey, ProjectName
from . import ProjectDataModel


class DatastoreProjectRepository(DatastoreRepositoryMixin, ProjectRepository):
    def save(self, project: Project):
        model = ProjectDataModel(
            key=self.to_datastore_key(entity_key=project.key),
            name=project.name.value,
            created_at=project.created_at,
        )
        doc = model.to_datastore_entity()
        self.datastore_client.put(doc)

    def delete(self, key: ProjectKey):
        datastore_key = self.to_datastore_key(entity_key=key)
        self.datastore_client.delete(datastore_key)

    def fetch_no_raise(self, key: ProjectKey) -> typing.Optional[Project]:
        datastore_key = self.to_datastore_key(entity_key=key)
        doc = self.datastore_client.get(key=datastore_key)
        if doc is None:
            return None

        return self._to_domain_entity(doc=doc)

    def _to_domain_entity(self, doc: DatastoreEntity) -> Project:
        model = ProjectDataModel.from_datastore_entity(doc=doc)
        return Project(
            key=ProjectKey.build_from_key(key=self.to_entity_key(datastore_key=model.key)),
            name=ProjectName(model.name),
            created_at=model.created_at,
        )

    def fetch_list(self) -> typing.List[Project]:
        query = self.datastore_client.query(kind=ProjectKey.KIND)
        tasks = [
            self._to_domain_entity(doc=doc)
            for doc in query.fetch()
        ]

        return tasks
