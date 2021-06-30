from tkinter import *
from tkinter import font
from mysql.connector.errors import IntegrityError, ProgrammingError
import packages.functions
import main_backend
from tkinter import ttk

### FUNCTIONS ###

def studentsubmit():
    def close():
        popup.destroy()

    name = (firstnamevar.get() + ' ' + lastnamevar.get())
    admno = str(admvar.get())
    gender = gendervar.get()
    
    try:
        cur = packages.functions.db.cursor(buffered=True)
        cur.execute("USE report_card_db;")
    
        cur.execute('INSERT INTO student (AdmissionNo, Name, Gender) \
            VALUES ("'+admno+'", "'+name+'", "'+gender+'");')
        packages.functions.db.commit()
    except:
        popup = Tk()
        popup.iconbitmap("assets/error.ico")
        popup.geometry("255x150+572+340")
        popup.title("Error!")
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

        error = Label(popup, text="Student already exists", font=("Bahnschrift", 17), fg="#fb4934")
        error.place(x=8,y=25)

        okbutton = Button(popup, text="Ok", command=close, width=10)
        okbutton.place(x=85,y=90)
    finally:
        cur.execute('ALTER TABLE student AUTO_INCREMENT=1')
    
    stutree.delete(*stutree.get_children())
    cur.execute("SELECT AdmissionNo, Name, Gender FROM student")
    row = cur.fetchall()
    for rw in row:
        stutree.insert('','end',iid=None,text="test",values=(rw[0],rw[1],rw[2])) 

def acasubmit():
    def close():
        popup.destroy()

    admno = str(admvar.get())
    classname_raw = classvar.get()
    section_raw = sectionvar.get()
    rollno = rollvar.get()
    year = yearvar.get()
    subject_raw = str(subvar.get())
    marks = marksvar.get()
    totalmarks = totalvar.get()
    exam = examvar.get()

    classname = classname_raw.strip("()',")
    section = section_raw.strip("()',")
    subject = subject_raw.strip("'(),")

    cur = packages.functions.db.cursor(buffered=True)

    cur.execute('SELECT SubjectID FROM subjects WHERE Name = "' + subject + '";')
    subjectid_raw = ''
    for i in cur:
        subjectid_raw = str(i)
    subjectid = subjectid_raw.strip('(),')

    cur = packages.functions.db.cursor(buffered=True)
    
    cur.execute('SELECT StudentID FROM student WHERE AdmissionNo = "'+admno+'";')
    studentid_raw = ''
    for i in cur:
        studentid_raw = str(i)
    studentid = studentid_raw.strip('(),')
    
    cur.execute('SELECT ClassID FROM class WHERE Name = "'+ classname +'";')
    classid_raw = ''
    for i in cur:
        classid_raw = str(i)
    classid = classid_raw.strip('(),')

    cur.execute('SELECT SectionID FROM sections WHERE Name = "' + section + '";')
    sectionid_raw = ''
    for i in cur:
        sectionid_raw = str(i)
    sectionid = sectionid_raw.strip('(),')

    sem_fail_integ = False
    sem_fail_prog = False
    mark_fail_integ = False
    mark_fail_prog = False

    try:
        cur.execute('INSERT INTO academics (StudentID, Year, ClassID, SectionID, RollNo, SubjectID) \
            VALUES ('+studentid+', '+year+', '+classid+', '+sectionid+', '+rollno+', '+subjectid+');')
        packages.functions.db.commit()
        sem_fail_integ = False
        sem_fail_prog = False
    except IntegrityError:
        sem_fail_integ = True
    except ProgrammingError:
        sem_fail_prog = True
    finally:
        cur.execute('ALTER TABLE academics AUTO_INCREMENT=1')

    cur.execute('SELECT AcademicID FROM academics WHERE \
    StudentID='+studentid+' \
    AND ClassID='+classid+' \
    AND Year='+year+' \
    AND SubjectID='+subjectid+';')

    academicid_raw = ''
    
    for i in cur:
        academicid_raw = str(i)
    
    academicid = academicid_raw.strip("'(),")

    try:
        cur.execute('INSERT INTO exam (AcademicID, Name, TotalMarks, MarksObtained, Year) \
            VALUES ('+academicid+', "'+exam+'", '+totalmarks+', '+marks+', '+year+');')
        packages.functions.db.commit()
        mark_fail_integ = False
        mark_fail_prog = False
    except IntegrityError:
        mark_fail_integ = True
    except ProgrammingError:
        mark_fail_prog = True
    finally:
        cur.execute('ALTER TABLE exam AUTO_INCREMENT=1')

    if sem_fail_prog == False and mark_fail_prog == False and sem_fail_integ == False and mark_fail_integ == False:
        pass

    elif sem_fail_integ == True and mark_fail_integ == True:
        popup = Tk()
        popup.iconbitmap("assets/error.ico")
        popup.geometry("255x150+572+340")
        popup.title("Error!")
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

        error = Label(popup, text="Record already exists", font=("Bahnschrift", 17), fg="#fb4934")
        error.place(x=8,y=25)

        okbutton = Button(popup, text="Ok", command=close, width=10)
        okbutton.place(x=85,y=90)
    elif sem_fail_integ == True and mark_fail_integ == False:
        pass
    elif sem_fail_prog == True and mark_fail_prog == True:
        popup = Tk()
        popup.iconbitmap("assets/error.ico")
        popup.geometry("255x150+572+340")
        popup.title("Error!")
        popup.tk_setPalette(background="#282828", foreground="#ebdbb2")

        error = Label(popup, text="Student not found,\nplease add student", font=("Bahnschrift", 17), fg="#fb4934")
        error.place(x=27,y=20)

        okbutton = Button(popup, text="Ok", command=close, width=10)
        okbutton.place(x=85,y=90)
    else:
        pass
    
    markstree.delete(*markstree.get_children())
        
    cur.execute('SELECT a.Year, \
        c.Name, \
        se.Name, \
        a.RollNo, \
        st.Name, \
        e.Name, \
        su.Name, \
        e.MarksObtained, \
        e.TotalMarks \
            FROM academics a \
                INNER JOIN class c \
                    ON c.ClassID = a.ClassID \
                INNER JOIN sections se \
                    ON se.SectionID = a.SectionID \
                INNER JOIN student st \
                    ON st.StudentID = a.StudentID \
                INNER JOIN subjects su \
                    ON su.SubjectID = a.SubjectID \
                INNER JOIN exam e \
                    ON e.AcademicID = a.AcademicID \
            ORDER BY a.Year, c.Name, se.Name, a.RollNo, e.Name, su.Name;')
    
    arow = cur.fetchall()

    for arw in arow:
        markstree.insert('','end',values=(arw[0],arw[1],arw[2],arw[3],arw[4],arw[5],arw[6],arw[7],arw[8]))

def s_fetch(event):
    sItem = stutree.focus()
    svalues = stutree.item(sItem)
    stuname = (svalues['values'][1]).split()
    firstnamevar.set(stuname[0])
    lastnamevar.set(stuname[1])
    admvar.set(svalues['values'][0])
    gendervar.set(svalues['values'][2])

def a_fetch(event):
    aItem = markstree.focus()
    avalues = markstree.item(aItem)
    yearvar.set(avalues['values'][0])
    classvar.set(avalues['values'][1])
    sectionvar.set(avalues['values'][2])
    rollvar.set(avalues['values'][3])
    examvar.set(avalues['values'][5])
    subvar.set(avalues['values'][6])
    marksvar.set(avalues['values'][7])
    totalvar.set(avalues['values'][8])

def s_delete():
    admno = admvar.get()
    cur.execute('DELETE FROM student WHERE AdmissionNo = "'+admno+'";')
    packages.functions.db.commit()
    
    stutree.delete(*stutree.get_children())
    cur.execute("SELECT AdmissionNo, Name, Gender FROM student")
    row = cur.fetchall()
    for rw in row:
        stutree.insert('','end',iid=None,text="test",values=(rw[0],rw[1],rw[2])) 

packages.functions.master_lists()

### WINDOW ###

window=Tk()
window.iconbitmap("assets/edit.ico")

# Canvas
canvas1 = Canvas()
canvas1.config(width='1280', height='720')
line1 = canvas1.create_line(360,60,360,768,fill='#458588',width=2)
line2 = canvas1.create_line(0,60,1366,60, fill = '#fb4934', width = 3)
canvas1.pack()

# Set Window Configurations
defaultFont = font.nametofont("TkDefaultFont")
defaultFont.configure(family="Tw Cen MT", size=13)
window.title('Editor')
window.geometry("1280x720+30+0")
window.tk_setPalette(background="#282828", foreground="#ebdbb2")
window.resizable(0, 0)
bg = "#282828"
fg = "#ebdbb2"
graybox = "#a89984"

### WIDGETS ###

# Title
title = Label(window, text="Student Marksheet", fg = "#b8bb26", font = ("Bahnschrift",30))
title.place(x=470,y=29)

# Headers
acad_lbl = Label(window, text="Academic Data", font=("Bahnschrift",20))
acad_lbl.place(x=545, y=125)

data_lbl = Label(window, text="Student Data", font = ("Bahnschrift",20))
data_lbl.place(x = 103, y = 125) 

## STUDENT INFO ##

# Student Details
firstname_lbl = Label(window, text = "First Name")
firstname_lbl.place(x = 65, y = 200)
firstnamevar = StringVar()
firstname_txt = Entry(window, textvariable=firstnamevar, selectbackground=fg, selectforeground=bg, justify='center')
firstname_txt.place(x = 165, y = 202)

lastname_lbl = Label(window, text = "Last Name")
lastname_lbl.place(x=65 ,y=250 )
lastnamevar = StringVar()
lastname_txt = Entry(window, textvariable=lastnamevar, selectbackground=fg, selectforeground=bg, justify='center')
lastname_txt.place(x = 165, y = 252 )

adm_lbl = Label(window, text = "Admission No.")
adm_lbl.place(x = 65, y = 300)
admvar = StringVar()
adm_txt = Entry(window, textvariable=admvar, selectbackground=fg, selectforeground=bg, justify='center')
adm_txt.place(x = 165, y = 302)

# Gender-selection
gendervar = StringVar()
gendervar.set(' ')

gender_lbl = Label(window, text = "Gender")
gender_lbl.place(x = 65, y = 350)
male = Radiobutton(window, text ="Male",variable = gendervar, value = "Male", selectcolor = bg)
male.place(x = 145, y = 349)

female = Radiobutton(window, text = "Female",variable = gendervar, value = "Female", selectcolor = bg)
female.place(x = 225, y = 349)

# Submit button
addstudent_btn = Button(window, text = "Add", command = studentsubmit)
addstudent_btn.place(x=140,y = 400)

delstudent_btn = Button(window, text = "Delete", command=s_delete)
delstudent_btn.place(x=190,y = 400)

## ADDING/EDITING EXAM RESULTS ##

class_lbl = Label(window, text = "Class")
class_lbl.place(x = 415, y = 203)

classvar= StringVar()
classvar.set("None")
classdrop = OptionMenu(window, classvar, *packages.functions.classlist)
classdrop.place(x = 475, y = 200)

roll_lbl = Label(window, text = "Roll No.")
roll_lbl.place(x = 660, y = 200)
rollvar = StringVar()
roll_txt = Entry(window, textvariable=rollvar, selectbackground=fg, selectforeground=bg, justify='center')
roll_txt.place(x = 760, y = 203)

section = Label(window, text = "Section")
section.place(x = 415, y = 253)

sectionvar = StringVar()
sectionvar.set("None")
sectiondrop = OptionMenu(window, sectionvar, *packages.functions.sectionlist)
sectiondrop.place(x = 475, y= 250)

year_lbl = Label(window, text="Year of Session", font=('Tw Cen MT', 12))
year_lbl.place(x=660, y=250)

yearvar = StringVar()
year_txt = Entry(window, textvariable=yearvar, selectbackground=fg, selectforeground=bg, justify='center')
year_txt.place(x=760,y=253)

sub_lbl = Label(window, text="Subject")
sub_lbl.place(x=415,y=303)

subvar = StringVar()
subvar.set("None")
subject_drop = OptionMenu(window, subvar, *packages.functions.sublist)
subject_drop.place(x=475,y=300)

exam_lbl = Label(window, text="Exam Name")
exam_lbl.place(x=660,y=300)

examvar = StringVar()
exam_text = Entry(window, textvariable=examvar, selectbackground=fg, selectforeground=bg, justify='center')
exam_text.place(x=760,y=303)

marks_lbl = Label(window, text="Marks")
marks_lbl.place(x=415,y=350)

marksvar = StringVar()
marks_obt = Entry(window, textvariable=marksvar, width=3, selectbackground=fg, selectforeground=bg, justify='center')
marks_obt.place(x=475,y=354)

slash_lbl = Label(window, text='/', font=('Bahnschrift', 23))
slash_lbl.place(x=505,y=340)

totalvar = StringVar()
total_mks = Entry(window, textvariable=totalvar, width=3, selectbackground=fg, selectforeground=bg, justify='center')
total_mks.place(x=530,y=354)

#reset_btn = Button(window, text = "Reset", command = reset)
#reset_btn.place(x=450,y = 440)

stutree = ttk.Treeview(window, columns=('0', '1', '2'), show='headings')
stutree.place(x=10, y=465)

stutree.column('0', width=100, anchor=CENTER)
stutree.column('1', width=140, anchor=CENTER)
stutree.column('2', width=80, anchor=CENTER)

stutree.heading('0', text="Admission No.")
stutree.heading('1', text="Name")
stutree.heading('2', text="Gender")

stutree.bind("<ButtonRelease-1>", s_fetch)

cur = packages.functions.db.cursor()
cur.execute("SELECT AdmissionNo, Name, Gender FROM student")
srow = cur.fetchall()
for rw in srow:
    stutree.insert('','end',values=(rw[0],rw[1],rw[2]))

stuscrollbar = ttk.Scrollbar(window, orient="vertical", command=stutree.yview)
stuscrollbar.place(x=10+321, y=466, height=200+25)

stutree.configure(yscrollcommand=stuscrollbar.set)

markstree = ttk.Treeview(window, columns=('1', '2', '3', '4', '5', '6', '7', '8', '9'), show='headings', height=13)
markstree.place(x=373, y=405)

markstree.column('1', width=50, anchor=CENTER)
markstree.column('2', width=40, anchor=CENTER)
markstree.column('3', width=50, anchor=CENTER)
markstree.column('4', width=50, anchor=CENTER)
markstree.column('5', width=130, anchor=CENTER)
markstree.column('6', width=90, anchor=CENTER)
markstree.column('7', width=150, anchor=CENTER)
markstree.column('8', width=40, anchor=CENTER)
markstree.column('9', width=35, anchor=CENTER)

markstree.heading('1', text="Year")
markstree.heading('2', text="Class")
markstree.heading('3', text="Section")
markstree.heading('4', text="Roll No.")
markstree.heading('5', text="Name")
markstree.heading('6', text="Exam")
markstree.heading('7', text="Subject")
markstree.heading('8', text="Marks")
markstree.heading('9', text="Total")

cur.execute('SELECT a.Year, \
    c.Name, \
    se.Name, \
    a.RollNo, \
    st.Name, \
    e.Name, \
    su.Name, \
    e.MarksObtained, \
    e.TotalMarks \
        FROM academics a \
            INNER JOIN class c \
                ON c.ClassID = a.ClassID \
            INNER JOIN sections se \
                ON se.SectionID = a.SectionID \
            INNER JOIN student st \
                ON st.StudentID = a.StudentID \
            INNER JOIN subjects su \
                ON su.SubjectID = a.SubjectID \
            INNER JOIN exam e \
                ON e.AcademicID = a.AcademicID \
        ORDER BY a.Year, c.Name, se.Name, a.RollNo, e.Name, su.Name;')
arow = cur.fetchall()

for arw in arow:
    markstree.insert('','end',values=(arw[0],arw[1],arw[2],arw[3],arw[4],arw[5],arw[6],arw[7],arw[8]))

markstree.bind("<ButtonRelease-1>", a_fetch)

#markscrollbar = ttk.Scrollbar(window, orient="vertical", command=markstree.yview)
#markscrollbar.place(x=946, y=406, height=250+35)

#markstree.configure(yscrollcommand=markscrollbar.set)

submit_btn = Button(window, text="Submit", command=acasubmit)
submit_btn.place(x=617, y=345)

window.mainloop()