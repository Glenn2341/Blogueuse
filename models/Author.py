class Author:
    def __init__(self, id, name, role, bio):
        self.id = id
        self.name = name
        self.role = role
        self.bio = bio
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'bio': self.bio
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data['id'], data['name'], data['role'], data['bio'])