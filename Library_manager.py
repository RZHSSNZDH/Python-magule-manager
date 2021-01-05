from tkinter import *
from subprocess import *
import subprocess
import re
import requests
from bs4 import BeautifulSoup
import time

# Window settings

libraries = Tk()
libraries.title('My Libraries')
libraries.geometry('750x200')

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-= ListBox -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

list1 = Listbox(libraries, width=35, height=10)
list1.grid(row=0, column=0, rowspan=6, columnspan=2)

# ScrollBar

sb1 = Scrollbar(libraries)
sb1.grid(row=2, column=2, rowspan=6)

# Sync listbox and scrollbar together

list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Binding -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def get_lib_details(event):
    global selected_lib
    index = list1.curselection()
    selected_lib = list1.get(index)
    pattern = r'\s+'
    global library_details
    library_details = re.split(pattern, selected_lib)

list1.bind('<<ListboxSelect>>', get_lib_details)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Entries -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

e1 = Entry(libraries)
e1.grid(row=4, column=3)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Funcs -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def listOfLibs(): # Update listbox and insert installed mogules
    libs_names = check_output('pip list', shell=True)
    libs_names = libs_names.decode('utf-8')
    libs_names = libs_names.split('\n')
    list1.delete(0, END)
    for lib in libs_names[2:-1:]:
        list1.insert(END, lib)

def delete(): # Action for delete button. deletes selected mogule
    call(f'pip uninstall {library_details[0]}', shell=True)
    time.sleep(1)

def update(): # Action for update button. updates selected mogule
    call(f'pip install {library_details[0]} -U', shell=True)

def install_lib(): # Action for Install button. Installs selected mogule
    name = selected_lib
    url = f"https://pypi.org/search/?q={name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find_all("span", attrs={"class": "package-snippet__name"})
    call(f'pip install {result[0].text}', shell=True)
    listOfLibs() # Listing new list

def search_in_my_mogules(): # Action for Search in my mogules button. Lists list of installed maguls that e1.get() is in the mogules name
    libs_names = check_output('pip list', shell=True)
    libs_names = libs_names.decode('utf-8')
    libs_names = libs_names.split('\n')
    list1.delete(0, END)
    for lib in libs_names[2:-1:]:
        if e1.get() in lib:
            list1.insert(END, lib)

def search_in_pypi(): # Action for Search in Pypi button. Lists results of e1.get() search in pypi website. After this, appears install button
    url = f"https://pypi.org/search/?q={e1.get()}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find_all("span", attrs={"class": "package-snippet__name"})
    list1.delete(0,END)
    result = result[::-1]
    for mogule in result:
        list1.insert(0, mogule.text)
    b4.grid(row=4, column=4)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-= Buttons -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

b1 = Button(libraries, text='Delete', width=20, command=delete)
b1.grid(row=0, column=3)

b2 = Button(libraries, text='Update', width=20, command=update)
b2.grid(row=0, column=4)

b3 = Button(libraries, text='Update List', width=20, command=listOfLibs)
b3.grid(row=1, column=3)

b4 = Button(libraries, text='Install library', width=20, command=install_lib)

b5 = Button(libraries, text='Exit', width=20, command=exit)
b5.grid(row=1, column=4)

b6 = Button(libraries, text='Search in my mogules', width=20, command=search_in_my_mogules)
b6.grid(row=3, column=4)

b7 = Button(libraries, text='Search in Pypi', width=20, command=search_in_pypi)
b7.grid(row=3, column=3)

listOfLibs()
libraries.mainloop()
