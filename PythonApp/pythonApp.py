# Functions
import choices
# To work with MySQL
import pymysql
# For the "press any key" in option 1
from getkey import getkey
# To work with months
import datetime
# To work with Neo4j
from neo4j import exceptions

# Main function
def main():
    display_menu()

    while True:
        choice = input("\nChoice: ")
        
        
        # Choice ONE
        if (choice == "1"):
            # Set the offset for MySQL cypher (next 2 employees)
            offset = 0

            print ("EMPLOYEES AND DEPARTMENTS")
            print ("--------------------------")

            x = choices.one(offset)
            for i in x:
                print (i["name"], "|", i["d.name"])
            print("-- Quit (q) --")
            
            # Loop when pressing any key other then "q"
            while True:
                key = getkey()
                # If any key is pressed
                if key != "q":
                    offset += 2
                    x = choices.one(offset)
                    for i in x:
                        print (i["name"], "|", i["d.name"])
                    print("-- Quit (q) --")
                # If "q" is pressed
                else:
                    offset = 0
                    display_menu()
                    break
        
        # Choice TWO
        elif (choice == "2"):
            print ("SALARY DETAILS")
            print ("--------------------------")

            # Prompt the input
            eid = str(input("Enter Employee ID (EID): "))
    
            x = choices.two(eid)
            # If non-existing EID is entered
            for i in x:
                if i["eid"] == None:
                    print("Minimum", "|", "Avarage ", "|", "Maximum")
                    print("Non existing EID entered. Please try again.")
            # If existign EID is entered
                else:
                    for i in x:
                        print("\nSalary Details For Employee: " + eid)
                        print("Employee name: " + i["name"])
                        print("----------------------------")
                        print("Minimum", "|", "Avarage ", "|", "Maximum")
                        print("----------------------------")
                        print(i["Minimum"], "|", i["Avarage"], "|", i["Maximum"],"\n")
            
        # Choice THREE
        elif (choice == "3"):
            print ("EMPLOYEES BY MONTH OF BIRTH")
            print ("---------------------------")
            
            # Create a list of month names
            month_names = []
            for i in range(1,13):
                month_names.append (((datetime.date(2022, i, 1).strftime('%b'))).upper())
            # Create a list of month numbers
            month_num = []
            for i in range(1,13):
	            month_num.append(str(i)) # Convert to string (because input will be str)
            # Prompt for input
            month = (input("Enter Month of Birth: ")).upper()

            # Loop while the input isn't in either of 2 created lists
            while (month not in month_num) and (month not in month_names):
               month = (input("Enter Month of Birth: ")).upper() # Upper to match lower and upper case
            # If input is a number
            if month in month_num:
                x = choices.three(month)
                for i in x:
                        print(i["eid"], "|", i["name"], "|", i["dob"])
            # If input is a month name  
            elif month in month_names:
                x = choices.three(month)
                for i in x:
                        print(i["eid"], "|", i["name"], "|", i["dob"])
                
        # Choice FOUR
        elif (choice == "4"):
            
            print ("ADD NEW EMPLOYEE")
            print ("----------------")

            # Prompt for inputs
            employeeID = input ("EID: ")
            name = input ("Name: ")
            employeeDob = input ("DOB (YYYY-MM-DD): ")
            deptID = (input ("Dept ID: ")).upper()

            # If all input is valid run the function
            try:
                choices.four(employeeID, name, employeeDob, deptID)
            # ERROR handling
                # If EID or Dept ID input is invalid
            except pymysql.err.IntegrityError as e:
                if e.args[1] == ("Duplicate entry 'e01' for key 'employee.PRIMARY'"):
                    print("*** ERROR ***:", employeeID, " already exists")
                else:
                    print ("*** ERROR ***: ", deptID, "does not exist")
                # If DOB inout is invalid
            except pymysql.err.OperationalError as e:
                print ("*** ERROR ***: Invalid DOB")
                # If EID or Dept ID inputs are too long (limited in SQL database)
            except pymysql.err.DataError as e:
                if e.args[1] == ("Data too long for column 'did' at row 1"):
                    print("*** ERROR ***: ", deptID, "does not exist")
                else:
                    print("*** ERROR ***: EID too long. Use 3 characters max.")
                # Any other errors
            except Exception as e:
                print ("***ERROR***")

        # Choice FIVE
        elif (choice == "5"):
            print ("DEPARTMENTS MANAGED BY EMPLOYEE")
            print ("-------------------------------")

            # Neo4j function
            n = choices.five()
            print ("\nDepartment   |   Budget")

            # Loop through Neo4j results
            for i in n:
                # MySQL function - pass the results from Neo4j to MySQL
                x = choices.fiveSQL(i)
                for a in x:
                    print (a["did"], " | ", a["budget"])

        # Choice SIX
        elif (choice == "6"):
            print ("ADD MANAGER TO DEPARTMENT")
            print ("-------------------------")
            # Prompt for inputs
            eid = input("Enter EID: ")
            did = input ("Enter DID: ")

            x1 = choices.sqlEID(eid)
            x2 = choices.sqlDID(did)

            # Loop if inputs are not in SQL db
            while not x1 or not x2:
                if not x1 and not x2:
                    print ("EID does not exist.")
                    print ("DID does not exist.")
                elif not x1:
                    print ("EID does not exist.")
                elif not x2:
                    print ("DID does not exist.")
                
                eid = input("\nEnter EID: ")
                did = input ("Enter DID: ")

                x1 = choices.sqlEID(eid)
                x2 = choices.sqlDID(did)
            # If inputs are valid
            else:
                for i in x1:
                    eid = (i["eid"])
                for i in x2:
                    did = (i["did"])
            
            # Create Constraint
                # avoids creating a dept managed by multiple managers
            choices.NeoConst()

            # If inputs are valid, call the function
            try:
                choices.six(eid,did)
                print ("Employee", eid, "now manages Department", did,".")
            # If Dept already exists in Neo4j db (constraint)
            except exceptions.ConstraintError as e:
                x = choices.exception(did)
                print ("Department", did, "is already managed by Employee", x, ".")            

        # Choice SEVEN
        elif (choice == "7"):
            print ("VIEW DEPARTMENTS")
            print ("----------------")

            # Append the SQL db to an array to save it in memory
                # If array is empty, append results from SQL and output it
                # If it isn't empty, print out the array
            
            # Output from array (won't run first time when option is chosen)
            try:
                print ("Did    |    Name    |    Location    |    Budget")
                for i in db:
                    print(i["did"], " | ", i["name"], " | ", i["lid"], " | ", i["budget"] )
            # Create an array and append the SQL db (runs when option chosen first time)
            except:
                db = []
                x = choices.seven()
                for i in x:
                    db.append(i)
                for i in db:
                    print(i["did"], " | ", i["name"], " | ", i["lid"], " | ", i["budget"] )
           
        # Choice EIGHT
        elif (choice == "x"):
            break
        else:
            display_menu()
		

# Displaying the menu - Menu function
def display_menu():
    print("Employees")
    print("---------")
    print("")
    print("MENU")
    print("====")
    print("1 - View Employees & Departments")
    print("2 - View Salary Details")
    print("3 - View by Month of Birth")
    print("4 - Add New Employee")
    print("5 - View Departments managed by Employee")
    print("6 - Add Manager to Department")
    print("7 - View Departments")
    print("x - Exit application\n")

if __name__ == "__main__":
	main()