import re,time
from getpass import getpass


class Error(Exception):
    
    """Base class for other exceptions"""
    pass

class weakPassword(Error):
    
    """Raised when the entered password doesn't meet the requirements"""
    pass

class passwordMismatch(Error):
    
    """Raised when the passwords doesn't match"""

search_num = re.compile(".*[0-9].*") 
search_lowerCase = re.compile(".*[a-z].*")
search_upperCase = re.compile(".*[A-Z].*")
search_specialChar = re.compile(".*[^a-z^A-Z^0-9].*")

while True :
             
                 
            try:    
                print("\n\n Please create a password to make your account secure !")
                print("""\n Password should meet the following necessities : 
                            
                            * contain atleast 8 characters
                            * contain atleast 1 numeric value
                            * contain uppercase alphabets
                            * contain lowercase alphabets
                            * use special characters like */@$! etc..
                            
                            *Don't use your name as password""")
                
                pass1 = getpass(prompt="\n\n\n\t new password : ")
                
                if len(pass1) >= 8 :
                
                    if search_num.match(pass1) and search_upperCase.match(pass1) and search_lowerCase.match(pass1) and search_specialChar.match(pass1):  
                        
                        
                            print("\t\t Strong")
                    
                    else :
                        
                            print("\t\t Weak")
                            raise weakPassword  
                    
                
                else :
                    
                    raise weakPassword
                
                
                while True :
                    
                    
                    try:
                        pass2 = getpass(prompt="\n\t confirm password : ")
                        
                        if pass1 != pass2 :
                            
                            raise passwordMismatch
                        
                        break
                    
            
                    except passwordMismatch:
                        print("\n\t Passwords doesn't match. Please re-try..")
                        
                break        
            
            except weakPassword:
                print("\n\t Password doesn't meet the requirements..\n\t Please try again!!")
                time.sleep(0.5)
                
                
                
                
                
                
                
                
SELECT cust.customer_id,cust.first_name,cust.last_name,fsum.fdAmount FROM CUSTOMERS cust JOIN(SELECT customer_id,SUM(amount) AS fdAmount FROM FD_ACCOUNTS GROUP BY customer_id) fsum ON cust.customer_id = fsum.customer_id;

SELECT cust.customer_id,cust.first_name,cust.last_name,lsum.loanAmount FROM CUSTOMERS cust JOIN(SELECT ACCOUNTS.customer_id,SUM(amount) AS loanAmount FROM ACCOUNTS,LOAN_ACCOUNTS GROUP BY ACCOUNTS.customer_id HAVING ACCOUNTS.customer_id IN (SELECT customer_id FROM ACCOUNTS INNER JOIN LOAN_ACCOUNTS ON ACCOUNTS.account_id = LOAN_ACCOUNTS.savings_acc_id)) lsum ON cust.customer_id = lsum.customer_id;



SELECT customer_id,first_name,last_name FROM CUSTOMERS WHERE customer_id IN (SELECT customer_id FROM CUSTOMERS MINUS SELECT customer_id FROM FD_ACCOUNTS);

SELECT customer_id,first_name,last_name FROM CUSTOMERS WHERE customer_id IN (SELECT customer_id FROM CUSTOMERS MINUS SELECT customer_id FROM ACCOUNTS INNER JOIN LOAN_ACCOUNTS ON LOAN_ACCOUNTS.savings_acc_id = ACCOUNTS.account_id);

SELECT customer_id,first_name,last_name FROM CUSTOMERS WHERE customer_id IN (SELECT customer_id FROM CUSTOMERS MINUS (SELECT customer_id FROM FD_ACCOUNTS UNION SELECT customer_id FROM ACCOUNTS INNER JOIN LOAN_ACCOUNTS ON LOAN_ACCOUNTS.savings_acc_id = ACCOUNTS.account_id)); 