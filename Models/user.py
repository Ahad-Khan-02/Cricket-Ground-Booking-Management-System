from DB.connection import get_connection
from email_validator import validate_email,EmailNotValidError
import bcrypt


def authenticate_user(email, password):
    conn = get_connection()

    cursor = conn.cursor()
    cursor.execute(
        "SELECT Password,UserID FROM Users WHERE Email=:1",
        (email,)
    )
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result is None:
        print("Invalid Email")
        return False
    
    hash_password = result[0]
    hash_password_bytes = bytes.fromhex(hash_password)
    if bcrypt.checkpw(password.encode(), hash_password_bytes):
        return result[1]
    else:
        print("Invalid password")
        return False
    

def authenticate_email(email):
    try:
        valid = validate_email(email)  
        return "Valid Email",True
    except EmailNotValidError as e:
        return f"Invalid Email: {e}",False
    

def register_user(name, email,password, phone, role):
    conn = get_connection()
    cursor = conn.cursor()
    
    if not name.isalpha():
        return 'Name must be in alphabets'
    email_validity=authenticate_email(email)
    if not(email_validity[1]):
        return email_validity[0]
    if len(password)<8:
        return 'length of pass must be greater than 8'
    if not(phone.isdigit()):
        return 'Phone must a number'
    
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    
    try:
        cursor.execute("""
                INSERT INTO Users (Name, Email, Password, Phone, Role) 
                VALUES (:1, :2, :3, :4, :5)
            """, (name, email,hashed_password, phone, role))
        conn.commit()
        return "Account Created Succesfully"

    except Exception as e:
        conn.rollback()
        return "Error:" + str(e)
    finally:
        cursor.close()
        conn.close()
    
def get_role(userID):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM Users WHERE UserID=:1",
        (userID,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return result[0]


       
  
