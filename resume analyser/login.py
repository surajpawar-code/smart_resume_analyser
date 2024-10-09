from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from tkinter import Toplevel
import pymysql

background = "white"

# Functionality Part

def forget_password():
    new_window = Toplevel(login_window)
    new_window.title("Change Password")
    new_window.geometry("793x512+50+50")
    new_window.resizable(False, False)

    def change_password():
        if user_entry.get() == '' or newpass_entry.get() == '' or confirmpassword_entry.get() == '':
            messagebox.showerror('Error', 'All Fields are Required', parent=new_window)
        elif newpass_entry.get() != confirmpassword_entry.get():
            messagebox.showerror('Error', 'New Password and Confirm Password are not matching', parent=new_window)
        else:
            try:
                con = pymysql.connect(host='localhost', user='root', password='1234', database='userdata')
                mycursor = con.cursor()

                # Check if the username exists
                query = 'select * from data where username=%s'
                mycursor.execute(query, (user_entry.get(),))  # Comma added to properly format the tuple
                row = mycursor.fetchone()

                if row is None:
                    messagebox.showerror('Error', 'Incorrect Username', parent=new_window)
                else:
                    # Update the password
                    query = 'update data set password=%s where username=%s'
                    mycursor.execute(query, (newpass_entry.get(), user_entry.get()))  # Tuple with new password and username
                    con.commit()  # Save changes to the database
                    con.close()  # Close connection after update
                    messagebox.showinfo('Success', 'Password is reset, please login with new password', parent=new_window)
                    new_window.destroy()
            except Exception as e:
                messagebox.showerror('Error', f"Error due to: {str(e)}", parent=new_window)

    bgPic = ImageTk.PhotoImage(file='background1.jpg')
    bgLabel = Label(new_window, image=bgPic)
    bgLabel.grid()

    heading_Label = Label(new_window, text='RESET PASSWORD', font=('arial', '18', 'bold'),
                          bg='white', fg='magenta2')
    heading_Label.place(x=480, y=60)

    userLabel = Label(new_window, text='Username', font=('arial', '12', 'bold'), bg='white', fg='magenta2')
    userLabel.place(x=470, y=130)

    user_entry = Entry(new_window, width=25, font=('arial', 11, 'bold'),
                       bd=0, fg='magenta2')
    user_entry.place(x=470, y=160)

    Frame(new_window, width=250, height=2, bg='orchid1').place(x=470, y=180)

    passwordLabel = Label(new_window, text='New Password', font=('arial', '12', 'bold'), bg='white', fg='magenta2')
    passwordLabel.place(x=470, y=210)

    newpass_entry = Entry(new_window, width=25, font=('arial', 11, 'bold'),
                          bd=0, fg='magenta2')
    newpass_entry.place(x=470, y=240)

    Frame(new_window, width=250, height=2, bg='orchid1').place(x=470, y=260)

    confirmpasswordLabel = Label(new_window, text='Confirm Password', font=('arial', '12', 'bold'), bg='white', fg='magenta2')
    confirmpasswordLabel.place(x=470, y=290)

    confirmpassword_entry = Entry(new_window, width=25, font=('arial', 11, 'bold'),
                                  bd=0, fg='magenta2')
    confirmpassword_entry.place(x=470, y=320)

    Frame(new_window, width=250, height=2, bg='orchid1').place(x=470, y=340)

    submitButton = Button(new_window, text='Submit', bd=0, bg='magenta2', activebackground='magenta2',
                          cursor='hand2', font=('Open Sans', 16, 'bold'), width=19,
                          fg='white', activeforeground='white', command=change_password)
    submitButton.place(x=470, y=390)

    new_window.mainloop()

# Rest of the code...

def login_user():
    if  usernameEntry.get()=='' or passwordEntry.get()=='' :
        messagebox.showerror('Error','All fields are required')
        
    else:
        try:
            con=pymysql.connect(host='localhost',user='root',password='1234')
            mycursor=con.cursor()
        except:
            messagebox.showerror('Error','Connection is not established try again')
            return
        query ='use userdata'
        mycursor.execute(query)
        query='select * from data where username=%s and password=%s'
        mycursor.execute(query,(usernameEntry.get(),passwordEntry.get()))
        row=mycursor.fetchone()
        if row==None:
            messagebox.showerror('Error','Invalid username or password') 
        else:
            messagebox.showinfo('Welcome','Login is successful')
            import resume_analyser
                        
    

def signup_page():
    login_window.destroy()
    import signup

def hide():
    openeye.config(file='closeye.png')
    passwordEntry.config(show='*')
    eyeButton.config(command=show)
    
def show():
    openeye.config(file='openeye.png')
    passwordEntry.config(show='')
    eyeButton.config(command=hide)  
    
    
      
def user_enter(event):
    if usernameEntry.get()=='Username':
        usernameEntry.delete(0,END)
        
def password_enter(event):
    if passwordEntry.get()=='Password':
        passwordEntry.delete(0,END)
        
        
                
#GUI Part
login_window=Tk()
login_window.geometry('1450x730+40+40')
login_window.resizeable=(0,0)
login_window.title('Login Page')
login_window.config(bg=background)

bgImage=ImageTk.PhotoImage(file='chartt.jpg')

bgLabel=Label(login_window,image=bgImage,bg="white")
bgLabel.place(x=0,y=0)

heading=Label(login_window,text='USER LOGIN',font=('Microsoft Yahei UI Light',40,'bold')
              ,bg='white',fg='firebrick1')
heading.place(x=840,y=80)

usernameEntry=Entry(login_window,width=25,font=('Microsoft Yahei UI Light',25,'bold'),
                    bd=0,fg='firebrick1')
usernameEntry.place(x=850,y=200)
usernameEntry.insert(0,'Username')

usernameEntry.bind('<FocusIn>',user_enter)


frame1=Frame(login_window,width=350,height=3,bg='firebrick1')
frame1.place(x=850,y=250)

passwordEntry=Entry(login_window,width=25,font=('Microsoft Yahei UI Light',25,'bold')
                    ,bd=0,fg='firebrick1')
passwordEntry.place(x=850,y=300)
passwordEntry.insert(0,'Password')

passwordEntry.bind('<FocusIn>',password_enter)

frame2=Frame(login_window,width=350,height=3,bg='firebrick1')
frame2.place(x=850,y=350)
openeye=PhotoImage(file='openeye.png')
eyeButton=Button(login_window,image=openeye,bd=0,bg='white',activebackground='white'
                 ,cursor='hand2',command=hide)
eyeButton.place(x=1150,y=310)

forgetButton=Button(login_window,text='Forgot Password?',bd=0,bg='white',activebackground='white'
                 ,cursor='hand2',font=('Microsoft Yahei UI Light',14,'bold')
                 ,fg='firebrick1',activeforeground='firebrick1',command=forget_password)
forgetButton.place(x=1025,y=368)

loginButton=Button(login_window,text='Login',font=('Open Sans',21,'bold'),
                   fg='white',bg='firebrick1',activeforeground='white'
                   ,activebackground='firebrick1',cursor='hand2',bd=0,width=20,command=login_user)
loginButton.place(x=850,y=425)

orLabel=Label(login_window,text='-------------- OR --------------',font=('Open Sans',23),fg='firebrick1',bg='white')
orLabel.place(x=850,y=520)



signupLabel=Label(login_window,text='Dont have an account?',font=('Open Sans',14,'bold'),fg='firebrick1',bg='white')
signupLabel.place(x=850,y=600)

newaccountButton=Button(login_window,text='Create new one',font=('Open Sans',14,'bold underline'),
                   fg='blue',bg='white',activeforeground='blue'
                   ,activebackground='white',cursor='hand2',bd=0,command=signup_page)
newaccountButton.place(x=1065,y=595)

login_window.mainloop()
