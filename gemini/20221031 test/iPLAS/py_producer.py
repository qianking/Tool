import sys, platform, os
import ctypes, ctypes.util

class PyProducer():

	pega_producer = None
	encode = sys.getdefaultencoding()

	def __init__(self):
		try:
			print(platform.system(), platform.architecture()[0])

			if platform.system() == 'Windows':
				producer_lib = "pega_producer.dll"
				arch = "Win32" if platform.architecture()[0] == "32bit" else "x64"
				print ('dll path:'.format (arch))

			if platform.system() == 'Linux':
				producer_lib = "pega_producer.so"
				arch = "i386" if platform.architecture()[0] == "32bit" else "amd64"

			producer_path = self.__find_lib__(os.path.dirname(__file__), producer_lib, arch)
			if producer_path is None:
				producer_path = self.__find_lib__(os.getcwd(), producer_lib, arch)

			print("Load:", producer_path)
			self.pega_producer = ctypes.cdll.LoadLibrary(producer_path)

			self.pega_producer.get_ver.restype = ctypes.c_char_p
			self.pega_producer.initialize.argtypes = [ctypes.c_bool]
			self.pega_producer.initialize.restype = ctypes.c_int
			self.pega_producer.set_deviceid.argtypes = [ctypes.c_char_p]
			self.pega_producer.set_deviceid.restype = ctypes.c_int
			self.pega_producer.opmode.argtypes = [ctypes.c_int]
			self.pega_producer.opmode.restype = ctypes.c_int
			self.pega_producer.send_msg.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
			self.pega_producer.send_msg.restype = ctypes.c_int
			self.pega_producer.send_file.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
			self.pega_producer.send_file.restype = ctypes.c_int

			self.pega_producer.send_log.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
			self.pega_producer.send_log.restype = ctypes.c_int
			self.pega_producer.send_m2m_data.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
			self.pega_producer.send_m2m_data.restype = ctypes.c_int
			self.pega_producer.send_ts_data.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
			self.pega_producer.send_ts_data.restype = ctypes.c_int
			self.pega_producer.send_ts_msg.argtypes = [ctypes.c_char_p]
			self.pega_producer.send_ts_msg.restype = ctypes.c_int

			self.pega_producer.destroy.restype = ctypes.c_int

		except NameError:
			print("pega_producer not found")
			sys.exit(1)
		except OSError:
			print("Unable to load pega_producer")
			sys.exit(1)

	def __find_lib__(self, basedir, producer_lib, arch):
		for root, dirs, files in os.walk(basedir):
			if producer_lib in files:
				return os.path.join(root, producer_lib)
		return None

	def get_ver(self):
		return self.pega_producer.get_ver().decode(self.encode)

	def initialize(self, is_test):
		return self.pega_producer.initialize(is_test)

	def set_deviceid(self, id):
		return self.pega_producer.set_deviceid(bytes(id, self.encode))

	def opmode(self, mode):
		return self.pega_producer.opmode(mode)

	def send_msg(self, msg, id):
		return self.pega_producer.send_msg(bytes(msg, self.encode), bytes(id, self.encode))

	def send_file(self, path, id):
		return self.pega_producer.send_file(bytes(path, self.encode), bytes(id, self.encode))

	def send_log(self, path, key):
		return self.pega_producer.send_log(bytes(path, self.encode), bytes(key, self.encode))

	def send_m2m_data(self, file_path, m2m_data):
		return self.pega_producer.send_m2m_data(bytes(file_path, self.encode), bytes(m2m_data, self.encode))

	def send_ts_data(self, file_path, test_csv):
		return self.pega_producer.send_ts_data(bytes(file_path, self.encode), bytes(test_csv, self.encode))

	def send_ts_msg(self, _message):
		return self.pega_producer.send_ts_msg(bytes(_message, self.encode))

	def destroy(self):
		return self.pega_producer.destroy()
