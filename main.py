from UI.login import login
from UI.sign_up import signUp
from Models.user import get_role


e=input("Enter Email:")
p=input("Enter Password:")
m,l,user_ID=login(e,p)
print(m)
role=get_role(user_ID)
print(role)


