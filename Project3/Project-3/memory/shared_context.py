class SharedContext:
    def __init__(self):
        self.context = {}

    def set(self, key: str, value):
        self.context[key] = value

    def get(self, key: str, default=None):
        return self.context.get(key, default)

    def all(self):
        return self.context

    def clear(self):
        self.context = {}