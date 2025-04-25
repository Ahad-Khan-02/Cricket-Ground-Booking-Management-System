from Models.user import authenticate_user

def login(email,password):
    login=False
    data=authenticate_user(email,password)
    if data:
        msg="Login Successfully"
        login=True
    else:
        msg="Login Failed"
    return msg,login,data
    

