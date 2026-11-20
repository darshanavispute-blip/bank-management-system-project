# BANK MANAGEMENT SYSTEM WITH MYSQL
import mysql.connector

# 1.database connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="bank_manegement_system"
    )
    cursor = conn.cursor()
    if conn.is_connected():
        print("connected to the database")
except mysql.connector.Error as err:
    print(f"database connection error: {err}")
    exit()

# Exceptions
class loginerror(Exception):
    pass

class insufficientbalence(Exception):
    pass

# 2. Registration Function 
def reg(name, age, address, phoneno, userid, password, confirmpassword):
    try:
        query = """INSERT INTO bank_system 
                   (name, age, address, phoneno, userid, password, confirmpassword, deposit, withdraw, show_balance) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, 0, 0, 0)"""
        values = (name, age, address, str(phoneno), userid, password, confirmpassword)
        cursor.execute(query, values)
        conn.commit()
        print("Registration successful! Data saved in MySQL.")
    except mysql.connector.Error as err:
        print(f"Registration Error: {err}")

# 3. Login Function 
def login(userid, password):
    try:
        query = "SELECT * FROM bank_system WHERE userid = %s AND password = %s"
        cursor.execute(query, (userid, password))
        user = cursor.fetchone()
        if user:
            print("login successful")
            return True
        else:
            raise loginerror("invalid userid or password")
    except loginerror as e:
        print(e, "login error!")
        return False

# 4. Deposit Function
def deposite(userid):
    amount = int(input("enter your amount : "))
    if amount > 0:
        query = """UPDATE bank_system 
                   SET deposit = IFNULL(deposit, 0) + %s, 
                       show_balance = IFNULL(show_balance, 0) + %s 
                   WHERE userid = %s"""
        cursor.execute(query, (amount, amount, userid))
        conn.commit()
        print(amount, "your amount deposite sucssefully!")
    else:
        print("Please enter a valid amount.")

# 5. Withdrawal Function
def withdrawl(userid):
    amount = int(input("enter your amount : "))
    try:
        cursor.execute("SELECT IFNULL(show_balance, 0) FROM bank_system WHERE userid = %s", (userid,))
        result = cursor.fetchone()
        current_balance = int(result[0])

        if amount > current_balance:
            raise insufficientbalence("Insufficient balance!")
        else:
            query = """UPDATE bank_system 
                       SET withdraw = IFNULL(withdraw, 0) + %s, 
                           show_balance = IFNULL(show_balance, 0) - %s 
                       WHERE userid = %s"""
            cursor.execute(query, (amount, amount, userid))
            conn.commit()
            print(amount, "your amount withdrwl sucssefully!")
    except insufficientbalence as e:
        print(e)

# 6. Balance Check Function
def acbalence(userid):
    cursor.execute("SELECT IFNULL(show_balance, 0) FROM bank_system WHERE userid = %s", (userid,))
    result = cursor.fetchone()
    print("your acount balence is", result[0])

# 7. Main Menu
n = 0
while n != 3:
    print("\n===== welcome to bank menue ====")
    print("1. enter 1 for registration")
    print("2. enter 2 for login")
    print("3. enter 3 for exit")
    num = int(input("Please Enter Your Choise : "))

    if num == 1:
        name = input("enter the name : ")
        age = int(input("enter the age : "))
        address = input("enter the address : ")
        phone = input("enter the phone number : ")
        userid = input("enter the userid : ")
        password = input("enter the password : ")
        confirmpassword = input("enter confirm password : ")
        
        if password != confirmpassword:
            print("your password is wrong!")
        else:
            reg(name, age, address, phone, userid, password, confirmpassword)

    elif num == 2:
        userid = input("enter userid : ")
        password = input("enter your password : ")
        f = login(userid, password)
        
        if f:
            while True:
                print("\n===== your account detail =====")
                print("Enter 1 for deposit")
                print("Enter 2 for withdraw")
                print("Enter 3 for show balance")
                print("Enter 4 for exit")
                press = int(input("enter no : "))

                if press == 1:
                    deposite(userid)
                elif press == 2:
                    withdrawl(userid)
                elif press == 3:
                    acbalence(userid)
                elif press == 4:
                    print("thank you for visit !")
                    break
                else:
                    print("please try again!")

    elif num == 3:
        print("exit!")
        break

# 8. database connection close
if conn and conn.is_connected():
    cursor.close()
    conn.close()
    print("connection closed")