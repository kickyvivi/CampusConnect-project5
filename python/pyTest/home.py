import os, time
from sys import platform
import random,datetime

import cx_Oracle


import re,getpass


class Error(Exception):
    
    """Base class for other exceptions"""
    pass

class invalidNameError(Error):
    
    """Raised when the entered user name is invalid"""
    pass

class invalidAddressError(Error):
    
    """Raised when the entered address is invalid"""
    pass

class invalidPincodeError(Error):
    
    """Raised when the entered pincode is not 6 digit"""

class weakPassword(Error):
    
    """Raised when the entered password doesn't meet the requirements"""
    pass

class passwordMismatch(Error):
    
    """Raised when the passwords doesn't match"""


class invalidCredentials(Error):
    
    """Raised when input password or customer id doesn't match"""


class invalidAccountId(Error):
    
    """Raised when input account id doesn't exist"""
    
    
class invalidCustomerId(Error):
    
    """Raised when input customer id doesn't exist"""    

    

class configuration(object):          #For initial configuration of db & clear function
    
    
    
    def __init__(self): 
        
        
        self.DATE = datetime.datetime.now().date()
        self.TIME = datetime.datetime.now().time()
        
        self.clearFunction()
        self.dbSetup()
        self.dbCredentials()
        
          
    def clearFunction(self):    #Initialising clear
        
         
        ##To clear console according to the platform 
        
        if platform == "linux" or platform == "linux2" or platform == "darwin":
         
            self.clear = lambda: os.system('clear')
             
        elif platform == "win32":
             
            self.clear = lambda: os.system('cls')
            

    def dbSetup(self):          #Initialising db for linux

        ##To set environment variables for installed database 
        
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            
            os.environ['ORACLE_HOME'] = '/u01/app/oracle/product/11.2.0/xe'
            os.environ['LD_LIBRARY_PATH'] = '/u01/app/oracle/product/11.2.0/xe/lib'
        
            print(os.environ.get('ORACLE_HOME'))
            print(os.environ.get('LD_LIBRARY_PATH'))
        
    
    def dbCredentials(self):        #To prompt user for database login credentials
        
        self.id = input('\n Enter your username for database : ')
        self.passwd = input('\n Enter your password for database : ')
        self.dbStart()
    
    
    def dbStart(self):          #To connect to database
        
        self.con = cx_Oracle.connect('{0}/{1}'.format(self.id,self.passwd))   #To connect to database with user_name:$id & password:$passwd
        self.cur = self.con.cursor()
        
    
    def dbStop(self):
        
        self.con.close()
    
     
    def launchMenu(self):
        
        welcomeMenu_Object = mainMenu(self)
    
         

class tableConfiguration (configuration):         #Table for storing aacount no,name,date created,balance,account type,address
    
    
    def __init__(self):

        
        super().__init__()                      #super(tableConfiguration,self).__init__()
        
        self.createTables()
        
        self.launchMenu()
          
    
    def createTables(self):          #To check if CUSTOMERS table already exits or not & if not, create the table
        
        
        self.cur.execute("SELECT table_name FROM all_tables WHERE table_name IN ('CUSTOMERS','ACCOUNTS','CUSTOMER_PASSWORD','CLOSED_ACCOUNTS','TRANSACTIONS')") #Returns the name of tables if they are present in the database

        table_tuple = self.cur.fetchall()   #Returns a list of tuples of relations
        print(table_tuple)
        
        def CREATE_TABLE_CUSTOMERS() :      #For creating relation CUSTOMERS if it doesn't exist
            
            print("table CUSTOMERS does not exist")
                
            self.cur.execute("""CREATE TABLE CUSTOMERS(
                                customer_id VARCHAR2(12)         NOT NULL,
                                first_name VARCHAR2(20)          NOT NULL,
                                last_name VARCHAR2(20)           NOT NULL,
                                address_line1 VARCHAR2(70)       NOT NULL,
                                address_line2 VARCHAR2(70)       NOT NULL,
                                city VARCHAR2(20)                NOT NULL,
                                state VARCHAR2(20)               NOT NULL,
                                pincode NUMBER                   NOT NULL,
                                date_of_sign_up DATE             DEFAULT (SYSDATE),
                                PRIMARY KEY (customer_id))""")
        
        def CREATE_TABLE_ACCOUNTS():        #For creating relation ACCOUNTS if it doesn't exist
            
            print("table ACCOUNTS does not exist")
                
            self.cur.execute("""CREATE TABLE ACCOUNTS(
                                customer_id VARCHAR2(12)    NOT NULL,
                                account_id VARCHAR2(16)     NOT NULL,
                                account_type VARCHAR2(4)    NOT NULL,
                                main_balance FLOAT          NOT NULL,
                                date_created DATE           DEFAULT (SYSDATE),
                                status VARCHAR(2)           DEFAULT 'A',
                                PRIMARY KEY (account_id),
                                FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(customer_id))""")
            
        def CREATE_TABLE_CUSTOMER_PASSWORD():   #For creating relation CUSTOMER_PASSWORD if it doesn't exist
            
            print("table CUSTOMER_PASSWORD does not exist")
                
            self.cur.execute("""CREATE TABLE CUSTOMER_PASSWORD(
                                customer_id VARCHAR2(12)    NOT NULL UNIQUE,
                                password VARCHAR2(20)       NOT NULL,
                                date_modified DATE          DEFAULT (SYSDATE))""")
        
            
        def CREATE_TABLE_CLOSED_ACCOUNTS():     #For creating relation CLOSED_ACCOUNTS if it doesn't exist
            
            print("table CLOSED_ACCOUNTS does not exist")
                
            self.cur.execute("""CREATE TABLE CLOSED_ACCOUNTS(
                                account_id VARCHAR2(16)    NOT NULL UNIQUE,
                                date_of_closure DATE       NOT NULL)""")
            
        def CREATE_TABLE_TRANSACTIONS():        #For creating relation TRANSACTIONS if it doesn't exist
            
            print("table TRANSACTIONS does not exist")
                
            self.cur.execute("""CREATE TABLE TRANSACTIONS(
                                from_account_id VARCHAR2(16)    NOT NULL,
                                to_account_id VARCHAR2(16)      NOT NULL,
                                amount FLOAT                    NOT NULL,
                                date_of_transaction DATE        NOT NULL)""")
        
        
        switchCases = {
                
                'CUSTOMERS'         : CREATE_TABLE_CUSTOMERS,
                
                'ACCOUNTS'          : CREATE_TABLE_ACCOUNTS,
                
                'CUSTOMER_PASSWORD' : CREATE_TABLE_CUSTOMER_PASSWORD,
                
                'CLOSED_ACCOUNTS'   : CREATE_TABLE_CLOSED_ACCOUNTS,
                
                'TRANSACTIONS'      : CREATE_TABLE_TRANSACTIONS 
            
            }
            
        
        table_list = ['CUSTOMERS','ACCOUNTS','CUSTOMER_PASSWORD','CLOSED_ACCOUNTS','TRANSACTIONS']
        
        for i in range(0,len(table_tuple)):
             
            print(i)
            for name in table_tuple[i] :
                
                print(name)
                table_list.remove('{0}'.format(name))
                
        print(table_list)
        
        
        for name in table_list :
            
            print(name)
            switchCases[name]()
        
        
        #To check if all required relations are configured
        self.cur.execute("SELECT table_name FROM all_tables WHERE table_name IN ('CUSTOMERS','ACCOUNTS','CUSTOMER_PASSWORD','CLOSED_ACCOUNTS','TRANSACTIONS')")
        
        if len(self.cur.fetchall()) != 5 :
            
            
            print("\n\tYour database is not correctly configured.Some relations are missing.\n\n\tPlease check your database configuration and try again.....")
            exit()
            


class dbOperations(object):
    
    
    def __init__(self,parent):
        
        self.PARENT = parent

    
    def insertIntoTableCUSTOMERS(self,cust_id,fName,lName,line1,line2,city,state,pin):
        
        self.PARENT.cur.execute("""INSERT INTO CUSTOMERS 
                                 VALUES(:cust_id,:fName,:lName,:line1,:line2,:state,:city,:pinCode,SYSDATE)""",
                                 (cust_id,fName,lName,line1,line2,city,state,pin))
        
        self.PARENT.con.commit()
        print("Table CUSTOMERS updated successfully")
        
    
    def insertIntoTableACCOUNTS(self,cID,aID,acc_type,bal):
        
        self.PARENT.cur.execute("INSERT INTO ACCOUNTS VALUES(:cust_id,:acc_id,:acc_type,:balance,SYSDATE,'A')",(cID,aID,acc_type,bal))
        
        self.PARENT.con.commit()
        print("Table ACCOUNTS updated successfully")
        
        
    def insertIntoTableCUSTOMER_PASSWORD(self,cust_id,passwd):
        
        self.PARENT.cur.execute('INSERT INTO CUSTOMER_PASSWORD VALUES(:cust_id,:password,SYSDATE)',(cust_id,passwd))
        
        self.PARENT.con.commit()
        print("Table CUSTOMER_PASSWORD updated successfully")
    
    
    def insertIntoTableCLOSED_ACCOUNT(self,cust_id):
        
        self.PARENT.cur.execute('INSERT INTO CLOSED_ACCOUNT VALUES(:cust_id)',(cust_id))
        self.PARENT.con.commit()
        print("Table CLOSED_ACCOUNT updated successfully")
        
    
    def insertIntoTableTRANSACTIONS(self,fID,tID,amt):
        
        self.PARENT.cur.execute('INSERT INTO ACCOUNTS VALUES(:from_id,:to_id,:amount)',(fID,tID,amt))
        
        self.PARENT.con.commit()
        print("Table TRANSACTIONS updated successfully")
        
        
    def selectAllFromTable(self,table):
        
        self.PARENT.cur.execute('SELECT * FROM :table_name',(table))
    
    
    def customerAddressChange(self,cust_id,line1,line2,city,state,pincode):
        
        
        self.PARENT.cur.execute("""UPDATE CUSTOMERS
                                   SET address_line1 = :line1,
                                       address_line2 = :line2,
                                       city = :city,
                                       state = :state,
                                       pincode = :pincode,
                                   WHERE customer_id = :cust_id""",(line1,line2,city,state,pincode,cust_id))
        
        self.PARENT.con.commit()
        print("Table CUSTOMERS updated successfully")
        
    
    def customerPasswordChange(self,cust_id,passwd):
        
        
        self.PARENT.cur.execute("""UPDATE CUSTOMERS_PASSWORD
                                   SET password = :password
                                   WHERE customer_id = :cust_id""",(passwd,cust_id))
        
        self.PARENT.con.commit()
        print("Table CUSTOMER_PASSWORD updated successfully")
        
    
    def customerIdGeneration(self):
        
        
        self.PARENT.cur.execute("SELECT MAX(customer_id) FROM CUSTOMERS") 
        
        self.lastId = self.PARENT.cur.fetchall()
        print(self.lastId)
        
        if not self.lastId :
            
            self.cust_id = "C"+"001"+"R"
            print(self.cust_id)
        
        else :
             
            self.cust_id = self.lastId[0][0].strip("CR")
            self.cust_id = '{0:03d}'.format(int(self.cust_id)+1)
            self.cust_id = 'C'+self.cust_id+'R'

            print(self.cust_id)
    
    
    def accountIdGeneration(self,acc_type):
        
        
        self.PARENT.cur.execute("""SELECT MAX(account_id) FROM ACCOUNTS 
                                   WHERE account_type = :acc_type""",(acc_type))
        
        self.lastId = self.PARENT.cur.fetchall()
        print(self.lastId[0][0])
        
        if self.lastId[0][0] is None :
            
            if acc_type == 'C':
            
                self.accountId = str("CA")+str(random.randint(0,9999999999))+str("IN")
                print(self.accountId)
        
            elif acc_type == 'S' :
             
                self.accountId = str("SA")+str(random.randint(0,999999999999))+str("IN")
                print(self.accountId)
            
        else :    
            
            self.accountId = self.lastId[0][0].strip("CAINS")
            self.accountId = int(self.accountId)+1
            
            if acc_type == "C" :
                
                self.accountId = 'CA'+self.accountId+'IN'
            
            else :
                
                self.accountId = 'SA'+self.accountId+'IN'
            
            print(self.cust_id)
        
    
                

class mainMenu(object):
    
    
    def __init__(self,parent):
        
        
        self.PARENT = parent
        self.welcomeScreen()  # To display main menu at start
             
                
    def subMenu(self): # Function to handle user input
        
        if self.choice == 1 :   # sign up
            
            signInMenu_Object = signUpMenu(self.PARENT)
            signInMenu_Object.signUp()
        
        elif self.choice == 2 : # sign in
            
            signInMenu(self.PARENT)
        
        elif self.choice == 3 : # admin sign in
            
            adminSignInMenu(self.PARENT)

        elif self.choice == 4 : # quit
            
            self.quitProgram()
        
        else :                 # Invalid choice 
            
            print("\n Sorry! System can't determine the request....")
            self.welcomeScreen()
    
    
    def welcomeScreen(self): # Function to display main menu & prompting user choice
        
        self.PARENT.clear() # clear console
        
        print("\n\n\n\t Welcome to banking services....... ") # welcome message
        time.sleep(1) # sleep for 2 sec
        
        self.PARENT.clear() # clear console
        
        ##Menu 
        
        print(''' \n\n\t  MENU 
                  
                  1. Sign Up (New Customer)
                  2. Sign In (Existing Customer)
                  3. Admin Sign In
                  4. Quit ''')

        self.choice = int(input('\n Enter your choice : ')) # To capture desired input
    
        self.subMenu() # To interpret user choice & perform specific functions
        
    
    def quitProgram(self):
        
        
        self.PARENT.con.close()
        self.PARENT.clear()
        
        print("\n\n\n\t\tQuitting application......")
        time.sleep(1)
        
        self.PARENT.clear()
        exit()
    

class signUpMenu(dbOperations) :
    
    
    def __init__(self,parent):
        
        
        self.PARENT = parent
        
        self.desposit = 0    # Initializing of deposit money
            
    
    def userAddress(self):
                
            print("\n Address : ")                          # Address of user ( line 1 & 2, city, state, pincode )
            
            while True :
                
                try:
                    self.line1 = input('\n\t Line 1 : ')
                    self.line2 = input('\n\t Line 2 : ')
                    
                    if len(self.line1) < 6 or len(self.line2) < 6 :
                        
                        raise invalidAddressError
                    
                    break
                    
                except invalidAddressError:
                    print("\n\tPlease enter a valid address")
                    time.sleep(0.5)
                    self.PARENT.clear()
                    
            while True :
                    
                try:
                    self.city = input('\n\t City : ')
                    
                    if len(self.city) < 3 :
                        
                        raise invalidAddressError
                    
                    
                    while True :
                        
                        try:
                            self.state = input('\n\t State : ')
                            
                            if len(self.state) < 3 :
                                
                                raise invalidAddressError
                        
                            
                            while True :
                            
                                try:
                                    self.pinCode = int(input('\n\t Pincode : '))    
                                    
                                    if len(str(self.pinCode)) != 6 :
                                        
                                        raise invalidAddressError
                                    
                                    break
                            
                                except invalidAddressError:
                                    print("\n\tPlease enter a 6 digit pincode")
                                    time.sleep(0.5)
                                    self.PARENT.clear()
                            
                                except ValueError:
                                    print("\n\tPlease enter a valid pincode")
                                    time.sleep(0.5)
                                    self.PARENT.clear()
                            break
                        
                        except invalidAddressError:
                            print("\n\tPlease enter a valid state")
                            time.sleep(0.5)
                            self.PARENT.clear()
                        
                    break    
                
                except invalidAddressError:
                    print("\n\tPlease enter a valid city name")
                    time.sleep(0.5)
                    self.PARENT.clear()
                
                    
    
    def userName(self):
                
            while True:
            
                try:
                    print("\n Name : ")                                # Name of user ( fName & lName )
                    self.fName = input('\n\t First Name : ')
                    self.lName = input('\n\t Last Name : ')
                    
                    if not self.fName or not self.lName:
                    
                        raise invalidNameError
                     
                    break 
                     
                except invalidNameError:
                    print("\n\tPlease Enter a valid name")
                    time.sleep(0.5)
                    self.PARENT.clear()
    
    
            
    def accountType(self):   # Function for determining acnt type during sign up
            
            print("\n Choose your account type : "),         # Account type ( savings or current )
            print("\n \t a. Savings Account [s]"),
            print("\t b. Current Account [c]")
            self.accntType = input('\n Enter your choice (s/c) : ')
            self.accntType = self.accntType.upper()
            
            if self.accntType == 'S' :     # Prompt if savings account
                
                decision = input("\n Do you wish to make an initial deposit ? [y/n]")
                if decision.lower() == 'y' : # If chooses to pay
                    
                    self.desposit = int(input('\n Enter the amount to deposit : Rs. '))
                
        
            elif self.accntType == 'C' :   # Prompt if current account
                
                decision = input("\n Note : 'Current account' need a minimum balance of Rs. 5000. \n Do you wish to continue ? [y/n]")
                if decision.lower() == 'y' : # If choice is to make the payment
                    
                    while True :   # To check if entered amount is enough to create an account
                        
                        try:
                            self.PARENT.clear()
                            self.desposit = int(input('\n Enter the amount to deposit : Rs. '))
                            
                        except ValueError: # In case of an invalid input
                            
                            self.PARENT.clear()
                            print("\n\n\n\t Sorry! System can't process your request.... \n\n\t Please enter a valid amount....")
                            time.sleep(1)
                            continue
                        
                        if self.desposit < 5000 :  # Comparing the deposited amount with min bal
                            
                            self.PARENT.clear()
                            print("\n\n\t Note : Current accounts must have a minimum balance of Rs.5000.\n\n\t Please try again.....")
                            time.sleep(1)
                            continue
                        
                        else :
                            
                            break    # To break the loop if condition is satisfied
                
                else :  # Prompt for changing the account type or cancel application
                    
                    decision = input("\n Do you wish to change account type or cancel the process ? [y/q]")
                    if decision.lower() == 'y' :
                        
                        self.accountType()
                    
                    else : # If choice is to cancel application
                        
                        print("\n Processing your request... Please wait.....")
                        time.sleep(1)
                        exit()
                        
#                         mainMenu(self.PARENT).welcomeScreen()
            
            else : 
                
                print("\n Sorry! Our bank doesn't provide this type of account. Please choose from the available options.....")
                time.sleep(1)
                self.accountType()
                
            
    
    def signUp(self): # Function for new user registration data collection
        
        print("\n Please fill the neccessary details below : ")
    
        self.userName()
        self.userAddress()
        self.accountType()
        
        
        self.PARENT.clear()
        
        print("""\t Name :
                 \n\t\t First Name : {0}
                 \n\t\t Last Name : {1}
                 \n\t Address :
                 \n\t\t Line1 : {2}
                 \n\t\t Line2 : {3}
                 \n\t\t City : {4}
                 \n\t\t State : {5}
                 \n\t\t Pincode : {6}
                 \n\t Account type : {7}
                 \n\t Initial deposit : {8}"""
                 .format(self.fName,self.lName,self.line1,self.line2,self.city,self.state,self.pinCode,self.accntType,self.desposit))

        
        decision = input('\n\n Your account is to be created. Do you wish to proceed or quit ? [y/q]')
        
        if decision.lower() == 'y' :
            
            self.PARENT.clear()
            print("\n Processing your request..... Please wait.....")
            time.sleep(1)
            
            self.saveCustomerCredentials()
            
            self.PARENT.clear()
            print("\n Creating user account...... This may take a moment......")
            
#             self.saveCustomerCredentials()
            
            self.saveAccountCredentials()
            self.PARENT.clear()
            
            print("\n\n\t Congrats!!!!!\n\n\t Your Account was successfully created!")
            
            self.printCredentials()
            
            self.saveCustomerPassword()
            
            print("\n\n\t Your password has been successfully updated !")
            
  
    def saveCustomerCredentials(self):
        
        super().__init__(self.PARENT)
        
        self.customerIdGeneration()
        
        self.insertIntoTableCUSTOMERS(self.cust_id, self.fName, self.lName, self.line1, self.line2, self.city, self.state, self.pinCode)
             
    
    def saveAccountCredentials(self):
        
        self.accountIdGeneration(self.accntType)
        
        self.insertIntoTableACCOUNTS(self.cust_id, self.accountId, self.accntType, self.desposit)
        
    
    def printCredentials(self):
        
        
        self.search_num = re.compile(".*[0-9].*") 
        self.search_lowerCase = re.compile(".*[a-z].*")
        self.search_upperCase = re.compile(".*[A-Z].*")
        self.search_specialChar = re.compile(".*[^a-z^A-Z^0-9].*")
        
        while True :
             
                 
            try:    
                print("\n\n\t Your account credentials are : ")
                print("\n\t\t Customer id : ", self.cust_id)
                print("\n\t\t Account id : ", self.accountId)
                print("""\n\n Note : * This customer id will be used as your username from now on
                         \n        * Please remember these details for availing our services""")
                
                print("\n\n Please create a password to make your account secure !")
                print("""\n Password should meet the following necessities : 
                            
                            * contain atleast 8 characters
                            * contain atleast 1 numeric value
                            * contain uppercase alphabets
                            * contain lowercase alphabets
                            * use special characters like */@$! etc..
                            
                            *Don't use your name as password""")
                
                pass1 = getpass.getpass(prompt="\n\n\n\t new password : ")
                
                if len(pass1) >= 8 :
                
                    if self.search_num.match(pass1) and self.search_upperCase.match(pass1) and self.search_lowerCase.match(pass1) and self.search_specialChar.match(pass1):  
                        
                        
                            print("\t\t\t Strong")
                    
                    else :
                        
                            print("\t\t\t Weak")
                            raise weakPassword  
                    
                
                else :
                    
                    raise weakPassword
                
                
                while True :
                    
                    
                    try:
                        self.passwd = getpass.getpass(prompt="\n\t confirm password : ")
                        
                        if pass1 != self.passwd :
                            
                            raise passwordMismatch
                        
                        break
                    
            
                    except passwordMismatch:
                        print("\n\t Passwords doesn't match. Please re-try..")
                        
                break        
            
            except weakPassword:
                print("\n\t Password doesn't meet the requirements..\n\t Please try again!!")
                time.sleep(0.5)
                self.PARENT.clear()   
            
            
    
    def saveCustomerPassword(self):
        
        
        self.insertIntoTableCUSTOMER_PASSWORD(self.cust_id, self.passwd)
    
                
                                
                            
class signInMenu(dbOperations):
    
    
    def __init__(self,parent):
        
        
        self.PARENT = parent
        
        
        self.promptCredentials()
    
    
    def promptCredentials(self):
        
        super().__init__(self.PARENT)
        
        
        turns = 0
        
        while True:
        
                
            try:    
                self.PARENT.clear()
                
                self.cust_id = input("\n\t username/customer-id : ")
                
                self.PARENT.cur.execute("""SELECT customer_id
                                           FROM CUSTOMER_PASSWORD
                                           WHERE customer_id = :cust_id""",{"cust_id" : self.cust_id})
        
                query_id = self.PARENT.cur.fetchall()
                
#                 print(query_id)
                
                if not query_id :
                    
                    raise invalidCustomerId
                
                
                while turns < 3 :
                
                    try:
                        self.PARENT.clear()
                        
                        print("\n\t username/customer-id : ",self.cust_id)
                        self.passwd = getpass.getpass(prompt="\n\t Password : ")
                        
                        self.PARENT.cur.execute("""SELECT password
                                                   FROM CUSTOMER_PASSWORD
                                                   WHERE customer_id = :cust_id""",{"cust_id" : self.cust_id})
        
                        
                        query_passwd = self.PARENT.cur.fetchall()
                        
                        if query_passwd[0][0] != self.passwd :
                            
                            turns += 1
                            raise invalidCredentials
                            
                        
                        break
                    
                    
                    except invalidCredentials:
                        print("\n\n\t Username or Password doesn't match.\n\t Please try again....")
                        time.sleep(1.2)
                    
                
                break
                
            except invalidCustomerId:
                print("\n\n\t There is no user registered with this id.\n\t Please enter a valid id....")
                time.sleep(1.2)
                
        
        if turns < 3 :
            
            self.PARENT.clear() # clear console
        
            print("\n\n\n\t Welcome back....... ") # welcome message
            time.sleep(1) # sleep for 2 sec
            
            self.signInSubMenu()
        
        else :
            
            self.PARENT.clear()
            print("\n\n\n\t Sorry! Too many incorrect login attempts..\n\n\t Your account is locked..")
            exit()
            
    
    
    def signInSubMenu(self):
        
        
        self.PARENT.clear() # clear console
        
        ##Sub-menu for signIn
        
        print(''' \n\n\t  MENU 
                  
                  1. Address Change
                  2. Money Deposit
                  3. Money Withdrawal
                  4. Print Statement
                  5. Transfer Money
                  6. Account Closure
                  7. Customer Logout ''')

        self.signInChoice = int(input('\n Enter your choice : ')) # To capture desired input
        
        
        self.userChoice() # To interpret user choice & perform specific tasks

    
    def userChoice(self):
        
        if self.signInChoice == 1 :         # Address Change
            
            self.addressChange()

        elif self.signInChoice == 2 :       # Money Deposit
            
            self.depositMoney()
    
        elif self.signInChoice == 3 :       # Money Withdrawal
            
            self.withDrawMoney()

        elif self.signInChoice == 4 :       # Print Statement
            
            self.printStatement()

        elif self.signInChoice == 5 :       # Transfer Money
            
            self.moneyTransfer()

        elif self.signInChoice == 6 :       # Account Closure
            
            self.closeAccount()
        
        elif self.signInChoice == 7 :       # Customer Logout
            
            self.customerLogout()

        else :
            
            print("\n Sorry! System can't determine the request....")
            self.signInSubMenu()
     
     
     
    def addressChange(self):
        
        self.PARENT.clear()
        
        self.PARENT.cur.execute("""SELECT address_line1,address_line2,city,state,pincode
                                   FROM CUSTOMERS
                                   WHERE customer_id = :cust_id""",{"cust_id":self.cust_id})
         
        query_address = self.PARENT.cur.fetchall()
        
    
        signUpMenu_Object = signUpMenu(self.PARENT)
        
        signUpMenu_Object.userAddress()
        
        self.PARENT.clear()
        
        print("""\n\t Old addresss is : 
                 \n\t\t line1     : {0}
                 \n\t\t line2     : {1}
                 \n\t\t city      : {2}
                 \n\t\t state     : {3}
                 \n\t\t pincode   : {4}"""
                 .format(query_address[0][0],query_address[0][1],query_address[0][2],query_address[0][3],query_address[0][4]))
        
        
        
        print("""\n\t New addresss is : 
                 \n\t\t line1     : {0}
                 \n\t\t line2     : {1}
                 \n\t\t city      : {2}
                 \n\t\t state     : {3}
                 \n\t\t pincode   : {4}"""
                 .format(signUpMenu_Object.line1,signUpMenu_Object.line2,signUpMenu_Object.city,signUpMenu_Object.state,signUpMenu_Object.pinCode))
        
        
        decision = input("\n\n\t Do you wish to proceed ? [y/n]")
        
        
        if(decision.upper() == 'Y') :
            
            self.PARENT.clear()
            
            print("\n\t Please wait... Your request is being processed....")
            
            self.customerAddressChange(self.cust_id,signUpMenu_Object.line1,signUpMenu_Object.line2,signUpMenu_Object.city,signUpMenu_Object.state,signUpMenu_Object.pinCode)
            time.sleep(1)
            
            print("\n\n\t Address updated successfully")
            time.sleep(1)
            
        
        self.signInSubMenu()
            
            
if __name__ == '__main__':

    
    initialObject = tableConfiguration()