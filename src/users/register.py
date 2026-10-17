import json as js 
import os as o
import time as ti
from pathlib import Path
USERS_FILE = Path(__file__).parent / "users_information.json"

def register(email , password  , username  ) : 
    with open(USERS_FILE,"r" , encoding="utf-8-sig") as re : 
        current_information = js.load(re) 
        o.system("cls")
        print("please be patient some time , until finished some processing ")
        ti.sleep(3)
        while True : 
            email_taken = any(user_data["email"] == email 
                  for item in current_information 
                  for user_data in item.values())
            username_taken = any(user_data["username"] == username 
                     for item in current_information 
                     for user_data in item.values())

            
            if email_taken and username_taken : 
                 o.system("cls")
                 print("unfortunately both  email and username  already registerd , please enter new one  ")
                 email = input("Please re_enter new email : " )
                 username = input("please enter the new username : ")
            else :    
                if email_taken : 
                    o.system("cls")
                    print("unfortunately this email already registerd , please enter new one  ")

                    email = input("Please re_enter new email : " )
                elif username_taken : 
                    o.system("cls")
                    print("unfortunately this username already taken , please re-enter new one ")
                    username = input("please enter the new username : ")
                
            if not email_taken and not username_taken : 
                new_id = str(len(current_information) + 1)
                new_user = {
        new_id: {
            "username": username,
            "email": email,
            "password": password
        }
    }
                current_information.append(new_user)
                with open(USERS_FILE , "w" , encoding="utf-8-sig") as new_information : 
                    js.dump(current_information , new_information , indent=4 )
                    print("Email reigsterd successfully ")
                    break 





register(email="ahmedyay532@gmail.com" , password="2291970" , username="ahmed")               
