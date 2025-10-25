from dataclasses import dataclass
from typing import Union, Any, get_args, get_origin
from types import UnionType
from enum import Enum

from pydantic import BaseModel, Field, EmailStr, HttpUrl
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined


TYPE_MAPPING = {
    # python built-in types
    "int": "Integer",
    "float": "Float",
    "decimal": "Numeric",
    "str": "String",
    "bool": "Boolean",
    "list": "JSON",
    "dict": "JSON",
    "set": "JSON",
    "bytes": "LargeBinary",
    
    # enums
    "Enum": "Enum",
    "StrEnum": "Enum",
    
    # BaseModel are handled as relathionships i.e foreign keys
    "BaseModel": "Integer",
    
    # datetime types
    "datetime": "DateTime",
    "datetime.datetime": "DateTime",
    "date": "Date",
    "datetime.date": "Date",
    "time": "Time",
    "datetime.time": "Time",
    
    # pydantic validate types
    "UUID": "UUID",
    "pydantic.UUID": "UUID",
    "EmailStr": "String",
    "pydantic.EmailStr": "String",
    "AnyUrl": "String",
    "pydantic.AnyUrl": "String",
    "HttpUrl": "String",
    "pydantic.HttpUrl": "String",
    
    # Constrained Types
    "constr": "String",
    "conint": "Integer",
    "PositiveInt": "Integer",
    "NegativeInt": "Integer",
    
    # JSON
    "Json": "JSON",
    "pydantic.Json": "JSON",
    
    # Fallback
    "default_type": "Text"
}


@dataclass
class ColumnInfos:
    name: str | None
    type_: str 
    
    # keys
    primary_key: bool = False
    foreign_key: str | None = None

    # constraints
    nullable: bool = True
    unique: bool = False
    default: Any = None
    server_default: Any = None
    
    # metal build from pydantic field informations
    comment: str | None = None
    doc: str | None = None
    
    # Usefull for column name matchin sql protected words
    quote: bool = False
    
    # No usage
    #system: bool = False
    #autoincrement: bool = False


# --- Column args --- #
def _assert_type(field: FieldInfo) -> str:
    anno = field.annotation
    origin = get_origin(anno)
    args = get_args(anno)
    type_ = "default_type"
    
    if origin in {Union, UnionType}:
        real_types = [a_type for a_type in args if a_type is not type(None)]
        if len(real_types) == 1:
            rtype = real_types[0]
            type_ = rtype.__name__ if hasattr(rtype, "__name__") else str(rtype)
        else:
            msg = "Multiple types in Union are not supported for database columns"
            raise ValueError(msg)
    elif not origin:
        if anno is None:
            msg = "Field annotation cannot be NoneType"
            raise ValueError(msg)
        elif issubclass(anno, BaseModel):
            msg = "Field annotation cannot be a nested BaseModel"
            raise ValueError(msg)
        elif issubclass(anno, Enum):
            type_ = f"Enum({anno.__name__})"
            # Not in mapping
            return type_ 
        else:
            type_ = anno.__name__ if hasattr(anno, "__name__") else str(anno)
        
    return TYPE_MAPPING[type_]

def _default(field: FieldInfo) -> Any:
    if field.default is not PydanticUndefined:
        return field.default
    # ignore the case of default_factory
    return None

def _server_default(field: FieldInfo) -> Any:
    extras = field.json_schema_extra or {}
    server_default = extras.get("server_default", None)
    return server_default

def _is_required(field: FieldInfo) -> bool:
    return field.is_required()

def _is_unique(field: FieldInfo) -> bool:
    extras = field.json_schema_extra or {}
    return bool(extras.get("unique", False))

def _is_primary_key(field: FieldInfo) -> bool:
    extras = field.json_schema_extra or {}
    return bool(extras.get("primary_key", False))

def _is_foreign_key(field: FieldInfo) -> str | None:
    extras = field.json_schema_extra or {}
    fk = extras.get("foreign_key", None)
    return str(fk) if fk else None
    
def _description(field: FieldInfo) -> str | None:
    desc = ""
    if field.title:
        desc += "Title: " + field.title
    if field.description:
        desc += "\nDescription:\n" + field.description
    if field.examples:
        desc += "\nExamples:\n" + "\n".join([str(e) for e in field.examples])
    return desc if desc else None        

    
def adapt_enum_column_infos(infos: ColumnInfos) -> ColumnInfos:
    assert "Enum" in infos.type_
    infos.default = infos.default.value if infos.default else None
    infos.server_default = infos.server_default.value if infos.server_default else None
    return infos

def extract_field_infos(name: str, field: FieldInfo) -> ColumnInfos:
    infos = ColumnInfos(
        name=name,
        type_=_assert_type(field),
        primary_key=_is_primary_key(field),
        foreign_key=_is_foreign_key(field),
        
        nullable=not _is_required(field),
        unique=_is_unique(field),
        
        default=_default(field),
        server_default=_server_default(field),
        
        comment=_description(field),
        doc=_description(field),
        quote=False
    )
    if infos.type_ == "Enum":
        infos= adapt_enum_column_infos(infos)
    return infos
    
def column_code_line(infos: ColumnInfos) -> str:
    code_line = f"Column(\"{infos.name}\", {infos.type_}"
    if infos.default:
        code_line += f", default={infos.default}"
    if infos.server_default:
        code_line += f", server_default=text(\"{infos.server_default}\")"
    if infos.primary_key:
        code_line += ", primary_key=True"
    if infos.foreign_key:
        code_line += f", ForeignKey('{infos.foreign_key}')"
    if not infos.nullable:
        code_line += ", nullable=False"
    if infos.unique:
        code_line += ", unique=True"
    if infos.comment:
        code_line += f", comment=\"\"\"{infos.comment}\"\"\""
    code_line += ")"    
    
    return code_line

def table_code_lines(model: type[BaseModel]) -> list[str]:
    lines = [f"{model.__name__.lower()} = Table(",f"\t\"{model.__name__.lower()}\",", "\tmetadata,"]
    for field_name, model_field in model.model_fields.items():
        infos = extract_field_infos(field_name, model_field)
        line = "\t" + column_code_line(infos) + ","
        lines.append(line)
    lines.append(")")
    return lines
    
if __name__ == "__main__":
    class Role(str, Enum):
        admin = "admin"
        user = "user"

    class Address(BaseModel):
        city: str
        zip: str

    class UserModel(BaseModel):
        id: int = Field(..., json_schema_extra={"primary_key": True})
        username: str = Field(..., max_length=50, json_schema_extra={"unique": True, "index": True})
        email: EmailStr = Field(..., json_schema_extra={"unique": True})
        age: int = Field(default=18,)
        is_active: bool = True
        role: Role = Role.user
        profile_url: HttpUrl | None = None
        settings: dict = Field(default_factory=dict)
        created_at: str = Field(..., description="ISO timestamp", json_schema_extra={"server_default": "NOW()"})
        referrer_id: int | None = Field(None, json_schema_extra={"foreign_key": "users.id"})
        metadata: dict | None = None  # tests JSON, nullable
        backup_codes: list[str] = []  # unsupported type?

    for field_name, model_field in UserModel.model_fields.items():
        print(column_code_line(extract_field_infos(field_name, model_field)))
        
    print("\n".join(table_code_lines(UserModel)))
        
    from sqlalchemy import MetaData, Table, Column, Integer, String
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.dialects import sqlite

    metadata = MetaData()

    users = Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("username", String, nullable=False, unique=True),
    )

    # Generate raw SQL for the SQLite dialect
    sql = str(CreateTable(users).compile(dialect=sqlite.dialect()))
    print(sql)
