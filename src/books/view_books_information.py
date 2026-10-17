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
            for ii in information_books.values() : 
                print("you'r collection books is : ")

            
        




view_books(user_id="1")

   
