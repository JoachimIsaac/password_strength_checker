
import tkinter as tk
from tkinter.font import Font
import requests 
import hashlib
import sys
from tkinter import font

HEIGHT = 700
WIDTH = 800


    
    
    


#This gets the api data of the password.
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the api and try again')

    return response
    
#This returns the amount of times a password was leaked.
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for hash, count in hashes:
        if hash == hash_to_check:
            return count
    return 0
    
    
#Takes in password converts it to hexformat and
# seperates it into the first 5 hex and the tail end.
# Then it returns the count on the passwords that are leaked.
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail = sha1password[ : 5], sha1password[ 5: ]
    response = request_api_data(first5_char)

    return get_password_leaks_count(response,tail)
    
def get_password_info(password,condition):
    
    label['text'] = ''
    count = pwned_api_check(password)
    
    print_contents(count,condition,password)
    


def print_contents(count,condition,password):
    if count:
        if condition[0] == True:
            label['text']=f'{password} was found {count} times...\nyou should probably change your password!'
        
        if condition[0] == False:
            password = '*' * len(password)
            label['text']=f'{password} was found {count} times...\nyou should probably change your password!'
            
    else:
        if condition[0] == True:
            label['text']=f'{password} was NOT found.\nCarry on!'
        if condition[0] == False:
            password = '*' * len(password)
            label['text']=f'{password} was NOT found.\nCarry on!'
        
    


def reveal_password(counter,condition):

    if counter[0] == 0:
        entry['show'] = ""
        counter[0] += 1
        button2['text'] = 'Hide'
        condition[0] = True
    else:
        counter[0]= 0 
        entry['show'] = "*"
        button2['text'] = 'Reveal'
        condition[0] = False
    
    

#Start of gui app 
root = tk.Tk()
######################################
#Everything else goes inbetween here.
#sorta controls size of window, initial screen size anyway
#Make sure it is scalable with larger screens.
canvas  = tk.Canvas(root, height= HEIGHT, width = WIDTH)
canvas.pack()

background_image= tk.PhotoImage(file="The-Demise-of-the-Password.png")
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)
#To orgranize widgets on the screen we use frame
frame = tk.Frame(root, bg='#abc1ff',bd=15)
frame.place(relx = 0.5,rely=0.1,relwidth=0.75, relheight=0.1, anchor='n')


#Trying to make another title. 
############################################################################
# frame = tk.Frame(root, bg='red',bd=15)
# frame.place(relx = 0.5,rely=0.1,relwidth=0.75, relheight=0.1, anchor='n')
# 
# label = tk.Label(root, text = "Password strength checker")
############################################################################
#Trying to make another title. 



entry = tk.Entry(frame,bg='#cedbdb',bd=10, show="*")

entry.place(relwidth=0.45, relheight=1.2, rely= -0.1 )
entry.config(font=("Courier", 16))




counter = [0]
condition = [False]
button2 = tk.Button(frame, text= "Reveal",bg ="#bec2c2", command = lambda: reveal_password(counter,condition))

button2.place(relx=0.8, rely=0, relwidth=0.19, relheight=1)
button2.config(font=("Courier", 16))

#Passed in button into fram , you could also pass it into the root.
button1 = tk.Button(frame, text= "Check Password",bg ="#bec2c2", command = lambda: get_password_info(entry.get(),condition))

button1.place(relx=0.5, rely=0, relwidth=0.26, relheight=1)
button1.config(font=("Courier", 16))

    
    
    



lower_frame = tk.Frame(root, bg='#80c1ff',bd=15)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75,relheight=0.65, anchor='n')

label = tk.Label(lower_frame,anchor='nw',justify='left',bd=4)
label.config(font=("Courier", 20))
label.place(relwidth=1, relheight=1)


######################################
root.mainloop()
#End of gui app 