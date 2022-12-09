import requests
import os
import json
import pprint as pprint
import time
import sys
import subprocess
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

start_magenta = "\033[95m"
start_red = "\033[31m"
end_color = "\033[0m"
update_date = "Last Updated date : 2022.12.9, joocho"

try:
    import pwinput
except:
    subprocess.check_call([sys.executable, "pip", "install", "pwinput"])
    import pwinput
try:
    from tqdm import tqdm
except:
    subprocess.check_call([sys.executable, "pip", "install", "tqdm"])
    from tqdm import tqdm

class Login_NDFC():
    __doc__="Hello"
    def loginNDFC(self):
        self.userName = input("Insert your username: ")
        self.passWd = pwinput.pwinput("Input your password: ", mask="*")
        while True:
            try:
                self.payload = json.dumps({
                "userName": self.userName,
                "userPasswd": self.passWd,
                "domain": "DefaultAuth",
                "uiLogin": True
                })
                response = requests.request("POST", self.url, headers={'Content-Type': 'application/json'}, data=self.payload, verify=False)
                response = json.loads(response.text)
                if response["statusCode"] == 200:
                    print(f"{start_magenta}Authentication success{end_color}")
                    self.response = response
                    break
            except:
                print(f"{start_red}Authentication failed, Check your username/Password{end_color}")
                self.userName = input("Insert your username: ")
                self.passWd = pwinput.pwinput("Insert your password: ")
    

class NDFC_api(Login_NDFC):
    __doc__="Hello"
    def __init__(self):
        print("\033[95m" + "=" * 20 + "NDFC API easy Excutor Service" + "=" * 20)
        print(f"{update_date:>68}\n\033[0m")
        login_input = input("Insert your NDFC MgmtIP: ")
        while True:
            try:
                url = f"https://{login_input}/login"
                response = requests.request("GET", url, verify=False, timeout=2)
                if response.status_code == 200:
                    print(f"{start_magenta} ###Reachability verified### {end_color}\n")
                    self.login_input = login_input
                    self.url = url
                    break
            except requests.exceptions.Timeout as errd:
                print("Timeout Error : ", errd)
                login_input = input(f"{start_red}IP is not valid, Try again{end_color}\nNDFC MgmtIP: ")
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting : ", errc)
                login_input = input(f"{start_red}IP is not valid, Try again{end_color}\nNDFC MgmtIP: ")
            except requests.exceptions.HTTPError as errb:
                print("Http Error : ", errb)
                login_input = input(f"{start_red}IP is not valid, Try again{end_color}\nNDFC MgmtIP: ")
            except:
                login_input = input(f"{start_red}IP is not valid, Try again{end_color}\nNDFC MgmtIP: ")
        self.loginNDFC()
        self.headers = {
            'Content-Type': 'application/json',
            'Cookie': "AuthCookie=" + self.response["token"]
        } 

    def getSwitchMgmt(self):
        mgmt_IP = []
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/inventory/allswitches"
        response = requests.request("GET", url, headers=self.headers, data=self.payload, verify=False)
        res = json.loads(response.text)
        for k in range(len(res)):
          mgmt_IP.append(res[k]["ipAddress"])
        mgmt_IP.sort()
        return mgmt_IP

    def getSwitchStatus(self):
        sum_status = {}
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/lan-fabric/rest/inventory/allswitches"
        response = requests.request("GET", url, headers = self.headers, data = self.payload, verify = False)
        self.res = json.loads(response.text)
        for k in range(len(self.res)):
            sum_status[self.res[k]["logicalName"]] = {"ccStatus" : "", "fabricName" : "", "ipAddress": "", "Discover_status": ""}
            sum_status[self.res[k]["logicalName"]]["ccStatus"] = self.res[k]["ccStatus"]
            sum_status[self.res[k]["logicalName"]]["fabricName"] = self.res[k]["fabricName"]
            sum_status[self.res[k]["logicalName"]]["ipAddress"] = self.res[k]["ipAddress"]
            sum_status[self.res[k]["logicalName"]]["Discover_status"] = self.res[k]["status"]
        return sum_status, self.res


    def getAlarmInfo(self):
        id_list = []
        self.res_result = []
        self.call_time = int()
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/alarm/alarms/alarmlist?filter=device%3D%3D"
        for k in self.getSwitchMgmt():
            response = requests.request("GET", url + k, headers=self.headers, verify=False)
            self.call_time += response.elapsed.total_seconds()
            response_dict = json.loads(response.text)
            response_dict = response_dict["lastOperDataObject"]
            if response_dict == []:
                pass
            else:
                self.res_result.append(response_dict)
        for idx in range(len(self.res_result)):
            for val in self.res_result[idx]:
                id_list.append(val["id"])
        #print("*"*20 + str(len(self.res_result)) + "*"*20)
        if id_list == []:
            print("There is no alarm.\nClosing...")
        return id_list, self.res_result


    def deleteAlarms(self):
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/alarm/alarms/deletealarms"
        payload = json.dumps({"alarmId":self.getAlarmInfo()[0],"actBy":self.response["username"]})
        response = requests.request("POST", url, headers = self.headers, data = payload, verify = False)
        if response.status_code == 200:
            print("DELETE Excution complete.")
        if self.getAlarmInfo()[0] != []:
            self.deleteAlarms()

    def returnAlmMsg(self):
        total_alm_count = 0
        alarm_ID, res_contents = self.getAlarmInfo()
        inner_list = []
        msg_dict = {"Info" : inner_list}
        for idx in tqdm(range(len(res_contents))):
            for msg in res_contents[idx]:
                inner_list.append("Device = " + msg["deviceName"] + ", Message = " + msg["message"])
        for idx, val in enumerate(msg_dict["Info"]):
            print(f"Index: {idx+1}\n -> {val}")
            total_alm_count += 1
        print(f"{start_magenta}Total Alarm Count = {total_alm_count}\nTotal API call time = {self.call_time:.3f} seconds.{end_color}")
    
    def rediscoverSwitch(self):
        sw_payload = self.getSwitchStatus()[1]
        payload = []
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/lan-discovery/rediscoverSwitch"
        for k in range(len(sw_payload)):
            payload.append(sw_payload[k]["switchDbID"])
        response = requests.request("POST", url, headers= self.headers, data= str(payload), verify = False)
        response = json.loads(response.text)
        if response["resultMessage"] == "OK":
            for _ in tqdm(range(15)):
                time.sleep(1)
            while True:
                sw_status = self.getSwitchStatus()[1]
                tmp_list = set()
                for sts in range(len(sw_status)):
                    tmp_list.add(sw_status[sts]["status"])
                tmp_list = list(tmp_list)    
                if (len(tmp_list) == 1 and ("Rediscovering" not in tmp_list) and ("ok" in tmp_list)):
                    print("All swiches are discovered")
                    for k,v in self.getSwitchStatus()[0].items():
                        print("Discover status(", k ,") = ",v["Discover_status"])
                    return response
                elif ("Rediscovering" in tmp_list):
                    print("Discovering...")
                else:
                    print("Check the switch connectivity\nClosing...")
                    break
        


#test = NDFC_api()
#print(test.getSwitchStatus()[0])
