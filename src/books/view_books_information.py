import os as o 
import json as js 
import time as ti 

COLLECTION_FILE = o.path.join(o.path.dirname(__file__), "..", "data", "person_collectingbooks.json")

def view_books(user_id = None) : 
    with open(COLLECTION_FILE , "r" , encoding="utf-8") as books_of_user : 
        information_books = js.load(books_of_user)

        if user_id not in information_books.keys() : 
            print("u don't have any collecting books yet ! ")
        else : 

            for  ff,ii in enumerate(information_books[user_id]) :
                print(f"{ff+1} -Title:{ii["title"]}\n Author : {ii["author"]}\nLanguage:{ii["language"]}\n")
                if (ff + 1) % 2 == 0 and (ff + 1) < len(information_books[user_id]):
                    input("Press Enter to see more books...")
                    o.system("cls")  
                    print("Your collection books (continued):\n-----------------------------------------")

            
        

view_books(user_id="1")

   
