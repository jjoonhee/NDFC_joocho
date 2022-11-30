import requests
import os
import json
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)



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
        print("=" * 20 + "NDFC API easy Excutorservice" + "=" * 20)
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


    def getAlarms(self):
        id_list = []
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/alarm/alarms/alarmlist?filter=device%3D%3D"
        for k in self.getSwitchMgmt():
            response = requests.request("GET", url + k, headers=self.headers, verify=False)
            response_dict = json.loads(response.text)
            response_dict = response_dict["lastOperDataObject"]
            for val in response_dict:
                id_list.append(val["id"])
        if id_list == []:
            print("There is no alarm.\nClosing...")
            exit()
        return id_list


    def deleteAlarms(self):
        url = f"https://{self.login_input}/appcenter/cisco/ndfc/api/v1/alarm/alarms/deletealarms"
        payload = json.dumps({"alarmId":self.getAlarms(),"actBy":self.response["username"]})
        response = requests.request("POST", url, headers = self.headers, data = payload, verify = False)
        if response.status_code == 200:
            print("DELETE Excution complete.")
        if self.getAlarms() != []:
            self.deleteAlarms()
        exit()
