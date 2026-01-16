class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
Geom_CartesianPoint = MockObject()
Geom_Curve = MockObject()
Geom_Surface = MockObject()

__all__ = ['Geom_CartesianPoint', 'Geom_Curve', 'Geom_Surface']

def __getattr__(name):
    return MockObject()
