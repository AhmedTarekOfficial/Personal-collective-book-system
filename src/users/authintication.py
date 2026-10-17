
import json as js
from pathlib import Path
import os as o 
import time as ti

USERS_FILE = Path(__file__).parent / "users_information.json"


def Login(username=None , password =None):
    with open(USERS_FILE, "r", encoding="utf-8-sig") as use:
        readed_information = js.load(use)
    for userinformationn in readed_information:        
        Loginwrongcount = 0
        while True : 
            check_email_information  = any(userdata["username"] == username for userdata in userinformationn.values())
            check_password_information = any(userdata["password"] == password for userdata in userinformationn.values())
            if not check_email_information and not check_password_information : 
                print("there is something wrong in you'r username  or password ")
                username = input("Please re-input your username :  " )
                password = input("please re-input you'r password : ")
                Loginwrongcount+=1
            elif not check_password_information :
                print("there is something wrong in you'r password ")
                password = input("Please re-enter you'r password again ")
                Loginwrongcount+=1
            elif not check_email_information :
                print("there is something wrong in you'r username please check again ")
                username = input("please check you'r username again ")    
                Loginwrongcount+=1
            else  :
                o.system("cls")
                print("Successfully register to you'r account") 
                break
            if Loginwrongcount == 3 : 
                print("You faild to sign in in you account and u reach the limit of attempts so you can try again later : ")
                ti.sleep(5)
        break 

      
                


Login(username="dfafadfdsafdsa" , password="daffdafdafda@__")
