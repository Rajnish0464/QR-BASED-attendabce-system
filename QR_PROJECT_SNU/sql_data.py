# Importing module
import mysql.connector as connector

# Creating connection object
class DBhelper:
    def __init__(self):
        self.con=connector.connect(
	host = "localhost",
	user = "root",
	password = "Rajnish",
        database="student_data" )

        query='create table if not exists student(StudentId int primary key ,StudentName varchar(200),enorll_No varchar (20))'
        
        cur=self.con.cursor()
        cur.execute(query)
        print("Created")

    #insert user
    def insert_user(self,StudentId ,StudentName, enroll_No):
        query="insert into student(StudentId,StudentName,enorll_No) values({},'{}','{}')".format(StudentId,StudentName,enroll_No)
        print(query)
        cur=self.con.cursor()
        cur.execute(query)
        self.con.commit()
        print("user saved to db")

    def fetch_all(self):
        query="select * from student"  
        cur= self.con.cursor()
        cur.execute(query)
        for row in cur:
            print(row)
            print(row[1])
            

helper=DBhelper()
#helper.insert_user(3,"Ranjeet","567")
helper.fetch_all()
