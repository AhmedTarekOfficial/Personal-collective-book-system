import json
import os
import random

BOOKS_FILE = os.path.join(os.path.dirname(__file__), "src", "data", "books_data.json")
USERS_FILE = os.path.join(os.path.dirname(__file__), "src", "data", "users_information.json")
COLLECTION_FILE = os.path.join(os.path.dirname(__file__), "src", "data", "person_collectingbooks.json")

with open(BOOKS_FILE, "r", encoding="utf-8") as f:
    all_books = json.load(f)["books"]

with open(USERS_FILE, "r", encoding="utf-8-sig") as f:
    users_data = json.load(f)

users = []
for user_entry in users_data:
    for user_id, user_info in user_entry.items():
        users.append((user_id, user_info["username"]))

print(f"Found users: {[(uid, uname) for uid, uname in users]}")
print(f"Total books available: {len(all_books)}")
print()

collection = {}
books_per_user = 30

for user_id, username in users:
    assigned_books = random.sample(all_books, books_per_user)
    collection[user_id] = assigned_books
    print(f"Assigned {len(assigned_books)} random books to '{username}' (ID: {user_id})")

with open(COLLECTION_FILE, "w", encoding="utf-8") as f:
    json.dump(collection, f, ensure_ascii=False, indent=2)

print()
print("Done! Collection saved to person_collectingbooks.json")
