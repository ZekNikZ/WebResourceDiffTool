from caches import BaseCache

class HTMLCache(BaseCache):
    def __init__(self):
        super().__init__('html')

class TextCache(BaseCache):
    def __init__(self):
        super().__init__('text', 'txt')