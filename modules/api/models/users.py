class User:

    def __init__(self, username=None, password=None, role=None, _id=None, firstname=None, surname=None, email=None):
        self._id = _id
        self.resource = "user"
        self.username = username
        self.password = password
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.role = role 


    def __repr__(self):
        return (f"User(username='{self.username}', password='{self.password}', role='{self.role}', "
                f"_id='{self._id}', firstname='{self.firstname}', surname='{self.surname}', email='{self.email}')")
    

    
