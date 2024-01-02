class User:
    def __init__(self, id, email=None, name=None, avatar=None):
        self._id = id
        self._email = email
        self._name = name
        self._avatar = avatar
        self.active = True

    def is_active(self):
        return True 
    
    def is_authenticated(self):
        return self.id != None

    def get_id(self):
        return self.id

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email
    @property
    def avatar(self):
        return self._avatar

