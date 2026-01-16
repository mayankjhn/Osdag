class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
BRepPrimAPI_MakeWedge = MockObject()
BRepPrimAPI_MakeBox = MockObject()
BRepPrimAPI_MakeCylinder = MockObject()
BRepPrimAPI_MakePrism = MockObject()
BRepPrimAPI_MakeSphere = MockObject()
BRepPrimAPI_MakeRevol = MockObject()

__all__ = ['BRepPrimAPI_MakeWedge', 'BRepPrimAPI_MakeBox', 'BRepPrimAPI_MakeCylinder', 'BRepPrimAPI_MakePrism', 'BRepPrimAPI_MakeSphere', 'BRepPrimAPI_MakeRevol']

def __getattr__(name):
    return MockObject()
