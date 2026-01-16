class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
BRepBuilderAPI_MakeVertex = MockObject()
BRepBuilderAPI_Transform = MockObject()
BRepBuilderAPI_MakePolygon = MockObject()
BRepBuilderAPI_MakeWire = MockObject()
BRepBuilderAPI_MakeFace = MockObject()
BRepBuilderAPI_MakeEdge = MockObject()

__all__ = ['BRepBuilderAPI_MakeVertex', 'BRepBuilderAPI_Transform', 'BRepBuilderAPI_MakePolygon', 'BRepBuilderAPI_MakeWire', 'BRepBuilderAPI_MakeFace', 'BRepBuilderAPI_MakeEdge']

def __getattr__(name):
    return MockObject()
