from tkinter import *
from tkinter import messagebox 
from PIL import ImageTk
import pymysql

background="white"

def clear():
    emailEntry.delete(0,END)
    usernameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    confirmpasswordEntry.delete(0,END)
    check.set(0)
    
def connect_database():
    if emailEntry.get()=='' or  usernameEntry.get()=='' or passwordEntry.get()=='' or  confirmpasswordEntry.get()=='' :
        messagebox.showerror('Error','All Fields Are Required')
    elif passwordEntry.get() != confirmpasswordEntry.get():
         messagebox.showerror('Error','Password Mismatch')
    elif check.get()==0:
         messagebox.showerror('Error','Please accept Terms and Conditions')
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='1234')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Database Connectivity Issue Please Try Again')
            return
        try:
            query='create database userdata'
            mycursor.execute(query)
            query='use userdata'
            mycursor.execute(query)
            query='create table data(id int auto_increment primary key not null, email varchar(50),username varchar(100),password varchar(20))'
            mycursor.execute(query)
        except:
            mycursor.execute('use userdata')                   
        query='select * from data where username=%s'
        mycursor.execute(query,(usernameEntry.get()))
        
        row=mycursor.fetchone()
        if row !=None:
            messagebox.showerror('Error','Username already exists')
            
        else:
             query='insert into data(email,username,password) values(%s,%s,%s)'
             mycursor.execute(query,(emailEntry.get(),usernameEntry.get(),passwordEntry.get()))
             con.commit()
             con.close()
             messagebox.showinfo('Success','Registration is Successful')
             clear()
             signup_window.destroy()
             import login
            
            
            
        
        
def login_page():
    signup_window.destroy()
    import login

signup_window=Tk()
signup_window.title('Signup Page')
signup_window.geometry('1450x730+40+40')
#signup_window.resizable(False,False)
signup_window.config(bg=background)
background=ImageTk.PhotoImage(file='chartt.jpg')

bgLabel=Label(signup_window,image=background,bg="white")
bgLabel.grid()

frame=Frame(signup_window,width=200,height=730,bg='white')
frame.place(x=800,y=100)

heading=Label(frame,text='CREATE AN ACCOUNT',font=('Microsoft Yahei UI Light',25,'bold')
              ,bg='white',fg='firebrick1')
heading.grid(row=0,column=0,padx=10,pady=10)

emailLabel=Label(frame,text='Email',font=('Microsoft Yahei UI Light',15,'bold'),bg='white',fg='firebrick1')
emailLabel.grid(row=1,column=0,sticky='w',padx=50,pady=(10,0))

emailEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',15,'bold'),fg='white',bg='firebrick1')
emailEntry.grid(row=2,column=0,stick='w',padx=50)

usernameLabel=Label(frame,text='Username',font=('Microsoft Yahei UI Light',15,'bold'),bg='white',fg='firebrick1')
usernameLabel.grid(row=3,column=0,sticky='w',padx=50,pady=(10,0))

usernameEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',15,'bold'),fg='white',bg='firebrick1')
usernameEntry.grid(row=4,column=0,stick='w',padx=50)

passwordLabel=Label(frame,text='Password',font=('Microsoft Yahei UI Light',15,'bold'),bg='white',fg='firebrick1')
passwordLabel.grid(row=5,column=0,sticky='w',padx=50,pady=(10,0))

passwordEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',15,'bold'),fg='white',bg='firebrick1')
passwordEntry.grid(row=6,column=0,stick='w',padx=50)

confirmpasswordLabel=Label(frame,text='Confirm Password',font=('Microsoft Yahei UI Light',15,'bold'),bg='white',fg='firebrick1')
confirmpasswordLabel.grid(row=7,column=0,sticky='w',padx=50,pady=(10,0))

confirmpasswordEntry=Entry(frame,width=30,font=('Microsoft Yahei UI Light',15,'bold'),fg='white',bg='firebrick1')
confirmpasswordEntry.grid(row=8,column=0,stick='w',padx=50)
check=IntVar()
termsandconditions=Checkbutton(frame,text='I agree to the Terms and Conditions',font=('Microsoft Yahei UI Light',12,'bold'),
                               fg='firebrick1',bg='white',activebackground='white',activeforeground='firebrick1'
                               ,cursor='hand2',variable=check)
termsandconditions.grid(row=9,column=0,pady=15,padx=25)

signupButton=Button(frame,text='Signup',font=('Open sans',20,'bold'),bd=0,bg='firebrick1',fg='white'
                    ,activebackground='firebrick1',activeforeground='white',width=20,command=connect_database)
signupButton.grid(row=10,column=0,pady=10)

alreadyaccount=Label(frame,text="Already,have an account?",font=('Open sans','12','bold'),
                     bg='white',fg='firebrick1')
alreadyaccount.grid(row=15,column=0,sticky='w',padx=75,pady=10)

loginButton=Button(frame,text='Login',font=('Open Sans',15,'bold underline'),bd=0,fg='blue',bg='white',activeforeground='blue'
                   ,activebackground='white',cursor='hand2',command=login_page)
loginButton.place(x=285,y=500)

signup_window.mainloop()
