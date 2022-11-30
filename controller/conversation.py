from model.handler import *
from pprint import pprint

def talk_about_API_action():
    obj_joocho = NDFC_api()
    
    select_method = input("Select action you want:\n\
            1. Get Switches Management IP\n\
            2. Get Alarms Counter Info\n\
            3. Delete Alarms\nYour input is : \
        ")
    while True:
        if select_method == "1":
            pprint(obj_joocho.getSwitchMgmt())
            break
        elif select_method == "2":
            pprint(f"Alarms Counter: {len(obj_joocho.getAlarms())}")
            clear_var = input("Do you want clear the alarms? Y/n")
            clear_var = clear_var.upper()
            while True:
                if clear_var == "Y":
                    obj_joocho.deleteAlarms()
                    break
                elif clear_var == "N":
                    break
                else:
                    pprint("Wrong Input please input Y or N")
                    clear_var = input("Do you want clear the alarms? Y/n")
            break
        elif select_method == "3":
            pprint(obj_joocho.deleteAlarms())
            break
        else:
            print("Wrong input. Try again\n")
            select_method = input("""Select action you want:
                1. Get Switches Management IP
                2. Get Alarms ID Info
                3. Delete Alarms
                Your input is : """)
    pprint("Closing...")
