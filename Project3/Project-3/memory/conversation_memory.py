from datetime import datetime

class ConversationMemory:
    def __init__(self):
        self.history = []
        self.session_start = datetime.now().isoformat()

    def add(self, role: str, content: str):
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

    def last_n(self, n: int = 5):
        return self.history[-n:]