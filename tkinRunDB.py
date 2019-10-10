from tkinter import * #GUI package
import sqlite3 as sq #For tables and database
import datetime

window = Tk()
window.withdraw()
window.title("Run Tracker")
window.geometry('1000x800+0+0')
header = Label(window, text="Running Tracker", font=("impact",30,"bold"), fg="steelblue").pack()

con = sq.connect('Run.db') #dB browser for sqlite needed
c = con.cursor() #SQLite command, to connect to db so 'execute' method can be called


L1 = Label(window, text = "Run Type", font=("impact", 18)).place(x=10,y=100)
L2 = Label(window, text = "Day (dd)", font=("impact",18)).place(x=10,y=150)
L3 = Label(window, text = "Month (mm)", font=("impact",18)).place(x=10,y=200)
L4 = Label(window, text = "Year (yyyy)", font=("impact",18)).place(x=10,y=250)
L5 = Label(window, text = "Time Taken(mins)", font=("impact",18)).place(x=10,y=300)
L6 = Label(window, text = "Miles", font=("impact",18)).place(x=10,y=350)

#Create variables for each list
runtype = StringVar(window)#For 1st drop time
runtype.set('Choose') #Inital placeholder for field


rundb = StringVar(window)#2nd dropdown list
rundb.set('choose')

day = StringVar(window)
month = StringVar(window)
year = StringVar(window)
timetaken = StringVar(window)
miles = StringVar(window)

#Dictionary for drop down list
runtypelist = {'HillTrain', 'Speed', 'Recovery','Interval'}

dropdownrun = OptionMenu(window, runtype, *runtypelist) #For 1st drop down list
dropdownrun.place(x=220,y=105)
dropdownrun.configure(font=('Impact', 18))

dropdowndbase = OptionMenu(window, rundb, *runtypelist)#For 2nd drop down list
dropdowndbase.place(x=100,y=500)

#Entry for 'input' in GUI
dayT = Entry(window, textvariable=day)
dayT.configure(font=('Impact', 18))
dayT.place(x=220,y=155)

monthT = Entry(window, textvariable=month)
monthT.place(x=220,y=205)

yearT = Entry(window, textvariable=year)
yearT.place(x=220,y=255)

timeT = Entry(window, textvariable=timetaken)
timeT.place(x=220,y=305)

milesT = Entry(window, textvariable=miles)
milesT.place(x=220,y=355)

#get func to isolate the text entered in the entry boxes and submit to database
def sendrecord():
        print("You have submitted a record")
       
        c.execute('CREATE TABLE IF NOT EXISTS ' +runtype.get()+ ' (Datestamp TEXT, timetaken INTEGER, miles INTEGER)') #SQL syntax
       
        date = datetime.date(int(year.get()),int(month.get()), int(day.get())) #Date in format from 'import datetime'

        c.execute('INSERT INTO ' +runtype.get()+ ' (Datestamp, timetaken, miles) VALUES (?, ?, ?)',
                  (date, timetaken.get(), miles.get())) #Insert record into database.
        con.commit()

#Reset fields after submit
        runtype.set('----')
        day.set('')
        month.set('')
        year.set('')
        timetaken.set('')
        miles.set('')

#Clear boxes when submit button is hit
def clear():
    runtype.set('----')
    rundb.set('----')
    day.set('')
    month.set('')
    year.set('')
    timetaken.set('')
    miles.set('')
   
def record():
    c.execute('SELECT * FROM ' +rundb.get()) #Select from which ever compound lift is selected

    frame = Frame(window)
    frame.place(x= 400, y = 150)
   
    Lb = Listbox(frame, height = 8, width = 25,font=("arial", 12))
    Lb.pack(side = LEFT, fill = Y)
   
    scroll = Scrollbar(frame, orient = VERTICAL) # set scrollbar to list box for when entries exceed size of list box
    scroll.config(command = Lb.yview)
    scroll.pack(side = RIGHT, fill = Y)
    Lb.config(yscrollcommand = scroll.set)
   

    Lb.insert(0, 'Date, Time Taken, Miles') #first row in listbox
   
    data = c.fetchall() # Gets the data from the table
    
    
    for row in data:
        Lb.insert(1,row) # Inserts record row by row in list box

    L7 = Label(window, text = rundb.get()+ '      ',
              font=("arial", 16)).place(x=400,y=100) # Title of list box, given which compound lift is chosen

    L8 = Label(window, text = "They are ordered from most recent",
              font=("arial", 16)).place(x=400,y=350)
    con.commit()


button_1 = Button(window, text="Submit",command=sendrecord)
button_1.configure(font=('Impact', 18))
button_1.place(x=100,y=400)

button_2 = Button(window,text= "Clear",command=clear)
button_2.place(x=10,y=400)

button_3 = Button(window,text="Open DB",command=record)
button_3.place(x=10,y=500)


lgwindow = Toplevel(window)
lgwindow.title("Login")

con = sq.connect("My Database")
c = con.cursor()

def checklogin():
    user = entry1.get()
    pswd = entry2.get()
    c.execute('SELECT username, password from Users WHERE username=? AND password=?', (user, pswd))
    if c.fetchone() is not None:
    #record = c.fetchall()
        welcomelabel = Label(lgwindow, text="Welcome").grid(row=3, column=0)
        window.deiconify()
   # print(record)
   # uname = record[0][0]
   # pword = record[0][1]
   # print(uname,pword)

    else:
        faillabel = Label(lgwindow, text="Login Failed").grid(row=3, column=0)
     # print ("Login failed")
    

def register():
    user = entry1.get()
    pswd = entry2.get()
    c.execute('SELECT username from Users WHERE username=?', (user,))
    if c.fetchone() is not None:
        existslabel = Label(lgwindow, text="Username Already Exists").grid(row=3, column=0)
        #print("Username already exists")

    else:
        c.execute ('INSERT INTO Users (username, password) VALUES(?,?)',(user, pswd))
        con.commit()
        reglabel = Label(lgwindow, text="Registered").grid(row=3, column=0)
        #print("Registered")

# creating 2 text labels and input labels

label1 = Label(lgwindow, text = "Username").grid(row = 0) # this is placed in 0 0
# 'Entry' is used to display the input-field
entry1 = Entry(lgwindow)
entry1.grid(row = 0, column = 1) # this is placed in 0 1

label2 = Label(lgwindow, text="Password").grid(row = 1) # this is placed in 1 0
entry2 = Entry(lgwindow)
entry2.grid(row = 1, column = 1) # this is placed in 1 1
blanklabel = Label(lgwindow).grid(row=3, column=0)

# 'buttons
btnReg = Button(lgwindow, text='Register', command=register)
btnReg.grid(row=2, column=0)
btnLogin = Button(lgwindow, text="Login", command=checklogin)
btnLogin.grid(row=2, column=1)





window.mainloop() #mainloop() -> make sure that window stays open
