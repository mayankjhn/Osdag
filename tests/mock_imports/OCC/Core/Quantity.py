class MockObject:
    def __init__(self, *args, **kwargs): pass
    def __call__(self, *args, **kwargs): return MockObject()
    def __getattr__(self, name): return MockObject()
    def __iter__(self): return iter([])
    def __getitem__(self, key): return MockObject()
    def __setitem__(self, key, value): pass
    def __len__(self): return 0
    def __contains__(self, item): return False
Quantity_NOC_GRAY = MockObject()
Quantity_NOC_GRAY25 = MockObject()
Quantity_NOC_RED = MockObject()
Quantity_NOC_WHITE = MockObject()
Quantity_NOC_SADDLEBROWN = MockObject()
Quantity_Color = MockObject()
Quantity_NOC_BLACK = MockObject()
Quantity_TOC_RGB = MockObject()
Quantity_NOC_BLUE1 = MockObject()

__all__ = ['Quantity_NOC_GRAY', 'Quantity_NOC_GRAY25', 'Quantity_NOC_RED', 'Quantity_NOC_WHITE', 'Quantity_NOC_SADDLEBROWN', 'Quantity_Color', 'Quantity_NOC_BLACK', 'Quantity_TOC_RGB', 'Quantity_NOC_BLUE1']

def __getattr__(name):
    return MockObject()
