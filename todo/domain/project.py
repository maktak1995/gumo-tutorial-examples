import dataclasses
import datetime
import re

from gumo.core import EntityKey
from gumo.core import EntityKeyFactory
from gumo.core import NoneKey
from gumo.core import EntityKeyGenerator
from dataclass_type_validator import dataclass_type_validator


@dataclasses.dataclass(frozen=True)
class ProjectKey(EntityKey):
    KIND = "Project"
    key_generator = EntityKeyGenerator(
        key_generate_style=EntityKeyGenerator.KeyGenerateStyle.INT
    )

    @classmethod
    def build_by_id(cls, project_id: int) -> "ProjectKey":
        if isinstance(project_id, str) and project_id.isdigit():
            project_id = int(project_id)
        return cls(_kind=cls.KIND, _name=project_id, _parent=NoneKey.get_instance(),)

    @classmethod
    def build_from_key(cls, key: EntityKey) -> "ProjectKey":
        if key.has_parent():
            raise ValueError(f"key must not have parent: {key.key_literal()}")
        if key.kind() != cls.KIND:
            raise ValueError(f"key.KIND must equal to {cls.KIND}: {key.key_literal()}")

        return cls.build_by_id(project_id=key.name())

    @classmethod
    def build_for_new(cls) -> "ProjectKey":
        incomplete_key = EntityKeyFactory().build_incomplete_key(cls.KIND)
        entity_key = cls.key_generator.generate(incomplete_key=incomplete_key)
        return cls.build_from_key(entity_key)

    @property
    def project_id(self) -> int:
        return self.name()


@dataclasses.dataclass(frozen=True)
class ProjectName:
    value: str

    MAX_LENGTH = 100

    def __post_init__(self):
        dataclass_type_validator(self)

        if len(self.value) == 0:
            raise ValueError(f"ProjectName must be present.")

        if len(self.value) > self.MAX_LENGTH:
            raise ValueError(f"ProjectName is too long (maximum length is {self.MAX_LENGTH})")

        if re.fullmatch(r'\s', self.value):
            raise ValueError(f"Only space character cannot be used as ProjectName")


@dataclasses.dataclass(frozen=True)
class Project:
    key: ProjectKey
    name: ProjectName
    created_at: datetime.datetime

    def __post_init__(self):
        dataclass_type_validator(self)