class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
Prs3d_Drawer = MockObject()
Prs3d_Text = MockObject()
Prs3d_DatumAspect = MockObject()
Prs3d_TextAspect = MockObject()
Prs3d_Presentation = MockObject()
Prs3d_Arrow = MockObject()

__all__ = ['Prs3d_Drawer', 'Prs3d_Text', 'Prs3d_DatumAspect', 'Prs3d_TextAspect', 'Prs3d_Presentation', 'Prs3d_Arrow']

def __getattr__(name):
    return MockObject()
