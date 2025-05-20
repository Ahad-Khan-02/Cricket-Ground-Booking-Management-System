from DB.connection import get_connection
import bcrypt
import re


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
        return False
    
    hash_password = result[0]
    hash_password_bytes = bytes.fromhex(hash_password)
    if bcrypt.checkpw(password.encode(), hash_password_bytes):
        return result[1]
    else:
        return False
    

def validate_registration(name, email, password, phone, role,confirm_password):
    info=[name,email,phone,password,confirm_password,role]
    if any(i == '' for i in info):
        return "All fields must be filled",False
    
    if password != confirm_password:
        return "Passwords do not match",False

    name_regex = r"^[A-Za-z'-]{4,50}$"
    if not re.match(name_regex, name):
        return "Name must be 4-50 letters only (not numbers or any special character) without spaces", False
    
    email_regex = r'^(?!.*\.\.)(?!\.)(?!.*\.$)[a-zA-Z0-9._]+@gmail\.com$'
    if not re.match(email_regex, email):
        return "Invalid Email", False

    phone_regex = r'^03[0-9]{9}$'
    if not re.match(phone_regex, phone):
        return "Phone number must be 11 digits, start with '03', and contain only numbers", False

    if len(password) < 8:
        return 'Password must contain at least 8 characters', False
    if len(password) > 72:
        return 'Password must not exceed 72 characters', False


    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Users WHERE Email=:1", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return 'Email already exists', False

    cursor.execute("SELECT * FROM Users WHERE Phone=:1", (phone,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return 'Phone already exists', False

    cursor.close()
    conn.close()
    return "Validation successful", True


def register_user(name, email, password, phone, role):
    conn = get_connection()
    cursor = conn.cursor()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    try:
        cursor.execute("""
            INSERT INTO Users (Name, Email, Password, Phone, Role) 
            VALUES (:1, :2, :3, :4, :5)
        """, (name, email, hashed_password, phone, role))
        conn.commit()
        return "Account created successfully", True
    except Exception as e:
        conn.rollback()
        print(f"DB Error: {e}")  # log it
        return "Something went wrong during registration", False    
    finally:
        cursor.close()
        conn.close()

    
def get_user_info(email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT UserID,Name,Phone,Role FROM Users WHERE Email=:1",
        (email,)
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return result


       
  
