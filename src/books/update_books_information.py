import json
import os
import time as ti

COLLECTION_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "person_collectingbooks.json")

def update_book(user_id, book_title):

    os.system("cls")
    print("Loading your book collection...")
    ti.sleep(1)

    with open(COLLECTION_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        collection = json.loads(content) if content else {}

    if user_id not in collection or len(collection[user_id]) == 0:
        os.system("cls")
        print("You don't have any books in your collection yet.")
        return

    user_books = collection[user_id]

    os.system("cls")
    print("Searching for books with that title...")
    ti.sleep(1)

    matching_books = []
    for i, book in enumerate(user_books):
        if book["title"].lower() == book_title.lower():
            matching_books.append((i, book))

    if len(matching_books) == 0:
        os.system("cls")
        print(f"No book with the title '{book_title}' was found in your collection.")
        return

    if len(matching_books) == 1:
        chosen_index = matching_books[0][0]
        chosen_book = matching_books[0][1]
    else:
        os.system("cls")
        print(f"Found {len(matching_books)} copies of '{book_title}' in your collection:\n")

        for number, (index, book) in enumerate(matching_books, start=1):
            print(f"  [{number}] Title   : {book['title']}")
            print(f"       Author  : {book.get('author', 'N/A')}")
            print(f"       ISBN    : {book.get('isbn', 'N/A')}")
            print(f"       Language: {book.get('language', 'N/A')}")
            print(f"       Released: {book.get('release_date', 'N/A')}")
            print()

        while True:
            choice = input(f"Which book do you want to update? Enter a number (1 to {len(matching_books)}): ").strip()

            if choice.isdigit() and 1 <= int(choice) <= len(matching_books):
                chosen_number = int(choice)
                break
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(matching_books)}.")

        chosen_index = matching_books[chosen_number - 1][0]
        chosen_book = matching_books[chosen_number - 1][1]

    os.system("cls")
    print(f"What do you want to update for '{chosen_book['title']}'?\n")
    print("  [1] Title")
    print("  [2] Language")
    print("  [3] Subjects (Categories)")
    print()

    while True:
        field_choice = input("Enter your choice (1, 2, or 3): ").strip()

        if field_choice in ("1", "2", "3"):
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    if field_choice == "1":
        os.system("cls")
        print(f"Current title: {chosen_book['title']}\n")
        new_title = input("Enter the new title: ").strip()

        while True : 
            if new_title == "":
                os.system("cls")
                print("Title cannot be empty Please Fill the new Title you want it ")
                new_title = input("Enter the new title : ").strip()
            else : 
                break 
            
                

                

        collection[user_id][chosen_index]["title"] = new_title
        updated_field = "Title"
        new_value = new_title

    elif field_choice == "2":
        os.system("cls")
        print(f"Current language: {chosen_book.get('language', 'N/A')}\n")
        new_language = input("Enter the new language: ").strip()

        if new_language == "":
            os.system("cls")
            print("Language cannot be empty. Update cancelled.")
            return

        collection[user_id][chosen_index]["language"] = new_language
        updated_field = "Language"
        new_value = new_language

    elif field_choice == "3":
        os.system("cls")
        current_subjects = chosen_book.get("subjects", [])
        print(f"Current subjects: {', '.join(current_subjects) if current_subjects else 'N/A'}\n")
        print("Enter the new subjects separated by commas.")
        print("Example: Science fiction, Short stories, Adventure\n")
        new_subjects_input = input("New subjects: ").strip()

        if new_subjects_input == "":
            os.system("cls")
            print("Subjects cannot be empty. Update cancelled.")
            return

        new_subjects = [s.strip() for s in new_subjects_input.split(",")]
        collection[user_id][chosen_index]["subjects"] = new_subjects
        updated_field = "Subjects"
        new_value = ", ".join(new_subjects)

    os.system("cls")
    print("Saving your changes...")
    ti.sleep(1)

    with open(COLLECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(collection, f, ensure_ascii=False, indent=2)

    os.system("cls")
    print(f"Book updated successfully!")
    print(f"  {updated_field} changed to: {new_value}")

update_book(user_id="1", book_title="Secret societies and the French revolution :  together with some kindred…")