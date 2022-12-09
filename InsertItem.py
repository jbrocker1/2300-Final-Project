from mysql.connector import connection
import random
import datetime
import os
import datetime

def clearScreen():
    print("\033[H\033[J")

def connect():
    cnx = connection.MySQLConnection(user='Daniel', password='Ethernet754',
                                    host='grocerydatabase.c18yikjkwckw.us-east-2.rds.amazonaws.com', database="ProjectG")
    return cnx

def main():
    
    
    
    
    insert_item()
    return


#Inserts item into DBMS
def insert_item():
    connection = connect()
    if not connection.is_connected():
        print("Unable to connect to the database")
        return
    cursor = connection.cursor()
    #Item Attributes
    DEPT = ("Meat","Bakery","Seafood","Deli","Grocery")
    item_date = datetime.date.today()
    item_tax = random.randint(1,4)
    ValidInput = False
    item_location = 0
    item_price = 0.00
    item_stock = 1
    item_profPer = 1
    item_Dep_num = 0

    #Get the most recent item's ID and increase by 1
    cursor.execute("SELECT * FROM ITEM ORDER BY Item_ID DESC LIMIT 1;")
    item_id = cursor.fetchone()[0] + 1

    

    #Welcome message for inserting intems
    print("----Insert Item into Inventory----\n")
    prompt = input("press ENTER to continue or q to quit ")
    if prompt.lower() == 'q':
        return
    clearScreen()
    #Enter item's name and brand
    while not ValidInput:
        print("----Insert Item into Inventory----\n")
        item_name = input("Item name: ")
        item_brand = input("Brand: ")
        if not item_name.isspace() or not item_brand.isspace():
            ValidInput = True
        clearScreen()
    print("----Insert Item into Inventory----\n")
    ValidInput = False
    #Enter item location
    while not ValidInput:
        try:
            item_location = int(input("Item location (Aisle #): "))
            ValidInput = True
        except ValueError as e:
            print("---Please enter a valid NUMBER")
    clearScreen()
    print("----Insert Item into Inventory----\n")
    ValidInput = False
    #Enter item's price
    while not ValidInput:
        try:
            item_price = float(input("Enter item price: $"))
            item_profPer = round(item_price%4*.99,2)
            ValidInput = True
        except ValueError as e:
            print("---Please enter a valid NUMBER")
    clearScreen()
    print("----Insert Item into Inventory----\n")
    ValidInput = False
    #Enter the stock amount
    while not ValidInput:
        try:
            item_stock = int(input("Enter stock amount: "))
            ValidInput = True
        except ValueError as e:
            print("---Please enter a valid NUMBER")
    clearScreen()
    print("----Insert Item into Inventory----\n")
    ValidInput = False
    #Enter department number for the item
    while not ValidInput:
        try:
            print(f"Which department is in charge of {item_brand} {item_name}?\n")
            print(" 1 Meat")
            print(" 2 Bakery")
            print(" 3 Seafood")
            print(" 4 Deli")
            print(" 5 Grocery")
            item_Dep_num = int(input("Select Department based on number (1-5): "))
            ValidInput = item_Dep_num in (1,2,3,4,5)
            clearScreen()
        except ValueError:
            print("---Please enter a valid NUMBER")
            ValidInput = False

    #Confirm
    print("----Insert Item into Inventory----\n")
    print(f"Assigned Item ID: {item_id}")
    print(f"Item name: {item_name}")
    print(f"Item brand: {item_brand}")
    print(f"Item Location: Aisle {item_location}")
    print(f"Item price: ${f'{item_price:.2f}'}")
    print(f"Date Acquired (Today): {item_date}")
    print(f"Calculated Tax Percent: {item_tax}%")
    print(f"Calculated Profit per Item: ${f'{item_profPer:.2f}'}")
    print(f"Item Department: {DEPT[item_Dep_num-1]}")
    prompt = input("\nIs this information correct? y/n ")
    if prompt.lower() != 'y':
        insert_item()

    #Query String
    INSERT_INTO = f"""
    INSERT into ITEM (Item_ID, Item_Name, Brand, Location, Price, Date_Aqrid, Tax_Percent, Stock_Amount, Prof_Per, Dep_Num)
    VALUES({item_id},'{item_name}','{item_brand}','Aisle {item_location}',{item_price},'{item_date}',{item_tax},{item_stock},{item_profPer},{item_Dep_num});
    """
    cursor.execute(INSERT_INTO)
    cursor.close()
    #connection.commit()
    connection.close()
        




    

    


if __name__ == '__main__':
    main()