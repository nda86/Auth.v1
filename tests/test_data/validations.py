VALID_USER = dict(username="User", password="1213456789", email="email@example.com")

check_password_validation = [
    (dict(username="Admin", password="Admin"), ['Length must be between 8 and 20.'], 400),
    (dict(username="Admin", password="1"*30), ['Length must be between 8 and 20.'], 400),
    (dict(username="Admin", password=""), ['Length must be between 8 and 20.'], 400),
]

check_username_validation = [
    (dict(username="Ad", password="123456789"), ['Length must be between 3 and 15.'], 400),
    (dict(username="A"*30, password="123456789"), ['Length must be between 3 and 15.'], 400),
    (dict(username="", password="123456789"), ['Length must be between 3 and 15.'], 400),
]

check_email_validation = [
    (dict(username="Admin", password="123456789", email="assa@kl."), ['Not a valid email address.'], 400),
]
