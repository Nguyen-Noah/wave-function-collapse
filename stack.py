class Stack:
    def __init__(self):
        self.items = []

    @property
    def size(self):
        return len(self.items)
    
    def is_empty(self):
        return self.size == 0
    
    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            raise IndexError('Stack is empty')
        
