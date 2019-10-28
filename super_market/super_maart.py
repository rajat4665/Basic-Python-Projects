# import required modules 
import json 
from datetime import datetime
from beautifultable import BeautifulTable

def load_json(database_json_file="super_mart.json"):
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

def save_json(data, database_json_file="super_mart.json"):
    """
    This function Save data sync all data in library.json file if it exist else create it.
    """
    with open(database_json_file, "w") as p: 
        json.dump(data, p) 
        
def all_data_init():
    """
    This function initialse data if it exist else create an empty one 
    """
    all_products = all_data_base.get("all_products")
    if all_products is None:
        all_data_base['all_products'] = dict()
        
    all_transitions = all_data_base.get("all_trans")
    if all_transitions is None:
        all_data_base['all_trans'] = dict()
    return None

def current_time_is():
    """
    This function create time stamp for keep our book issue record trackable 
    """
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string

def product_addition():
    """
    This function is use to add products in your cart
    """
    product_name  = input("Please enter product name that you want to add :")
    prduct_price = float(input("plese enter price for this product :"))

    all_data_base['all_products'][product_name] = prduct_price
    futher_choice = input('If you want to add more producr preess Y else any other key :').lower()
    if futher_choice == 'y':
        product_addition()
    else:
        pass
    return None


def product_buying():
    """
    This function is use to display checkout table 
    """
    billing_table = BeautifulTable()
    billing_table.column_headers = ["Sr no.", "Product Name ", "Price","Quantity", "Row total"]
    total_charges = list()
    dict_of_record = dict()
    
    def buy_pro():
        """
        Here I use another function to display each row of checkout table dynamically
        """
        product_buy = input("enter product name to buy :").title()
        #print(product_buy)
        if product_buy in all_data_base['all_products']:
            
            product_quantity = int(input("please enter how many piece do you want to purchase :"))
            sub_total = product_quantity* all_data_base['all_products'][product_buy]
            dict_of_record[product_buy] = product_quantity
            dict_of_record[str(product_buy)+"*"+str(product_quantity)] = sub_total
            total_charges.append(sub_total)
            billing_table.append_row([count, product_buy, all_data_base['all_products'][product_buy],
                              product_quantity, sub_total
                             ])
            buy_choice = input("if you want to add more product press y else anyother key:").lower()
            if buy_choice == "y":
                buy_pro()
            else:
                print(" ")
                print(billing_table)
                # return billing_table, sum(total_charges), dict_of_record
        else:
            print("sorry this product is not present :")
            
    buy_pro()
    return sum(total_charges), dict_of_record
        

print("""  ================ Welcome to this library program =============

    ==>> press 1 for buy availble products 
    ==>> press 2 for admin panel
    ==>> press 3 for exit

    """)

choice = int(input("==>> Please enter your choice :"))

all_data_base = load_json()
all_data_init()

if choice ==1:
    table = BeautifulTable()
    table.column_headers = ["Sr no.", "Product Name ", "Price"]
    count = 1
    print(  )
    for data in all_data_base['all_products']:
        table.append_row([count, data, all_data_base['all_products'][data]])
        count += 1  
    print(table)
    sum_of_total,dict_of_record  = product_buying()
    print()
    print("+--------+----------TOTAL SUM IS -----+----------+-",sum_of_total)
    serial_no = (len(all_data_base['all_trans']))
    all_data_base['all_trans'][serial_no] = dict()
    all_data_base['all_trans'][serial_no]["total_price"] = sum_of_total
    all_data_base['all_trans'][serial_no]["time_of_trans"] = current_time_is()
    all_data_base['all_trans'][serial_no]["complete_detals"] = dict_of_record
    save_json(all_data_base)
    print("thanks have a good day !!!!")
elif choice == 2:
    user_name = input("plese entrer your user name :")
    user_pass = input("please enter your secret passwords :")

    if user_name == "admin" and user_pass == "admin":
        print('''\n ======= Welcome to the admin pannel =======

    ==>> press 1 for checking existing products
    ==>> press 2 for adding products
    ==>> press 3 for removing products
    ==>> press 4 for cheching transitaction history 
    ==>> press 5 for exit 

        ''')

        admin_choice = int(input("==>> Please enter your choice :"))
        if admin_choice == 1:
            
            print("++++++ All products are ++++++ \n",all_data_base["all_products"])
            alterations = input("Press y to make alteration in price else print any key :").lower()
            if alterations == "y":
                print(" >>>>>>> you can change price of lsited producted >>>>>>>>")
                prroduct_name = input("Please enter product name :").title()
                if prroduct_name in all_data_base['all_products']:
                    new_price =float(input("Enter new price for this product "))
                    all_data_base['all_products'][prroduct_name] = new_price
                    
                    print("\n Congratulations changes has been reflect ")
                    save_json(all_data_base)
                else:
                    print(" Sorry this product is not present in this list ")
            else:
                pass
            
        elif admin_choice == 2:
            product_addition()
            save_json(all_data_base)
            print("+++++++++ product has bee added successfully ++++++++++")
            
        elif admin_choice == 3:
            product_name  = input("Please enter product name that you want to remove  :").title()
            if product_name in all_data_base["all_products"]:
                del all_data_base['all_books'][book_name]
                print("+++++++++ product has bee deleted successfully ++++++++++")
                save_json(all_data_base)
            else:
                print("Sorry this product is not present in listed products ")
        
        elif admin_choice == 4:
            try:
                print(all_data_base['all_trans'])
            except:
                print("No transaction is found ")
        
        elif admin_choice ==5:
             print("+++++++++ Have a nice day Admin ++++++++++")
                
elif choice == 3:
    print(" thank you for visiting ")
else:
    print("Please enter a valid choice ")
        
