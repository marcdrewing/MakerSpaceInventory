import pymongo
from pymongo import MongoClient                 #(windows)##Pymongo muss mit PIP installiert werden mit: py -m pip install pymongo #(windows)
from tkinter import *
from tkinter.scrolledtext import ScrolledText 
from tkinter import font
import tkinter
import csv
import os.path
import cv2                                      #(windows)##cv2 kamera library muss mit pip installiert werden  mit: py -m pip install opencv-python-headless 
from PIL import Image         #(windows)##Pillow library muss mit pip installiert werden: py -m pip install Pillow
import xlsxwriter             #(windows)##xlsxwriter library muss mit pip installiert werden: py -m pip install xlsxwriter
import pyimgur
import os, sys
import qrcode
import barcode  #pip install python-barcode
from barcode.writer import ImageWriter
from barcode import generate
#import numpy as np

program_version = "V1.5"



def setup_settings():
    
    if os.path.isfile("settings.txt"):
        return

    settingfile = open('settings.txt',"w+")
    settingfile.write("connection_string=")
    settingfile.write('\n')
    settingfile.write("database_name= Enter the MongoDB Database name here. If there is no existing Database you can set the name here")
    settingfile.write('\n')
    settingfile.write("collection_name= Enter the Collection name here. If there is no existing Collection you can set the name here")
    settingfile.write('\n')
    settingfile.write("imgur_client= Enter Imgur CLientID here. https://api.imgur.com/oauth2/addclient - If you dont want to use Imgur to save images, leave this empty")
    settingfile.write('\n')
    settingfile.write("missing_collection= Enter the collection name for the missing items here ")
    settingfile.write('\n')
    settingfile.write("facility_name= Please enter information into settings.txt")
    settingfile.write('\n')
    settingfile.write("background_colour=grey")
    settingfile.write('\n')
    settingfile.write("label_path= Enter path to label template here - if you dont use a label printer leave this empty")
    settingfile.write('\n')

def get_setting(setting):                               #benötigt zum verbinden zur Database
    setup_settings()
    settingfile = open('settings.txt')                  #auslesen der txt Datei in der der Connection String zur Database steht
    Lines = settingfile.readlines()
    count = 0
    for line in Lines:
        count += 1
        splitted_line = line.split("=")
        if splitted_line[0] == setting:
           str_without_new_line = splitted_line[1].strip() 
           return str_without_new_line

if get_setting("connection_string") != '':        

    CONNECTION_STRING = get_setting("connection_string")
    DATABASE_NAME_STRING = get_setting("database_name")
    COLLECTION_NAME_STRING = get_setting("collection_name")
    MISSING_COLLECTION_NAME_STRING = get_setting("missing_collection")

    #CONNECTION_STRING = "mongodb+srv://marcdrewing:eragonsaphira@cluster0.3c5ac.mongodb.net/myFirstDatabase"

    client = MongoClient(CONNECTION_STRING)


    dbname = client[DATABASE_NAME_STRING]
    collection_name = dbname[COLLECTION_NAME_STRING]
    missing_collection = dbname[MISSING_COLLECTION_NAME_STRING]

    #dbname = client['Items']
    #collection_name = dbname['MakerLab']

imgur_active = False
if get_setting("imgur_client") != '':
    imgur_object = pyimgur.Imgur(get_setting('imgur_client'))
    imgur_active = True
    
image_url_global = ''

def delete_image_url_global():
    image_url_item_view_var.set('')
    image_url_global = ''

def get_image_url_global():#
    return image_url_global

def test_database():
    item_found_list = missing_collection.find({"serialnumber":4})
    for item in item_found_list:
        print(item)

def open_label():
    if get_setting("label_path")=='':
        return
    else:
        os.system(get_setting("label_path"))

def print_qrcode(name,content):
    if not os.path.isdir("qrcodes"):
        os.mkdir('qrcodes')
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    qr_path = os.getcwd()+'/qrcodes/' + name + '.png'

    img.save(qr_path)
    
##    image = cv2.imread(qr_path)
##
##    row, col = image.shape[:2]
##    bottom = image[row-2:row, 0:col]
##    mean = cv2.mean(bottom)[0]
##
##    add_border = len(name)
##
##    print(add_border*5)
##
##    border = cv2.copyMakeBorder(
##        image,
##        top=25,
##        bottom=5,
##        left=add_border*6,
##        right=add_border*6,
##        borderType=cv2.BORDER_CONSTANT,
##        value=[mean, mean, mean]
##    )
##
##    cv2.putText(border,name, (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, 255, 2, cv2.LINE_AA)
##
##    cv2.imwrite(qr_path, border)
        
    os.startfile(qr_path, "print")

def print_barcode(content):
    if not os.path.isdir("barcodes"):
        os.mkdir('barcodes')

    if content.isnumeric() == True:   
        bar_path = os.getcwd()+'/barcodes/' + content

        number_length = len(str(content))

        if number_length <= 6:
            for i in range(6-number_length):
                content = '0'+ content
        elif number_length <= 8:
            for i in range(8-number_length):
                content = '0'+ content
        elif number_length <= 10:
            for i in range(10-number_length):
                content = '0'+ content       
        
        EAN = barcode.get_barcode_class('itf')
        ean = EAN(content, writer=ImageWriter())
        fullname = ean.save(bar_path, {"module_width":0.2, "module_height":5, "font_size": 10, "text_distance": 3, "quiet_zone": 4})


        barcode_img = cv2.imread(bar_path+'.png')
        barcode_width = barcode_img.shape[1]
        crop_img = barcode_img[0:0+110, 0:0+barcode_width]
        cv2.imwrite(bar_path+'.png', crop_img)

        os.startfile(bar_path+'.png', "print")
        
    else:
        print("Barcodes can only contain numbers")


def font_size_read():
    
    screen_width = terminal.winfo_screenwidth()
    screen_height = terminal.winfo_screenheight()
    window_height = terminal.winfo_height()
    window_width = terminal.winfo_width()

    #print(screen_width)

    new_font_size = (screen_width/1920)*26

    #print(new_font_size)
    return int(new_font_size)

def resize_picture(picture_path,width):
    image = cv2.imread(picture_path, cv2.IMREAD_UNCHANGED)
    wanted_width = width
    scale_percent = (wanted_width/image.shape[1])
    #print(scale_percent)
    height = int(image.shape[0] * scale_percent)
    dim = (wanted_width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    cv2.imwrite(picture_path, resized)

def take_picture(name):

    if name == "":
        print("Fill serialnumber first")
        return 0

    if not os.path.isdir("pictures"):
        os.mkdir('pictures')
        
    camera_port = 0
    ramp_frames = 30
    camera = cv2.VideoCapture(camera_port)
    png, image = camera.read()
    wanted_width = 400
    scale_percent = (wanted_width/image.shape[1])
    #print(scale_percent)
    height = int(image.shape[0] * scale_percent)
    dim = (wanted_width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    file = 'pictures/'+name+'.png'
    cv2.imwrite(file, resized)
    del(camera)
    add_item_item_picture['file']=file
    item_picture['file']=file
    
        

def upload_image(name):
    if imgur_active == True:                                                    #Uploads Picture to Imgur and returns the URL if there is a IMGUR Client given in the settings
        file = 'pictures/'+name+'.png'
        if os.path.isfile(file):
            uploaded_image = imgur_object.upload_image(file, title=name)
            image_url_global = uploaded_image.link
            image_url_item_view_var.set(uploaded_image.link)
            print(image_url_global)
            return uploaded_image.link
        else:
            print("No picture to Upload")
            return ''
        
def write_settings(setting,content):
    settingfile = open('settings.txt')

def delete_picture():
    add_item_item_picture['file']=''

def find_latest_serialnumber():
    latest_serial = 0
    latest_item = collection_name.find().sort("serialnumber", -1).limit(1)
    for item in latest_item:
        #print(item)
        return item['serialnumber']



def pull_item_info(serialnumberToPull):

    ##pulls the information for the given serialnumber from the database and saves them to the StringVars that are being defined at the main window section

    #print("SerialNumberTOPullIs:")
    #print(serialnumberToPull)
    
    item_details3 = collection_name.find({"serialnumber" : int(serialnumberToPull)})
    for item in item_details3:                                          
        itemname = item['itemname']
        quantity = item['quantity']
        unit = item['unit']
        threshhold = item['threshhold']
        price = item['price']
        url = item['url']
        serialnumber = item['serialnumber']
        room = item['room']
        locker = item['locker']
        compartment = item['compartment']
        info = item['info']
        image_url = item['image_url']
        tags = item['tags']

    #print("Serialnumber is")
    #print(serialnumber)
    
    serialnumber_item_view_var.set(serialnumber)

    picture_path_string = 'pictures/'+str(serialnumber)+ ".png"

    #serialnumber_item_view_var.set(serialnumber)
    itemname_item_view_var.set(itemname)
    quantity_item_view_var.set(quantity)
    unit_item_view_var.set(unit)
    threshhold_item_view_var.set(threshhold)
    price_item_view_var.set(price)
    url_item_view_var.set(url)
    room_item_view_var.set(room)
    locker_item_view_var.set(locker)
    compartment_item_view_var.set(compartment)
    info_item_view_var.set(info)
    image_url_item_view_var.set(image_url)
    tags_item_view_var.set(tags)

    if os.path.isfile(picture_path_string):      #testen ob sich entsprechendes Bild in Speicher befindet
        item_picture['file'] = picture_path_string
        #print("Bild gefunden")
    #else:
        #item_picture['file'] = "assets/place_holder.png"
        #print("Kein Bild gefunden")

   
def item_view_function(serialnumberToView):

    
    pull_item_info(serialnumberToView)
    quantity_view.delete(0, 'end')
    quantity_view.insert(0,quantity_item_view_var.get())
    info_view_entry.delete("1.0",END)
    info_view_entry.insert(tkinter.END, info_item_view_var.get())
    #print(itemname_item_view_var.get())
    view_item_window.tkraise()

def item_change_function(serialnumberToChange):

    change_item_name_entry.delete(0, 'end')
    change_item_quantity_entry.delete(0, 'end')
    change_item_unit_entry.delete(0, 'end')
    change_item_threshhold_entry.delete(0, 'end')
    change_item_price_entry.delete(0, 'end')
    change_item_url_entry.delete(0, 'end')
    change_item_room_entry.delete(0, 'end')
    change_item_locker_entry.delete(0, 'end')
    change_item_compartment_entry.delete(0, 'end')
    change_item_image_url_entry.delete(0, 'end')
    change_item_info_entry.delete("1.0",END)
    change_item_tags_entry.delete("1.0",END)

    pull_item_info(serialnumberToChange)

    change_item_name_entry.insert(0,itemname_item_view_var.get())
    change_item_quantity_entry.insert(0,quantity_item_view_var.get())
    change_item_unit_entry.insert(0,unit_item_view_var.get())
    change_item_threshhold_entry.insert(0,threshhold_item_view_var.get())
    change_item_price_entry.insert(0,price_item_view_var.get())
    change_item_url_entry.insert(0,url_item_view_var.get())
    change_item_room_entry.insert(0,room_item_view_var.get())
    change_item_locker_entry.insert(0,locker_item_view_var.get())
    change_item_compartment_entry.insert(0,compartment_item_view_var.get())
    change_item_image_url_entry.insert(0,image_url_item_view_var.get())
    change_item_info_entry.insert(tkinter.END, info_item_view_var.get())
    change_item_tags_entry.insert(tkinter.END, tags_item_view_var.get())

    change_item_window.tkraise()

###########################################################################################################################################################################################

def write_to_database(itemnameentry,quantityentry,unitentry,threshholdentry,priceentry,urlentry,serialnumberentry,roomentry,lockerentry,compartmententry,infoentry,image_url,tagsentry):

    item_to_save = {
    "itemname" : itemnameentry,
    "quantity" : int(quantityentry),
    "unit" : unitentry,
    "threshhold" : int(threshholdentry),
    "price" : priceentry,
    "url" : urlentry,
    "serialnumber" : int(serialnumberentry),
    "room": roomentry,
    "locker" : lockerentry,
    "compartment" : compartmententry,
    "info" : infoentry,
    "image_url" : image_url,
    "tags" : tagsentry
    }
    print(image_url)
    
    collection_name.insert_one(item_to_save)

################################################################################################################################################################

def write_to_missing_database(already_in_database, name, info, serialnumber):

    item_to_save = {
    "already_in_database" : already_in_database,
    "name" : name,
    "info" : info,
    "serialnumber" : int(serialnumber)
    }
    
    missing_collection.insert_one(item_to_save)

############################################################################################################################################################    

def change_one_database(serialnumber, attribute, newValue):


    myquery = { "serialnumber": int(serialnumber) }

    if attribute == 'quantity' or attribute == 'threshhold' or attribute == 'serialnumber':
        newvalues = { "$set": { attribute: int(newValue) } }
    else:
        newvalues = { "$set": { attribute: newValue } }
    
    collection_name.find_one_and_update(myquery, newvalues,upsert=False)
    item_details = collection_name.find({"serialnumber" : int(serialnumber)})
    missing_item_details = missing_collection.find({"serialnumber" : int(serialnumber)})

    for item in item_details:
        threshhold = item['threshhold']
        quantity = item['quantity']
        name = item['itemname'] 

    if (int(quantity) < int(threshhold)) and (missing_collection.count_documents({"serialnumber" : int(serialnumber)}) == 0):         #wenn anzahl unter threshhold ist und kein eintrag mit der entsprechenden serialnumber in der Missing datenbank zu finden ist, dann wird ein Eintrag in der Missing Datenbank gemacht
            write_to_missing_database("Yes",name,'',serialnumber)
            print("Item has been added to missing collection")    

    
    

def add_one_to_entry(objectToAdd):
    v1 = int(objectToAdd.get())
    v1 = v1+1
    objectToAdd.delete(0, 'end')
    objectToAdd.insert(0, v1)

def subtract_one_from_entry(objectToSub):
    v2 = int(objectToSub.get())
    v2 = v2-1
    objectToSub.delete(0, 'end')
    objectToSub.insert(0, v2)
        
        


    

######################################### Backend: Suche #####################################################

def item_search_function(searchdata):

    collection_name.create_index([('tags', 'text' )])

    #print( collection_name.index_information())

    #for len(searchdata)
    
    #print(searchdata)
    entryempty = True
    if searchdata.isnumeric() == True:
        item_found_list = collection_name.find({"serialnumber" : int(searchdata)})
        
        for item in item_found_list:                                           ##falls bei der Seriennummer etwas gefunden wurd direkt zu View Item gehen und nicht erst zu Suchergebnisse
            if item: entryempty = False
        if  not entryempty:
            item_view_function(item['serialnumber'])
            return
    #item_found_list = collection_name.find({"itemname" : searchdata})
    #for item in item_found_list:                                           ##falls bei der Seriennummer etwas gefunden wurd direkt zu View Item gehen und nicht erst zu Suchergebnisse
    #    if item: entryempty = False
    #if  not entryempty:
    #    item_view_function(item['serialnumber'])
    #    return
    else:
        #item_details = collection_name.find({"itemname" : searchdata})
        item_found_list = collection_name.find( { "$text": { "$search" : searchdata } } )
        item_search_results_function(item_found_list)
        return

####################################### Frontend: Suchergebnisse ##############################################

def item_search_results_function(item_found_list):

    search_results_window.tkraise()
    
    #search_results_window = Tk()
    #search_results_window.title("Suchergebnisse")
    #search_results_window.geometry("600x800")
    #pad=200
    #search_results_window.geometry("{0}x{1}+0+0".format(int(search_results_window.winfo_screenwidth()*(0.5)) , int(search_results_window.winfo_screenheight()*(0.5))))


    #serialnumberlist = []
    serialnumberlist.clear()

    itemnamelist = []
    #quantitylist = []
    #pricelist = []
    #urllist = []
    #tagslist = []
    #serialnumberlist = []
    #roomlist = []
    #lockerlist = []
    #compartmentlist = []

    for item in item_found_list:
        itemnamelist.append(item['itemname'])
        serialnumberlist.append(item['serialnumber'])
        #quantitylist.append(item['quantity'])
        #pricelist.append(item['price'])
        #urllist.append(item['url'])
        #tagslist.append(item['tags'])
        #roomlist.append(item['room'])
        #lockerlist.append(item['locker'])
        #compartmentlist.append(item['compartment'])
        
    listlength = len(itemnamelist)

    #for x in range(listlength):
        #print(itemnamelist[x])
        #print(serialnumberlist[x])
    mylist.delete(0,END)

    for k in range(listlength):
        mylist.insert(END, itemnamelist[k])
    
    
    
    #print(mylist.curselection())

    #search_results_window.mainloop()
        

######################## Main Page ##################################################################
    
terminal = Tk()
terminal.title("MakerLab Hannover Inventory System Terminal M.I.S.T")
#terminal.attributes('-fullscreen', True)
#terminal.geometry("1550x800") #1920 × 1080
pad=3
terminal.geometry("{0}x{1}+0+0".format(terminal.winfo_screenwidth()-pad, terminal.winfo_screenheight()-pad))

main_window = Frame(terminal)
main_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
main_window['bg'] = get_setting("background_colour")

#main_window_element1 = Frame(main_window,width = 600, height = 400)
#main_window_element1.place(relx=.5, rely=.5, anchor="c")

add_item_window = Frame(terminal)
add_item_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
add_item_window['bg'] = get_setting("background_colour")

view_item_window = Frame(terminal)
view_item_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
view_item_window['bg'] = get_setting("background_colour")

change_item_window = Frame(terminal)
change_item_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
change_item_window['bg'] = get_setting("background_colour")

settings_window = Frame(terminal)
settings_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
settings_window['bg'] = get_setting("background_colour")

search_results_window = Frame(terminal)
search_results_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
search_results_window['bg'] = get_setting("background_colour")

missing_window = Frame(terminal)
missing_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
missing_window['bg'] = get_setting("background_colour")

create_custom_label_window = Frame(terminal)
create_custom_label_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
create_custom_label_window['bg'] = get_setting("background_colour")

create_csv_window = Frame(terminal)
create_csv_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
create_csv_window['bg'] = get_setting("background_colour")

subtract_list_window = Frame(terminal)
subtract_list_window.place(x= 0, y = 0,relwidth = 1, relheight = 1)
subtract_list_window['bg'] = get_setting("background_colour")


#suchleiste 600x60
#resize_picture('assets/plus.png', int(terminal.winfo_screenwidth()*(0.028)))
#plus_picture = PhotoImage(master=view_item_window, width= int(terminal.winfo_screenwidth()*(1/32)), height=int(terminal.winfo_screenwidth()*(1/32)), file="assets/plus.png")
#resize_picture('assets/minus.png', int(terminal.winfo_screenwidth()*(0.028)))
#minus_picture = PhotoImage(master=view_item_window, width= int(terminal.winfo_screenwidth()*(1/32)), height=int(terminal.winfo_screenwidth()*(1/32)), file="assets/minus.png")
#bg_main = PhotoImage(master=main_window, width= 1550, height=800, file='assets/bg_main.png')
#add_item_button_image = PhotoImage(master=main_window_element1, width= 275, height=165, file='assets/add_button.png')
#search_button_image = PhotoImage(master=main_window_element1, width= 275, height=165, file='assets/search_button.png')
#settings_button_image = PhotoImage(master=main_window, width= 76, height=76, file='assets/settings_button.png')


item_picture = PhotoImage(master=view_item_window, width= 400, height=300, file='')
add_item_item_picture = PhotoImage(master=view_item_window, width= 400, height=300, file='')

serialnumber_item_view_var = tkinter.StringVar()
itemname_item_view_var = tkinter.StringVar()
quantity_item_view_var = tkinter.StringVar()
unit_item_view_var = tkinter.StringVar()
threshhold_item_view_var = tkinter.StringVar()
price_item_view_var = tkinter.StringVar()
url_item_view_var = tkinter.StringVar()
room_item_view_var = tkinter.StringVar()
locker_item_view_var = tkinter.StringVar()
compartment_item_view_var = tkinter.StringVar()
info_item_view_var = tkinter.StringVar()
image_url_item_view_var = tkinter.StringVar()
tags_item_view_var = tkinter.StringVar()

info_main_window_label = Label(main_window, text=get_setting("facility_name"),font=('Arial',int(font_size_read()*1.5),'bold'), bg=get_setting("background_colour"))
info_main_window_label.place(relx= 0.3, rely = 0.01)

add_item_button = Button(main_window, text="Add Item",font=('Arial', font_size_read()), command = lambda: add_item_window.tkraise())
add_item_button.place(relx= 0.02, rely = 0.25,relwidth = 0.3, relheight = 0.06)


settings_button = Button(main_window, text="Settings",font=('Arial',font_size_read()), command = lambda: settings_window.tkraise())
settings_button.place(relx= 0.02, rely = 0.325,relwidth = 0.3, relheight = 0.06)

missing_button = Button(main_window, text="Add missing Item",font=('Arial',font_size_read()), command = lambda: missing_window.tkraise())
missing_button.place(relx= 0.02, rely = 0.4,relwidth = 0.3, relheight = 0.06)

search_latest_serialnumber_button = Button(main_window, text="Show last Entry",font=('Arial',font_size_read()), command = lambda: item_view_function(find_latest_serialnumber()))
search_latest_serialnumber_button.place(relx= 0.02, rely = 0.475,relwidth = 0.3, relheight = 0.06)

create_csv_button = Button(main_window, text="Create CSV/Excel",font=('Arial',font_size_read()), command = lambda: create_csv_window.tkraise())
create_csv_button.place(relx= 0.02, rely = 0.55,relwidth = 0.3, relheight = 0.06)

suchfeldentry = Entry(main_window, bd=2, width=20,font=('Arial',font_size_read()))
suchfeldentry.place(relx = 0.4, rely = 0.1, relheight = 0.06)

    #Rahmen der Entry auf 0 setzen, damit man ihn nicht mehr sieht. Dann Entry auf Bild positionieren sodass es so aussieht, als wäre das Bild die Entry

suchfeldentry.bind('<Return>', lambda e: item_search_function(suchfeldentry.get()))

item_suche_execute = Button(main_window, text="Search", font=('Arial',font_size_read()), command = lambda: [item_search_function(suchfeldentry.get())])
item_suche_execute.place(relx= 0.6, rely = 0.1, relwidth = 0.1, relheight = 0.06)

print_label_execute = Button(main_window, text="Test Label Printer", font=('Arial',font_size_read()), command = lambda: [print_barcode('12345')])
print_label_execute.place(relx= 0.02, rely = 0.625, relwidth = 0.3, relheight = 0.06)

subtract_list_button = Button(main_window, text="Subtract Items by Scanning", font=('Arial',font_size_read()), command = lambda: [subtract_list_window.tkraise(),scan_list_entry.focus_set()])
subtract_list_button.place(relx= 0.02, rely = 0.7, relwidth = 0.3, relheight = 0.06)

print_custom_label = Button(main_window, text="Create Qrcode for private Material", font=('Arial',font_size_read()), command = lambda: [create_custom_label_window.tkraise()])
print_custom_label.place(relx= 0.02, rely = 0.775, relwidth = 0.3, relheight = 0.06)

suchfeldentry.focus_set()

####################################################################################Search Results###########################################################################

scrollbar = Scrollbar(search_results_window)
scrollbar.place(relx= 0.005, rely = 0.01, relwidth = 0.02, relheight = 0.8)
#scrollbar.pack( side = RIGHT, fill = Y )
    

mylist = Listbox(search_results_window, yscrollcommand = scrollbar.set, font=('Arial',font_size_read()))
mylist.place(relx= 0.03, rely = 0.01, relwidth = 0.6, relheight = 0.8)
scrollbar.config( command = mylist.yview )

serialnumberlist = []

view_item_button = Button(search_results_window, text="View Item", font=('Arial',font_size_read()), command = lambda: [item_view_function(serialnumberlist[mylist.curselection()[0]]),serialnumberlist.clear()]) #[item_view_function(serialnumberlist[mylist.curselection()[0]])])
view_item_button.place(relx= 0.05, rely = 0.9, relwidth=0.2, relheight = 0.06)

close_view_item_button = Button(search_results_window, text="Close Search Results", font=('Arial',font_size_read()), command = lambda: [main_window.tkraise(),suchfeldentry.delete(0, 'end')])
close_view_item_button.place(relx= 0.75, rely = 0.9, relwidth=0.2, relheight = 0.06)

#################################################################################### Add Item ###########################################################################################################################

unit_list = ["Stück","m", "qm"]     #Dropown Menu
variable = StringVar(add_item_window)
variable.set(unit_list[0])

itemnameentry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
quantityentry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
unitentry = Entry(add_item_window, bd=5, width=6,font=('Arial',font_size_read()))

#unit2 = OptionMenu(add_item_window, variable, *unit_list)
#unit2.config(width=6,font=('Arial',font_size_read()))

lowthreshholdentry = Entry(add_item_window, bd=5, width=6,font=('Arial',font_size_read()))
priceentry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
urlentry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
serialnumberentry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
roomentry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
lockerentry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
compartmententry = Entry(add_item_window, bd=5, width=40,font=('Arial',font_size_read()))
infoentry = Text(add_item_window,font=('Arial',font_size_read()))
tagsentry = Text(add_item_window,font=('Arial',font_size_read()))

unitentry.insert(0, "Pieces")
lowthreshholdentry.insert(0,5)

    
itemnameentry_label = Label(add_item_window, text="Name",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
quantityentry_label = Label(add_item_window, text="Amount",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
unitentry_label = Label(add_item_window, text="Unit",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
lowthreshholdentry_label = Label(add_item_window, text="Reorder if under threshhold",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
priceentry_label = Label(add_item_window, text="Price",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
urlentry_label = Label(add_item_window, text="URL",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
serialnumberentry_label = Label(add_item_window, text="Serialnumber",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
roomentry_label = Label(add_item_window, text="Room",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
lockerentry_label = Label(add_item_window, text="Locker",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
compartmententry_label = Label(add_item_window, text="Compartment",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
infoentry_label = Label(add_item_window, text="Information",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
tagsentry_label = Label(add_item_window, text="Search Tags",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))

    
itemnameentry.place(relx= 0.02, rely = 0.025, relheight = 0.06)
quantityentry.place(relx= 0.02, rely = 0.1, relheight = 0.06)
unitentry.place(relx= 0.6, rely = 0.1, relheight = 0.06)
#unit2.place(relx= 0.6, rely = 0.1, relheight = 0.06)
lowthreshholdentry.place(relx= 0.6, rely = 0.175, relheight = 0.06)
priceentry.place(relx= 0.02, rely = 0.175, relheight = 0.06)
urlentry.place(relx= 0.02, rely = 0.25, relheight = 0.06)
serialnumberentry.place(relx= 0.02, rely = 0.325, relheight = 0.06)
roomentry.place(relx= 0.02, rely = 0.4, relheight = 0.06)
lockerentry.place(relx= 0.02, rely = 0.475, relheight = 0.06)
compartmententry.place(relx= 0.02, rely = 0.55, relheight = 0.06)
infoentry.place(relx= 0.02, rely = 0.625, relheight = 0.15, relwidth=0.4)
tagsentry.place(relx= 0.02, rely = 0.785, relheight = 0.075, relwidth=0.4)


itemnameentry_label.place(relx= 0.45, rely = 0.025, relheight = 0.06)
quantityentry_label.place(relx= 0.45, rely = 0.1, relheight = 0.06)
unitentry_label.place(relx= 0.7, rely = 0.1, relheight = 0.06)
lowthreshholdentry_label.place(relx= 0.7, rely = 0.175, relheight = 0.06)
priceentry_label.place(relx= 0.45, rely = 0.175, relheight = 0.06)
urlentry_label.place(relx= 0.45, rely = 0.25, relheight = 0.06)
serialnumberentry_label.place(relx= 0.45, rely = 0.325, relheight = 0.06)
roomentry_label.place(relx= 0.45, rely = 0.4, relheight = 0.06)
lockerentry_label.place(relx= 0.45, rely = 0.475, relheight = 0.06)
compartmententry_label.place(relx= 0.45, rely = 0.55, relheight = 0.06)
infoentry_label.place(relx= 0.45, rely = 0.625, relheight = 0.06)
tagsentry_label.place(relx= 0.45, rely = 0.785, relheight = 0.06)


itemnameentry.bind('<Return>', lambda e: quantityentry.focus_set())
quantityentry.bind('<Return>', lambda e: unitentry.focus_set())
unitentry.bind('<Return>', lambda e: lowthreshholdentry.focus_set())
lowthreshholdentry.bind('<Return>', lambda e: priceentry.focus_set())
priceentry.bind('<Return>', lambda e: urlentry.focus_set())
urlentry.bind('<Return>', lambda e: serialnumberentry.focus_set())
serialnumberentry.bind('<Return>', lambda e: roomentry.focus_set())
roomentry.bind('<Return>', lambda e: lockerentry.focus_set())
lockerentry.bind('<Return>', lambda e: compartmententry.focus_set())
compartmententry.bind('<Return>', lambda e: infoentry.focus_set())
infoentry.bind('<Return>', lambda e: tagsentry.focus_set())


no_picture_label = Label(add_item_window, text="Picture not available",font=('Arial',font_size_read(),'bold'))
no_picture_label.place(relx= 0.65, rely = 0.45)
new_picture_label = Label(add_item_window, image=add_item_item_picture)
new_picture_label.place(relx= 0.6, rely = 0.4)



new_item_save_item = Button(add_item_window, text="Speichern",font=('Arial',font_size_read()), command = lambda:[write_to_database(itemnameentry.get(),
                                                                                       int(quantityentry.get()),
                                                                                       unitentry.get(),
                                                                                       int(lowthreshholdentry.get()),                                            
                                                                                       priceentry.get(),
                                                                                       urlentry.get(),
                                                                                       int(serialnumberentry.get()),
                                                                                       roomentry.get(),
                                                                                       lockerentry.get(),
                                                                                       compartmententry.get(),
                                                                                       infoentry.get("1.0",END),
                                                                                       upload_image(serialnumberentry.get()),                                            
                                                                                       (tagsentry.get("1.0",END)+itemnameentry.get()+" "+roomentry.get()+" "+lockerentry.get()+" "+compartmententry.get())) , #tags ist ein Textfeld, kein Entry, deshalb extra Parameter benötigt

                                                                                       print(get_image_url_global()),
                                                                                       serialnumberentry.delete(0, 'end'),
                                                                                       itemnameentry.delete(0, 'end'),
                                                                                       quantityentry.delete(0, 'end'),                          
                                                                                       priceentry.delete(0, 'end'),
                                                                                       urlentry.delete(0, 'end'),
                                                                                       tagsentry.delete("1.0",END),
                                                                                       infoentry.delete("1.0",END),
                                                                                       roomentry.delete(0, 'end'),
                                                                                       lockerentry.delete(0, 'end'),
                                                                                       compartmententry.delete(0, 'end'),
                                                                                       delete_image_url_global(),
                                                                                       delete_picture()])

new_item_save_item.place(relx = 0.02, rely = 0.90, relwidth=0.2, relheight=0.06)

new_item_back_to_main_window = Button(add_item_window, text="Zurück",font=('Arial',font_size_read()), command = lambda:[main_window.tkraise(),
                                                                        serialnumberentry.delete(0, 'end'),
                                                                        itemnameentry.delete(0, 'end'),
                                                                        quantityentry.delete(0, 'end'),
                                                                        priceentry.delete(0, 'end'),
                                                                        urlentry.delete(0, 'end'),
                                                                        tagsentry.delete("1.0",END),
                                                                        infoentry.delete("1.0",END),
                                                                        roomentry.delete(0, 'end'),
                                                                        lockerentry.delete(0, 'end'),
                                                                        compartmententry.delete(0, 'end'),
                                                                        delete_image_url_global(),                                                
                                                                        delete_picture()])

new_item_back_to_main_window.place(relx = 0.22, rely = 0.9, relwidth=0.2, relheight=0.06)

take_picture_button = Button(add_item_window, text="Take Picture",font=('Arial',font_size_read()), command = lambda: take_picture(serialnumberentry.get()))
take_picture_button.place(relx = 0.82, rely = 0.90, relwidth=0.2, relheight=0.06)

print_qrcode_add_item = Button(add_item_window, text="Print QRCode", font=('Arial',font_size_read()), command = lambda: [print_qrcode(itemnameentry.get(),serialnumberentry.get()+'_'+itemnameentry.get()+'_'+infoentry.get("1.0",END))])
print_qrcode_add_item.place(relx= 0.42, rely = 0.9, relwidth = 0.2, relheight = 0.06)

print_barcode_add_item = Button(add_item_window, text="Print Barcode", font=('Arial',font_size_read()), command = lambda: [print_barcode(serialnumberentry.get())])
print_barcode_add_item.place(relx= 0.62, rely = 0.9, relwidth = 0.2, relheight = 0.06)

fill_serialnumber_button = Button(add_item_window, text="Fill Serialnumber",font=('Arial',font_size_read()), command = lambda: serialnumberentry.insert(0,find_latest_serialnumber()+1))
fill_serialnumber_button.place(relx = 0.6, rely = 0.325, relwidth=0.2, relheight=0.06)

######################################################################################Item View###############################################################################################################
                                      ## In Labels StringVar OHNE .get() verwenden. Überall anders StringVars MIT .get() verwenden
                                                                                               



item_picture_label = Label(view_item_window, image=item_picture)
item_picture_label.place(relx= 0.6, rely = 0.1)

name_label = Label(view_item_window,font=('Arial',font_size_read()+4,'bold'),bg=get_setting("background_colour"), textvariable=itemname_item_view_var)
name_label.place(relx=0.2, rely = 0.025)

quantity_Label = Label(view_item_window, text="Amount:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
quantity_Label.place(relx=0.05, rely = 0.075)
quantity_view = Entry(view_item_window, bd=5, width=5, font=('Arial',font_size_read()))
quantity_view.place(relx= 0.2, rely = 0.075)
unitview_label = Label(view_item_window, font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"),textvariable=unit_item_view_var)
unitview_label.place(relx= 0.26, rely = 0.075)

#plus_label = Label(view_item_window, image=plus_picture, bg=get_setting("background_colour"))
#plus_label.place(relx= 0.33, rely = 0.075)
#minus_label = Label(view_item_window, image=minus_picture, bg=get_setting("background_colour"))
#minus_label.place(relx= 0.37, rely = 0.075)
#plus_label.bind("<Button-1>",lambda e:[add_one_to_entry(quantity_view), change_one_database(serialnumber_item_view_var.get(), "quantity", quantity_view.get())])  #ändern der Anzahl in der Database, dafür übergeben Seriennummer des Items, Key des Dicts das geändert werden soll und der neue Wert
#minus_label.bind("<Button-1>",lambda e:[subtract_one_from_entry(quantity_view), change_one_database(serialnumber_item_view_var.get(), "quantity", quantity_view.get())])

plus_button = Button(view_item_window, text="+",font=('Arial',font_size_read()), command = lambda:[add_one_to_entry(quantity_view), change_one_database(serialnumber_item_view_var.get(), "quantity", quantity_view.get()) ])
plus_button.place(relx= 0.33, rely = 0.075, relwidth = 0.03, relheight = 0.05)
minus_button = Button(view_item_window, text="-",font=('Arial',font_size_read()+2), command = lambda:[subtract_one_from_entry(quantity_view), change_one_database(serialnumber_item_view_var.get(), "quantity", quantity_view.get())])
minus_button.place(relx= 0.37, rely = 0.075, relwidth = 0.03, relheight = 0.05)

price_label = Label(view_item_window, text=("Price:"),font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
price_label.place(relx=0.05, rely = 0.15)
price_label2 = Label(view_item_window, textvariable=price_item_view_var,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
price_label2.place(relx=0.2, rely = 0.15)

url_label = Label(view_item_window, text=("URL:"),font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
url_label.place(relx=0.05, rely = 0.225)
url_label2 = Label(view_item_window, textvariable=url_item_view_var,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
url_label2.place(relx=0.2, rely = 0.225)

serialnumber_label = Label(view_item_window, text=("Serialnumber:"),font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
serialnumber_label.place(relx=0.05, rely = 0.3)
serialnumber_label2 = Label(view_item_window, textvariable=serialnumber_item_view_var,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
serialnumber_label2.place(relx=0.2, rely = 0.3)

room_label = Label(view_item_window, text="Room:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
room_label.place(relx=0.05, rely = 0.375)
room_label2 = Label(view_item_window, textvariable=room_item_view_var,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
room_label2.place(relx=0.2, rely = 0.375)

locker_label = Label(view_item_window, text="Locker:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
locker_label.place(relx=0.05, rely = 0.45)
locker_label2 = Label(view_item_window, textvariable=locker_item_view_var,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
locker_label2.place(relx=0.2, rely = 0.45)

compartment_label = Label(view_item_window, text="Compartment:"+compartment_item_view_var.get(),font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
compartment_label.place(relx=0.05, rely = 0.525)
compartment_label = Label(view_item_window, textvariable=compartment_item_view_var,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
compartment_label.place(relx=0.2, rely = 0.525)

info_view_label = Label(view_item_window, text="Information:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
info_view_label.place(relx=0.05, rely = 0.6)
info_view_entry = Text(view_item_window,font=('Arial',font_size_read()))
info_view_entry.place(relx= 0.05, rely = 0.6, relheight = 0.175, relwidth=0.45)


item_change_button = Button(view_item_window, text="Change Item",font=('Arial',font_size_read()), command = lambda: [item_change_function(serialnumber_item_view_var.get())])
item_change_button.place(relx= 0.05, rely = 0.9, relwidth = 0.2, relheight = 0.06)

back_to_results_window_button = Button(view_item_window, text="Search Results",font=('Arial',font_size_read()), command = lambda: [item_search_function(suchfeldentry.get())])
back_to_results_window_button.place(relx= 0.75, rely = 0.84, relwidth = 0.2, relheight = 0.06)

print_barcode_view_item = Button(view_item_window, text="Print Barcode", font=('Arial',font_size_read()), command = lambda: [print_barcode(serialnumber_item_view_var.get())])
print_barcode_view_item.place(relx= 0.35, rely = 0.9, relwidth = 0.2, relheight = 0.06)

reorder_view_item = Button(view_item_window, text="Reorder", font=('Arial',font_size_read()), command = lambda: [write_to_missing_database('yes',itemname_item_view_var.get(),'', serialnumber_item_view_var.get())])
reorder_view_item.place(relx= 0.55, rely = 0.9, relwidth = 0.2, relheight = 0.06)

print_qrcode_view_item = Button(view_item_window, text="Print QRcode", font=('Arial',font_size_read()), command = lambda: [print_qrcode(itemname_item_view_var.get(),serialnumber_item_view_var.get()+'_'+itemname_item_view_var.get()+'_'+info_item_view_var.get())])
print_qrcode_view_item.place(relx= 0.35, rely = 0.84, relwidth = 0.2, relheight = 0.06)

back_to_main_window_button = Button(view_item_window, text="Main Menu",font=('Arial',font_size_read()), command = lambda: [main_window.tkraise(),suchfeldentry.delete(0, 'end')])
back_to_main_window_button.place(relx= 0.75, rely = 0.9, relwidth = 0.2, relheight = 0.06)
######################################################################################Item Change################################################################################################################

change_item_item_picture_label = Label(change_item_window, image=item_picture)
change_item_item_picture_label.place(relx= 0.7, rely = 0.4)

change_item_name_label = Label(change_item_window, text="Name",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_name_label.place(relx=0.05, rely = 0.025)
change_item_name_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_name_entry.place(relx= 0.2, rely = 0.025)


change_item_quantity_Label = Label(change_item_window, text="Amount:  ",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_quantity_Label.place(relx=0.05, rely = 0.075)
change_item_quantity_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_quantity_entry.place(relx= 0.2, rely = 0.075)

change_item_unit_Label = Label(change_item_window, text="Unit:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_unit_Label.place(relx=0.5, rely = 0.075)
change_item_unit_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_unit_entry.place(relx= 0.7, rely = 0.075)


change_item_price_label = Label(change_item_window, text=("Price:           "),font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_price_label.place(relx=0.05, rely = 0.125)
change_item_price_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_price_entry.place(relx= 0.2, rely = 0.125)

change_item_threshhold_Label = Label(change_item_window, text="Reorder when under Threshhold:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_threshhold_Label.place(relx=0.5, rely = 0.125)
change_item_threshhold_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_threshhold_entry.place(relx= 0.7, rely = 0.125)


change_item_url_label = Label(change_item_window, text=("URL:"),font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_url_label.place(relx=0.05, rely = 0.175)
change_item_url_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_url_entry.place(relx= 0.2, rely = 0.175)


change_item_serialnumber_label = Label(change_item_window, text=("Serialnumber:"),font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_serialnumber_label.place(relx=0.05, rely = 0.225)
change_item_serialnumber_label2 = Label(change_item_window, textvariable=serialnumber_item_view_var,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_serialnumber_label2.place(relx= 0.2, rely = 0.225)
    

change_item_room_label = Label(change_item_window, text="Room:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_room_label.place(relx=0.05, rely = 0.275)
change_item_room_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_room_entry.place(relx= 0.2, rely = 0.275)


change_item_locker_label = Label(change_item_window, text="Locker:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_locker_label.place(relx=0.05, rely = 0.325)
change_item_locker_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_locker_entry.place(relx= 0.2, rely = 0.325)


change_item_compartment_label = Label(change_item_window, text="Compartment:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_compartment_label.place(relx=0.05, rely = 0.375)
change_item_compartment_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_compartment_entry.place(relx= 0.2, rely = 0.375)

change_item_image_url_label = Label(change_item_window, text="Image URL:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_image_url_label.place(relx=0.05, rely = 0.425)
change_item_image_url_entry = Entry(change_item_window, bd=5, width=20, font=('Arial',font_size_read()))
change_item_image_url_entry.place(relx= 0.2, rely = 0.425)


change_item_tags_label = Label(change_item_window, text="Tags:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_tags_label.place(relx=0.05, rely = 0.5)
change_item_tags_entry = Text(change_item_window,font=('Arial',font_size_read()))
change_item_tags_entry.place(relx= 0.2, rely = 0.5, relheight = 0.18, relwidth=0.45)

change_item_info_label = Label(change_item_window, text="Information:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_info_label.place(relx=0.05, rely = 0.7)
change_item_info_entry = Text(change_item_window,font=('Arial',font_size_read()))
change_item_info_entry.place(relx= 0.2, rely = 0.7, relheight = 0.18, relwidth=0.45)

    
change_item_item_save = Button(change_item_window, text="Save", font=('Arial',font_size_read()), command = lambda:[ item_view_function(serialnumber_item_view_var.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "itemname", change_item_name_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "quantity", int(change_item_quantity_entry.get())),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "unit", change_item_unit_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "threshhold", int(change_item_threshhold_entry.get())),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "price", change_item_price_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "url", change_item_url_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "room", change_item_room_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "locker", change_item_locker_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "compartment", change_item_compartment_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "image_url", change_item_image_url_entry.get()),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "tags", change_item_tags_entry.get("1.0",END)),
                                                                                                    change_one_database(serialnumber_item_view_var.get(), "info", change_item_info_entry.get("1.0",END)),
                                                                                                    item_view_function(serialnumber_item_view_var.get())])
change_item_item_save.place(relx= 0.05, rely = 0.92, relwidth = 0.3, relheight = 0.06)

take_picture_button = Button(change_item_window, text="Take new Picture",font=('Arial',font_size_read()), command = lambda: take_picture(serialnumber_item_view_var.get()))
take_picture_button.place(relx = 0.7, rely = 0.92, relwidth=0.2, relheight=0.06)

def upload_if_not_empty():
    imagelink = upload_image(serialnumber_item_view_var.get())
    if not imagelink == '':
        change_item_image_url_entry.delete(0, 'end')
        change_item_image_url_entry.insert(0, imagelink)
    else:
        print("Kein Bilder-Link")

upload_picture_button = Button(change_item_window, text="Upload Image",font=('Arial',font_size_read()), command = lambda:[upload_if_not_empty()])
upload_picture_button.place(relx = 0.5, rely = 0.92, relwidth=0.2, relheight=0.06)


############################################################################################## Options ##############################################################################################################

back_to_main_options_button = Button(settings_window, text="Main Menu",font=('Arial',font_size_read()), command = lambda: main_window.tkraise())
back_to_main_options_button.place(relx = 0.02, rely = 0.85, relwidth=0.2, relheight=0.06)

open_options_button = Button(settings_window, text="Open Settings",font=('Arial',font_size_read()), command = lambda: os.system('settings.txt'))
open_options_button.place(relx = 0.02, rely = 0.45, relwidth=0.2, relheight=0.06)

test_database_options_button = Button(settings_window, text="Test Database Connection",font=('Arial',font_size_read()), command = lambda: test_database())
test_database_options_button.place(relx = 0.02, rely = 0.6, relwidth=0.2, relheight=0.06)

connection_string_label = Label(settings_window, text="MongoDB Connection String",font=('Arial',16))
connection_string_label.place(x=60, y = 280)
connection_string_entry = Entry(settings_window, bd=5, width=20, font=('Arial',16))
connection_string_entry.place(x= 60, y = 320)

change_item_tags_label = Label(settings_window, text=program_version,font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
change_item_tags_label.place(relx=0.9, rely = 0.9)


############################################################################################# Missing ################################################################################################################

info_main_window_label = Label(missing_window, text="Enter missing Items",font=('Arial',int(font_size_read()*1.5),'bold'), bg=get_setting("background_colour"))
info_main_window_label.place(relx= 0.3, rely = 0.01)

missing_item_label = Label(missing_window, text="Enter missing Items",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
missing_item_label.place(relx=0.02, rely = 0.2)
missing_item_entry = Entry(missing_window, bd=5, width=40,font=('Arial',font_size_read()))
missing_item_entry.place(relx = 0.02, rely = 0.25)

missing_item_label = Label(missing_window, text="Information about missing Items",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
missing_item_label.place(relx=0.02, rely = 0.4)
info_box_entry = Text(missing_window,font=('Arial',font_size_read()))
info_box_entry.place(relx= 0.02, rely = 0.5, relheight = 0.2, relwidth=0.4)


back_to_main_options_button = Button(missing_window, text="Save",font=('Arial',font_size_read()), command = lambda: [write_to_missing_database('No', missing_item_entry.get(), info_box_entry.get("1.0",END), 0),
                                                                                                                            missing_item_entry.delete(0, 'end'),
                                                                                                                            info_box_entry.delete("1.0",END)])
back_to_main_options_button.place(relx = 0.2, rely = 0.85, relwidth=0.2, relheight=0.06)

back_to_main_options_button = Button(missing_window, text="Main Menu",font=('Arial',font_size_read()), command = lambda: main_window.tkraise())
back_to_main_options_button.place(relx = 0.02, rely = 0.85, relwidth=0.2, relheight=0.06)





############################################################################################# create CSV ##################################################################################################################

def output_csv(datenbank):

    if datenbank == "items":
        print("creating CSV of Items Database")
        header = ['itemname','quantity','price','url','serialnumber','room','locker','compartment']
        with open('items.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            all_items = collection_name.find({})
            for item in all_items:
               data = [item['itemname'],item['quantity'],item['price'],item['url'],item['serialnumber'],item['room'],item['locker'],item['compartment']]
               writer.writerow(data) 

def output_excel(start_at):        
     workbook = xlsxwriter.Workbook('items.xlsx')
     worksheet = workbook.add_worksheet()
     header = ['itemname','quantity','price','url','serialnumber','room','locker','compartment']

     if start_at == '':
         start_at = 0

     worksheet.write(0,0,header[0])
     worksheet.write(0,1,header[1])
     worksheet.write(0,2,header[2])
     worksheet.write(0,3,header[3])
     worksheet.write(0,4,header[4])
     worksheet.write(0,5,header[5])
     worksheet.write(0,6,header[6])
     worksheet.write(0,7,header[7])
     
     row=1
     print("Creating Excel File of Items Database")
     all_items = collection_name.find({})
     for item in all_items:
        if int(item['serialnumber']) >= int(start_at):
            print(row)
            data = [item['itemname'],item['quantity'],item['price'],item['url'],item['serialnumber'],item['room'],item['locker'],item['compartment']]
            worksheet.write(row,0,item['itemname'])
            worksheet.write(row,1,item['quantity'])
            worksheet.write(row,2,item['price'])
            worksheet.write(row,3,item['url'])
            worksheet.write(row,4,item['serialnumber'])
            worksheet.write(row,5,item['room'])
            worksheet.write(row,6,item['locker'])
            worksheet.write(row,7,item['compartment'])
            row+=1
     workbook.close()

def output_missing_excel(start_at):        
     workbook = xlsxwriter.Workbook('missing_items.xlsx')
     worksheet = workbook.add_worksheet()
     header = ['already_in_database','name','info','serialnumber']

     if start_at == '':
         start_at = 0

     worksheet.write(0,0,header[0])
     worksheet.write(0,1,header[1])
     worksheet.write(0,2,header[2])
     worksheet.write(0,3,header[3])
     
     row=1
     print("Creating Excel File of missing Items Database")
     all_items = missing_collection.find({})
     for item in all_items:
            print(row)
            data = [item['already_in_database'],item['name'],item['info'],item['serialnumber']]
            worksheet.write(row,0,item['already_in_database'])
            worksheet.write(row,1,item['name'])
            worksheet.write(row,2,item['info'])
            worksheet.write(row,3,item['serialnumber'])
            row+=1
     workbook.close()

start_item_label = Label(create_csv_window, text="Start List at Serialnumber:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
start_item_label.place(relx=0.02, rely = 0.2)
start_item_entry = Entry(create_csv_window, bd=5, width=6,font=('Arial',font_size_read()))
start_item_entry.place(relx = 0.02, rely = 0.25)

back_to_main_csv_button = Button(create_csv_window, text="Main Menu",font=('Arial',font_size_read()), command = lambda: main_window.tkraise())
back_to_main_csv_button.place(relx = 0.02, rely = 0.85, relwidth=0.2, relheight=0.06)

create_csv_button = Button(create_csv_window, text="Create CVS of the Items Database",font=('Arial',font_size_read()), command = lambda: output_csv("items"))
create_csv_button.place(relx= 0.02, rely = 0.35,relwidth = 0.5, relheight = 0.06)

create_excel_button = Button(create_csv_window, text="Create Excel of the Items Database",font=('Arial',font_size_read()), command = lambda: [output_excel(start_item_entry.get()),open_label()])
create_excel_button.place(relx= 0.02, rely = 0.425,relwidth = 0.5, relheight = 0.06)

create_missing_excel_button = Button(create_csv_window, text="Create Excel of the missing Items",font=('Arial',font_size_read()), command = lambda: [output_missing_excel(0)])
create_missing_excel_button.place(relx= 0.02, rely = 0.5,relwidth = 0.5, relheight = 0.06)

############################################################################################subtract list###################################################################################################################

def scanned_list_subtract(entry):

    if entry.isnumeric() == True:
        item_found_list = collection_name.find({"serialnumber" : int(entry)})
        
        for item in item_found_list:                                           ##falls bei der Seriennummer etwas gefunden wurd direkt zu View Item gehen und nicht erst zu Suchergebnisse
            if item: entryempty = False
        if  not entryempty:
            
            scanned_list.insert(0, item['itemname'])
            hidden_scanned_list.insert(0, item['serialnumber'])
            
            change_one_database(item['serialnumber'], 'quantity', item['quantity']-1)
            scan_list_entry.delete(0, 'end')
        
def print_list_subtract():

    qr_text = ''

    list_content = hidden_scanned_list.get(0, END)

    for entry in list_content:
        item_found_list = collection_name.find({"serialnumber" : int(entry)})
        for item in item_found_list:                                           ##falls bei der Seriennummer etwas gefunden wurd direkt zu View Item gehen und nicht erst zu Suchergebnisse
            if item: entryempty = False
        if  not entryempty:
            qr_text =  qr_text+item['itemname']+' '+str(item['serialnumber'])+' '+item['price']+'\n'

    print_qrcode('Scanned Items',qr_text)
            
        
    
    

subtract_list_label = Label(subtract_list_window, text="Scanned:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
subtract_list_label.place(relx=0.02, rely = 0.08)

scan_list_entry = Entry(subtract_list_window, bd=2, width=20,font=('Arial',font_size_read()))
scan_list_entry.place(relx = 0.02, rely = 0.01, relheight = 0.06)

scrollbar = Scrollbar(subtract_list_window)
scrollbar.place(relx= 0.82, rely = 0.12, relwidth = 0.02, relheight = 0.6)

hidden_scanned_list = Listbox(subtract_list_window, yscrollcommand = scrollbar.set, font=('Arial',font_size_read()))
hidden_scanned_list.place(relx= 0.02, rely = 0.12, relwidth = 0.8, relheight = 0.6)

scanned_list = Listbox(subtract_list_window, yscrollcommand = scrollbar.set, font=('Arial',font_size_read()))
scanned_list.place(relx= 0.02, rely = 0.12, relwidth = 0.8, relheight = 0.6)
scrollbar.config( command = scanned_list.yview )

scan_list_entry.bind('<Return>', lambda e: scanned_list_subtract(scan_list_entry.get()))

back_to_main_window_button = Button(subtract_list_window, text="Main Menu",font=('Arial',font_size_read()), command = lambda: [main_window.tkraise(),scan_list_entry.delete(0, 'end'),scanned_list.delete(0,END),hidden_scanned_list.delete(0,END)])
back_to_main_window_button.place(relx= 0.75, rely = 0.9, relwidth = 0.2, relheight = 0.06)

print_list_subtract_button = Button(subtract_list_window, text="Print List",font=('Arial',font_size_read()), command = lambda: [print_list_subtract()])
print_list_subtract_button.place(relx= 0.55, rely = 0.9, relwidth = 0.2, relheight = 0.06)

##################################################################################################Create Custom Label################################################################################################

owner_create_custom_label_label = Label(create_custom_label_window, text="Owner:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
owner_create_custom_label_label.place(relx=0.02, rely = 0.05)

owner_create_custom_label_entry = Entry(create_custom_label_window, bd=2, width=20,font=('Arial',font_size_read()))
owner_create_custom_label_entry.place(relx = 0.02, rely = 0.1, relheight = 0.06)

material_create_custom_label_label = Label(create_custom_label_window, text="Material:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
material_create_custom_label_label.place(relx=0.02, rely = 0.175)

material_create_custom_label_entry = Entry(create_custom_label_window, bd=2, width=20,font=('Arial',font_size_read()))
material_create_custom_label_entry.place(relx = 0.02, rely = 0.225, relheight = 0.06)

size_create_custom_label_label = Label(create_custom_label_window, text="Size:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
size_create_custom_label_label.place(relx=0.02, rely = 0.3)

size_create_custom_label_entry = Entry(create_custom_label_window, bd=2, width=20,font=('Arial',font_size_read()))
size_create_custom_label_entry.place(relx = 0.02, rely = 0.35, relheight = 0.06)

info_create_custom_label_label = Label(create_custom_label_window, text="Information about the Item:",font=('Arial',font_size_read(),'bold'), bg=get_setting("background_colour"))
info_create_custom_label_label.place(relx=0.02, rely = 0.425)
info_create_custom_label_entry = Text(create_custom_label_window,font=('Arial',font_size_read()))
info_create_custom_label_entry.place(relx= 0.02, rely = 0.475, relheight = 0.2, relwidth=0.4)

print_create_custom_label_button = Button(create_custom_label_window, text="Print QRCode",font=('Arial',font_size_read()), command = lambda: [print_qrcode("custom_label",owner_create_custom_label_entry.get()+"\n"+material_create_custom_label_entry.get()+"\n"+size_create_custom_label_entry.get()+"\n"+info_create_custom_label_entry.get("1.0",END))])
print_create_custom_label_button.place(relx= 0.02, rely = 0.9, relwidth = 0.2, relheight = 0.06)

back_to_main_window_button = Button(create_custom_label_window, text="Main Menu",font=('Arial',font_size_read()), command = lambda: [main_window.tkraise(),owner_create_custom_label_entry.delete(0, 'end'),material_create_custom_label_entry.delete(0,END),size_create_custom_label_entry.delete(0,END),info_create_custom_label_entry.delete("1.0",END)])
back_to_main_window_button.place(relx= 0.75, rely = 0.9, relwidth = 0.2, relheight = 0.06)

################################################################################################## Start Routine ##############################################################################################################

main_window.tkraise()
#main_window_element1.tkraise()

terminal.mainloop()


