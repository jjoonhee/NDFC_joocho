from model.handler import *
from pprint import pprint


def talk_about_API_action():
    obj_joocho = NDFC_api()
    fin_var = False
    while True:
        select_method = input(f"""{start_magenta}Select action you want:{end_color}\n\
            1. Get Switches Management IP\n\
            2. Get Switches status\n\
            3. Get Alarms Info\n\
            4. Delete Alarms\n\
            5. Rediscover All switches\n*Press 0(Zero) if you wanna close\n Your input is : """)
        if select_method == "1":
            pprint(f"Management IP = {obj_joocho.getSwitchMgmt()}", indent = 4)
            fin_var = True
        elif select_method == "2":
            pprint(obj_joocho.getSwitchStatus()[0])
            fin_var = True
        elif select_method == "3":
            if bool(obj_joocho.returnAlmMsg()) is False:
                fin_var = True
            else:
                clear_var = input(f"\n{start_magenta}Do you want to clear the alarms? Y/n{end_color} ").upper()
                while True:
                    if clear_var == "Y":
                        obj_joocho.deleteAlarms()
                        fin_var = True
                        break
                    elif clear_var == "N":
                        fin_var = True
                        break
                    else:
                        print(f"{start_red}Wrong Input please input Y or N{end_color}")
                        clear_var = input(f"{start_magenta}Do you want to clear the alarms? Y/n{end_color} ").upper()
        elif select_method == "4":
            obj_joocho.deleteAlarms()
            fin_var = True
        elif select_method == "5":
            print(obj_joocho.rediscoverSwitch()["resultMessage"])
            fin_var = True
        elif select_method == "0":
            print("Closing...")
            exit()
        else:
            print(f"{start_red}Wrong input. Try again{end_color}\n")
            select_method = input(f"""{start_magenta}Select action you want:{end_color}\n\
                1. Get Switches Management IP\n\
                2. Get Switches status\n\
                3. Get Alarms Info\n\
                4. Delete Alarms\n\
                5. Rediscover All switches\n\n*Press 0(Zero) if you wanna close\n Your input is : """)
        if fin_var == True:
            while True:
                fin_go = input("Wanna continue? Y/n ").upper()
                if fin_go == "Y":
                    break
                elif fin_go == "N":
                    print("Closing...\n")
                    exit()
                else:
                    print("Wrong Input\n")
        else:
            pass
    pprint("Closing...")
