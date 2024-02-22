import tkinter as tk
from tkinter.ttk import *
import sys
import os
#import tkMessageBox
from PIL import Image, ImageTk
import mysql.connector as connector
import pygame
from gtts import gTTS

class DBhelper:
    def __init__(self):
        self.con=connector.connect(
	host = "localhost",
	user = "root",
	password = "subham",
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

    def count(self):
        c=0
        query="select * from student"  
        cur= self.con.cursor()
        cur.execute(query)
        for row in cur:
            print(row)
            c+=1
        return c+1
helper=DBhelper()

def register():
    sid=helper.count()
    s_name=Name_Entry.get()
    s_enroll_no=Enroll_Entry.get()
    if not s_name.isalpha():
        ad.config(text="Invalid student name format. Only alphabets allowed.")
    elif not s_enroll_no.isdigit():
        ad.config(text="Invalid enroll number format. Only digits allowed.")
    else:
        ad.config(text="")
    ##print("Name:", sname)
    print("ID:",sid)
    print("Name:",s_name)
    print("enroll:", s_enroll_no)
    
    
    helper.insert_user(sid,s_name,s_enroll_no)
    Name_Entry.delete(0, tk.END)
    Enroll_Entry.delete(0, tk.END)



# Create the main window
root = tk.Tk()
root.title("ATTENDANCE SOFTWARE")
root.iconbitmap("icon.ico")
root.geometry('1200x700')


bg = ImageTk.PhotoImage(file="BG3.jpg")
label = tk.Label(
    root,
    image=bg
)
label.place(x=0,y=0,relwidth=1,relheight=1)
def start():
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load("welcome.mp3")  # Load the MP3 file
    pygame.mixer.music.play() 
    
start()
def helloCallBack():
    pygame.mixer.init()  # Initialize the mixer
    pygame.mixer.music.load("a_start.mp3")  # Load the MP3 file
    pygame.mixer.music.play() 
    os.system('python scanner.py')

B1=tk.Frame(root)
B1.pack(pady=80)

B=tk.Button(root,text="START ATTENDANCE",command= helloCallBack,padx=1,pady=1,width=30,height=2 ,font='Helvetica 24 bold',bg="yellow")
B.pack(pady=20)


# a button widget which will open a
# new window on button click
btn = tk.Label(root,
             text ="Register New Student",
             font='Helvetica 18 bold',bg="yellow")
btn.pack(pady = 10)


L2=tk.Label(root,text ="Student Name:")
L2.pack(pady=5)
Name_Entry=tk.Entry(root)
Name_Entry.pack(pady=5)
L3=tk.Label(root,text ="Enroll No:")
L3.pack(pady=5)
Enroll_Entry=tk.Entry(root)
Enroll_Entry.pack(pady=5)
submit_button=tk.Button(root,text="Submit",command=register)
submit_button.pack(pady=10)

n=Name_Entry.get()

ad = tk.Label(root,
             text =n,
             font='Helvetica 18 bold',bg="yellow")
ad.pack(pady = 10)

#Start the main loop
root.mainloop()
