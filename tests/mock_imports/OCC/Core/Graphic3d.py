class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
Graphic3d_NOM_STEEL = MockObject()
Graphic3d_TMF_TriedronPers = MockObject()
Quantity_NOC_GRAY = MockObject()
Graphic3d_TransformPers = MockObject()
Graphic3d_Vec2i = MockObject()
Graphic3d_NOM_ALUMINIUM = MockObject()
Graphic3d_NOM_NEON_GNC = MockObject()
Graphic3d_NOT_ENV_CLOUDS = MockObject()
Graphic3d_TMF_2d = MockObject()

__all__ = ['Graphic3d_NOM_STEEL', 'Graphic3d_TMF_TriedronPers', 'Quantity_NOC_GRAY', 'Graphic3d_TransformPers', 'Graphic3d_Vec2i', 'Graphic3d_NOM_ALUMINIUM', 'Graphic3d_NOM_NEON_GNC', 'Graphic3d_NOT_ENV_CLOUDS', 'Graphic3d_TMF_2d']

def __getattr__(name):
    return MockObject()
