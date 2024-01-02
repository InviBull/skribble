class User:
    def __init__(self, id, email=None, name=None, avatar=None):
        self.id = id
        self.email = email
        self.name = name
        self.avatar = name
        self.active = True

    def is_active(self):
        return True 
    
    def is_authenticated(self):
        return self.id != None

    def get_id(self):
        return self.id
