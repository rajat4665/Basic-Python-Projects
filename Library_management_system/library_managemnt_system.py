# import required modules 
from datetime import datetime
import json 

def load_json(database_json_file="library.json"):
    """
    This function will load json data from library.json file if it exist else crean an empty array
    """
    try:
        with open(database_json_file, "r") as read_it: 
            all_data_base = json.load(read_it) 
            #print("data has been readed from existing file ")
            return all_data_base
    except:
       # print("new data base created ")
        all_data_base = dict()
        return all_data_base

def save_json(data, database_json_file="library.json"):
    """
    This function Save data sync all data in library.json file if it exist else create it.
    """
    with open(database_json_file, "w") as p: 
        json.dump(data, p) 


def all_books_init():
    """
    This function fetch all present books detail from json file if it exist else create an empty array
    """
    all_books = all_data_base.get("all_books")
    if all_books is None:
        all_data_base['all_books'] = dict()
    all_student = all_data_base.get("all_students")
    if all_student is None:
        all_data_base['all_students'] = dict()
    return None


def current_time_is():
    """
    This function create time stamp for keep our book issue record trackable 
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string


# Here I used Ifinite loop because i don't want to run it again and again.
while True:

    print("""  ================ Welcome to this library program =============

    ==>> press 1 for checking existing books
    ==>> press 2 for issueing book
    ==>> press 3 for returning book
    ==>> press 4 for admin panel
    ==>> press 5 for exit

    """)

    choice = int(input("==>> Please enter your choice :"))

    # Load json function called for fetching/creating data from json file.
    all_data_base = load_json()
    if choice == 1:
        all_books_init()
        all_aviable_books = [books for books in all_data_base['all_books']]
        print(all_aviable_books)

    elif choice == 2:
        all_aviable_books = [books for books in all_data_base['all_books']]
        print("Availbele books are :",all_aviable_books)
        student_name = input("enter your name :")
        student_roll_no = input("enter your unique roll number :")
        book_name_is = input("enter name to issue book :").title()
        if all_data_base['all_books'][book_name_is] > 0:
            print("congratulation this book is present  !!!")
            current_student = all_data_base["all_students"].get(student_roll_no)

            if current_student is None:
                all_data_base['all_students'][student_roll_no] = dict()
                current_student = all_data_base['all_students'][student_roll_no]

            all_data_base['all_students'][student_roll_no]['Name'] = student_name
            issued_books = all_data_base['all_students'][student_roll_no].get('total_issued_book')

            if issued_books is None:
                all_data_base['all_students'][student_roll_no]['total_issued_book'] = dict()
                #print("===== dict is created ====")
            if book_name_is in current_student['total_issued_book']:
                print("Sorry you can't issue same book more than one ")
            else:
                all_data_base['all_students'][student_roll_no]['total_issued_book'][book_name_is] = current_time_is()

                quantity = 1
                all_books = all_data_base.get("all_books")
                prev_value = all_books[book_name_is]

                if prev_value == quantity:
                    del all_data_base['all_books'][book_name_is]
                else:
                    all_books[book_name_is] = prev_value-quantity
                    
                print("===== congoratulations you book has been issued successfuly ===")
                # this fucntion save all data in our database 
                save_json(all_data_base)

        else:
            print("sorry this books is not present, please select in availble books ")

    elif choice == 3:
        user_id = input("please enter your user id :")
        current_user = all_data_base['all_students'].get(user_id)
        if current_user is None:
            print("sorry this id has not issued any book yet !! ")
        else:
            book_name = input("please enter book name that you want to return :").title()
            if book_name in current_user['total_issued_book']:
                date_of_issue = current_user['total_issued_book'][book_name]
                print(f"you have issued this book on {date_of_issue}")
                for i in range(2):
                    print("+++++++++++++ processing +++++++++++++++")
                del current_user['total_issued_book'][book_name]
                all_books = all_data_base.get("all_books")
                try:
                    prev_value = all_books[book_name]
                except:
                    prev_value = 0
                all_books[book_name] = prev_value+1
                # json saved
                save_json(all_data_base)
                print("Congratulation this book has been returned successfuly ")

    elif choice == 4:
        print("++++++ user_name = admin & user_pass = admin ++++++")
        user_name = input("plese entrer your user name :")
        user_pass = input("please enter your secret passwords :")

        if user_name == "admin" and user_pass == "admin":
            print('''\n ======= Welcome to the admin pannel =======

        ==>> press 1 for checking existing record
        ==>> press 2 for adding book
        ==>> press 3 for removing book
        ==>> press 4 for exit

            ''')

            admin_choice = int(input("==>> Please enter your choice :"))
        
            if admin_choice == 1:
                all_books = all_data_base.get("all_books")
                all_issued = all_data_base.get("all_students")
                print(f"\n ========== Total remaining books are =============\n {all_books}\n ================= Total issued books are ============= \n {all_issued}")

            elif admin_choice == 2:
                book_name = input("enter book name :").title()
                quantity = int(input("how many books do you wan to add :"))
                all_books_init()
                all_books = all_data_base.get("all_books")
                if book_name in all_books:
                    prev_value = all_books[book_name]
                    all_books[book_name] = prev_value+quantity
                else:
                    all_books[book_name] = quantity
                save_json(all_data_base)

            elif admin_choice == 3:
                book_name = input("enter book name :").title()
                quantity = int(input("how many books do you want to remove :"))
                all_books_init()
                all_books = all_data_base.get("all_books")

                if book_name in all_books:
                    prev_value = all_books[book_name]
                    if prev_value < quantity:
                        print(f" Only {prev_value} numbers of {book_name} present we can't remove more than that")
                    elif prev_value == quantity:
                        del all_data_base['all_books'][book_name]
                        save_json(all_data_base)
                    else:
                        all_books[book_name] = prev_value-quantity
                        save_json(all_data_base)
                else:
                    print("Sorry this book is not present")

            elif admin_choice == 4:
                print('Thank you for visting !!!')
                break  
        else:
            print("Sorry your credentials are not valid !!! ")

    elif choice == 5:
        print('Thank you for visting !!!')
        break

    else:
        print("enter a valid choice ")