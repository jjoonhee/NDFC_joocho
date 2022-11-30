from model.handler import *
from pprint import pprint

def talk_about_API_action():
    obj_joocho = NDFC_api()
    
    select_method = input("Select action you want:\n\
            1. Get Switches Management IP\n\
            2. Get Alarms Info\n\
            3. Delete Alarms\nYour input is : \
        ")
    while True:
        if select_method == "1":
            pprint(obj_joocho.getSwitchMgmt())
            break
        elif select_method == "2":
            obj_joocho.returnAlmMsg()
            clear_var = input("\033[95mDo you want clear the alarms? Y/n\033[0m ")
            clear_var = clear_var.upper()
            while True:
                if clear_var == "Y":
                    obj_joocho.deleteAlarms()
                    break
                elif clear_var == "N":
                    break
                else:
                    pprint("Wrong Input please input Y or N")
                    clear_var = input("\033[95mDo you want clear the alarms? Y/n\033[0m ")
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
