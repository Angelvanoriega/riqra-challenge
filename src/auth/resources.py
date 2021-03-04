from src.auth.dao import Login


class User(object):
    email = ''
    password = ''

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def login(self):
        store = Login()
        store.email = self.email
        store.password = self.password
        result = store.execute()
        if 'token' in result:
            pass
        return result
