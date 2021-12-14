class User:

    def __init__(self):
        self.username = "none"
        self.password = "none"

    def __init__(self, u,p):
        self.username = u
        self.password = p

    def checkPassword(self, passw):
        if(self.password == passw):
            return True
        return False