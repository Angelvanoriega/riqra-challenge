from src.core import Store


class SignUp(Store):
    email = ''
    password = ''


class Login(Store):
    email = ''
    password = ''

class Reset(Store):
    pass