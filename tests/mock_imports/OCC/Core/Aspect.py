class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
Aspect_FM_STRETCH = MockObject()
Aspect_GT_Rectangular = MockObject()
Aspect_GFM_VER = MockObject()
Aspect_TOTP_RIGHT_UPPER = MockObject()
Aspect_TOTP_RIGHT_LOWER = MockObject()
Aspect_FM_NONE = MockObject()
Aspect_GDM_Lines = MockObject()

__all__ = ['Aspect_FM_STRETCH', 'Aspect_GT_Rectangular', 'Aspect_GFM_VER', 'Aspect_TOTP_RIGHT_UPPER', 'Aspect_TOTP_RIGHT_LOWER', 'Aspect_FM_NONE', 'Aspect_GDM_Lines']

def __getattr__(name):
    return MockObject()
