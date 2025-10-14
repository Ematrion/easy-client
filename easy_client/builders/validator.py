import json
import os
from pathlib import Path

import re
from collections import defaultdict, Counter

from typing import Any
from pydantic import HttpUrl, ValidationError
from uuid import UUID
from dateutil.parser import parse as parse_date

DataPoint = dict[str, Any]
TypedData = dict[str, set[str]]



POTENTIAL_IMPORTS = [
    "from pydantic import BaseModel",
    ", EmailStr",
    ", HttpUrl",
    "\nfrom uuid import UUID",
    "\nfrom typing import Any",
    "\nfrom enum import StrEnum",
    "\nfrom datetime import datetime"
]
IMPORTS_CHECKERS = {
    "BaseModel": [0],
    "EmailStr": [0,1],
    "HttpUrl": [0,2],
    "UUID": [3],
    "Any": [4],
    "StrEnum": [5],
    "datetime": [6]
}


# Simple rule for pydantic.EmailStr without import of the dedicated email-validator
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
IDENTIFIER_REGEX = re.compile(r'\W|^(?=\d)')


# ------------------------ #
# --- top file imports --- #
# ------------------------ #
def get_needed_imports(code_str: str) -> set[int]:
    needed_imports: set[int] = set()
    for checker, import_indices in IMPORTS_CHECKERS.items():
        if checker in code_str:
            needed_imports.update(import_indices)
    return needed_imports

def import_code(needed_imports: set[int]) -> str:
    import_code: list[str] = []
    for i in sorted(needed_imports):
        import_code.append(POTENTIAL_IMPORTS[i])
    return "".join(import_code)


# ----------------------------- #
# --- data structure checks --- #
# ----------------------------- #
def fields_with_dict(data: dict[str, Any]) -> list[str]:
    dict_fields = []
    for field, value in data.items():
        if isinstance(value, dict):
            dict_fields.append(field)
    return dict_fields

def fields_with_list(data: dict[str, Any]) -> list[str]:
    list_fields = []
    for field, value in data.items():
        if isinstance(value, list):
            list_fields.append(field)
    return list_fields


# ---------------------- #
# --- type inference --- #
# ---------------------- #
def is_uuid(value: str) -> bool:
    try:
        UUID(value)
        return True
    except ValueError:
        return False

def is_email(value: str) -> bool:
    return bool(EMAIL_REGEX.match(value))

def is_url(url: str) -> bool:
    try:
        HttpUrl(url)
        return True
    except ValidationError:
        return False

def is_datetime(value: str) -> bool:
    try:
        parse_date(value, fuzzy=False)
        return True
    except (ValueError, TypeError):
        return False

def subtype_of_string(s: str) -> str:
    if is_uuid(s):
        return "UUID"
    elif is_email(s):
        return "EmailStr" 
    elif is_url(s):
        return "HttpUrl"
    elif is_datetime(s):
        return "datetime"
    else:
        return "str"

def infer_type(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return subtype_of_string(value)
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "dict"
    elif value is None:
        return "None"
    else:
        msg = f"Unsupported type for data: {value} - {type(value)}"
        raise ValueError(msg)


# ----------------------- #
# --- data processor  --- #
# ----------------------- #
def summary_item(items: list[DataPoint]) -> dict[str, list[Any]]:
    field_values: dict[str, list[Any]] = defaultdict(list)
    for item in items:
        for field, value in item.items():
            field_values[field].append(value)
    return field_values

def enums_from_values(values: list[str | None], max_enum: int = 10, min_freq: float = 0.01, threshold: float = 0.95) -> tuple[bool, list[str | None]]:
    is_enum = False
    value_counts = Counter(values)
    total_count = len(values)
    enums = [value for value, count in value_counts.most_common(max_enum) if count / total_count >= min_freq]
    if sum([count for count in [value_counts[enum_value] for enum_value in enums]]) / total_count >= threshold and len(enums) > 1:
        is_enum = True
    else:
        enums = []
    return is_enum, enums

def relevant_types(types: list[str], threshold: float = 0.05) -> set[str]:
    frequencies = Counter(types)
    total_count = len(types)
    types = [t for t, count in frequencies.items() if count / total_count >= threshold]
    return set(types)

def split_atomic_values(values: list[Any]) -> tuple[list[Any], list[dict | list]]:
    atomic_values = []
    non_atomic_values = []
    for v in values:
        if isinstance(v, (list, dict)):
            non_atomic_values.append(v)
        else:
            atomic_values.append(v)
    return atomic_values, non_atomic_values

def join_list_values(items: list[Any]) -> list[Any]:
    joined_items = []
    for item in items:
        if isinstance(item, list):
            joined_items.extend(item)
        else:
            joined_items.append(item)
    return joined_items

def joind_dict_values(items: list[Any]) -> list[dict]:
    joined_items = []
    for item in items:
        if isinstance(item, dict):
            joined_items.append(item)
    return joined_items


# ----------------------- #
# --- Code generation --- #
# ----------------------- #
def add_imports_to_file(code_str: str) -> str:
    needed_imports = get_needed_imports(code_str)
    import_code_str = import_code(needed_imports)
    full_code = import_code_str + "\n\n" + code_str
    return full_code

def safe_enum_name(value: str) -> str:
    return IDENTIFIER_REGEX.sub('_', value).upper()

def enum_code_string(class_name: str, field: str, enum_values: list[str]) -> str:
    enum_code = [f"class {class_name}(StrEnum):"]
    for value in enum_values:
        enum_code.append(f"\t{safe_enum_name(value)} = '{value}'")
    return "\n".join(enum_code)

def atomic_model_code_string(class_name: str, field_infos: TypedData) -> str:
    class_code = ["class " + class_name + "(BaseModel):"]
    for field, types in field_infos.items():
        type_str = " | ".join(sorted(types))
        class_code.append(f"\t{field}: {type_str}")
    return "\n".join(class_code)

def typehint_of_list_field(list_items: list[Any], new_class_name: str, code_lines: list[str]) -> str:
    field_types: set[str] = set()
    atomic_data, non_atomic_data = split_atomic_values(list_items)
    data_items = join_list_values(non_atomic_data)
    atomic_types = relevant_types([infer_type(v) for v in atomic_data])
    if atomic_types:
        field_types.update(atomic_types)
    if data_items:
        field_types.add(new_class_name)
        nested_code = infer_schema_from_data(data_items, new_class_name)
        code_lines.append(nested_code)
    return "list[" + " | ".join(field_types) + "]"

# ----------------------------------- #
# --- Data Aware Schema Inference --- #
# ----------------------------------- #
def infer_schema_from_data(items: list[DataPoint], class_name: str, build_enums: bool = True, max_enum: int = 10, min_freq: float = 0.01, threshold: float = 0.95) -> str:
    code_lines: list[str] = []
    fields_infos: TypedData = {}
    
    if len(items) == 0:
        raise ValueError("No items provided for schema inference")
    
    # find nested structures
    field_of_list = fields_with_list(items[0])
    field_of_dict = fields_with_dict(items[0])

    # deal with list fields
    while field_of_list:
        field = field_of_list.pop()
        new_class_name = f"{field.capitalize()}Items"
        list_items = [item[field] for item in items if field in item and isinstance(item[field], list)]
        fields_infos[field] = {typehint_of_list_field(list_items, new_class_name, code_lines)}

    # deals with dict fields
    while field_of_dict:
        field = field_of_dict.pop()
        new_class_name = f"{field.capitalize()}Model"
        dict_items = [item[field] for item in items if field in item and isinstance(item[field], dict)]
        all_items = joind_dict_values(dict_items)
        nested_code = infer_schema_from_data(all_items, new_class_name, build_enums, max_enum, min_freq, threshold)
        code_lines.append(nested_code)
        fields_infos[field] = {new_class_name}
    
    if not field_of_dict and not field_of_list:
        one_big_item: dict[str, list[Any]] = summary_item(items)
        for field, values in one_big_item.items():
            types = relevant_types([infer_type(value) for value in values])
            if "str" in types and build_enums:
                candidates = [v if isinstance(v, str) else None for v in values]
                is_enum, enum_values = enums_from_values(candidates, max_enum, min_freq, threshold)
                if is_enum:
                    enum_class_name = f"{class_name}{field.capitalize()}"
                    enum_code = enum_code_string(enum_class_name, field, enum_values) # type: ignore
                    code_lines.append(enum_code)
                    types.remove("str")
                    types.add(enum_class_name)
            fields_infos[field] = types
    
    class_code = atomic_model_code_string(class_name, fields_infos)
    code_lines.append(class_code)

    code_str = "\n\n".join(code_lines)
    return code_str


def build_schema_file(json_path: str | Path, output_path: str | Path, enums: bool = True, max_enum: int = 10, min_freq: float = 0.01, threshold: float = 0.95) -> None:
    """
    Infers a Pydantic model schema from a JSON file and writes it to a Python file.

    Args:
        json_path (str): Path to the input JSON file (should be a list of dictionaries).
        output_path (str, optional): Output .py file path. If not provided, defaults to same dir as .json with .py extension.
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Expected a JSON file containing a list of dictionaries")

    # Infer class name from file name
    base_name = os.path.basename(json_path)
    class_name = os.path.splitext(base_name)[0]
    class_name = class_name[:1].upper() + class_name[1:]  # Capitalize first letter

    # Infer schema and add imports
    model_code = infer_schema_from_data(data, class_name, build_enums=enums, max_enum=max_enum, min_freq=min_freq, threshold=threshold)
    full_code = add_imports_to_file(model_code)

    # Determine output file
    if output_path is None:
        output_path = os.path.splitext(json_path)[0] + ".py"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_code)




'''

Limitations:

- Does not support Annotated types 
- Dynamic keys dictionaries like: "user_stats": {"user_123": {...},"user_456": {...}}
- Any is never inferred


Improvements
- Better enum detection (Jaccard similarity ?)
- Naming of fields and classes (Upper, Capitalize, slugify, need of parentclass or not ...)
- Configuration for thresholds, max enum values, min frequency


'''