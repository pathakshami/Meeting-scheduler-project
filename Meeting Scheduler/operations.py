import json
import string
import random
from json import JSONDecodeError
from datetime import datetime,date 

def AutoGenerate_EventID():
    #generate a random Event ID
    Event_ID=''.join(random.choices(string.ascii_uppercase+string.digits,k=3))
    return Event_ID

def Register(type,member_json_file,organizer_json_file,Full_Name,Email,Password):
    '''Register the member/ogranizer based on the type with the given details'''
    if type.lower()=='organizer':
        f=open(organizer_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()
    else:
        f=open(member_json_file,'r+')
        d={
            "Full Name":Full_Name,
            "Email":Email,
            "Password":Password
        }
        try:
            content=json.load(f)
            if d not in content:
                content.append(d)
                f.seek(0)
                f.truncate()
                json.dump(content,f)
        except JSONDecodeError:
            l=[]
            l.append(d)
            json.dump(l,f)
        f.close()


def Login(type,members_json_file,organizers_json_file,Email,Password):
    '''Login Functionality || Return True if successful else False'''
    d=0
    if type.lower()=='organizer':
        f=open(organizers_json_file,'r+')
    else:
        f=open(members_json_file,'r+')
    try:
        content=json.load(f)
    except JSONDecodeError:
        f.close()
        return False
    for i in range(len(content)):
        if content[i]["Email"]==Email and content[i]["Password"]==Password:
            d=1
            break
    if d==0:
        f.close()
        return False
    f.close()
    return True

def Create_Event(org,events_json_file,Event_ID,Event_Name,Start_Date,Start_Time,End_Date,End_Time,Users_Registered,Capacity,Availability):
    '''Create an Event with the details entered by organizer'''
    f1=open(events_json_file,'r+')
    d1={
        "ID": Event_ID,
        "Name": Event_Name,
        "Organizer":org,
        "Start Date":Start_Date,
        "Start Time":Start_Time,
        "End Date":End_Date,
        "End Time":End_Time,
        "Users Registered":Users_Registered,
        "Capacity":Capacity,
        "Seats Available":Availability

        }
    try:
        content1=json.load(f1)
        if d1 not in content1:
            content1.append(d1)
            f1.seek(0)
            f1.truncate()
            json.dump(content1,f1)
    except JSONDecodeError:
        l1=[]
        l1.append(d1)
        json.dump(l1,f1)
    f1.close()
    

    

def View_Events(org,events_json_file):
    '''Return a list of all events created by the logged in organizer'''
    e_list=[]
    f2=open(events_json_file,'r+')
    try:
        contents2=json.load(f2)
    except JSONDecodeError:    
         print("An error occured")

    for i in range(len(contents2)):
        if contents2[i]["Organizer"]==org:
           e_list.append(contents2[i])
    return e_list

    

def View_Event_ByID(events_json_file,Event_ID):
    '''Return details of the event for the event ID entered by user'''
    e_list2=[]
    f3=open(events_json_file,'r+')
    try:
        contents3=json.load(f3)
    except JSONDecodeError:
     print("An error occured")
    for i in range(len(contents3)):
        if contents3[i]["ID"]==Event_ID:
            e_list2.append(contents3[i])
    return(e_list2)
        





    

def Update_Event(org,events_json_file,event_id,detail_to_be_updated,updated_detail):
    '''Update Event by ID || Take the key name to be updated from member, then update the value entered by user for that key for the selected event
    || Return True if successful else False'''
    details=detail_to_be_updated.split("||")
    up_details=updated_detail.split("||")
    f1=open(events_json_file,'r+')
    try:
       content1=json.load(f1)
    except JSONDecodeError:
        return False
         

    my_dict={}
    for key,value in zip(details,up_details):
        my_dict[key]=value

    for i in range(len(content1)):
        if content1[i]["ID"]==event_id:
           content1[i].update(my_dict) 
           f1.seek(0)
           f1.truncate()
           json.dump(content1,f1)
           return True
    f1.close()


           

   

    

def Delete_Event(org,events_json_file,event_ID):
    '''Delete the Event with the entered Event ID || Return True if successful else False'''
    f1=open(events_json_file,'r+')
    try:
        content1=json.load(f1)
        
    except JSONDecodeError:
        f1.close()
        return False
    for i in range(len(content1)):
        if content1[i]["ID"]==event_ID:
            del content1[i]
            f1.seek(0)
            f1.truncate()
            json.dump(content1,f1)
            f1.close()
            return True
        
    
    



def Register_for_Event(events_json_file,event_id,Full_Name):
    '''Register the logged in member in the event with the event ID entered by member. 
    (append Full Name inside the "Users Registered" list of the selected event)) 
    Return True if successful else return False'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''
    f1=open(events_json_file,'r+')
    try:
        content1=json.load(f1)
        
    except JSONDecodeError:
     f1.close()
     return False
    for i in range(len(content1)):
        if content1[i]["ID"]==event_id:
            if content1[i]["Start Date"]>= date_today  and content1[i]["Seats Available"]>=1 :
                content1[i]["Users Registered"].append(Full_Name)
                x=content1[i]["Seats Available"]
                x=x-1
                content1[i]["Seats Available"]=x 
                f1.seek(0)
                f1.truncate()
                json.dump(content1,f1)
                f1.close()
                return True
          
                



       

def fetch_all_events(events_json_file,Full_Name,event_details,upcoming_ongoing):
    '''View Registered Events | Fetch a list of all events of the logged in memeber'''
    '''Append the details of all upcoming and ongoing events list based on the today's date/time and event's date/time'''
    date_today=str(date.today())
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    '''Write your code below this line'''

    

def Update_Password(members_json_file,Full_Name,new_password):
    '''Update the password of the member by taking a new passowrd || Return True if successful else return False'''
    f1=open(members_json_file,'r+')
    try:
        content1=json.load(f1)
        
    except JSONDecodeError:
        f1.close()
        return False
    for i in range(len(content1)):
        if content1[i]["Full Name"]==Full_Name:
            content1[i]["Password"]=new_password
            f1.seek(0)
            f1.truncate()
            json.dump(content1,f1)
            f1.close()
            return True
        

    

def View_all_events(events_json_file):
    '''Read all the events created | DO NOT change this function'''
    '''Already Implemented Helper Function'''
    details=[]
    f=open(events_json_file,'r')
    try:
        content=json.load(f)
        f.close()
    except JSONDecodeError:
        f.close()
        return details
    for i in range(len(content)):
        details.append(content[i])
    return details
