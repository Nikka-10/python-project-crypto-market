import database
import Hashing
import ValidChecker
import Balance
import pyodbc
import Operations
import history



class sign_up():
    def __init__(self,fname, lname, email, password):
        self.db = database.database()
        self.fname = fname
        self.lname = lname
        self.email = email
        self.password = password
            
    def check(self):
        try: 
            if ValidChecker.check_mail(self.email) == True and  ValidChecker.check_password(self.password) == True:
                return True
        except ValueError as problem:
            print(problem)
        
    def add_user(self):        
        hashing = Hashing.Hashing_password(self.password)
        self.hashed_password = hashing.hashing_scrypt()
        try:
            if_add = self.db.add_data("insert into user_info(fname, lname, email, password_) values(?,?,?,?)", (self.fname, self.lname, self.email, self.hashed_password))
            return if_add
        except pyodbc.IntegrityError:
            print("account with this email is already exist")
            
    @classmethod
    def get_user_info(cls):
        fname = input("wirte your first name: ")    
        lname = input("wirte your last name: ")     
        email = input("wirte your email address: ")    
        password = input("wirte password: ")
        
        return cls(fname, lname, email, password)   
            
class sign_in():
    def __init__(self, email, password):
        self.db = database.database()
        self.connection_str = self.db.connection_str
        self.email = email
        self.password = password
        
        
    def check(self):
        checkpassword  = Hashing.check_password(self.connection_str ,self.email, self.password)
        if checkpassword.check_hash_password() == True:
            return self.db.get_data("SELECT userid FROM user_info WHERE email = ?", (self.email,))
        else:
            raise ValueError
        
    @classmethod
    def get_user_info(cls):
        email = input("enter user email: ")
        password = input("enter user password: ")
        return cls(email, password)
            
def main():
    signin  = sign_in()
    
    print("welcome to our crypto market!")
    answer = input(" 1. sign in \n 2. sign up \n ")
    
    if answer == '1':   
        while True:
            try:
                signin.get_user_info()
            except ValueError as error:
                print(error)
            else:
                user_id = signin.check()
                print("you successfully signed in")
                break
            
        balance_operations = Balance.Balance_Operations(user_id)
        action = input(" 1.add balance \n 2.withdraw balance \n 3.skip \n")
        if action == "1":
            balance_operations.insert_balance()
        elif action == "2":
            balance_operations.withdraw_balance()
        elif action == "3":
            pass
        
        while True:
            crypto = input("what cryptocurrency are you interested in? ")
            crypto_list = [coin.strip().lower() for coin in crypto.split(",")]
            crypto_operation = Operations.crypto_operations(user_id, crypto_list)
            action = input(" 1.show price \n 2.buy \n 3.sell \n 4.convert \n 5.exit \n")
            
            if action == "1":
                print(crypto_operation.show_price())
                continue
            elif action == "2":
                crypto_operation.buy_crypto()
                continue
            elif action == "3":
                crypto_operation.sell_crypto()
                continue
            elif action == "4":
                crypto_operation.convert()
                continue
            elif action == "5":
                break
            
    elif answer == '2':
         while True:
             signup = sign_up.get_user_info()
             if signup.check() !=  True:
                 continue
             if signup.add_user() == True: 
                 print("you successfully signed up")
                 break
        
     
if __name__ == "__main__":
    main()