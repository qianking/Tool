import SFISlib
import re

class SFIS():   
    def __init__(self, ProgramId = None, ProgramPassword = None):
            """
            建構式       
            
            參考網址:http://sfistsp-szascd0-n0.sz.pegatroncorp.com/SFISWebService/SFISTSPWebService.asmx
            """        
            self.SFIS_web=SFISlib.SFIS_Web()
   

    def Login(self, op, deviceID, TSP):
        sfis_return = self.SFIS_web.WTSP_LOGINOUT(op=op, password = 'pegatron', device=deviceID, TSP=TSP, status='1')
        return sfis_return
        

    def Logout(self, op, deviceID, TSP):
        sfis_return = self.SFIS_web.WTSP_LOGINOUT(op=op, password = 'pegatron', device=deviceID, TSP=TSP, status='2')
        return sfis_return

    def Get_ModelName(self):
        pass

    def Get_ABBBStatus(self):
        pass

    def Get_PSN(self):
        pass

    def CheckRoute(self, ISN, deviceID):
        sfis_return = self.SFIS_web.WTSP_CHKROUTE(ISN = ISN, device=deviceID)
        sfis_data = get_pure_sfif(sfis_return)
        return sfis_data
 
    def Get_MAC(self):
        pass

    def Get_SSN(self, SN, deviceID):
        sfis_return = self.SFIS_web.WTSP_GETVERSION(ISN = SN, device= deviceID, type='ASSIGN_SSN', ChkData='SSN', ChkData2 = '')
        sfis_data = get_pure_sfif(sfis_return)
        return sfis_data

    def Get_MNAME(self):
        pass

    def UploadRawData(self, ISN, error, deviceID, TSP, status, data_list):
        data = data_list[0]
        data2 = data_list[1]
        data3 = data_list[2]
        data4 = data_list[3]
        data5 = data_list[4]
        data6 = data_list[5]
        data7 = data_list[6]
        data8 = data_list[7]
        sfis_return = self.SFIS_web.WTSP_RESULT_MASSDATA(ISN = ISN, error = error, device = deviceID, TSP = TSP, data = data, status = status, 
                                                        data2 = data2, 
                                                        data3 = data3, 
                                                        data4 = data4,
                                                        data5 = data5,
                                                        data6 = data6,
                                                        data7 = data7,
                                                        data8 = data8,)
        sfis_data = get_pure_sfif(sfis_return)
        return sfis_data

    def Get_Date(self):
        pass

    def Get_SataionName(self):
        pass

    def Get_SNA(self):
        pass



def get_pure_sfif(sfis_return):
    pattern = re.compile(r'/">(.*)</', re.I)
    sfis_data = pattern.findall(sfis_return)
    if sfis_data:
        sfis_data = sfis_data[0].split('\x7f')
    return sfis_data

