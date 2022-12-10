import mysql.connector
import random
import datetime

'''
insert = "INSERT INTO EMPLOYEE(ID, First_Name, Last_Name, DOB, Address, Dep_Num) VALUES (%s, %s, %s, %s, %s, %s)"
data = (2345, "Jimmys", "Johson", datetime.date(2001, 5, 21), "123 black people lane", 2) 

cursor.execute(insert, data)
'''

'''
insert_stmt = (
  "INSERT INTO employees (emp_no, first_name, last_name, hire_date) "
  "VALUES (%s, %s, %s, %s)"
)
data = (2, 'Jane', 'Doe', datetime.date(2012, 3, 23))
cursor.execute(insert_stmt, data)

select_stmt = "SELECT * FROM employees WHERE emp_no = %(emp_no)s"
cursor.execute(select_stmt, { 'emp_no': 2 })
'''
QUIT = 'q'

def update_department_employee_numbers():
    for i in range(1, 6):
            cursor.execute(f"SELECT ID FROM EMPLOYEE WHERE Dep_Num={i}")
            employees = cursor.fetchall()
            numEmps = len(employees)
            cursor.execute(f"UPDATE DEPARTMENT SET Num_Employees={numEmps} WHERE Number={i}")

def add_employee():
    print("Adding an employee! Make sure to welcome them to the team!\n\nPlease enter the following information.\n")
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
        print()

    print("Where will", First_Name, Last_Name, "be working? (Department Number)")
    # getting employee department number
    Dep_Num = input("Department Number: ")
     
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
    print(First_Name, Last_Name, "added")
    # incrementing department number employees of this employee by one
    cursor.execute(f"UPDATE DEPARTMENT SET Num_Employees=Num_Employees-1  WHERE Number={Dep_Num}")

def remove_employee(ID):
    # get all of the employee ids
    cursor.execute("SELECT ID FROM EMPLOYEE")
    Ids = cursor.fetchall()
    Ids = [i[0] for i in Ids]

    # if the id is in the list of employee ids then we know its legit
    if ID in Ids:
        # find the department they work for
        cursor.execute(f"SELECT Dep_Num FROM EMPLOYEE WHERE ID={ID}")
        departmentNumber = cursor.fetchall()[0][0]

        # get the manager of the department they work for
        cursor.execute(f"select ManagerID from DEPARTMENT where Number={departmentNumber}")
        managerID = cursor.fetchall()[0][0]

        # getting the name of the department
        cursor.execute(f"select Name from DEPARTMENT where Number={departmentNumber}")
        depName = cursor.fetchall()[0][0]

        # getting the name of the individual
        cursor.execute(f"select First_Name, Last_Name from EMPLOYEE where ID={ID}")
        name = cursor.fetchall()[0]
        name = name[0] + ' ' + name[1]

        # if they are the manager print a message and kill the remove request
        if managerID == ID:
            print("You are trying to remove a manager. Update the", depName, "manager then you can remove employee", managerID)
            return

        # ask the user if they would like to remove an employee
        userIn = input(f"Are you sure you want to remove {name} ({ID}) from the {depName} department?\n(y/n)")
        if userIn == "y":
            # remove the employee and decrement the number of employees from that department
            cursor.execute(f"DELETE FROM EMPLOYEE WHERE ID={ID}")
            cursor.execute(f"update DEPARTMENT set Num_Employees=Num_Employees-1 where Number={departmentNumber}")
            print(f"{name} removed")
        else:
            print("No action was taken")

    else:
        print(f"{ID} not a valid employee id")

def get_employee_id(fname, lname):
    try:
        cursor.execute(f"select ID from EMPLOYEE where First_Name='{fname}' and Last_Name='{lname}'")
        empid = cursor.fetchall()[0][0]
        return empid
    except Exception as e:
        print(f"{fname} {lname} is an invalid name")

def view_employees():
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

def view_items():
    cursor.execute("select * from ITEM")
    items = cursor.fetchall()

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

    for i in range(7):
        transDate -= timeIterate

    print(transDate)

    departmentProfit = [0, 0, 0, 0, 0]
    
    for transNum in range(110, 200):
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

    # printing prompts along wth list of vendors 
    print("Please select a vendor\n")

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
        print("\033[H\033[J")
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
            print("\033[H\033[J")
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
    displayImage = "\n\t██████╗░███████╗██╗░██████╗  ░██████╗░██████╗░░█████╗░░█████╗░███████╗██████╗░██╗░░░██╗\n\t██╔══██╗██╔════╝╚█║██╔════╝  ██╔════╝░██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗╚██╗░██╔╝\n\t██║░░██║█████╗░░░╚╝╚█████╗░  ██║░░██╗░██████╔╝██║░░██║██║░░╚═╝█████╗░░██████╔╝░╚████╔╝░\n\t██║░░██║██╔══╝░░░░░░╚═══██╗  ██║░░╚██╗██╔══██╗██║░░██║██║░░██╗██╔══╝░░██╔══██╗░░╚██╔╝░░\n\t██████╔╝███████╗░░░██████╔╝  ╚██████╔╝██║░░██║╚█████╔╝╚█████╔╝███████╗██║░░██║░░░██║░░░\n\t╚═════╝░╚══════╝░░░╚═════╝░  ░╚═════╝░╚═╝░░╚═╝░╚════╝░░╚════╝░╚══════╝╚═╝░░╚═╝░░░╚═╝░░░\n\n"

    print(displayImage)

def main():
    print("\033[H\033[J")
    # [('DEPARTMENT',), ('EMERGENCY_CONTACT',), ('EMPLOYEE',), ('ITEM',), ('PRODUCTS',), ('SOLD',), ('TRANSACTION',), ('VENDOR',)]
    
    # simulate_transactions()

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
    # mydb.commit()
    mydb.close()


