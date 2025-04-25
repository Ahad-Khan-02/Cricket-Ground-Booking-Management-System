from Models.user import register_user


def signUp():
    name = input("Enter name:")
    email = input("Enter email:")
    password = input("Enter password:")
    phone = input("Enter phon:")
    role = input("Enter role:")

    msg=register_user(name, email,str(password), phone, role)
    return msg

    


