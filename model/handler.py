import requests
import os
import json
import pprint as pprint
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

update_date = "Last Updated date : 2022.12.1, joocho"

class Login_NDFC():
    __doc__="Hello"
    def loginNDFC(self):
        self.userName = input("Insert your username: ")
        self.passWd = input("Input your password: ")
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
                    print("Authentication success")
                    self.response = response
                    break
            except:
                print("Authentication failed, Check your username/Password")
                self.userName = input("Insert your username: ")
                self.passWd = input("Insert your password: ")
    

class NDFC_api(Login_NDFC):
    __doc__="Hello"
    def __init__(self):
        print("\033[95m" + "=" * 20 + "NDFC API easy Excutorservice" + "=" * 20)
        print(f"{update_date:>68}\n\033[0m")
        login_input = input("Insert your NDFC MgmtIP: ")
        while True:
            try:
                url = f"https://{login_input}/login"
                response = requests.request("GET", url, verify=False, timeout=2)
                if response.status_code == 200:
                    print("###Reachability verified###\n")
                    self.login_input = login_input
                    self.url = url
                    break
            except requests.exceptions.Timeout as errd:
                print("Timeout Error : ", errd)
                login_input = input("IP is not valid, Try again\nNDFC MgmtIP: ")
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting : ", errc)
                login_input = input("IP is not valid, Try again\nNDFC MgmtIP: ")
            except requests.exceptions.HTTPError as errb:
                print("Http Error : ", errb)
                login_input = input("IP is not valid, Try again\nNDFC MgmtIP: ")
            except:
                login_input = input("IP is not valid, Try again\nNDFC MgmtIP: ")
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
        res = json.loads(response.text)
        for k in range(len(res)):
            sum_status[res[k]["logicalName"]] = {"ccStatus" : "", "fabricName" : "", "ipAddress": ""}
            sum_status[res[k]["logicalName"]]["ccStatus"] = res[k]["ccStatus"]
            sum_status[res[k]["logicalName"]]["fabricName"] = res[k]["fabricName"]
            sum_status[res[k]["logicalName"]]["ipAddress"] = res[k]["ipAddress"]
        return sum_status


    def getAlarmInfo(self):
        id_list = []
        self.res_result = []
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/alarm/alarms/alarmlist?filter=device%3D%3D"
        for k in self.getSwitchMgmt():
            response = requests.request("GET", url + k, headers=self.headers, verify=False)
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
            exit()
        return id_list, self.res_result


    def deleteAlarms(self):
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/alarm/alarms/deletealarms"
        payload = json.dumps({"alarmId":self.getAlarmInfo()[0],"actBy":self.response["username"]})
        response = requests.request("POST", url, headers = self.headers, data = payload, verify = False)
        if response.status_code == 200:
            print("DELETE Excution complete.")
        if self.getAlarmInfo()[0] != []:
            self.deleteAlarms()
        exit()

    def returnAlmMsg(self):
        total_alm_count = 0
        alarm_ID, res_contents = self.getAlarmInfo()
        inner_list = []
        msg_dict = {"Info" : inner_list}
        for idx in range(len(res_contents)):
            for msg in res_contents[idx]:
                inner_list.append("Device = " + msg["deviceName"] + ", Message = " + msg["message"])
        for idx, val in enumerate(msg_dict["Info"]):
            print(f"Index: {idx}\n -> {val}")
            total_alm_count += 1
        print(f"Total Alarm Count = {total_alm_count}")


#test = NDFC_api()
#test.getSwitchStatus()
