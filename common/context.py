class Context:
    def __init__(self, db, executor):
        self.executor = executor
        self.db = db
