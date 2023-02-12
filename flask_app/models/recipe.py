

class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name= data["name"]
        self.description= data["description"]
        self.instructions= data["instructions"]
        self.date_cooked= data["date_cooked"]
        self.cooked_under_30m= data["cooked_under_30m"]
        self.created_at= data["created_at"]
        self.updated_at= data["updated_at"]
        self.creator = None