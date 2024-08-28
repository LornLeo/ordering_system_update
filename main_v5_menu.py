from tkinter import *
from PIL import ImageTk, Image
import subprocess
import math
from tkinter import ttk
import csv
from tkinter import messagebox
from csv import writer
# Read data from 'user_database.csv' to find the 'user_id' of the user who is currently 'online'.
# 'user_database.csv' should have columns like 'user_id', 'username', 'status' (e.g., 'online' or 'offline'), etc.
with open("user_database.csv", 'r') as file:
    csvreader = csv.reader(file)
    row = list(csvreader)

# Loop through each row in the CSV file to find the 'user_id' of the user who is currently 'online'.
for item in row:
    if item[3] == "online":
        user_id = item[0]

# Read data from 'order_database.csv' to find the 'Order_number' for the current user.
# 'order_database.csv' should have columns like 'user_id', 'Order_number', 'status' (e.g., 'unpaid', 'paid'), etc.
with open("order_database.csv", 'r') as file:
    csvreader = csv.reader(file)
    row = list(csvreader)

# Loop through each row in the 'order_database.csv' to find the 'Order_number' for the current user.
for item in row:
    if item[0] == user_id:
        if item[3] == "unpaid":
            Order_number = item[1]
        else:
            Order_number = int(item[1]) + 1

# Set up lists to store the food items for each category.
filename = "menu_database.csv"
category_1_dict = []  # Store food items for category "Special"
category_2_dict = []  # Store food items for category "Burgers and Sandwiches"
category_3_dict = []  # Store food items for category "Asian Cuisine"
category_4_dict = []  # Store food items for category "Pizza"
category_5_dict = []  # Store food items for category "Fried Foods"
category_6_dict = []  # Store food items for category "Salads and Wrap"
category_7_dict = []  # Store food items for category "Drinks"
category_8_dict = []  # Store food items for category "Pasta"

# Create a function to access data in the 'menu_database.csv' file and add the food items to the corresponding category list.
def category_func(category_list, category_name):
    with open(filename, 'r') as data:
        for line in csv.DictReader(data):
            if line["Category"] == category_name:
                category_list.append(line)

# Call the 'category_func' function for each category to populate the category lists.
category_func(category_1_dict, "Special")
category_func(category_2_dict, "Burgers and Sandwiches")
category_func(category_3_dict, "Asian Cuisine")
category_func(category_4_dict, "Pizza")
category_func(category_5_dict, "Fried Foods")
category_func(category_6_dict, "Salads and Wrap")
category_func(category_7_dict, "Drinks")
category_func(category_8_dict, "Pasta")
#Set up the initial menu item dictionaries list
Menu_index=category_1_dict
initial_quantity1=0
initial_quantity2=0
initial_quantity3=0
#set up the category list and category name list to direct the correspond category and its name
category_list=[category_1_dict,category_2_dict,category_3_dict,category_4_dict,category_5_dict,category_6_dict,category_7_dict,category_8_dict]
category_name=["Special","Burgers and Sandwiches","Asian Cuisine","Pizza","Fried Foods","Salads and Wraps","Drinks","Pasta"]

#Set up the page number and calculate the total page based on the item in each current menu
page_number=1
total_page_number=math.ceil(len(Menu_index)/3)

#To disable the button selected
disable_list=[None]

#set up the cart list to store the cart_item
cart_list=[]
#set up the total cost list to calculate the total cost of the food item stored in cart  
Totalcost=[]

#Create the function for the category button when clicking
#When clicking the button, it will change the current menu item to the correspond category
def selected_button(button_name, button_press):
    global Menu_index
    Menu_index = category_list[button_press]

    # Calculate the total number of pages based on the number of items in the Menu_index list.
    global total_page_number
    total_page_number = math.ceil(len(Menu_index) / 3)

    # Configure the "Next" and "Last" page buttons based on the total number of pages.
    if total_page_number == 1:
        Bunext_page.configure(state="disabled")
        Bulast_page.configure(state="disabled")
    else:
        Bunext_page.configure(state="normal")
        Bulast_page.configure(state="normal")

    # Reset the page number to 1 and update the page display.
    global page_number
    page_number = 1
    page_displayed.configure(text="1" + "/" + str(total_page_number))

    # Set the background of the previously selected category button to white (if any).
    if disable_list[0] != None:
        disable_list[0].configure(state="normal", bg="white")
    else:
        category_1.configure(state="normal", bg="white")

    # Disable the newly selected category button and change its background to yellow.
    disable_list[0] = button_name
    button_name.configure(state="disabled")
    button_name.configure(bg="yellow")

    # Initialize quantity variables for each food item on the current category page.
    quantity_1 = 0
    quantity_2 = 0
    quantity_3 = 0

    # Loop through the cart_list to find the quantity of each food item on the current category page.
    for item in cart_list:
        if item['Name'] == Menu_index[0]['Name']:
            quantity_1 = item['Quantity']

    # Create and configure the FoodItem for the first food item on the current category page.
    food_item_1 = FoodItem(Menu_index[0]['Image_path'], Menu_index[0]['Name'], Menu_index[0]['Price'], Menu_index[0]['Description'], quantity_1, remove_frame=False)
    food_item_1.configure(item1_image, item1_name, item1_price, item1_description, item1_order, item1_quantity)

    # Create and configure the FoodItem for the second food item on the current category page (if any).
    if len(category_list[button_press]) > 1:
        for item in cart_list:
            if item['Name'] == Menu_index[1]['Name']:
                quantity_2 = item['Quantity']

        food_item2 = FoodItem(Menu_index[1]['Image_path'], Menu_index[1]['Name'], Menu_index[1]['Price'], Menu_index[1]['Description'], quantity_2, remove_frame=False)
        food_item2.grid(item2_image, item2_name, item2_price, item2_description, item2_order, item2_quantity)
        food_item2.configure(item2_image, item2_name, item2_price, item2_description, item2_order, item2_quantity)
    else:
        # If there is no second item, create an empty frame (remove_frame=True).
        food_item2 = FoodItem('', '', '', '', quantity_2, remove_frame=True)
        food_item2.configure(item2_image, item2_name, item2_price, item2_description, item2_order, item2_quantity)

    # Create and configure the FoodItem for the third food item on the current category page (if any).
    if len(category_list[button_press]) > 2:
        for item in cart_list:
            if item['Name'] == Menu_index[2]['Name']:
                quantity_3 = item['Quantity']

        food_item3 = FoodItem(Menu_index[2]['Image_path'], Menu_index[2]['Name'], Menu_index[2]['Price'], Menu_index[2]['Description'], quantity_3, remove_frame=False)
        food_item3.grid(item3_image, item3_name, item3_price, item3_description, item3_order, item3_quantity)
        food_item3.configure(item3_image, item3_name, item3_price, item3_description, item3_order, item3_quantity)
    else:
        # If there is no third item, create an empty frame (remove_frame=True).
        food_item3 = FoodItem('', '', '', '', quantity_3, remove_frame=True)
        food_item3.configure(item3_image, item3_name, item3_price, item3_description, item3_order, item3_quantity)
#create the function for order button when clicking
#When clicking, the food item will add to the cart
def add_order(item_name,item_quantity,item_price):
    item_number=0
    # If the item_quantity is '0', it means the user wants to remove the item from the cart.
    if item_quantity==str(0):
        if cart_list!=[]:
            # Remove the item from the cart_list and update the cart_table accordingly
            for item in cart_list:
                if item["Name"]==item_name:
                    cart_list.remove(item)
            if cart_list==[]:
                cart_table.delete(*cart_table.get_children())
                Total_cost.configure(text="Total cost: $0.00")
                # If the cart is now empty, update the Total_cost and delete corresponding order details.
                with open("orderdetail_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows=list(csvreader)
                    for item in rows:
                        if item[0]==user_id and item[1]==Order_number and item[2]==item_name:
                            rows.remove(item)
                with open("orderdetail_database.csv", 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)
            else:
                 # Calculate the new Total cost and update it in the 'order_database.csv'.
                Totalprice=[]
                for item in cart_list:
                    price_1=float(item["Price"].replace('$',""))
                    quantity=int(item["Quantity"])
                    item_cost=price_1*quantity
                    Totalprice.append(item_cost)
                    Total=0
                    for item in Totalprice:
                        Total=Total+item
                    Total_2dp="%.2f" %Total
                    Total_cost.configure(text="Total cost: ${}".format(Total_2dp))
                with open("order_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows=list(csvreader)
                for item in rows:
                    if item[0]==user_id and item[1]==Order_number:
                        row_index=rows.index(item)
                update_value("order_database.csv",row_index,"Total amount",Total_2dp)
                # Update the cart_table with the new cart_list.
                cart_table.delete(*cart_table.get_children())
                for item in cart_list:
                    cart_table.insert('', 'end',values=(item["Name"],item["Quantity"],item["Price"]))  
                with open("orderdetail_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows=list(csvreader)
                    for item in rows:
                        if item[0]==user_id and item[1]==Order_number and item[2]==item_name:
                            rows.remove(item)
                with open("orderdetail_database.csv", 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)
        else:
            messagebox.showerror("Error","Please select the quantity")
            # If the cart is empty, do nothing.
            pass            
    else:
        # If item_quantity is not '0', it means the user wants to add/update the item in the cart.
        cart_item={}
        cart_item["Name"] = item_name
        cart_item["Quantity"] = item_quantity
        cart_item["Price"] = item_price
        # If the spinbox value is not changing which is same as the quantity value in cart, then do nothing.
        if cart_item in cart_list:
            messagebox.showerror("Error","The item has already added into the cart.\nPlease change the quantity to update it")
            pass
        else:
        # If the item is already in the cart, update its quantity.
            for item in cart_list:
                if item["Name"]!=item_name:
                    item_number=item_number+1
            for item in cart_list:
                if item["Name"]==item_name:
                    index=cart_list.index(item)
            if item_number<len(cart_list):
                cart_list[index]["Quantity"]=item_quantity
                price=float(cart_item["Price"].replace('$',""))
                quantity=int(cart_list[index]["Quantity"])
                item_cost=price*quantity
                Totalprice=[]

                for item in cart_list:
                    price_1=float(item["Price"].replace('$',""))
                    quantity=int(item["Quantity"])
                    item_cost=price_1*quantity
                    Totalprice.append(item_cost)
                    Total=0
                    for item in Totalprice:
                        Total=Total+item
                    Total_2dp="%.2f" %Total
                    Total_cost.configure(text="Total cost: ${}".format(Total_2dp))
                with open("order_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows=list(csvreader)
                for item in rows:
                    if item[0]==user_id and item[1]==Order_number:
                        row_index=rows.index(item)
                update_value("order_database.csv",row_index,"Total amount",Total_2dp)
                # Update the cart_table with the updated cart_list.
                cart_table.delete(*cart_table.get_children())
                for item in cart_list:
                    cart_table.insert('', 'end',values=(item["Name"],item["Quantity"],item["Price"])) 
                # Update the corresponding order detail in the 'orderdetail_database.csv'.
                List=[user_id,Order_number,item_name,item_price]
                with open("orderdetail_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows=list(csvreader)
                    for item in rows:
                        if item[0]==user_id and item[1]==Order_number and item[2]==item_name:
                            item[3]=item_quantity
                    with open("orderdetail_database.csv", 'w', newline='') as file:
                        csv_writer = csv.writer(file)
                        csv_writer.writerows(rows)
            else:
                # If the item is not in the cart, add it to the cart_list and recalculate the Total cost.
                cart_list.append(cart_item)
                Totalprice=[]
                for item in cart_list:
                    price_1=float(item["Price"].replace('$',""))
                    quantity=int(item["Quantity"])
                    item_cost=price_1*quantity
                    Totalprice.append(item_cost)
                    Total=0
                    for item in Totalprice:
                        Total=Total+item
                    Total_2dp="%.2f" %Total
                    Total_cost.configure(text="Total cost: ${}".format(Total_2dp))
                with open("order_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows=list(csvreader)
                for item in rows:
                    if item[0]==user_id and item[1]==Order_number:
                        row_index=rows.index(item)
                # Update the cart_table with the new cart_list.
                update_value("order_database.csv",row_index,"Total amount",Total_2dp)
                cart_table.insert('', 'end',values=(item_name,item_quantity,item_price))
                List=[user_id,Order_number,item_name,item_quantity,item_price]
                # Add the new order detail to the 'orderdetail_database.csv'.
                with open("orderdetail_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows=list(csvreader)
                    rows.append(List)
                with open("orderdetail_database.csv", 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)
                    
#When clicking the next page button or last page button, the page will change and show another set of food item
def next_page():
    global page_number

    # If the current page number is equal to the total number of pages, reset to the first page.
    if page_number == total_page_number:
        page_number = 1
    else:
        page_number = page_number + 1

    # Update the page display text.
    display = str(page_number) + '/' + str(total_page_number)
    page_displayed.configure(text=display)
    page_displayed.text = display

    quantity_1 = 0
    quantity_2 = 0
    quantity_3 = 0

    # Check if any items on the current page are already in the cart and get their quantities.
    for item in cart_list:
        if item['Name'] == Menu_index[(page_number-1)*3]['Name']:
            quantity_1 = item['Quantity']

    # Create and configure the first food item on the current page.
    food_item_1 = FoodItem(Menu_index[(page_number-1)*3]['Image_path'], Menu_index[(page_number-1)*3]['Name'], Menu_index[(page_number-1)*3]['Price'], Menu_index[(page_number-1)*3]['Description'], quantity_1, remove_frame=False)
    food_item_1.configure(item1_image, item1_name, item1_price, item1_description, item1_order, item1_quantity)

    # Check if there is a second item on the current page and set its quantity from the cart if available.
    if ((page_number-1)*3+1) < len(Menu_index):
        for item in cart_list:
            if item['Name'] == Menu_index[(page_number-1)*3+1]['Name']:
                quantity_2 = item['Quantity']
        food_item2 = FoodItem(Menu_index[(page_number-1)*3+1]['Image_path'], Menu_index[(page_number-1)*3+1]['Name'], Menu_index[(page_number-1)*3+1]['Price'], Menu_index[(page_number-1)*3+1]['Description'], quantity_2, remove_frame=False)
        food_item2.grid(item2_image, item2_name, item2_price, item2_description, item2_order, item2_quantity)
        food_item2.configure(item2_image, item2_name, item2_price, item2_description, item2_order, item2_quantity)
    else:
        # If there is no second item, create a blank FoodItem with quantity=0 to remove the previous item's details from the UI.
        food_item2 = FoodItem('', '', '', '', quantity=0, remove_frame=True)
        food_item2.configure(item2_image, item2_name, item2_price, item2_description, item2_order, item2_quantity)

    # Check if there is a third item on the current page and set its quantity from the cart if available.
    if ((page_number-1)*3+2) < len(Menu_index):
        for item in cart_list:
            if item['Name'] == Menu_index[(page_number-1)*3+2]['Name']:
                quantity_3 = item['Quantity']
        food_item3 = FoodItem(Menu_index[(page_number-1)*3+2]['Image_path'], Menu_index[(page_number-1)*3+2]['Name'], Menu_index[(page_number-1)*3+2]['Price'], Menu_index[(page_number-1)*3+2]['Description'], quantity_3, remove_frame=False)
        food_item3.grid(item3_image, item3_name, item3_price, item3_description, item3_order, item3_quantity)
        food_item3.configure(item3_image, item3_name, item3_price, item3_description, item3_order, item3_quantity)
    else:
        # If there is no third item, create a blank FoodItem with quantity=0 to remove the previous item's details from the UI.
        food_item3 = FoodItem('', '', '', '', quantity=0, remove_frame=True)
        food_item3.configure(item3_image, item3_name, item3_price, item3_description, item3_order, item3_quantity)

        
def last_page():
    global page_number   
    if page_number==1:
        page_number=total_page_number
    else:
        page_number=page_number-1
    display=str(page_number)+'/'+str(total_page_number)
    page_displayed.configure(text=display)
    page_displayed.text=display
    quantity_1=0
    quantity_2=0
    quantity_3=0
    for item in cart_list:
        if item['Name']==Menu_index[(page_number-1)*3]['Name']:
            quantity_1=item['Quantity']
    food_item_1 = FoodItem(Menu_index[(page_number-1)*3]['Image_path'], Menu_index[(page_number-1)*3]['Name'], Menu_index[(page_number-1)*3]['Price'],Menu_index[(page_number-1)*3]['Description'],quantity_1,remove_frame=False)
    food_item_1.configure(item1_image, item1_name, item1_price, item1_description,item1_order,item1_quantity)
    if ((page_number-1)*3+1)<len(Menu_index):
        for item in cart_list:
            if item['Name']==Menu_index[(page_number-1)*3+1]['Name']:
                quantity_2=item['Quantity']
        food_item2 = FoodItem(Menu_index[(page_number-1)*3+1]['Image_path'], Menu_index[(page_number-1)*3+1]['Name'], Menu_index[(page_number-1)*3+1]['Price'], Menu_index[(page_number-1)*3+1]['Description'],quantity_2,remove_frame=False)
        food_item2.grid(item2_image, item2_name, item2_price, item2_description,item2_order,item2_quantity)
        food_item2.configure(item2_image, item2_name, item2_price, item2_description,item2_order,item2_quantity)
    else:
        food_item2 = FoodItem('', '','', '',quantity=0,remove_frame=True)
        
        food_item2.configure(item2_image, item2_name, item2_price, item2_description,item2_order,item2_quantity)
    if ((page_number-1)*3+2)<len(Menu_index):
        for item in cart_list:
            if item['Name']==Menu_index[(page_number-1)*3+2]['Name']:
                quantity_3=item['Quantity']
        food_item3 = FoodItem(Menu_index[(page_number-1)*3+2]['Image_path'], Menu_index[(page_number-1)*3+2]['Name'], Menu_index[(page_number-1)*3+2]['Price'], Menu_index[(page_number-1)*3+2]['Description'],quantity_3,remove_frame=False)
        food_item3.grid(item3_image, item3_name, item3_price, item3_description,item3_order,item3_quantity)
        food_item3.configure(item3_image, item3_name, item3_price, item3_description,item3_order,item3_quantity)
    else:
        food_item3 = FoodItem('', '','', '',quantity=0,remove_frame=True)
        food_item3.configure(item3_image, item3_name, item3_price, item3_description,item3_order,item3_quantity)

#when clicking the button, delete the selected item from cart
def delete_item():
    if cart_table.selection() == ():
        messagebox.showerror('Error','Please select an item')
        # If no item is selected in the cart table, do nothing.
        pass
    else:
        result = messagebox.askyesno("Delete", "Are you sure?")
        if result == True:
            try:
                selected_item = cart_table.selection()[0]
                current_idx = cart_table.index(selected_item)

                # Remove the corresponding item from the "orderdetail_database.csv" file.
                with open("orderdetail_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows = list(csvreader)
                for item in rows:
                    if item[0] == user_id and item[1] == Order_number and item[2] == cart_list[current_idx]["Name"]:
                        rows.remove(item)
                with open("orderdetail_database.csv", 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)

                # Update the FoodItem objects and remove the item from the cart list and cart table.
                for item in Menu_index:
                    if item["Name"] == cart_list[current_idx]["Name"]:
                        if Menu_index.index(item) == (page_number-1)*3:
                            food_item_1 = FoodItem(item['Image_path'], item['Name'], item['Price'], item['Description'], quantity=0, remove_frame=False)
                            food_item_1.configure(item1_image, item1_name, item1_price, item1_description, item1_order, item1_quantity)
                        elif Menu_index.index(item) == ((page_number-1)*3 + 1):
                            food_item_2 = FoodItem(item['Image_path'], item['Name'], item['Price'], item['Description'], quantity=0, remove_frame=False)
                            food_item_2.configure(item2_image, item2_name, item2_price, item2_description, item2_order, item2_quantity)
                        elif Menu_index.index(item) == ((page_number-1)*3 + 2):
                            food_item_3 = FoodItem(item['Image_path'], item['Name'], item['Price'], item['Description'], quantity=0, remove_frame=False)
                            food_item_3.configure(item3_image, item3_name, item3_price, item3_description, item3_order, item3_quantity)

                # Remove the item from the cart list and cart table.
                cart_list.remove(cart_list[current_idx])
                cart_table.delete(selected_item)

                # Recalculate the total cost and update it in the "order_database.csv" file.
                Totalprice = []
                if cart_list == []:
                    # If the cart is empty, update the total cost to $0.00 in "order_database.csv".
                    Total_cost.configure(text="Total cost: $0.00")
                    with open("order_database.csv", 'r') as file:
                        csvreader = csv.reader(file)
                        rows = list(csvreader)
                    for item in rows:
                        if item[0] == user_id and item[1] == Order_number:
                            row_index = rows.index(item)
                    update_value("order_database.csv", row_index, "Total amount", "0.00")
                else:
                    # If the cart still contains items, recalculate the total cost and update "order_database.csv".
                    for item in cart_list:
                        price_1 = float(item["Price"].replace('$', ""))
                        quantity = int(item["Quantity"])
                        item_cost = price_1 * quantity
                        Totalprice.append(item_cost)
                        Total = 0
                        for item in Totalprice:
                            Total = Total + item
                        Total_2dp = "%.2f" % Total
                        Total_cost.configure(text="Total cost: ${}".format(Total_2dp))
                        with open("order_database.csv", 'r') as file:
                            csvreader = csv.reader(file)
                            rows = list(csvreader)
                        for item in rows:
                            if item[0] == user_id and item[1] == Order_number:
                                row_index = rows.index(item)
                        update_value("order_database.csv", row_index, "Total amount", Total_2dp)
            except:
                pass
        else:
            pass

def deleteall_item():
    if cart_list == []:
        messagebox.showerror("Error","Your cart is empty")
        # If the cart is already empty, do nothing.
        pass
    else:
        result = messagebox.askyesno("Delete All", "Are you sure?")
        if result == True:
            # Set item quantities to zero and clear the cart list and cart table.
            integer_var = IntVar()
            integer_var.set(0)
            integer_var2 = IntVar()
            integer_var2.set(0)
            integer_var3 = IntVar()
            integer_var3.set(0)
            item1_quantity.configure(textvariable=integer_var)
            item2_quantity.configure(textvariable=integer_var2)
            item3_quantity.configure(textvariable=integer_var3)
            Totalcost.clear()
            cart_list.clear()
            cart_table.delete(*cart_table.get_children())

            # Update the total cost to $0.00 in "order_database.csv".
            Total = 0
            for item in Totalcost:
                Total = Total + item
            Total_2dp = "%.2f" % Total
            Total_cost.configure(text="Total cost: ${}".format(Total_2dp))
            with open("order_database.csv", 'r') as file:
                csvreader = csv.reader(file)
                rows = list(csvreader)
            for item in rows:
                if item[0] == user_id and item[1] == Order_number:
                    row_index = rows.index(item)
            update_value("order_database.csv", row_index, "Total amount", Total_2dp)

            # Remove all items associated with the order from "orderdetail_database.csv".
            with open("orderdetail_database.csv", 'r') as file:
                csvreader = csv.reader(file)
                rows = list(csvreader)
                remove_item = []
                for item in rows:
                    if item[0] == user_id and item[1] == Order_number:
                        remove_item.append(item)
                for item in remove_item:
                    rows.remove(item)
                with open("orderdetail_database.csv", 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)
        else:
            pass
            
def logout():
    result=messagebox.askyesno('Log out','Are you sure?')
    if result==False:
        pass
    else:
    # Close the current window and start the login window.
        with open("user_database.csv", 'r') as file:
            csvreader = csv.reader(file)
            rows=list(csvreader)
        for item in rows:
            if item[0]==user_id:
                item[3]="offline"
        with open("user_database.csv", 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(rows)
        window.destroy()
        subprocess.run(['python', 'main_v5_login.py'])

def update_value(csv_file, row_index, column_name, new_value):
    # Update the value of a specific cell in the CSV file at the given row and column.
    with open(csv_file, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        rows = list(csv_reader)
        column_index = rows[0].index(column_name)
        rows[row_index][column_index] = new_value

        with open(csv_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerows(rows)

def pay():
    # Ask for confirmation before proceeding with payment.
    if cart_list==[]:
        messagebox.showerror('Error','Your cart is empty')
    else:
        result = messagebox.askyesno("Pay", "Are you sure?")
        if result == True:
            # Close the current window and start the checkout window for payment.
            window.destroy()
            subprocess.run(['python', 'main_v5_checkout.py'])
        else:
            pass

def open_orderhistory():
    # Create a new window for displaying the order history.
    order_history = Toplevel(window)
    order_history.geometry("370x470")
    order_history.title("New Window")
    order_history.resizable(0, 0)
    order_history.configure(bg="white")

    # Display the title of the order history window.
    title = Label(order_history, text="Order history", font=('Rockwell 21'), bg='#fcc302', fg="white", width=18, padx=30, pady=2)
    title.grid(row=0, column=1)

    # Create a treeview (cart_table) to display the order history.
    cart_table = ttk.Treeview(order_history, column=("Order number", "Name", "Quantity", "Price"), show='headings', height=17)
    style = ttk.Style()
    style.theme_use('clam')
    cart_table.column("# 1", anchor=CENTER, width=120)
    cart_table.heading("# 1", text="Order Number")
    cart_table.column("# 2", anchor=CENTER, width=120)
    cart_table.heading("# 2", text="Name")
    cart_table.column("# 3", anchor=CENTER, width=57)
    cart_table.heading("# 3", text="Quantity")
    cart_table.column("# 4", anchor=CENTER, width=70)
    cart_table.heading("# 4", text="Price")
    cart_table.grid(row=1, column=1, columnspan=3, pady=(25, 0), sticky=E+W+N+S)

    # Populate the cart_table with order history data for the user.
    with open("order_database.csv", 'r') as file:
        csvreader = csv.reader(file)
        rows = list(csvreader)
    with open("orderdetail_database.csv", 'r') as file:
        csvreader1 = csv.reader(file)
        rows1 = list(csvreader1)
    History_list = []
    for item in rows:
        if item[0] == user_id and item[3] == "Paid":
            History_list.append(item[1])
            
    for item in History_list:
        for item1 in rows1:
            if item1[0] == user_id and item1[1] == item:
                cart_table.insert('', 'end', values=(item1[1], item1[2], item1[3], item1[4]))
                
def disable_event():
    messagebox.showerror("Error","Please first log out")
    pass

#Set up the window 
window = Tk()
window.geometry('1020x550')
window.title("Menu")
window.resizable(0, 0)
window.configure(bg="white")
window.protocol("WM_DELETE_WINDOW", disable_event)
#Set up the left frame for category button
left_frame = Frame(window,bg="white")
left_frame.grid(row=0,column=0,rowspan=3,sticky=N)

#Set up the middle frame for food item
middle_frame=Frame(window,bg="white",height=400)
middle_frame.grid(row=0, column=1,rowspan=3,padx=(20,0),pady=(62,0),sticky=N)

#Set up the right frame for cart
right_frame=Frame(window,bg="white",width=100)
right_frame.grid(row=0, column=2,rowspan=3,sticky=N)

#Set up all the category buttons and menu title
menu_title = Label(left_frame,text="Our Menu",font=('Rockwell 21'),bg='#fcc302',fg="white",width=9,padx=30,pady=2)
menu_title.grid(row=0,column=0,columnspan=2)
category_1=Button(left_frame,text=category_name[0],font=('serif 13'),bg="yellow",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,state="disabled",command=lambda:selected_button(category_1,0))
category_1.grid(row=1,column=0,columnspan=2,pady=(25,0),sticky=W)
category_2=Button(left_frame,text=category_name[1],font=('serif 13'),bg="white",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,command=lambda:selected_button(category_2,1))
category_2.grid(row=2,column=0,columnspan=2,pady=(12,0),sticky=W)
category_3=Button(left_frame,text=category_name[2],font=('serif 13'),bg="white",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,command=lambda:selected_button(category_3,2))
category_3.grid(row=3,column=0,columnspan=2,pady=(12,0),sticky=W)
category_4=Button(left_frame,text=category_name[3],font=('serif 13'),bg="white",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,command=lambda:selected_button(category_4,3))
category_4.grid(row=4,column=0,columnspan=2,pady=(12,0),sticky=W)
category_5=Button(left_frame,text=category_name[4],font=('serif 13'),bg="white",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,command=lambda:selected_button(category_5,4))
category_5.grid(row=5,column=0,columnspan=2,pady=(12,0),sticky=W)
category_6=Button(left_frame,text=category_name[5],font=('serif 13'),bg="white",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,command=lambda:selected_button(category_6,5))
category_6.grid(row=6,column=0,columnspan=2,pady=(12,0),sticky=W)
category_7=Button(left_frame,text=category_name[6],font=('serif 13'),bg="white",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,command=lambda:selected_button(category_7,6))
category_7.grid(row=7,column=0,columnspan=2,pady=(12,0),sticky=W)
category_8=Button(left_frame,text=category_name[7],font=('serif 13'),bg="white",width=22,activebackground="#FBFF3C",activeforeground="black",padx=5,pady=5,command=lambda:selected_button(category_8,7))
category_8.grid(row=8,column=0,columnspan=2,pady=(12,0),sticky=W)
Logout_button=Button(left_frame,text="Log out",width=9,command=logout)
Logout_button.grid(row=9,column=0,sticky=N,pady=22,padx=20)
Orderhistory_button=Button(left_frame,text="Order history",width=10,command=open_orderhistory)
Orderhistory_button.grid(row=9,column=1,sticky=N,pady=22,padx=(20,0))

#Set up GUI for each food items' image, name, price and description.
food_item1=Frame(middle_frame,bg='white')           
food_item1.grid(row=0,column=0,pady=(0,51),padx=0)

food_image1=Image.open(Menu_index[0]["Image_path"])
resized_image = food_image1.resize((150, 100))
food_image1 = ImageTk.PhotoImage(resized_image)
item1_image=Label(food_item1,image='',bg="white",height=100,width=150)
item1_image.grid(row=0,column=0,rowspan=4,sticky=NW)
item1_name=Label(food_item1,text=Menu_index[0]['Name'],bg="white",font=("Arial", 15, "bold"),width=20,anchor=W)
item1_name.grid(row=0,column=1,columnspan=3,sticky=NW,padx=(0,100))
item1_description=Label(food_item1,text=Menu_index[0]['Description'],justify="left",anchor=W,bg="white",wraplength=330,font=("Arial", 9),width=50)
item1_description.grid(row=1,column=1,columnspan=3,padx=0,sticky=NW)
item1_price=Label(food_item1,text=Menu_index[0]['Price'],justify="left",fg="red",wraplength=350,font=("Arial", 12),pady=7,width=10)
item1_price.grid(row=2,column=2,sticky=W,padx=15)
item1_quantity=Spinbox(food_item1,from_=0,to=10,width=5,state="readonly")
item1_quantity.grid(row=2,column=1,sticky=W+E+N+S,padx=3)
item1_order=Button(food_item1,text="ORDER",fg="white",bg="red",width=9,font=("Arial", 11,"bold"),command=lambda: add_order(item1_name.cget('text'),item1_quantity.get(),item1_price.cget('text')))
item1_order.grid(row=2,column=3,sticky=W) 

food_item2=Frame(middle_frame,bg='white')           
food_item2.grid(row=1,column=0,pady=(0,51),padx=0)

food_image2=Image.open(Menu_index[0]["Image_path"])
resized_image2 = food_image2.resize((150, 100))
food_image2 = ImageTk.PhotoImage(resized_image)
item2_image=Label(food_item2,image=food_image2,bg="white",height=100,width=150)
item2_image.grid(row=0,column=0,rowspan=4,sticky=NW)
item2_name=Label(food_item2,text=Menu_index[0]['Name'],bg="white",font=("Arial", 15, "bold"),width=20,anchor=W)
item2_name.grid(row=0,column=1,columnspan=3,sticky=NW,padx=(0,100))
item2_description=Label(food_item2,text=Menu_index[0]['Description'],justify="left",anchor=W,bg="white",wraplength=330,font=("Arial", 9),width=50)
item2_description.grid(row=1,column=1,columnspan=3,padx=0,sticky=NW)
item2_price=Label(food_item2,text=Menu_index[0]['Price'],justify="left",fg="red",wraplength=350,font=("Arial", 12),pady=7,width=10)
item2_price.grid(row=2,column=2,sticky=W,padx=15)
item2_quantity=Spinbox(food_item2,from_=0,to=10,width=5,state="readonly")
item2_quantity.grid(row=2,column=1,sticky=W+E+N+S,padx=3)
item2_order=Button(food_item2,text="ORDER",fg="white",bg="red",width=9,font=("Arial", 11,"bold"),command=lambda: add_order(item2_name.cget('text'),item2_quantity.get(),item2_price.cget('text')))
item2_order.grid(row=2,column=3,sticky=W)

food_item3=Frame(middle_frame,bg='white')           
food_item3.grid(row=2,column=0,pady=(0,0),padx=0)

food_image3=Image.open(Menu_index[0]["Image_path"])
resized_image3 = food_image3.resize((150, 100))
food_image3 = ImageTk.PhotoImage(resized_image3)
item3_image=Label(food_item3,image=food_image3,bg="white",height=100,width=150)
item3_image.grid(row=0,column=0,rowspan=4,sticky=NW)
item3_name=Label(food_item3,text=Menu_index[0]['Name'],bg="white",font=("Arial", 15, "bold"),width=20,anchor=W)
item3_name.grid(row=0,column=1,columnspan=3,sticky=NW,padx=(0,100))
item3_description=Label(food_item3,text=Menu_index[0]['Description'],justify="left",anchor=W,bg="white",wraplength=330,font=("Arial", 9),width=50)
item3_description.grid(row=1,column=1,columnspan=3,padx=0,sticky=NW)
item3_price=Label(food_item3,text=Menu_index[0]['Price'],justify="left",fg="red",wraplength=350,font=("Arial", 12),pady=7,width=10)
item3_price.grid(row=2,column=2,sticky=W,padx=15)
item3_quantity=Spinbox(food_item3,from_=0,to=10,width=5,state="readonly")
item3_quantity.grid(row=2,column=1,sticky=W+E+N+S,padx=3)
item3_order=Button(food_item3,text="ORDER",fg="white",bg="red",width=9,font=("Arial", 11,"bold"),command=lambda: add_order(item3_name.cget('text'),item3_quantity.get(),item3_price.cget('text')))
item3_order.grid(row=2,column=3,sticky=W)

#Set up the page change button and page displayed label
page_change=Frame(window,bg='white')
page_change.place(x=400,y=480)
page_displayed=Label(page_change,borderwidth=1,width=7,text=str(page_number)+'/'+str(total_page_number),bg="white",font=("Arial", 13),relief="solid")
page_displayed.grid(row=0,column=1,sticky=N,pady=(20))
icon_image1=Image.open("11.png")
resized_icon = icon_image1.resize((30, 20))
left_arrowicon = ImageTk.PhotoImage(resized_icon)
Bunext_page=Button(page_change,image=left_arrowicon,command=next_page)
Bunext_page.grid(row=0,column=2,padx=10)
icon_image2=Image.open("b033.png")
resized_icon = icon_image2.resize((30, 20))
right_arrowicon = ImageTk.PhotoImage(resized_icon)
Bulast_page=Button(page_change,image=right_arrowicon,command=last_page)
Bulast_page.grid(row=0,column=0,padx=(0,10))
if total_page_number==1:
    Bunext_page.configure(state="disabled")
    Bulast_page.configure(state="disabled")
#Set up the cart
cart_title = Label(right_frame,text="Your Cart",font=('Rockwell 21'),bg='#fcc302',fg="white",width=11,padx=30,pady=3)
cart_title.grid(row=0,column=0,columnspan=3)
cart_table=ttk.Treeview(right_frame, column=("Name", "Quantity","Price"), show='headings', height=17)
style=ttk.Style()
style.theme_use('clam')

cart_table.column("# 1",anchor=CENTER,width=120)
cart_table.heading("# 1", text="Name")
cart_table.column("# 2", anchor=CENTER,width=57)
cart_table.heading("# 2", text="Quantity")
cart_table.column("# 3", anchor=CENTER,width=70)
cart_table.heading("# 3", text="Price")
cart_table.grid(row=1,column=0,columnspan=3,pady=(25,0))
with open("order_database.csv", 'r') as file:
    csvreader = csv.reader(file)
    order=list(csvreader)
for item in order:
    if item[0]==user_id and item[1]==Order_number and item[3]=="unpaid":
        Total_amount=item[2]
Total_cost=Label(right_frame,text="Total cost: ${}".format(Total_amount),bg="white",font=('Arial 19'),width=15,anchor=W)
with open("orderdetail_database.csv", 'r') as file:
    csvreader = csv.reader(file)
    order=list(csvreader)
# Update the 'cart_table' to display the user's specific order details
# Also, populate the 'cart_list' with the order details for later use
# And set the 'initial_quantity' variables for each item based on user's order
for item in order:
    if item[0]==user_id and item[1]==Order_number:
        cart_table.insert('', 'end',values=(item[2],item[3],item[4]))  
        cart_item={}
        cart_item["Name"] = item[2]
        cart_item["Quantity"] = item[3]
        cart_item["Price"] = item[4]
        cart_list.append(cart_item)
        if item[2]==Menu_index[0]["Name"]:
          initial_quantity1=item[3]
        elif item[2]==Menu_index[1]["Name"]:
            initial_quantity2=item[3]
        elif item[2]==Menu_index[2]["Name"]:
            initial_quantity3=item[3]
Total_cost.grid(row=2,column=0,sticky=W,columnspan=3,pady=10)
delete_button=Button(right_frame,text="Delete",width=9,command=delete_item)
delete_button.grid(row=3,column=0,sticky=N,pady=9)
deleteall_button=Button(right_frame,text="Delete All",width=9,command=deleteall_item)
deleteall_button.grid(row=3,column=1,sticky=N,pady=9)
pay_button=Button(right_frame,text="Pay",width=9,command=pay)
pay_button.grid(row=3,column=2,sticky=N,pady=9)

#class the food item
#use init method to set the attribute for each food item,including image, name, price,description
#use grid method to locate each component 
#use configure method to configure each component
class FoodItem:
    def __init__(self,image_path,name,price,description,quantity,remove_frame=False):
        self.image_path=image_path
        self.name=name
        self.price=price
        self.description=description
        self.quantity=quantity
        self.remove_frame=remove_frame
    def grid(self, item_image, item_name, item_price, item_description,item_order,item_quantity):
            item_image.grid(row=0,column=0,rowspan=4,sticky=NW)
            item_name.grid(row=0,column=1,columnspan=3,sticky=NW,padx=(0,100))
            item_description.grid(row=1,column=1,columnspan=3,padx=0,sticky=NW)
            item_price.grid(row=2,column=2,sticky=W,padx=15)
            item_quantity.grid(row=2,column=1,sticky=W+E+N+S,padx=3)
            item_order.grid(row=2,column=3,sticky=W) 

    def configure(self, item_image, item_name, item_price, item_description,item_order,item_quantity):
        if self.remove_frame:
            item_image.grid_remove()
            item_name.grid_remove()
            item_price.grid_remove()
            item_description.grid_remove()
            item_order.grid_remove()
            item_quantity.grid_remove()
        else:
            food_image = Image.open(self.image_path)
            resized_image = food_image.resize((150, 100))
            self.image = ImageTk.PhotoImage(resized_image)
            item_image.image = self.image 
            item_image.configure(image=self.image)
            item_name.configure(text=self.name)
            item_price.configure(text=self.price)
            item_description.configure(text=self.description)
            integer_var = IntVar()
            integer_var.set(self.quantity)
            item_quantity.configure(textvariable=integer_var)
            
#Set the value of each attribute for each food item
food_item1 = FoodItem(Menu_index[0]['Image_path'], Menu_index[0]['Name'], Menu_index[0]['Price'], Menu_index[0]['Description'],initial_quantity1,remove_frame=False)
food_item1.configure(item1_image, item1_name, item1_price, item1_description,item1_order,item1_quantity)

food_item2 = FoodItem(Menu_index[1]['Image_path'], Menu_index[1]['Name'], Menu_index[1]['Price'], Menu_index[1]['Description'],initial_quantity2,remove_frame=False)
food_item2.configure(item2_image, item2_name, item2_price, item2_description,item2_order,item2_quantity)

food_item3 = FoodItem(Menu_index[2]['Image_path'], Menu_index[2]['Name'], Menu_index[2]['Price'], Menu_index[2]['Description'],initial_quantity3,remove_frame=False)
food_item3.configure(item3_image, item3_name, item3_price, item3_description,item3_order,item3_quantity)

window.mainloop()
