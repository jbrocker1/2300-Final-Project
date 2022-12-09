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
    delete_item()
    return


#Inserts item into DBMS
def delete_item():
    validInput = False

    print("---DELETE an Item from Inventory---\n")
    prompt = input("press ENTER to continue or q to quit")
    if prompt.lower == 'q':
        return
    clearScreen()

    view_items()
    return
    
        




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
    

    


if __name__ == '__main__':
    cnx = connection.MySQLConnection(user='Daniel', password='Ethernet754',
                                    host='grocerydatabase.c18yikjkwckw.us-east-2.rds.amazonaws.com', database="ProjectG")
    cursor = cnx.cursor()
    main()
    cursor.close()
    cnx.close()
