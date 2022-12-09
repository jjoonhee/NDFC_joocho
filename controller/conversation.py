from model.handler import *
from pprint import pprint


def talk_about_API_action():
    obj_joocho = NDFC_api()
    while True:
        select_method = input(f"{start_magenta}Select action you want:{end_color}\n\
                1. Get Switches Management IP\n\
                2. Get Switches status\n\
                3. Get Alarms Info\n\
                4. Delete Alarms\n\
                5. Rediscover All switches\n Your input is : ")
        if select_method == "1":
            pprint(f"Management IP = {obj_joocho.getSwitchMgmt()}")
            fin_var = 999
        elif select_method == "2":
            pprint(obj_joocho.getSwitchStatus()[0])
            fin_var = 999
        elif select_method == "3":
            obj_joocho.returnAlmMsg()
            clear_var = input(f"\n{start_magenta}Do you want clear the alarms? Y/n{end_color} ").upper()
            while True:
                if clear_var == "Y":
                    obj_joocho.deleteAlarms()
                    fin_var = 999
                elif clear_var == "N":
                    fin_var = 999
                    break
                else:
                    print(f"{start_red}Wrong Input please input Y or N{end_color}")
                    clear_var = input(f"{start_magenta}Do you want clear the alarms? Y/n{end_color} ").upper()
        elif select_method == "4":
            pprint(obj_joocho.deleteAlarms())
            fin_var = 999
        elif select_method == "5":
            print(obj_joocho.rediscoverSwitch()["resultMessage"])
            fin_var = 999
        else:
            print(f"{start_red}Wrong input. Try again{end_color}\n")
            select_method = input("""Select action you want:
                1. Get Switches Management IP
                2. Get Alarms ID Info
                3. Delete Alarms
                Your input is : """)
        if fin_var == 999:
            fin_go = input("Wanna continue? Y/n").upper()
            if fin_go == "Y":
                continue
            elif fin_go == "N":
                break
            else:
                print("Wrong Input\n")
        else:
            pass
    pprint("Closing...")
