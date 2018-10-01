import cx_Oracle
# # 
con = cx_Oracle.connect('system/campusConnect')   #To connect to database with user_name:$id & password:$passwd
cur = con.cursor()
# 
# cust_id = input("\n\t Username/Customer Id : ")
# 
# cur.execute("""SELECT address_line1,address_line2,city,state,pincode
#                FROM CUSTOMERS
#                WHERE customer_id = :cust_id""",{"cust_id":cust_id})
# 
# query_id = cur.fetchall()
#                 
# print(query_id)

# import unittest
# import home as home
# 
# 
# class test(unittest.TestCase):
#     
#     object = home.signInMenu(home.configuration())
#     object.addressChange()
#     
#     
#     
#     
#  UPDATE CUSTOMERS SET 'address_line1' = 'aaaaaa','address_line2' = 'aaaaaaaaaaa','city' = 'aaaaaaaaaaaaa','state' = 'aaaaaaaa','pincode' = 123456,WHERE customer_id = 'C001R'   


# from prettytable import from_db_cursor
# 
# # con = lite.connect('data.db')
#     
# with con:
#     
# #     cur = con.cursor()    
#     cur.execute('SELECT * FROM TRANSACTIONS')   
#     
#     x = from_db_cursor(cur) 
#     
# print(x)

import datetime
 
from prettytable import PrettyTable
 
# print("\n\t from (dd mm yy) - ")
# fromDay = int(input("\n\t\t day     : "))
# fromMonth = int(input("\n\t\t month : "))
# fromYear = int(input("\n\t\t year   : "))
# 
# fromDate = '18-08-08'
# fromDate = datetime.datetime.strptime(fromDate, '%y-%m-%d').strftime('%y-%b-%d')
#  
# print("\n\t to (dd mm yy) - ")
# toDay = int(input("\n\t\t day : "))
# toMonth = int(input("\n\t\t month : "))
# toYear = int(input("\n\t\t year : "))
#  
# toDate = '18-08-28'
# toDate = datetime.datetime.strptime(toDate, '%y-%m-%d').strftime('%y-%b-%d')
 
 
cur.execute("""SELECT TO_CHAR(date_of_transaction),
                                   CASE WHEN from_account_id = 'CA7300877646IN' THEN 'Debit' 
                                        WHEN to_account_id = 'CA7300877646IN' THEN 'Credit'
                                   END CASE,
                                   amount,
                                   CASE WHEN  from_account_id = 'CA7300877646IN' THEN balance_from
                                        WHEN to_account_id = 'CA7300877646IN' THEN balance_to
                                   END CASE
                                   FROM TRANSACTIONS
                                   WHERE TRUNC(date_of_transaction) >= '30-AUG-18' AND TRUNC(date_of_transaction) <= '30-AUG-18'""")
query_rows = cur.fetchall()
 
print(query_rows,len(query_rows))
printDetails = PrettyTable()
 
printDetails.field_names = ["Date", "Type of Transaction", "Amount", "Balance"]
 
for i in range(0,len(query_rows)):
             
#                 for row_list in query_rows[i] :
                     
#                     date = datetime.datetime.strptime(date, '%d-%b-%y').strftime('%d-%b-%y')
#                     
#                     row_list = list(query_rows[i])
#                     row_list[0] = date
                     
#                     print(row_list)
                    printDetails.add_row(query_rows[i])
                     
print(printDetails)




# cur.execute("""INSERT INTO CLOSED_ACCOUNTS (customer_id,account_id,account_type,date_of_closure)
#                                    SELECT customer_id,account_id,account_type,SYSDATE FROM ACCOUNTS WHERE account_id = :acc_id""",{"acc_id":'SA108772323354IN'})
#         
#         
# cur.execute("DELETE FROM ACCOUNTS WHERE account_id = :acc_id",{"acc_id":'SA108772323354IN'})
# 
# con.commit()