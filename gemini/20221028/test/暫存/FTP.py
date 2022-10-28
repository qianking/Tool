from ftplib import FTP
from ftplib import error_perm
import os
from socket import socket
import socket


class FTP_UP_Down():
    def __init__(self, ftp_logger):
        self.ftb_logger = ftp_logger
        self.ftp = FTP()
        self.ftp.set_pasv(0)

    def open_debug_mode(self, level = 2):
        self.ftp.set_debuglevel(level)
    
    def connect_ftp(self, ip, port, user, password):
        """
        連接FTP
        需輸入: IP、PORT、USERNAME、PASSWORD
        """
        try:
            self.ftp.connect(ip, port)
            self.ftp.login(user, password)
            print(self.ftp.getwelcome())
        except(socket.error, socket.gaierror):
            self.ftb_logger.exception(f"cannot reach {ip}")
            raise Exception(f"ERROR: cannot reach {ip}")
        except error_perm:
            self.ftb_logger.exception("cannot login")
            raise Exception("ERROR: cannot login")

    
    def check_localfile_exists(self, localpath):
        if not os.path.isfile(localpath):
            self.ftb_logger.exception(f"cannot find local path: {localpath}")
            raise Exception("本地端找不到文件")

    
    def check_localdir_exists(self, localdir):
        if not os.path.isdir(localdir):
            #elf.ftb_logger.exception(f"cannot find local folder: {localdir}")
            raise Exception("本地端找不到資料夾")

    
    def create_localdir(self, localdir):
        if not os.path.isdir(localdir):
            os.makedirs(localdir)
    
    def check_open_remotedir(self, remotedir):
        try:
            self.ftb_logger.info(f"open FTP folder: {remotedir}")
            self.ftp.cwd(remotedir)
        except:
            self.ftb_logger.exception(f"cannot find FTP folder: {remotedir}")
            raise Exception('遠端資料夾路徑不存在')


    def create_open_remote_file(self, remotedir):
        now_path = self.ftp.pwd()
        now_path_list = [i.upper() for i in now_path.split('/') if i != '']         #得到全大寫的現在路徑列表
        remotepath_list = [i.upper() for i in remotedir.split('/') if i != '']     #得到全大寫的要上傳路徑列表
        return_times, new_remotepath = self.get_return_times(now_path_list, remotepath_list)
       
        for i in range(return_times):
            self.ftp.cwd('..')

        for file in new_remotepath:                                                            
            try:
                self.ftp.cwd(file)
                self.ftb_logger.info(f"open FTP folder: {file}")                             
            except Exception as ex:  
                try:
                    self.ftp.mkd(file)
                    self.ftb_logger.info(f"create FTP folder: {file}")   
                    self.ftp.cwd(file)
                    self.ftb_logger.info(f"open FTP folder: {file}")
                except Exception as ex:
                    self.ftb_logger.exception(f"create file exception: {ex}")
                    self.ftp.cwd(file)
                    self.ftb_logger.info(f"open FTP folder: {file}")
                    


    @staticmethod
    def get_return_times(now_path_list, remotepath_list):
        return_times = len(now_path_list)
        same_index = 0
        for i in range(len(now_path_list)):
            if now_path_list[i] == remotepath_list[i]:
                same_index += 1
        return_times -= same_index
        new_remotepath = remotepath_list[same_index:]
        return return_times, new_remotepath   

      
    def UploadFile(self, localfile, remotedir):
        """
        上傳檔案
        輸入參數: 本地端檔案路徑、FTP端欲上傳的資料夾路徑
        如FTP端路徑不存在會創新路徑
        """
        self.check_localfile_exists(localfile)
        self.create_open_remote_file(remotedir)
        filename = localfile.split('\\')[-1]
    
        try:
            file_handler = open(localfile, "rb")
            res = self.ftp.storbinary(f'STOR {filename}', file_handler, 1024)
        except Exception as ex:
            self.ftb_logger.exception(f"exception:") 
            raise Exception(ex)
        else:
            if '226' in res:
                self.ftb_logger.info(f"{filename} upload finished")   
                print(f'{filename}上傳完成')

        finally:
            file_handler.close()
    
    def DownloadFile(self, remotefile, localdir):
        """
        上傳檔案
        輸入參數: FTP端欲下載的檔案路徑、本地端目的資料夾
        下載檔案名子根FTP上一樣
        如本地端目的資料夾不存在會創新資料夾
        """
        self.create_localdir(localdir)
        local_filename = remotefile.split('/')[-1]
        local = os.path.join(localdir, local_filename)
        try:
            file_handler = open(local, "wb")
            res = self.ftp.retrbinary(f'RETR {remotefile}', file_handler.write)
            file_handler.close()
        except Exception as ex:
            str_ex = str(ex)
            if 'cannot find the file' in str_ex or 'cannot find the path' in str_ex:
                self.ftb_logger.exception(f"exception:")  
                raise Exception('在FTP上找不到指定檔案或路徑')
        else:
            if '226' in res:
                self.ftb_logger.info(f"{local_filename} download finished")  
                print(f'{local_filename}下載完成')
        
    
    def UploadFileTree(self, localdir, remotedir):
        """
        上傳本地端資料夾裡面的所有檔案
        輸入參數: 本地端欲上傳資料夾、FTP端資料夾路徑
        如FTP端資料夾路徑不存在會創新資料夾
        """
        self.check_localdir_exists(localdir)
        self.create_open_remote_file(remotedir)
        filename_list = os.listdir(localdir)
        for name in filename_list:
            local = os.path.join(localdir, name)
            if os.path.isdir(local):
                remote = remotedir + '/' + name
                self.UploadFileTree(local, remote)
            else:
                self.UploadFile(local, remotedir)
                
        self.ftp.cwd('..')        
        return

    def DownloadFileTree(self, remotedir, localdir):
        """
        下載FTP資料夾裡面的所有檔案
        輸入參數: FTP端欲下載資料夾、本地端資料夾路徑
        如本地端資料夾路徑不存在會創新資料夾
        """
        self.create_localdir(localdir)
        self.check_open_remotedir(remotedir)
        remotefile_list = self.ftp.nlst()
        for file in remotefile_list:
            if self.IsDir(file):
                local = os.path.join(localdir, file)
                self.DownloadFileTree(file, local)
            else:
                self.DownloadFile(file, localdir)
        self.ftp.cwd('..')
        return

    def IsDir(self, filename):
        attributes_list = []
        self.ftp.retrlines('LIST', attributes_list.append)
        for attributes in attributes_list:
            if filename in attributes and '<DIR>' in attributes:
                return True


    def close(self):
        self.ftp.quit()

    


if "__main__" == __name__:
    ip = '172.24.255.118'
    port = 2100
    user = 'logbackup'
    password = 'pega#$34'

    localfile = r'D:\SWITCH\python\andy\20220714\PSZ23251G08_ORT_Cycle0_V1.00.10_[Pass].txt'
    remotedir = r'/SWITCH/EZ1K-ORT/C1000-8P-2G-L/2022-08-23'

    localdir = r'D:\Qian\python\NPI\ORT\log\C1000-8P-2G-L\2022-08-23'
    remotefile = r'/SWITCH/EZ1K-ORT'

    

