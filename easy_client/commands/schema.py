from pathlib import Path
from types import ModuleType

import pydantic
import enum
import networkx as nx
import matplotlib.pyplot as plt

from easy_client.utils import DynamicLoader, get_api_name, get_api_endpoints


def get_BaseModels(module: ModuleType):
    basemodels = []
    content = getattr(module, "__all__")
    for attr_name in content:
        attr = getattr(module, attr_name)
        if issubclass(attr, pydantic.BaseModel):
            basemodels.append(attr)
    return basemodels

def get_StrEnums(module: ModuleType):
    enum_types = []
    content = getattr(module, "__all__")
    for attr_name in content:
        attr = getattr(module, attr_name)
        if issubclass(attr, enum.Enum):
            enum_types.append(attr)
    return enum_types

def build_models_graph(models: list[type[pydantic.BaseModel]]):
    graph = {}
    for model in models:
        fields = model.model_fields
        dependencies = set()
        for field in fields.values():
            field_type = field.annotation
            if isinstance(field_type, type) and issubclass(field_type, pydantic.BaseModel):
                dependencies.add(field_type.__name__)
        graph[model.__name__] = dependencies
    return graph

def build_dependancy_graph(models: list[type[pydantic.BaseModel]]) -> nx.DiGraph:
    dependencies = build_models_graph(models)
    dg = nx.DiGraph()
    for model, deps in dependencies.items():
        dg.add_node(model)
        for dep in deps:
            dg.add_edge(model, dep)
    return dg

def nodes_ordering(graph: nx.DiGraph):
    all_nodes = list(graph.nodes)
    ordered_nodes: list[str] = []
    while all_nodes:
        node = all_nodes.pop(0)
        successors = list(graph.successors(node))
        if all(succ in ordered_nodes for succ in successors): # check this
            ordered_nodes.append(node)
        else:
            all_nodes.append(node)
    return ordered_nodes

def pydantic_to_alchemy(model: type[pydantic.BaseModel]) -> str:
    ...

def schema(root: Path | None = None):
    print("Create Schema models for collected data...")
    if root is None:
        root = Path.cwd()
        
    api_name = get_api_name()
    endpoints = get_api_endpoints()
    
    # --- load model class --- #
    loader = DynamicLoader(api_name=api_name, api_root=root)
    validate_module = loader.load_validate_module()
    basemodels = get_BaseModels(validate_module)
    enums = get_StrEnums(validate_module)
    
    for model in basemodels:
        print(f"\nModel: {model.__name__}")

    for enum in enums:
        print(f"\nEnum: {enum.__name__}")

    graph = build_models_graph(basemodels)
    print("\nModels dependency graph:")
    for model_name, dependencies in graph.items():
        print(f"  {model_name}: {dependencies}")
        
    nx_graph = build_dependancy_graph(basemodels)
    #plt.show()
    #nx.draw(nx_graph, with_labels=True)
    
    print(nodes_ordering(nx_graph))

    for node in nodes_ordering(nx_graph):
        print("---", node, "---")
        basemodel = getattr(validate_module, node)
        for column in basemodel.model_fields.keys():
            print(column, f"  - {column}")
        
if __name__ == "__main__":
    schema()