from importlib.resources import read_binary
import read_ini
import serial.tools.list_ports as port_list

config_path = r'D:\Qian\python\NPI\ORT\config.ini'

serial_name_list = ['EZ1K_A1', 'EZ1K_A2']                                       #機種名稱
serial_port_list = [8, 48]                                                      #port種類
package_machine_list = ['PG', 'Nustream']                                       #封包產生器種類
test_time_list = [1, 24, 144]                                                      #測試時間
computer_ports = []
for port in list(port_list.comports()):
    tmp = str(port).split(' ')[0]
    computer_ports.append(tmp)
 
def check_config(config_path):                                          
    config_error_msg = str()
    open_station = list()
    config = dict()
    tmp_config = read_ini.read_ini(config_path)
    #print(tmp_config)
    for info, datas in tmp_config.items():
        if info == 'Data':
            serial_name = datas['serial_name'].strip()
            serial_port = int(datas['port'].strip())
            package_machine = datas["package_machine"].strip()
            test_time = int(datas["test_time"].strip())
            terminal_server_comport = datas['terminal_server_comport'].strip()
            pg_comport = datas['pg_comport'].strip()
            if serial_name == '' or serial_port == ''or package_machine == '' or test_time == '' or terminal_server_comport == '' or pg_comport == '':
                config_error_msg += '有欄位未填寫!'
               
                
            if terminal_server_comport not in computer_ports:
                config_error_msg += 'Terminal Server COM填寫錯誤'
                
            if package_machine == 'PG':
                if pg_comport not in computer_ports:
                    config_error_msg += 'PG COM填寫錯誤'

        if info == 'Station':
            for num, state in datas.items():
                if state == "ON":
                    open_station.append(1)
                elif state == "OFF":
                    open_station.append(0)
                else:
                    config_error_msg += f'{num}值填寫錯誤\n'
                    
                    open_station.append(0)
        
        if info == 'FTP':
            if datas['upload_function'].strip() == 'ON':
                ftp_upload_funtion = True
            elif datas['upload_function'].strip() == 'OFF':
                ftp_upload_funtion = False
            ftp_upload_path = datas['upload_path'].strip()
        
        if info == 'SFIS':
            if datas['sfis_function'].strip() == 'ON':
                SFIS_function = True
            elif datas['sfis_function'].strip() == 'OFF':
                SFIS_function = False
            
            op = datas['op'].strip()

    if len(open_station) != 20:
            
            config_error_msg += f'[Station]長度有誤\n'  
                 
    if serial_name not in serial_name_list:
        config_error_msg += '錯誤的serial name名稱\n'
        
    if serial_port not in serial_port_list:
        config_error_msg += '錯誤的port名稱\n'
       
    if package_machine not in package_machine_list:
        config_error_msg += '錯誤的package machine名稱\n'
        
    if test_time not in test_time_list:
        config_error_msg += '錯誤的test time名稱\n'
        
    
    config['config_error_msg'] = config_error_msg
    config['serial_name'] = serial_name
    config['serial_port'] = serial_port
    config['test_time'] = test_time
    config['package_machine'] = package_machine
    config['terminal_server_comport'] = terminal_server_comport
    config['pg_comport'] = pg_comport
    config['open_station'] = open_station
    config['ftp_upload_funtion'] = ftp_upload_funtion
    config['ftp_upload_path'] = ftp_upload_path
    config['SFIS_function'] = SFIS_function
    config['op'] = op

    return config



if "__main__" == __name__:
    print(check_config(config_path))



