#!/usr/bin/env python3
import psycopg2
import sys

#####################################################
##  Database Connection
#####################################################

def openConnection():
    # connection parameters - ENTER YOUR LOGIN AND PASSWORD HERE
    userid = "y22s1c9120_qilu3337"
    passwd = "Ltx981024#*"
    myHost = "soit-db-pro-2.ucc.usyd.edu.au"

    # Create a connection to the database
    conn = None
    try:
        # Parses the config file and connects using the connect string
        conn = psycopg2.connect(database=userid,
                                    user=userid,
                                    password=passwd,
                                    host=myHost)
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
    
    # return the connection to use
    return conn



'''
Validate employee login based on username and password
'''
def checkEmpCredentials(username, password):  
    conn=openConnection() # get connection to postgresql
    curs= conn.cursor()   # get cursor
    #error handle
    try:
        curs.execute('SELECT * FROM Employee WHERE UserName = %s ', (username,)) # execute the sql query for the current user's details.
        result = curs.fetchone()  # get the user's details tuple.
        #convert the tuple to list
        if result != None:
            user_detail_list=[]
            if result[3] == password:
                user_detail_list.append(result[0])
                user_detail_list.append(result[1])
                user_detail_list.append(result[2])
                user_detail_list.append(result[3])
                user_detail_list.append(result[4])
                user_detail_list.append(result[5])
                user_detail_list[0]=int(user_detail_list[0])
                user_detail_list[1]=str(user_detail_list[1])
                conn.close() #release resource    
                return user_detail_list
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Error Invalid Login")            
    conn.close()   #release resource                     
    return None



'''
List all the associated tests in the database for an employee
'''
def findTestsByEmployee(username):
    conn= openConnection() # get connection to postgresql
    curs= conn.cursor() # get cursor
    # error handle
    try:
        curs.execute("""SELECT testid, testdate, regno, TestStatusDesc ,techni.name, testeng.name, techni.username,testeng.username
    FROM Testevent JOIN employee techni ON technician=techni.userid JOIN employee testeng ON testengineer = testeng.userid JOIN TestStatus ON Status=TestStatusCode
    WHERE techni.UserName = %s OR testeng.UserName = %s ORDER BY (status ='TODO', status ='INPROG',status ='FAIL', status = 'PASS') DESC , testdate""", (username,username,)) # execute the sql query for all test belong to current user
        result_fe = curs.fetchall() # get all the event list
        #convert each of the envent list to a dictionary then add them to the return list     
        return_list=[]
        for row in result_fe:            
            result_dict = {'test_id': str(row[0]),'test_date':row[1].strftime("%Y-%m-%d"), 'regno': row[2], 'status': row[3], 'technician':row[4], 'testengineer': row[5],'technicianuser': username}
            return_list.append(result_dict)    
        else:
            conn.close() #release resource 
            return return_list
        
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])               
        conn.close() #release resource   
        return None
                



'''
Find a list of test events based on the searchString provided as parameter
See assignment description for search specification
'''
def findTestsByCriteria(searchString):
    conn=openConnection() # get connection to postgresql
    curs= conn.cursor() # get cursor
    #fuzzy search
    search=searchString.lower() #handle the case sensetive
    #if the searchstring is only spaces then return the user's events
    # if search.isspace():
    #     return findTestsByEmployee(routes.user_details['username'])
    search='%'+search+'%' #handle the string in LIKE clause in postgresql's fuzzy search
    # error handle
    try:
        curs.execute("""SELECT testid, testdate, regno, TestStatusDesc ,techni.name, testeng.name,  techni.username ,testeng.username
        FROM Testevent JOIN employee techni ON technician=techni.userid JOIN employee testeng ON testengineer = testeng.userid JOIN TestStatus ON Status=TestStatusCode 
        WHERE lower(TestStatusDesc) LIKE %sOR lower(regno) LIKE %s OR lower(techni.name) LIKE %s OR lower(testeng.name) LIKE %s
        ORDER BY (status ='TODO', status ='INPROG',status ='FAIL', status = 'PASS') DESC , testdate""",(search,search,search,search,))# execute the sql query for event satified the search requirements.
        event_find= curs.fetchall() # get all the result from sql query
        if event_find != None:
        #convert each of the envent list to a dictionary then add them to the return list
            return_event=[]
            for row in event_find:
                if routes.user_details['role']=='Technician':
                    event_dict = {'test_id':row[0], 'test_date':row[1].strftime("%Y-%m-%d"), 'regno': row[2], 'status': row[3], 'technician':row[4], 'testengineer': row[5],'technicianuser': row[6] }
                    return_event.append(event_dict)
                elif routes.user_details['role']=='TestEngineer':
                    event_dict = {'test_id':row[0], 'test_date':row[1].strftime("%Y-%m-%d"), 'regno': row[2], 'status': row[3], 'technician':row[4], 'testengineer': row[5],'technicianuser': row[7] }
                    return_event.append(event_dict)
            conn.close() #release resource    
            return return_event
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])                    
        conn.close() #release resource    
        return None



'''
Add a new test event
'''
def addTest(test_date, regno, status, technician, testengineer):
    #todo: 1 check aircraft # 2+4 format 2 status is in test status table 3 technician  testengignner  select id from emplyee techinican id.)
    conn=openConnection() # get connection to postgresql
    curs= conn.cursor() # get cursor
    try:
        curs.execute("""select * from Aircraft where RegNo = '%s'"""% (regno))             
        result1 = curs.fetchall()
        print(result1)
        curs.execute("""select userid from Employee where UserName = '%s' and Role = 'Technician'"""% (technician))
        result2 = curs.fetchall()
        print(result2)
        curs.execute("""select userid from Employee where UserName = '%s' and Role = 'TestEngineer'"""% (testengineer))
        result3 = curs.fetchall()
        print(result3)
        curs.execute("""select TestStatusCode from TestStatus where TestStatusDesc = '%s'"""% (status))             
        result4 = curs.fetchall()
        if len(result1) == 0 or len(result2) == 0 or len(result3) == 0 or len(result4) == 0:
            curs.close()
            return False
        else:
            status_code= result4[0][0]
            technician_userid = result2[0][0]
            testengineer_userid = result3[0][0]

        curs.callproc("addEvent", [test_date, regno, status_code, technician_userid, testengineer_userid])
        conn.commit()
        curs.close()
        return True
    
    except psycopg2.Error as sqle:
        print("psycopg2.Error : " + sqle.pgerror)
        conn.close()
        return False

    finally:
        if conn is not None:
           conn.close()

'''
Update an existing test event
'''
def updateTest(test_id, test_date, regno, status, technician, testengineer):
    conn = openConnection()
    curs = conn.cursor()

    try:
        curs.execute("""select * from testevent t1,teststatus t2,employee t3,employee t4,aircraft t5 WHERE t1.testid=%s
                     and t2.teststatusdesc='%s' and t3.username='%s' and t4.username = '%s'  and t5.regno = '%s'""" % (
        test_id, status, technician, testengineer, regno))
        result = curs.fetchall()
        if len(result) == 0:
            curs.close()
            print("")
            return False
        else:
            '''
            curs.execute("""UPDATE testevent t1 SET testdate='%s', regno='%s', status = t2.teststatuscode, technician = t3.userid, testengineer = t4.userid
FROM teststatus t2,employee t3,employee t4 WHERE t2.teststatusdesc='%s'  and t1.testid=%s and t3.username='%s' and t4.username = '%s'"""%(test_date, regno, status, test_id, technician, testengineer))        
            '''
            curs.callproc("update_event", (test_date, regno, status, test_id, technician, testengineer))
            conn.commit()
            curs.close()
            return True
    except:
        # If there were any errors, return a NULL row printing an error to the debug
        print("Unexpected error:", sys.exc_info()[0])
        conn.close()
        return False
        
import routes