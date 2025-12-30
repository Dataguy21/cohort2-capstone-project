# Simple in-memory session memory for agent interactions.
class Memory:
    def __init__(self):
        self.store = []
    def add(self, item):
        self.store.append(item)
    def get_all(self):
        return list(self.store)
