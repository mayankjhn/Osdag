class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
load_backend = MockObject()
off = MockObject()
get_qt_modules = MockObject()

__all__ = ['load_backend', 'off', 'get_qt_modules']

def __getattr__(name):
    return MockObject()
