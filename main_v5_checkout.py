from tkinter import *
from PIL import ImageTk, Image
from csv import writer
from tkinter import messagebox
import csv
import subprocess

# Read user details from the user_database.csv file
with open("user_database.csv", 'r') as file:
    csvreader = csv.reader(file)
    row = list(csvreader)
for item in row:
    if item[3] == "online":
        user_id = item[0]
        username = item[1]

# Read order details from the order_database.csv file
with open("order_database.csv", 'r') as file:
    csvreader = csv.reader(file)
    row = list(csvreader)
for item in row:
    if item[0] == user_id:
        orderNumber = item[1]
        totalPrice = item[2]

# Function to handle order option selection
def orderoption():
    if var.get() == 2:
        Address_ent.configure(state="disabled")
    elif var.get() == 1:
        Address_ent.configure(state="normal")

# Function to handle payment
def pay(Firstname, Lastname, Phonenumber, Address):
    if var.get() == 0:
        messagebox.showerror("Error", "Please select the order option")
    elif var.get() == 1:
        if Fname_ent.get() and Lname_ent.get() and Pnumber_ent.get() and Address_ent.get():
            result = messagebox.askyesno('Pay', 'Are you sure to pay?\n(Check your details carefully)')
            if result == True:
                # Update the order status and user details in order_database.csv
                with open("order_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows = list(csvreader)
                for item in rows:
                    if item[0] == user_id and item[1] == orderNumber:
                        item[3] = "Paid"
                        item.append(Firstname)
                        item.append(Lastname)
                        item.append(str(Phonenumber))
                        item.append(Address)
                with open("order_database.csv", 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)

                # Add a new order to order_database.csv
                rows = [user_id, int(orderNumber) + 1, "0", "unpaid"]
                with open('order_database.csv', 'a', newline='') as f_object:
                    writer_object = csv.writer(f_object)
                    writer_object.writerow(rows)
                    f_object.close()

                # Display success message and restart the main_v5.py
                messagebox.showinfo("Success", "Successfully paid")
                window.destroy()
                subprocess.run(['python', 'main_v5_menu.py'])
            else:
                pass
        else:
            messagebox.showerror("Error", "All the information should be entered")
    elif var.get() == 2:
        if Fname_ent.get() and Lname_ent.get() and Pnumber_ent.get():
            result = messagebox.askyesno('Pay', 'Are you sure to pay?\n(Check your details carefully)')
            if result == True:
                # Update the order status and user details in order_database.csv
                with open("order_database.csv", 'r') as file:
                    csvreader = csv.reader(file)
                    rows = list(csvreader)
                for item in rows:
                    if item[0] == user_id and item[1] == orderNumber:
                        item[3] = "Paid"
                        item.append(Firstname)
                        item.append(Lastname)
                        item.append(str(Phonenumber))
                        item.append("Pick up")
                with open("order_database.csv", 'w', newline='') as file:
                    csv_writer = csv.writer(file)
                    csv_writer.writerows(rows)

                # Add a new order to order_database.csv
                rows = [user_id, int(orderNumber) + 1, "0", "unpaid"]
                with open('order_database.csv', 'a', newline='') as f_object:
                    writer_object = csv.writer(f_object)
                    writer_object.writerow(rows)
                    f_object.close()

                # Display success message and restart the main_v5.py
                messagebox.showinfo("Success", "Successfully paid")
                window.destroy()
                subprocess.run(['python', 'main_v5_menu.py'])
        else:
            messagebox.showerror("Error", "All the information should be entered")

# Function to go back to main_v5.py
def back():
    window.destroy()
    subprocess.run(['python', 'main_v5_menu.py'])
# disable the close window function
def disable_event():
   pass
#GUI setting
window = Tk()
window.geometry('500x450')
window.title("Login")
window.resizable(0, 0)
window.configure(bg="white")
window.protocol("WM_DELETE_WINDOW", disable_event)
left_frame = Frame(window,bg="white")
left_frame.grid(row=0,column=0,sticky=N)
menu_title = Label(left_frame,text="Checkout",font=('Rockwell 21'),bg='#fcc302',fg="white",width=9,padx=30,pady=2)
menu_title.grid(row=0,column=0,columnspan=2,sticky=W)

Username_lbl=Label(left_frame,text="Username: ",bg="white",font=('Arial 13 bold'))
Username_lbl.grid(row=1,column=0,sticky=W,pady=(30,0),padx=(10,0))

Username=Label(left_frame,text="{}".format(username),bg="white",font=('Arial 13'),anchor=S)
Username.grid(row=1,column=1,sticky=W,pady=(30,0))

TotalAmount_lbl=Label(left_frame,text="Total amount: ",bg="white",font=('Arial 13 bold'),anchor=S)
TotalAmount_lbl.grid(row=2,column=0,sticky=W,pady=(5,0),padx=(10,0))

TotalAmount=Label(left_frame,text="${}".format(totalPrice),bg="white",font=('Arial 13'))
TotalAmount.grid(row=2,column=1,sticky=W,pady=(5,0))

Orderoption_lbl=Label(left_frame,text="Order option: ",bg="white",font=('Arial 13 bold'),anchor=S)
Orderoption_lbl.grid(row=3,column=0,sticky=W,pady=(5,0),padx=(10,0))

var=IntVar()
Orderoption=Radiobutton(left_frame,text="Delivery",variable=var,value=1,bg="white",font=('Arial 10'),command=orderoption)
Orderoption.grid(row=3,column=1,sticky=W,pady=(5,0))

Orderoption2=Radiobutton(left_frame,text="Pick up",variable=var,value=2,bg="white",font=('Arial 10'),command=orderoption)
Orderoption2.grid(row=3,column=2,sticky=W,pady=(5,0))

Fname_lbl=Label(left_frame,text="First Name: ",bg="white",font=('Arial 13'))
Fname_lbl.grid(row=4,column=0,sticky=W,pady=(15,0),padx=(10,0))
Fname_ent= Entry(left_frame,bd=3,width=30,font=('Arial 13'))
Fname_ent.grid(row=4, column=1,sticky=W,columnspan=6,pady=(15,0))

Lname_lbl=Label(left_frame,text="Last Name: ",bg="white",font=('Arial 13'))
Lname_lbl.grid(row=5,column=0,sticky=W,pady=(15,0),padx=(10,0))
Lname_ent= Entry(left_frame,bd=3,width=30,font=('Arial 13'))
Lname_ent.grid(row=5, column=1,sticky=W,columnspan=6,pady=(15,0))

Pnumber_lbl=Label(left_frame,text="Phone number: ",bg="white",font=('Arial 13'))
Pnumber_lbl.grid(row=6,column=0,sticky=W,pady=(15,0),padx=(10,0))
Pnumber_ent= Entry(left_frame,bd=3,width=30,font=('Arial 13'))
Pnumber_ent.grid(row=6, column=1,sticky=W,columnspan=6,pady=(15,0))

Address_lbl=Label(left_frame,text="Address: ",bg="white",font=('Arial 13'))
Address_lbl.grid(row=7,column=0,sticky=W,pady=(15,0),padx=(10,0))
Address_ent= Entry(left_frame,bd=3,width=30,font=('Arial 13'))
Address_ent.grid(row=7, column=1,sticky=W,columnspan=6,pady=(15,0))

Pay_button = Button(left_frame, text="Pay",width=20,font=('serif 13'),fg="white",bg="black",command=lambda: pay(Fname_ent.get(),Lname_ent.get(),Pnumber_ent.get(),Address_ent.get()))
Pay_button.grid(row=8,column=2,sticky=E,pady=10)
back_button = Button(left_frame, text="Back",width=10,command=back)
back_button.grid(row=8,column=0,sticky=W,pady=10,padx=(10,0))
window.mainloop()
