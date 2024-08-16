from tkinter import *
import tkinter.messagebox
import csv
import ctypes
import sys

if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
hospitals=["King's"]
students={}
placements={}
current = {}
preferences={}

def Finish():
    root.destroy()

def getentryHOSP():
    global current
    if current['E1'].get() in hospitals:
        tkinter.messagebox.showinfo("Error", "Hospital already added.")
    else:
        hospitals.append(current['E1'].get())
        current['T1'].grid_forget()
        if hospitals != []:
            var = IntVar(root)
            var.set(len(hospitals))
            current['T1'] = Text(root, width=55, height=var.get())
            for hospital in hospitals:
                # print('Hospital:')
                # print(hospital)
                current['T1'].insert(1.0, hospital + '\n')
            current['T1'].grid(row=3, column=1)
        else:
            current['T1'] = Text(root, width=55, height=1)
            current['T1'].insert(1.0, ' ')
            current['T1'].grid(row=3, column=1)
    placementmenu2 = Menu(menubar, tearoff=0)
    for hospital in hospitals:
        addplacements(hospital)
        placementmenu2.add_command(label=hospital, command=secplacement)
    menubar.entryconfig(2,menu=placementmenu2)

def getentryPLAC(hospital):
    global subentryPLAC
    def subentryPLAC():
        global current
        # print(current['OM1'].get())
        if hospital in placements.keys() and current['E2'].get() in placements[hospital]:
            tkinter.messagebox.showinfo("Error", "Placement already added.")
        else:
            if hospital in placements.keys():
                placements[hospital].append(current['E2'].get())
            else:
                placements[hospital]=[current['E2'].get()]
            current['T1'].grid_forget()
            if hospital in placements.keys():
                var = IntVar(root)
                var.set(len(placements[hospital]))
                current['T1'] = Text(root, width=55, height=var.get())
                for placement in placements[hospital]:
                    current['T1'].insert(1.0, placement + '\n')
                current['T1'].grid(row=3, column=1)
            else:
                current['T1'] = Text(root, width=55, height=1)
                current['T1'].insert(1.0, ' ')
                current['T1'].grid(row=3, column=1)

def getentrySTUD():
    global current, varO
    if current['E1'].get() in students.keys():
        tkinter.messagebox.showinfo("Error", "Student already added. Please go to 'Search and Edit' to change the placements completed or hospital assigned to this student.")
    else:
        placementstring=current['E2'].get()
        placementlist=[]
        checker=0
        word = ''
        while checker<=len(placementstring):
            if checker==len(placementstring) or placementstring[checker]==',':
                placementlist.append(word)
                word = ''
            else:
                word+=placementstring[checker]
            checker+=1
        test=True
        for placement in placementlist:
            if placement!="" and (varO.get() not in placements.keys() or placement not in placements[varO.get()]):
                tkinter.messagebox.showinfo("Error","That hospital doesn't offer that placement.")
                test=False
                break
        if test:
            students[current['E1'].get()]=[varO.get(),placementlist]
            current['T1'].grid_forget()
            if students != {}:
                var = IntVar(root)
                var.set(len(students.keys()))
                current['T1'] = Text(root, width=55, height=var.get())
                for student in students.keys():
                    # print('Hospital:')
                    # print(hospital)
                    current['T1'].insert(1.0, student + '\n')
                current['T1'].grid(row=3, column=1)
            else:
                current['T1'] = Text(root, width=55, height=1)
                current['T1'].insert(1.0, ' ')
                current['T1'].grid(row=3, column=1)

def remHOSP():
    global current
    if current['E1'].get() in hospitals:
        hospitals.remove(current['E1'].get())
        if current['E1'].get() in placements.keys():
            placements.pop(current['E1'].get())
        placementmenu2 = Menu(menubar, tearoff=0)
        for hospital in hospitals:
            addplacements(hospital)
            placementmenu2.add_command(label=hospital, command=secplacement)
        menubar.entryconfig(2, menu=placementmenu2)
        # print(current['T1'].search('\n', "1.0", stopindex="end"))
        current['T1'].grid_forget()
        if hospitals != []:
            var = IntVar(root)
            var.set(len(hospitals))
            current['T1'] = Text(root, width=55, height=var.get())
            for hospital in hospitals:
                # print('Hospital:')
                # print(hospital)
                current['T1'].insert(1.0, hospital + '\n')
            current['T1'].grid(row=3, column=1)
        else:
            current['T1'] = Text(root, width=55, height=1)
            current['T1'].insert(1.0, ' ')
            current['T1'].grid(row=3, column=1)
    else:
        tkinter.messagebox.showinfo("Error", "No such hospital.")

def remPLAC(hospital):
    global subremPLAC
    def subremPLAC():
        global current
        if hospital in placements.keys() and current['E2'].get() in placements[hospital]:
            placements[hospital].remove(current['E2'].get())
            # print(current['T1'].search('\n', "1.0", stopindex="end"))
            current['T1'].grid_forget()
            if hospital in placements.keys():
                var = IntVar(root)
                var.set(len(placements[hospital]))
                current['T1'] = Text(root, width=55, height=var.get())
                for placement in placements[hospital]:
                    current['T1'].insert(1.0, placement + '\n')
                current['T1'].grid(row=3, column=1)
            else:
                current['T1'] = Text(root, width=55, height=1)
                current['T1'].insert(1.0, ' ')
                current['T1'].grid(row=3, column=1)
        else:
            tkinter.messagebox.showinfo("Error", "No such placement.")

def remSTUD():
    global current
    student=current['E1'].get()
    if student in students.keys():
        students.pop(student)
        # print(current['T1'].search('\n', "1.0", stopindex="end"))
        current['T1'].grid_forget()
        if students != {}:
            var = IntVar(root)
            var.set(len(students.keys()))
            current['T1'] = Text(root, width=55, height=var.get())
            for student in students.keys():
                # print('Hospital:')
                # print(hospital)
                current['T1'].insert(1.0, student + '\n')
            current['T1'].grid(row=3, column=1)
        else:
            current['T1'] = Text(root, width=55, height=1)
            current['T1'].insert(1.0, ' ')
            current['T1'].grid(row=3, column=1)
    else:
        tkinter.messagebox.showinfo("Error", "No such student.")

def addhospitals():
    global current
    for key in current.keys():
        if current[key]!='':
            current[key].grid_forget()
            current[key]=''
    if hospitals!=[]:
        var=IntVar(root)
        var.set(len(hospitals))
        current['T1'] = Text(root,width=55,height=var.get())
        for hospital in hospitals:
            # print('Hospital:')
            # print(hospital)
            current['T1'].insert(1.0, hospital+'\n')
        current['T1'].grid(row=3, column=1)
    else:
        current['T1'] = Text(root, width=55, height=1)
        current['T1'].insert(1.0,' ')
        current['T1'].grid(row=3, column=1)
    current['F1'] = Frame(root)
    current['F1'].grid(row=1,column=1,sticky=W)
    current['L0'] = Label(root, text="Hospitals", relief=RAISED)
    current['L0'].grid(row=0, column=1,sticky=W)

    current['L1'] = Label(current['F1'], text="Hospital Name")
    current['L1'].grid(row=3, column=1)
    current['E1'] = Entry(current['F1'], bd=3, textvariable=StringVar())
    current['E1'].grid(row=3, column=2)
    current['B1'] = Button(current['F1'], text="Add", command=getentryHOSP)
    current['B1'].grid(row=3, column=3)
    current['B2'] = Button(current['F1'], text="Remove", command=remHOSP)
    current['B2'].grid(row=3, column=4)
    current['B3'] = Button(current['F1'], text="Finished",command=Finish)
    current['B3'].grid(row=3, column=5,sticky=E)

def addplacements(hospital):
    global secplacement
    def secplacement():
        global current
        for key in current.keys():
            if current[key]!='':
                current[key].grid_forget()
                current[key]=''
        if hospital in placements.keys():
            var=IntVar(root)
            var.set(len(placements[hospital]))
            current['T1'] = Text(root,width=55,height=var.get())
            for placement in placements[hospital]:
                current['T1'].insert(1.0, placement+'\n')
            current['T1'].grid(row=3, column=1)
        else:
            current['T1'] = Text(root, width=55, height=1)
            current['T1'].insert(1.0,' ')
            current['T1'].grid(row=3, column=1)
        current['F1'] = Frame(root)
        current['F1'].grid(row=1, column=1, sticky=W)
        current['L0'] = Label(root, text="Placements", relief=RAISED)
        current['L0'].grid(row=0, column=1, sticky=W)

        current['L1'] = Label(current['F1'], text=hospital)
        current['L1'].grid(row=3, column=1)
        # var = StringVar(root)
        # var.set(hospitals[0])
        # current['OM1'] = OptionMenu(current['F1'], var, *hospitals)
        # current['OM1'].grid(row=3, column=2)
        current['L2'] = Label(current['F1'], text="Placement Name")
        current['L2'].grid(row=4, column=1)
        current['E2'] = Entry(current['F1'], bd=3, textvariable=StringVar())
        current['E2'].grid(row=4, column=2)
        getentryPLAC(hospital)
        current['B1'] = Button(current['F1'], text="Add", command=subentryPLAC)
        current['B1'].grid(row=4, column=3)
        remPLAC(hospital)
        current['B2'] = Button(current['F1'], text="Remove",command=subremPLAC)
        current['B2'].grid(row=4, column=4, sticky=E)
        current['B2'] = Button(current['F1'], text="Finished",command=Finish)
        current['B2'].grid(row=4, column=5, sticky=E)

def addstudents():
    global current, varO
    for key in current.keys():
        if current[key]!='':
            current[key].grid_forget()
    if students != {}:
        var = IntVar(root)
        var.set(len(students.keys()))
        current['T1'] = Text(root, width=55, height=var.get())
        for student in students.keys():
            # print('Hospital:')
            # print(hospital)
            current['T1'].insert(1.0, student + '\n')
        current['T1'].grid(row=3, column=1)
    else:
        current['T1'] = Text(root, width=55, height=1)
        current['T1'].insert(1.0, ' ')
        current['T1'].grid(row=3, column=1)
    current['F1'] = Frame(root)
    current['F1'].grid(row=1, column=1, sticky=W)
    current['L0'] = Label(root, text="Students", relief=RAISED)
    current['L0'].grid(row=0, column=1, sticky=W)

    current['L1'] = Label(current['F1'], text="Student Name")
    current['L1'].grid(row=3, column=1)
    current['L2'] = Label(current['F1'], text="Placements done")
    current['L2'].grid(row=4, column=1)
    current['L3'] = Label(current['F1'], text="Hospital")
    current['L3'].grid(row=5, column=1)
    current['E1'] = Entry(current['F1'], bd=3, textvariable=StringVar())
    current['E1'].grid(row=3, column=2)
    current['E2'] = Entry(current['F1'], bd=3, textvariable=StringVar())
    current['E2'].grid(row=4, column=2)
    varO = StringVar(root)
    varO.set(hospitals[0])
    current['OM1'] = OptionMenu(current['F1'], varO, *hospitals)
    current['OM1'].grid(row=5, column=2)
    current['B1'] = Button(current['F1'], text="Add", command=getentrySTUD)
    current['B1'].grid(row=5, column=3)
    current['B2'] = Button(current['F1'], text="Remove", command=remSTUD)
    current['B2'].grid(row=5, column=4)
    current['B3'] = Button(current['F1'], text="Finished",command=Finish)
    current['B3'].grid(row=5, column=5, sticky=E)

def preferencesEdit():
    for key in current.keys():
        if current[key] != '':
            current[key].grid_forget()
    current['F1'] = Frame(root)
    current['F1'].grid(row=1, column=1, sticky=W)
    current['L0'] = Label(root, text="Preference Search", relief=RAISED)
    current['L0'].grid(row=0, column=1, sticky=W)
    current['L1'] = Label(current['F1'], text="Search by Student Name")
    current['L1'].grid(row=3, column=1)
    current['E1'] = Entry(current['F1'], bd=3, textvariable=StringVar())
    current['E1'].grid(row=3, column=2)
    current['B1'] = Button(current['F1'], text="Search Students", command=searchSTUDS2)
    current['B1'].grid(row=3, column=3)

def STUDchaHOSP():
    global current,student
    hospital=current['E2'].get()
    if hospital not in hospitals:
        tkinter.messagebox.showinfo("Error.", "That is not a valid hospital.")
    else:
        students[student][0]=hospital
    current['L2'].grid_forget()
    current['L2'] = Label(current['F1'], text="Hospital: " + students[student][0])
    current['L2'].grid(row=4, column=1)



def STUDaddPLAC():
    global current, student
    placement = current['E1'].get()
    if placement not in placements[students[student][0]]:
        tkinter.messagebox.showinfo("Error.", "That placement is not offered by that hospital.")
    else:
        students[student][1].append(placement)

    current['L3'].grid_forget()
    placementstring = ''
    for placement in students[student][1]:
        placementstring += str(placement) + ', '
    if placementstring != '':
        placementstring = placementstring[:-2]
        placementstring += '.'
    current['L3'] = Label(current['F1'], text="Placements: " + placementstring)
    current['L3'].grid(row=5, column=1)

def STUDaddPLAC():
    global current, student
    placement = current['E1'].get()
    if placement not in placements[students[student][0]]:
        tkinter.messagebox.showinfo("Error.", "That placement is not offered by that hospital.")
    else:
        students[student][1].append(placement)

    current['L3'].grid_forget()
    placementstring = ''
    for placement in students[student][1]:
        placementstring += str(placement) + ', '
    if placementstring != '':
        placementstring = placementstring[:-2]
        placementstring += '.'
    current['L3'] = Label(current['F1'], text="Placements: " + placementstring)
    current['L3'].grid(row=5, column=1)

def STUDremPLACS():
    global current,student
    students[student][1]=[]
    current['L3'].grid_forget()
    placementstring = ''
    current['L3'] = Label(current['F1'], text="Placements: " + placementstring)
    current['L3'].grid(row=5, column=1)

def STUDaddPREFS():
    global current, student
    preference1 = current['E1'].get()
    preference2 = current['E2'].get()
    preference3 = current['E3'].get()
    if preference1 not in placements[students[student][0]] or preference2 not in placements[students[student][0]] or preference3 not in placements[students[student][0]]:
        tkinter.messagebox.showinfo("Error.", "A preference is not offered to that student")
    else:
        preferences[student]=[preference1,preference2,preference3]

    current['L2'].grid_forget()
    preferencestring = ''
    for placement in preferences[student]:
        preferencestring += str(placement) + ', '
    if preferencestring != '':
        preferencestring = preferencestring[:-2]
        preferencestring += '.'
    current['L2'] = Label(current['F1'], text="Preferences: " + preferencestring)
    current['L2'].grid(row=5, column=1)

def STUDremPREFS():
    global current,student
    preferences[student]=[]
    current['L2'].grid_forget()
    preferencestring = 'None'
    current['L2'] = Label(current['F1'], text="Preferences: " + preferencestring)
    current['L2'].grid(row=5, column=1)

def searchHOSPS():
    tkinter.messagebox.showinfo("Feature coming soon.", "Sorry, this feature is not yet available.")



def searchSTUDS2():
    global current,student
    student=current['E1'].get()
    if student not in students.keys():
        tkinter.messagebox.showinfo("Error", "No such student.")
    else:
        for key in current.keys():
            if current[key] != '':
                current[key].grid_forget()
        current['F1'] = Frame(root)
        current['F1'].grid(row=1, column=1, sticky=W)
        current['L0'] = Label(root, text="Student", relief=RAISED)
        current['L0'].grid(row=0, column=1, sticky=W)

        current['L1'] = Label(current['F1'], text="Student Name: " + student)
        current['L1'].grid(row=3, column=1)
        if student in preferences.keys():
            displayPref=preferences[student][0]+', '+preferences[student][1]+', '+ preferences[student][2]
        else:
            displayPref="None"
        current['L2'] = Label(current['F1'], text="Preferences: " + displayPref)
        current['L2'].grid(row=4, column=1)
        current['E1'] = Entry(current['F1'], bd=3, textvariable=StringVar(),width=12)
        current['E1'].grid(row=6, column=2)
        current['E2'] = Entry(current['F1'], bd=3, textvariable=StringVar(),width=12)
        current['E2'].grid(row=6, column=3)
        current['E3'] = Entry(current['F1'], bd=3, textvariable=StringVar(),width=12)
        current['E3'].grid(row=6, column=4)
        current['B2'] = Button(current['F1'], text="Add Preferences", command=STUDaddPREFS)
        current['B2'].grid(row=6, column=1)
        current['B3'] = Button(current['F1'], text="Remove All Placements", command=STUDremPREFS)
        current['B3'].grid(row=8, column=1)
        current['B4'] = Button(current['F1'], text="Finished",command=Finish)
        current['B4'].grid(row=9, column=3, sticky=E)

def searchSTUDS():
    global current,student
    student=current['E1'].get()
    if student not in students.keys():
        tkinter.messagebox.showinfo("Error", "No such student.")
    else:
        for key in current.keys():
            if current[key] != '':
                current[key].grid_forget()
        current['F1'] = Frame(root)
        current['F1'].grid(row=1, column=1, sticky=W)
        current['L0'] = Label(root, text="Student", relief=RAISED)
        current['L0'].grid(row=0, column=1, sticky=W)

        current['L1'] = Label(current['F1'], text="Student Name: " + student)
        current['L1'].grid(row=3, column=1)
        current['L2'] = Label(current['F1'], text="Hospital: " + students[student][0])
        current['L2'].grid(row=4, column=1)
        placementstring=''
        for placement in students[student][1]:
            placementstring+=str(placement)+', '
        if placementstring!='':
            placementstring=placementstring[:-2]
            placementstring+='.'
        current['L3'] = Label(current['F1'], text="Placements: " + placementstring)
        current['L3'].grid(row=5, column=1)
        current['E1'] = Entry(current['F1'], bd=3, textvariable=StringVar())
        current['E1'].grid(row=6, column=3)
        current['E2'] = Entry(current['F1'], bd=3, textvariable=StringVar())
        current['E2'].grid(row=7, column=3)
        current['B1'] = Button(current['F1'], text="Change Hospital", command=STUDchaHOSP)
        current['B1'].grid(row=7, column=2)
        current['B2'] = Button(current['F1'], text="Add Placement", command=STUDaddPLAC)
        current['B2'].grid(row=6, column=2)
        current['B3'] = Button(current['F1'], text="Remove All Placements", command=STUDremPLACS)
        current['B3'].grid(row=8, column=2)
        current['B4'] = Button(current['F1'], text="Finished",command=Finish)
        current['B4'].grid(row=9, column=3, sticky=E)



def alterstudents():
    global current
    for key in current.keys():
        if current[key] != '':
            current[key].grid_forget()
    current['F1'] = Frame(root)
    current['F1'].grid(row=1, column=1, sticky=W)
    current['L0'] = Label(root, text="Student Search", relief=RAISED)
    current['L0'].grid(row=0, column=1, sticky=W)

    current['L1'] = Label(current['F1'], text="Search by Student Name")
    current['L1'].grid(row=3, column=1)
    current['L2'] = Label(current['F1'], text="Search by Hospital")
    current['L2'].grid(row=4, column=1)
    current['E1'] = Entry(current['F1'], bd=3, textvariable=StringVar())
    current['E1'].grid(row=3, column=2)
    current['E2'] = Entry(current['F1'], bd=3, textvariable=StringVar())
    current['E2'].grid(row=4, column=2)

    current['B1'] = Button(current['F1'], text="Search Students", command=searchSTUDS)
    current['B1'].grid(row=3, column=3)
    current['B2'] = Button(current['F1'], text="Search Hospitals", command=searchHOSPS)
    current['B2'].grid(row=4, column=3)
    current['B3'] = Button(current['F1'], text="Finished",command=Finish)
    current['B3'].grid(row=5, column=5, sticky=E)

root = Tk()
menubar = Menu(root)
menubar.add_cascade(label="Hospitals",command=addhospitals)
placementmenu = Menu(menubar, tearoff=0)
for hospital in hospitals:
    addplacements(hospital)
    placementmenu.add_command(label=hospital, command=secplacement)
menubar.add_cascade(label="Placements",menu=placementmenu)
placementmenu3 = Menu(menubar, tearoff=0)
placementmenu3.add_command(label='Add', command=addstudents)
placementmenu3.add_command(label='Search and Edit', command=alterstudents)
menubar.add_cascade(label="Students",menu=placementmenu3)#students)
menubar.add_cascade(label="Preferences",command=preferencesEdit)

w = 600 # width for the Tk root
h = 300 # height for the Tk root

ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen
# and where it is placed
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.config(menu=menubar)



# B.pack()
# text = Text(root)
# text.insert(INSERT, "Hospitals")
# text.insert(END, "Bye Bye.....")
# text.pack()
# text.tag_add("here", "1.0", "1.4")
# text.tag_add("start", "1.8", "1.13")
# text.tag_config("here", background="yellow", foreground="blue")
# text.tag_config("start", background="black", foreground="green")
# print(StringVar())
root.mainloop()
print(students)
print(placements)
print(hospitals)
print(preferences)

with open('hospitals.csv', 'w', newline="") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Hospital','Placements'])
    for hospital in hospitals:
        if hospital in placements.keys():
            for placement in placements[hospital]:
                filewriter.writerow([hospital,placement])

with open('students.csv', 'w', newline="") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Student Name','Hospital','Placement done'])
    for student in students.keys():
        for placement in students[student][1]:
            filewriter.writerow([student,students[student][0],placement])

with open('preferences.csv', 'w', newline="") as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Student Name','Preference 1','Preference 2','Preference 3'])
    for student in students.keys():
        if student in preferences.keys():
            filewriter.writerow([student,preferences[student][0],preferences[student][1],preferences[student][2]])