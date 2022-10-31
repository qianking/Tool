import requests
from urllib.parse import urlencode
from EnumSFIS import Enum_Url as eUrl
from enum import Enum




class SFIS_Web():
    def __init__(self, ProgramId =None, ProgramPassword = None):
        """
        建構式
        ProgramId = ex:TSP_IPPHON
        ProgramPassword = ex:m4OXy8
        
        參考網址:http://sfistsp-szascd0-n0.sz.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx
        """
        self.str_programId = "TSP_IPPHON"
        self.str_programPassword = "m4OXy8"
        self.str_header = {"content-type": "application/x-www-form-urlencoded"}    

    def WTSP_ASSIGN_DEVICE(self, type="", DEVType="", DEVID="", ACTType="", ISN="", flag="", data1="", data2=""):
        Url = eUrl.WTSP_ASSIGN_DEVICE.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "type": type,
            "DEVType": DEVType,
            "DEVID": DEVID,
            "ACTType": ACTType,
            "ISN": ISN,
            "flag": flag,
            "data1": data1,
            "data2": data2
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_CHKROUTE(self, ISN="", device="", checkFlag="", checkData="", type=1):
        Url = eUrl.WTSP_CHKROUTE.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "ISN": ISN,
            "device": device,
            "checkFlag": checkFlag,
            "checkData": checkData,
            "type": type
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_CHKROUTE_AOILOC(self, ISN="", device="", checkFlag="", checkData="", type="", aoiloc=""):
        Url = eUrl.WTSP_CHKROUTE_AOILOC.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "ISN": ISN,
            "device": device,
            "checkFlag": checkFlag,
            "checkData": checkData,
            "type": type,
            "aoiloc": aoiloc
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_DEVIF_MO(self, device="", MO=""):
        Url = eUrl.WTSP_DEVIF_MO.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "device": device,
            "Mo": MO
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_GETI1394(self, ISN="", device="", status="", I1394NUM=""):
        Url = eUrl.WTSP_GETI1394.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "ISN": ISN,
            "device": device,
            "status": status,
            "I1394NUM": I1394NUM
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_GETIMAC(self, device="", ISN="", status="", imacnum=""):
        Url = eUrl.WTSP_GETIMAC.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "device": device,
            "ISN": ISN,
            "status": status,
            "imacnum": imacnum
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_GETIMAC_T(self, device="", ISN="", status="", imacnum="", type=""):
        Url = eUrl.WTSP_GETIMAC_T.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "device": device,
            "ISN": ISN,
            "status": status,
            "imacnum": imacnum,
            "type": type
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_GETLABEL(self, type="", ISN="", DEV="", status=""):
        Url = eUrl.WTSP_GETLABEL.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "type": type,
            "ISN": ISN,
            "DEV": DEV,
            "status": status
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_GETVERSION(self, ISN="", device="", type="", ChkData="", ChkData2=""):
        Url = eUrl.WTSP_GETVERSION.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "ISN": ISN,
            "device": device,
            "type": type,
            "ChkData": ChkData,
            "ChkData2": ChkData2
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_INPUTGSDATA(self, ISN="", data=""):
        Url = eUrl.WTSP_INPUTGSDATA.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "ISN": ISN,
            "data": data
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_LOADINFO(self, pType="", pFlag="", pKey1="", pKey2="", pLndata1="", pLndata2="", pLndata3="", pLndata4="", pActtype="", pUserid=""):
        Url = eUrl.WTSP_LOADINFO.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "pType": pType,
            "pFlag": pFlag,
            "pKey1": pKey1,
            "pKey2": pKey2,
            "pLndata1": pLndata1,
            "pLndata2": pLndata2,
            "pLndata3": pLndata3,
            "pLndata4": pLndata4,
            "pActtype": pActtype,
            "pUserid": pUserid,
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_LOADKEY(self, SNTYPE="", DATA="", OP=""):
        Url = eUrl.WTSP_LOADKEY.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "SNTYPE": SNTYPE,
            "DATA": DATA,
            "OP": OP
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_LOGINOUT(self, op="", password="", device="", TSP="", status=""):
        Url = eUrl.WTSP_LOGINOUT.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "op": op,
            "password": password,
            "device": device,
            "TSP": TSP,
            "status": status
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_LOGINOUT_PROGID(self, op="", password="", device="", TSP="", status="", PROGID="", SRC="", VER=""):
        Url = eUrl.WTSP_LOGINOUT_PROGID.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "op": op,
            "password": password,
            "device": device,
            "TSP": TSP,
            "status": status,
            "PROGID": PROGID,
            "SRC": SRC,
            "VER": VER
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_ONLINE_REWORK_N(self, type="", data1="", data2="", data3="", flag=""):
        Url = eUrl.WTSP_ONLINE_REWORK_N.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "type": type,
            "data1": data1,
            "data2": data2,
            "data3": data3,
            "flag": flag
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_REPAIR(self, TYPE="", ISN="", DEV="", REASON="", DUTY="", NGRP="", TSP=""):
        Url = eUrl.WTSP_REPAIR.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "TYPE": TYPE,
            "ISN": ISN,
            "DEV": DEV,
            "REASON": REASON,
            "DUTY": DUTY,
            "NGRP": NGRP,
            "TSP": TSP
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_REPAIR_LOC(self, TYPE="", ISN="", DEV="", REASON="", DUTY="", NGRP="", TSP="", LOC=""):
        Url = eUrl.WTSP_REPAIR_LOC.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "TYPE": TYPE,
            "ISN": ISN,
            "DEV": DEV,
            "REASON": REASON,
            "DUTY": DUTY,
            "NGRP": NGRP,
            "TSP": TSP,
            "LOC": LOC
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_RESULT(self, ISN="", error="", device="", TSP="", data="", status="", CPKFlag=""):
        Url = eUrl.WTSP_RESULT.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "ISN": ISN,
            "error": error,
            "device": device,
            "TSP": TSP,
            "data": data,
            "status": status,
            "CPKFlag": CPKFlag
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_RESULT_MASSDATA(self, ISN="", error="", device="", TSP="", data="", status="", CPKFlag="", aoiloc="", data2="", data3="", data4="", data5="", data6="", data7="", data8=""):
        Url = eUrl.WTSP_RESULT_MASSDATA.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "ISN": ISN,
            "error": error,
            "device": device,
            "TSP": TSP,
            "data": data,
            "status": status,
            "CPKFlag": CPKFlag,
            "aoiloc": aoiloc,
            "data2": data2,
            "data3": data3,
            "data4": data4,
            "data5": data5,
            "data6": data6,
            "data7": data7,
            "data8": data8,
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_SEND_MAIL(self, subject="", sendto="", sendtext=""):
        Url = eUrl.WTSP_SEND_MAIL.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "subject": subject,
            "sendto": sendto,
            "sendtext": sendtext,

        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_SSD_INPUTDATA(self, device="", data="", type=""):
        Url = eUrl.WTSP_SSD_INPUTDATA.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "device": device,
            "data": data,
            "type": type,

        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

    def WTSP_TSP_GET_INPUTDATA(self, pFlag="", pType="", pData="", pDev="", pChkData1="", pChkData2=""):
        Url = eUrl.WTSP_TSP_GET_INPUTDATA.value
        Data = {
            "programId": self.str_programId,
            "programPassword": self.str_programPassword,
            "pFlag": pFlag,
            "pType": pType,
            "pData": pData,
            "pDev": pDev,
            "pChkData1": pChkData1,
            "pChkData2": pChkData2
        }
        Data = urlencode(Data).encode("utf-8")
        return requests.post(url=Url, headers=self.str_header, data=Data).text

base_url = "http://sfistsp-szascd0-n0.sz.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx/"

class Enum_Url(Enum):

    WTSP_ASSIGN_DEVICE = base_url + "WTSP_ASSIGN_DEVICE"
    WTSP_CHKROUTE = base_url + "WTSP_CHKROUTE"
    WTSP_CHKROUTE_AOILOC = base_url + "WTSP_CHKROUTE_AOILOC"
    WTSP_DEVIF_MO = base_url + "WTSP_DEVIF_MO"
    WTSP_GETI1394 = base_url + "WTSP_GETI1394"
    WTSP_GETIMAC = base_url + "WTSP_GETIMAC"
    WTSP_GETIMAC_T = base_url + "WTSP_GETIMAC_T"
    WTSP_GETLABEL = base_url + "WTSP_GETLABEL"
    WTSP_GETVERSION = base_url + "WTSP_GETVERSION"
    WTSP_INPUTGSDATA = base_url + "WTSP_INPUTGSDATA"
    WTSP_LOADINFO = base_url + "WTSP_LOADINFO"
    WTSP_LOADKEY = base_url + "WTSP_LOADKEY"
    WTSP_LOGINOUT = base_url + "WTSP_LOGINOUT"
    WTSP_LOGINOUT_PROGID = base_url + "WTSP_LOGINOUT_PROGID"
    WTSP_ONLINE_REWORK_N = base_url + "WTSP_ONLINE_REWORK_N"
    WTSP_REPAIR = base_url + "WTSP_REPAIR"
    WTSP_REPAIR_LOC = base_url + "WTSP_REPAIR_LOC"
    WTSP_RESULT = base_url + "WTSP_RESULT"
    WTSP_RESULT_MASSDATA = base_url + "WTSP_RESULT_MASSDATA"
    WTSP_SEND_MAIL = base_url + "WTSP_SEND_MAIL"
    WTSP_SSD_INPUTDATA = base_url + "WTSP_SSD_INPUTDATA"
    WTSP_TSP_GET_INPUTDATA = base_url + "WTSP_TSP_GET_INPUTDATA"