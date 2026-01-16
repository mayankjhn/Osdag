class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
gp_Trsf = MockObject()
gp_Pnt = MockObject()
gp_Dir = MockObject()
gp_Vec = MockObject()
gp_Pln = MockObject()
gp = MockObject()
gp_Circ = MockObject()
gp_OX = MockObject()
gp_Pnt2d = MockObject()
gp_OY = MockObject()
gp_Ax2 = MockObject()
gp_Ax1 = MockObject()
gp_Ax3 = MockObject()

__all__ = ['gp_Trsf', 'gp_Pnt', 'gp_Dir', 'gp_Vec', 'gp_Pln', 'gp', 'gp_Circ', 'gp_OX', 'gp_Pnt2d', 'gp_OY', 'gp_Ax2', 'gp_Ax1', 'gp_Ax3']

def __getattr__(name):
    return MockObject()
