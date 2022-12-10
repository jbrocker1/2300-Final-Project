import os

# check install of a certain python library
try:
    import mysql.connector
except ImportError:
    os.system("pip install mysql-connector-python")

import random
import datetime
import time

QUIT = 'q'

def clearScreen():
    print("\033[H\033[J", flush=True)

def update_department_employee_numbers():
    for i in range(1, 6):
            cursor.execute(f"SELECT ID FROM EMPLOYEE WHERE Dep_Num={i}")
            employees = cursor.fetchall()
            numEmps = len(employees)
            cursor.execute(f"UPDATE DEPARTMENT SET Num_Employees={numEmps} WHERE Number={i}")

def add_employee():
    clearScreen()
    print("----Adding Employee----\n")
    userInput =input("Are you sure you want to add an employee? (y/n): ")
    if userInput != 'y':
        return
    clearScreen()
    print("----Adding Employee----\n")
    print("Enter the new employees information below\n")
    # asking for user input to input an employee
    First_Name = input("First Name: ")
    Last_Name = input("Last Name: ")
    DOB = input("Date of Birth (YYYY-MM-DD): ")
    Address = input("Address: ")
    
    # giving list of department names and numbers to the user
    cursor.execute("select Number from DEPARTMENT")
    departmentNumbers = cursor.fetchall()
    departmentNames = []
    for depNumb in departmentNumbers:
        cursor.execute("select Name from DEPARTMENT where Number={}".format(depNumb[0]))
        departmentNames.append(cursor.fetchall()[0][0])

    print()
    for i in range(len(departmentNumbers)):
        depNumber = departmentNumbers[i]
        depName = departmentNames[i]
        print(depNumber[0], ":", depName)

    print("\nWhere will", First_Name, Last_Name, "be working? (Department Number)\n")
    # getting employee department number
    Dep_Num = input("Department Number: ")

    clearScreen()
    print("----Adding Employee----\n")
    print("Is the following information correct?\n")
    print("First Name:", First_Name)
    print("Last Name:", Last_Name)
    print("Date of Birth:", DOB)
    print("Address:", Address)
    print("Department Number:", Dep_Num)
    validation = input("\n(y/n): ")
    if validation != 'y':
        add_employee()
    else: 
        # get all of the used IDs in the data base already
        cursor.execute("SELECT ID FROM EMPLOYEE")
        Ids = cursor.fetchall()
        Ids = [i[0] for i in Ids]

        # generate a new id that is not used
        ID = random.randint(111111, 999999)
        while ID in Ids:
            ID = random.randint(111111, 999999)

        # adding new employee to the data base
        insertStatment = "INSERT INTO EMPLOYEE(ID, First_Name, Last_Name, DOB, Address, Dep_Num) VALUES(%s, %s, %s, %s, %s, %s)"
        data = (ID, First_Name, Last_Name, DOB, Address, Dep_Num)
        cursor.execute(insertStatment, data)
        # incrementing department number employees of this employee by one
        cursor.execute(f"UPDATE DEPARTMENT SET Num_Employees=Num_Employees+1  WHERE Number={Dep_Num}")
        # adding emergency contact
        randNames = ("Rachel","Emilee","Ron","Chris","Lauren","Ethan","Daniel","Andrew","Stacie","Bob")
        phoneNum = f"{random.randint(511,699)}-{random.randint(100,900)}-{random.randint(2000,9000)}"
        cursor.execute(f"insert into EMERGENCY_CONTACT (Employee_ID, Emergency_Name, Phone_num, Address) VALUES({ID},'{random.choice(randNames)}','{phoneNum}','123 Spooner Street');")

        view_employees(ID)
        print("\nEmployee Added\n")
        input("Press ENTER to continue")

def remove_employee():
    # get all of the employee ids
    cursor.execute("SELECT ID FROM EMPLOYEE")
    Ids = cursor.fetchall()
    Ids = [i[0] for i in Ids]

    run = True

    while run:
        clearScreen()
        print("----Remove Employees----")
        checkcont = input("\nWould you like to remove an employee? (y/n): ")
        if checkcont != "y":
            return

        validID = False
        while not validID:
            clearScreen()
            print("----Remove Employees----")
            view_employees(abortContinue=True)
            print("(or press {} to quit)".format(QUIT))
            removedID = input("\nEnter Employee ID: ")
            if removedID == QUIT:
                return
            try:
                ID = int(removedID)
                if ID in Ids:
                    validID = True
                else:
                    print("This employee doesn't exist")
                    time.sleep(2)
            except:
                print("Not a valid input")
                time.sleep(2)
                

        # find the department they work for
        cursor.execute(f"SELECT Dep_Num FROM EMPLOYEE WHERE ID={ID}")
        departmentNumber = cursor.fetchall()[0][0]

        # get the manager of the department they work for
        cursor.execute(f"select ManagerID from DEPARTMENT where Number={departmentNumber}")
        managerID = cursor.fetchall()[0][0]

        # getting the name of the department
        cursor.execute(f"select Name from DEPARTMENT where Number={departmentNumber}")
        depName = cursor.fetchall()[0][0]

        # if they are the manager print a message and kill the remove request
        if managerID == ID:
            print("You are trying to remove a manager. Update the", depName, "manager then you can remove employee", managerID)

        else:
            # ask the user if they would like to remove an employee
            view_employees(ID)
            userIn = input("\nAre you sure you would like to remove the above employee? (y/n): ")
            if userIn == "y":
                # remove the employee and decrement the number of employees from that department
                cursor.execute(f"delete from EMERGENCY_CONTACT where Employee_ID={ID}")
                cursor.execute(f"DELETE FROM EMPLOYEE WHERE ID={ID}")
                cursor.execute(f"update DEPARTMENT set Num_Employees=Num_Employees-1 where Number={departmentNumber}")
                print("Employee Removed")
                run = False
            else:
                print("No action was taken")

        input("Press ENTER to continue")

def get_employee_id():
    clearScreen()
    print("----Get Employee ID----")
    cont = input("\nWould you like to get an employee ID? (y/n): ")
    if cont == 'y':
        clearScreen()
        print("----Get Employee ID----")
        fname = input("\nEmployee First Name: ")
        lname = input("Employee Last Name: ")
        try:
            cursor.execute(f"select ID from EMPLOYEE where First_Name='{fname}' and Last_Name='{lname}'")
            empid = cursor.fetchall()[0][0]
            print('\n' + fname, lname, "ID:", empid)
        except Exception as e:
            print(f"\n{fname} {lname} is an invalid name")

        input("\nPress ENTER to continue")

def view_employees(ID=-1, *, abortContinue=False):
    clearScreen()

    print("----Employees---\n")
    if ID != -1:
        cursor.execute(f"select * from EMPLOYEE where ID={ID}")
        employees = cursor.fetchall()

    else:
        cursor.execute("select * from EMPLOYEE")
        employees = cursor.fetchall()

    print("----------------------------------------------------------------------------------------------------------------------")
    print("|     ID     |   First Name  |   Last Name   | Hours Worked |      DOB      |        Address        | Department Num |")
    print("----------------------------------------------------------------------------------------------------------------------")

    for emp in employees:
        outputString = "|"
        # number of spaces availeable in each section
        stringData = [12, 15, 15, 14, 15, 23, 16] 
        # getting data from employee
        empData = [emp[0], emp[1], emp[2], emp[3], emp[4], emp[5], emp[6]]
        # for every employee
        for i in range(len(empData)):
            # store the data
            data = str(empData[i])
            # len of the data string
            dataLen = len(data)
            # available spaces in the spot
            aSpaces = stringData[i]
            # number of spaces left open
            numSpaces = aSpaces - dataLen
            # if we have too much data chop a few spots off the end and add a ...
            if numSpaces < 0:
                outputString += data[:aSpaces-3]
                outputString += "..."
            # otherwise store the data and add enough white spaces to the end to keep formating consistent
            else:
                outputString += data
                for i in range(numSpaces):
                    outputString += " "
            outputString += "|"

        print(outputString)

    print("----------------------------------------------------------------------------------------------------------------------")

    if ID == -1 and not abortContinue:
        input("Press ENTER to contiue")

def view_items(item_id = -1):
    if item_id == -1:
        cursor.execute("select * from ITEM")
        items = cursor.fetchall()
    else:
        cursor.execute(f"select * from ITEM where Item_ID = {item_id}")
        items = cursor.fetchall()

    clearScreen()
    print("----Items----\n")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("|  ID  |      Name     |      Brand     |  Location  |   Price ($)  |  Date Aquired  | Tax% | Stock Amount | Profit Per Unit ($) | Department Number | Vendor Company |")
    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    for item in items:
        outputString = "|"
        itemData = [item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9], item[10]]
        stringData = [6, 15, 16, 12, 14, 16, 6, 14, 21, 19, 16] 
        for i in range(len(itemData)):
            # store the data
            data = str(itemData[i])
            # len of the data string
            dataLen = len(data)
            # available spaces in the spot
            aSpaces = stringData[i]
            # number of spaces left open
            numSpaces = aSpaces - dataLen
            # if we have too much data chop a few spots off the end and add a ...
            if numSpaces < 0:
                outputString += data[:aSpaces-3]
                outputString += "..."
            # otherwise store the data and add enough white spaces to the end to keep formating consistent
            else:
                outputString += data
                for i in range(numSpaces):
                    outputString += " "
            outputString += "|"

        print(outputString)

    print("-----------------------------------------------------------------------------------------------------------------------------------------------------------------------")

#Insert itme into DBMS
def insert_item():
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

    
    clearScreen()
    #Welcome message for inserting intems
    print("----Insert Item into Inventory----\n")
    prompt = input("press ENTER to continue or q to quit ")
    if prompt.lower() == QUIT:
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
            item_Dep_num = int(input("\nSelect Department based on number (1-5): "))
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
        clearScreen()
        insert_item()
    else:
        #Query String
        INSERT_INTO = f"""
        INSERT into ITEM (Item_ID, Item_Name, Brand, Location, Price, Date_Aqrid, Tax_Percent, Stock_Amount, Prof_Per, Dep_Num)
        VALUES({item_id},'{item_name}','{item_brand}','Aisle {item_location}',{item_price},'{item_date}',{item_tax},{item_stock},{item_profPer},{item_Dep_num});
        """
        cursor.execute(INSERT_INTO)
        clearScreen()
        view_items(item_id)
        input("\nItem added. Press ENTER to continue...")
        clearScreen()
    return

#removes item into DBMS
def delete_item():
    validInput = False
    IDs = []
    #welcome message
    clearScreen()
    print("---DELETE an Item from Inventory---\n")
    prompt = input("press ENTER to continue or q to quit")
    if prompt.lower() == QUIT:
        return
    clearScreen()
    print("---DELETE an Item from Inventory---\n")
    view_items()
    #get item ids
    cursor.execute("select Item_ID from ITEM;")
    rawOut = cursor.fetchall()
    for id in rawOut:
        IDs.append(id[0])
    #user prompted to select item to delete based on ID 
    while not validInput:
        try:
            item_id = int(input("\nSelect item to remove based on ID: (Vendor items cannot be removed)"))
            validInput = item_id in IDs and item_id not in (100,101,102,103,104,105,106)
        except ValueError:
            print("---Please insert a valid item ID---")
    clearScreen()
    print("---DELETE an Item from Inventory---\n")
    view_items(item_id)
    prompt = input("\nWARNING! Are you sure you want to delete this item? y/n ")
    if prompt.lower() != 'y':
        clearScreen()
        delete_item()
    clearScreen()
    print("---DELETE an Item from Inventory---\n")
    #query to delete the item
    cursor.execute(f"delete from ITEM where Item_ID={item_id}")
    input("Item removed. Press ENTER to continue")
    clearScreen()
    return 

#modifies item in DBMS
def modify_item():
    validInput = False
    DEPS = ("Meat","Bakery","Seafood","Deli","Grocery")
    IDs = []
    #welcome message
    clearScreen()
    print("---MODIFY an Item from Inventory---\n")
    prompt = input("press ENTER to continue or q to quit")
    if prompt.lower() == QUIT:
        return
    clearScreen()
    print("---MODIFY an Item from Inventory---\n")
    view_items()
    #get item ids
    cursor.execute("select Item_ID from ITEM;")
    rawOut = cursor.fetchall()
    for id in rawOut:
        IDs.append(id[0])
    #Select item to be modified
    while not validInput:
        try:
            item_id = int(input("\nSelect item to modify based on ID (Vendor items cannot be modified): "))
            validInput = item_id in IDs and item_id not in (100,101,102,103,104,105,106,107,108) 
        except ValueError:
            print("---Please insert a valid item ID---")
    
    #select which attribute to be modified
    validInput = False
    while not validInput:
        try:
            clearScreen()
            print("---MODIFY an Item from Inventory---\n")
            view_items(item_id)
            print(" 1 Name ")
            print(" 2 Brand ")
            print(" 3 Location ")
            print(" 4 Price ")
            print(" 5 Stock amount ")
            print(" 6 Department Number ")
            prompt = int(input("\nSelect attribute to modify based on number (some attribbutes may not be modified): "))
            validInput = prompt in (1,2,3,4,5,6)
        except ValueError:
            print("---Please insert a valid number---")
    validInput = False
    clearScreen()
    
    if prompt == 1:
        while not validInput:
            print("---MODIFY an Item from Inventory---\n")
            newName = input("Enter the new name for the item: ")
            prompt = input(f"Item's name will be changed to {newName}. Is this correct? y/n ")
            clearScreen()
            if prompt.lower()=='y' and not prompt.isspace():
                validInput = True
                cursor.execute(f"UPDATE ITEM set Item_Name='{newName}' where Item_ID = {item_id}")
                clearScreen()

                
    elif prompt == 2:
        while not validInput:
            print("---MODIFY an Item from Inventory---\n")
            newName = input("Enter the new brand for the item: ")
            prompt = input(f"Item's brand will be changed to {newName}. Is this correct? y/n ")
            clearScreen()
            if prompt.lower()=='y' and not prompt.isspace():
                validInput = True
                cursor.execute(f"UPDATE ITEM set Brand='{newName}' where Item_ID = {item_id};")
                clearScreen()
 
    elif prompt == 3:
        while not validInput:
            try:
                print("---MODIFY an Item from Inventory---\n")
                newAisle = int(input("Enter a new aisle number for the item: "))
                prompt = input(f"Item's location will be changed to aisle {newAisle}. Is this correct? y/n ")
                clearScreen()
                if prompt.lower()=='y' and not prompt.isspace():
                    validInput = True
                    cursor.execute(f"UPDATE ITEM set Location='Aisle {newAisle}' where Item_ID = {item_id};")
                    clearScreen()

            except ValueError:
                print("Please enter a valid number")
                clearScreen()
    elif prompt == 4:
        while not validInput:
            try:
                    
                print("---MODIFY an Item from Inventory---\n")
                newPrice = float(input("Enter a new price for the item: $ "))
                print(f"The calculated profit for this item has been updated to ${f'{round(newPrice%4*.95,2):.2f}'}")
                prompt = input(f"Item's price will be changed to ${f'{newPrice:.2f}'} Is this correct? y/n ")
                
                clearScreen()
                if prompt.lower()=='y' and not prompt.isspace():
                    validInput = True
                    cursor.execute(f"UPDATE ITEM set Price={newPrice} where Item_ID = {item_id};")
                    cursor.execute(f"UPDATE ITEM set Prof_Per={round(newPrice%4*.95,2)} where Item_ID = {item_id};")
                    clearScreen()
                    
            except ValueError:
                print("Please enter a valid number")
                clearScreen()
    elif prompt == 5:
        while not validInput:
            try:
                print("---MODIFY an Item from Inventory---\n")
                newStock = int(input("Enter a new stock amount for the item: "))
                prompt = input(f"Item's stock amount will be changed to {newStock}. Is this correct? y/n ")
                clearScreen()
                if prompt.lower()=='y' and not prompt.isspace():
                    validInput = True
                    cursor.execute(f"UPDATE ITEM set Stock_Amount={newStock} where Item_ID = {item_id};")
                    clearScreen()
                    
            except ValueError:
                print("Please enter a valid number")
                clearScreen()
    elif prompt == 6:
        
        while not validInput:
            print("---MODIFY an Item from Inventory---\n")
            try:
                print(f"Which department would you like to change the item to?\n")
                print(" 1 Meat")
                print(" 2 Bakery")
                print(" 3 Seafood")
                print(" 4 Deli")
                print(" 5 Grocery")
                item_Dep_num = int(input("\nSelect Department based on number (1-5): "))
                clearScreen()
                
                prompt = input(f"Item's department will be changed to {DEPS[item_Dep_num-1]}. Is this correct? y/n ")
                clearScreen()
                if prompt.lower()=='y' and not prompt.isspace() and item_Dep_num in (1,2,3,4,5):
                    print("Im here")
                    validInput = True
                    cursor.execute(f"UPDATE ITEM set Dep_Num={item_Dep_num} where Item_ID = {item_id};")
                    clearScreen()
            except ValueError:
                print("---Please enter a valid NUMBER")
        
    clearScreen()
    print("---Item Modified---\n")
    view_items(item_id=item_id)
    input("\nPress ENTER to continue...")
    return
    
def simulate_transactions():
    # getting item information
    cursor.execute("select Item_ID from ITEM")
    itemIds = cursor.fetchall()
    itemIds = [i[0] for i in itemIds]

    # getting names of employees
    cursor.execute("select First_Name from EMPLOYEE")
    empNames = cursor.fetchall()

    transDate = datetime.date.today()
    timeIterate = datetime.timedelta(days=1)

    transDate -= timeIterate

    print(transDate)

    departmentProfit = [0, 0, 0, 0, 0]
    
    for transNum in range(200, 230):
        print("working on", transNum)
        # transaction item information
        numItems = random.randint(3, 30)
        soldItemIds = random.choices(itemIds, k=numItems)

        # moving the day forward based on probability of a random variable
        changeDay = random.random()
        if changeDay > 0.75:
            transDate += timeIterate

        # string version of the day to add into the transaction
        transDateString = str(transDate)
        
        paymentType = random.choice(["Check", "Card", "Cash"])

        subTotal = 0
        totalTax = 0
        totalProfit = 0

        cursor.execute(f"insert into TRANSACTION (Trans_Number, Date) values ({transNum}, '{transDateString}')")

        for itemId in soldItemIds:
            # getting name if item sold
            cursor.execute("select Item_Name from ITEM where Item_ID={}".format(itemId))
            itemName = cursor.fetchall()[0][0]

            # adding sold table into db
            cursor.execute(f"insert into SOLD (Trans_Number, Item_Name, Item_ID) values ({transNum}, '{itemName}', {itemId})")

            # decrement the stock of these items
            cursor.execute(f"update ITEM set Stock_Amount=Stock_Amount-1 where Item_ID={itemId}")

            # calculating price information
            cursor.execute(f"select Price, Tax_Percent, Prof_Per, Dep_Num from ITEM where Item_ID={itemId}")
            itemPriceInfo = cursor.fetchall()

            price = itemPriceInfo[0][0]
            taxPercent = itemPriceInfo[0][1]
            profit = itemPriceInfo[0][2]
            departmentNum = itemPriceInfo[0][3]

            departmentProfit[departmentNum - 1] += profit

            totalProfit += profit
            totalTax += (price * (taxPercent / 100))
            subTotal += price

        total = subTotal + totalTax

        randName = random.choice(empNames)[0]
        
        # updateing the transaction with price information
        cursor.execute(f"update TRANSACTION set Payment_Type='{paymentType}', Customer_Name='{randName}', Total={total}, Sub_Total={subTotal}, Tax={totalTax}, Store_Profit={totalProfit} where Trans_Number={transNum}")

    for i in range(len(departmentProfit)):
        depProfit = departmentProfit[i]
        depNum = i + 1
        cursor.execute(f"update DEPARTMENT set Sales={depProfit}+Sales where Number={depNum}")
 
def vendor_menu():
    # getting company names from data base
    cursor.execute("select Company from VENDOR")
    vendorCompanys = cursor.fetchall()
    vendorCompanys = [vc[0] for vc in vendorCompanys]

    clearScreen()
    print("----Vendor Menu----")
    cont = input("\nAre you sure you want to view the vendor menu? (y/n): ")
    if cont != 'y':
        return
    clearScreen()
    print("----Vendor Menu----")
    # printing prompts along wth list of vendors 
    print("\nPlease select a vendor\n")

    for vCI in range(len(vendorCompanys)):
        print(vCI, ": ",  vendorCompanys[vCI], sep="")
    print(f"{QUIT}: to quit")
        
    # get and validate user input
    userVendorIndex = input("\nSelect vendor based on number: ")

    possibleInputs = [str(i) for i in range(len(vendorCompanys))] 
    possibleInputs.append(QUIT)

    while userVendorIndex not in possibleInputs:
        print("That vendor does not exist. Please try again")
        userVendorIndex = input("Select vendor based on number: ")

    # loop variable
    run = False if userVendorIndex == QUIT else True

    while run:
        # use the user index input to get the  name of the vendor they wish to look at
        userVendorIndex = int(userVendorIndex)
        vendorName = vendorCompanys[userVendorIndex]

        # clear screen and prompt for various actions they can do
        clearScreen()
        print("----Vendor Menu----\n")
        print("What would you like to know about {}?\n".format(vendorName))
        print("0: Operational Hours")
        print("1: Aisle Location")
        print("2: Sales")
        print("3: Items Sold")
        print(f"{QUIT}: Leave menu")

        # input validation
        possibleInputs = ['0', '1', '2', '3', QUIT]

        userVendorSpecificIn = input("\nEnter your choice here: ")
        while userVendorSpecificIn not in possibleInputs:
            print("What you entered was not a viable input")
            userVendorSpecificIn = input("Enter your choice here: ")
        
        # switch cases for possible inputs
        if userVendorSpecificIn == '0':
            cursor.execute(f"select OperationHrs from VENDOR where Company='{vendorName}'")
            operHours = cursor.fetchall()[0][0]
            print(f"\n{vendorName}'s Operating hours are {operHours}")

        elif userVendorSpecificIn == '1':
            cursor.execute(f"select Aisles from VENDOR where Company='{vendorName}'")
            aisle = cursor.fetchall()[0][0]
            print(f"\n{vendorName} items can be found in aisle {aisle}")
            
        elif userVendorSpecificIn == '2':
            cursor.execute(f"select Sales from VENDOR where Company='{vendorName}'")
            sales = cursor.fetchall()[0][0]
            print(f"\n{vendorName} has made ${sales} in sales in total")

        elif userVendorSpecificIn == '3':
            cursor.execute(f"select Item_ID, Item_Name, Brand from ITEM where Vend_Company='{vendorName}'")
            items = cursor.fetchall()
            clearScreen()
            print(f"The following is a list if items sold by {vendorName}\n")
            # formating in order to list the items a vendor sells
            print("-------------------------------------------")
            print("|   ID   |    Name    |       Brand       |")
            print("-------------------------------------------")

            stringData = [8, 12, 19] 

            for item in items:
                itemData = [item[i] for i in range(len(item))]
                outputString = '|'

                for i in range(len(itemData)):
                    idString = str(itemData[i])
                    dataLen = len(idString)
                    aSpaces = stringData[i]
                    numSpaces = aSpaces - dataLen

                    if numSpaces < 0:
                        outputString += idString[:-3] + "..."
                    else:
                        outputString += idString + (numSpaces * " ")

                    outputString += "|"

                print(outputString)
            print("-------------------------------------------")
                
            
        elif userVendorSpecificIn == QUIT:
            run = False
        else:
            raise ValueError("You entered something weird that we didn't know how to handle")

        # continuation validation input
        if run:
            input("\nPress ENTER to continue")

def print_welcome():
    displayImage = "\n\n\n\n\t██████╗░███████╗██╗░██████╗  ░██████╗░██████╗░░█████╗░░█████╗░███████╗██████╗░██╗░░░██╗\n\t██╔══██╗██╔════╝╚█║██╔════╝  ██╔════╝░██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚██╗░██╔╝\n\t██║░░██║█████╗░░░╚╝╚█████╗░  ██║░░██╗░██████╔╝██║░░██║██║░░╚═╝█████╗░░██████╔╝░╚████╔╝░\n\t██║░░██║██╔══╝░░░░░░╚═══██╗  ██║░░╚██╗██╔══██╗██║░░██║██║░░██╗██╔══╝░░██╔══██╗░░╚██╔╝░░\n\t██████╔╝███████╗░░░██████╔╝  ╚██████╔╝██║░░██║╚█████╔╝╚█████╔╝███████╗██║░░██║░░░██║░░░\n\t╚═════╝░╚══════╝░░░╚═════╝░  ░╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░\n\n\n\n\n"

    print(displayImage)

def get_transaction_report():
    cursor.execute("select Date, Store_Profit from TRANSACTION")
    transactions = cursor.fetchall()
    
    currentDate = datetime.date.today()
    timeDelta = datetime.timedelta(days=1)
    iterDate = currentDate - (timeDelta * 7)

    profPerDay = []
    while iterDate < currentDate:
        dayProfit = 0
        for transaction in transactions:
            if transaction[0] == iterDate:
                dayProfit += transaction[1]

        iterDate += timeDelta
        profPerDay.append(dayProfit)


    clearScreen()

    graphHeight = 28
    graphWidth = 24
    graph = [['|' if i == 0 else '-' for i in range(graphWidth)] for j in range(graphHeight)]

    minDayProfit = min(profPerDay)
    maxDayProfit = max(profPerDay)
    averageDayProfit = sum(profPerDay) / len(profPerDay)
    normalizedProfit = [round(((p - minDayProfit) * (graphHeight - 1)) / (maxDayProfit - minDayProfit)) for p in profPerDay]

    print("\nHere are the following statistics for all transasctions over the last week\n")
    print("Minimum Total Day Profit: ${}".format(round(minDayProfit, 2)))
    print("Maximum Total Day Profit: ${}".format(round(maxDayProfit, 2)))
    print("Average Day Profit: ${}".format(round(averageDayProfit, 2)))
    print()

    xIter = graphWidth // 6

    for col in range(1, graphWidth - xIter):
        percent = ((col % xIter) / xIter)
        currentDayIndex = col // xIter
        if percent != 0:
            todayProf = normalizedProfit[currentDayIndex]
            tomorowProf = normalizedProfit[currentDayIndex + 1]
            currentProf = round(((tomorowProf - todayProf) * percent) + todayProf)
        else:
            currentProf = normalizedProfit[currentDayIndex]

        graph[currentProf][col] = '█'

    for row in graph:
        for col in row:
            print(col, end='  ')
        print()
    for i in range(graphWidth * 3):
        print('-', end='')
    print("\n\t\t\tProfit vs Time (Weekly)\n")

    input("press ENTER to continue")
    return # just for you daniel (D)

def main():
    run = True
    while run:
        clearScreen()

        print_welcome()

        print("What would you like to do?\n")
        print("0: Add Employee")
        print("1: Remove Employee")
        print("2: Get Employee ID")
        print("3: View Employees")
        print("4: Insert Items")
        print("5: Delete Item")
        print("6: Modify Item")
        print("7: View Items")
        print("8: Vendor Menu")
        print("9: Weekly Sales Report")
        print(f"{QUIT}: Quit")
        
        possibleInputs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', QUIT, '69']

        userInput = input("\nMenu Selection: ")
        while userInput not in possibleInputs:
            print("Invalid Input")
            userInput = input("Menu Selection: ")

        if userInput == '0':
            add_employee()
        elif userInput == '1':
            remove_employee()
        elif userInput == '2':
            get_employee_id()
        elif userInput == '3':
            view_employees()
        elif userInput == '4':
            insert_item()
        elif userInput == '5':
            delete_item()
        elif userInput == '6':
            modify_item()
        elif userInput == '7':
            view_items()
            input("Press ENTER to continue")
        elif userInput == '8':
            vendor_menu()
        elif userInput == '9':
            get_transaction_report()
        elif userInput == "69":
            clearScreen()
            print("\n\n\n\n\t\t███╗░░██╗██╗░█████╗░███████╗\n\t\t████╗░██║██║██╔══██╗██╔════╝\n\t\t██╔██╗██║██║██║░░╚═╝█████╗░░\n\t\t██║╚████║██║██║░░██╗██╔══╝░░\n\t\t██║░╚███║██║╚█████╔╝███████╗\n\t\t╚═╝░░╚══╝╚═╝░╚════╝░╚══════╝\n\n")
            time.sleep(0.5)
        elif userInput == QUIT:
            print("\nHave a good day!!")
            run = False

if __name__ == "__main__":
    # initialize connection to data base
    mydb = mysql.connector.connect(
            host="grocerydatabase.c18yikjkwckw.us-east-2.rds.amazonaws.com",
            user="Ethan",
            password="Password1!",
            database="ProjectG"
    )

    cursor = mydb.cursor()

    # running program
    main()

    # closing and saving connections and data
    cursor.close()
    mydb.commit()
    mydb.close()


