class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
AIS_WireFrame = MockObject()
AIS_ViewCube = MockObject()
AIS_Shaded = MockObject()
AIS_Shape = MockObject()
Erase = MockObject()
AIS_TexturedShape = MockObject()
AIS_Point = MockObject()

__all__ = ['AIS_WireFrame', 'AIS_ViewCube', 'AIS_Shaded', 'AIS_Shape', 'Erase', 'AIS_TexturedShape', 'AIS_Point']

def __getattr__(name):
    return MockObject()
