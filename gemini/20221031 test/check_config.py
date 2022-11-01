import configparser
from copy import deepcopy
import serial.tools.list_ports as port_list

config_path = r'.\config.ini'


serial_name_list = ['Gemini']  #機種名稱
test_time_list = [0, 8] #測試時間

computer_ports = []
for port in list(port_list.comports()):
    tmp = str(port).split(' ')[0]
    computer_ports.append(tmp)


def read_ini(path):
    data = dict()
    config = configparser.ConfigParser()
    config.read(path)

    for section in config.sections():
        Tmp_data = dict()
        for k in config[section]:
            Tmp_data[k] = config[section][k]
        data[section] = deepcopy(Tmp_data)   
    
    return data
 
def check_config(config_path):                                          
    config_error_msg = str()
    open_station = list()
    config = dict()
    tmp_config = read_ini(config_path)
    #print(tmp_config)
    for info, datas in tmp_config.items():
        if info == 'Data':
            serial_name = datas['serial_name'].strip()
            test_time = int(datas["test_time"].strip())
            terminal_server_comport = datas['terminal_server_comport'].strip()
            if serial_name == '' or test_time == '' or terminal_server_comport == '':
                config_error_msg += '有欄位未填寫!'
                
            if terminal_server_comport not in computer_ports:
                config_error_msg += 'Terminal Server COM填寫錯誤'

        if info == 'Station':
            for num, state in datas.items():
                if len(state):
                    try:
                        state_i = int(state)
                    except:
                        config_error_msg += 'telent port 請填寫數字'
                        open_station.append(state)
                    else:
                        open_station.append(state_i)

                else:
                    open_station.append(0)
        
        if info == 'FTP':
            temp = datas['upload_function'].strip()
            ftp_function = True if temp == 'ON' else False
            ftp_upload_path = datas['upload_path'].strip()
        
        if info == 'SFIS':
            temp = datas['upload_function'].strip()
            SFIS_function = True if temp == 'ON' else False
            op = datas['op'].strip()

    if len(open_station) != 20:
            config_error_msg += f'[Station]長度有誤\n'  
                 
    if serial_name not in serial_name_list:
        config_error_msg += '錯誤的serial name值\n'
        
    if test_time not in test_time_list:
        config_error_msg += '錯誤的test time值\n'
        
    
    config['config_error_msg'] = config_error_msg
    config['serial_name'] = serial_name
    config['test_time'] = test_time
    config['terminal_comport'] = terminal_server_comport
    config['open_station'] = open_station
    config['ftp_function'] = ftp_function
    config['ftp_upload_path'] = ftp_upload_path
    config['online_function'] = SFIS_function
    config['op'] = op

    return config


if "__main__" == __name__:
    print(check_config(config_path))



