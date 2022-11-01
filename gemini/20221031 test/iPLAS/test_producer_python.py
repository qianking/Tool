import os
from os import sys, path
from shutil import copyfile
import time
import datetime
import argparse
sys.path.append (os.getcwd())
from py_producer import PyProducer

class Usage ( Exception ):
    def __init__ ( self , msg ):
        self . msg = msg

def main():
	parser = argparse.ArgumentParser(description='Python test producer')
	parser.add_argument('-r', metavar='rounds', type=int, default=1, help='test rounds')
	parser.add_argument('-d', metavar='delay', type=int, default=1000, help='delay(ms) between each round')
	parser.add_argument('-t', metavar='type', type=int, default=0, help='data type: 0(text); 1(file); 2(log); 3(m2m data); 4(ts msg);5(ts data)')
	parser.add_argument('-e', metavar='exit', type=bool, default=False, help='exit after test')
	args = parser.parse_args()

	rounds = args.r
	delay = args.d
	data_type = args.t
	bExit = args.e

	Producer = PyProducer()

	print("Rounds:", rounds, ", Delay(ms):", delay, ", Type:", data_type, ", Exit:", bExit, datetime.datetime.time(datetime.datetime.now()))
	print("producer ver:", Producer.get_ver())

	ret = Producer.initialize(True)
	print("initialize:", ret)
	if 0 != ret:
		return ret

	ret = Producer.set_deviceid("TestProducer_Python")
	print("set_deviceid:", ret)
	if 0 != ret:
		return ret

	ret = Producer.opmode(1)
	print("opmode:", ret)
	if 0 != ret:
		return ret

	if 0 == data_type or data_type == 4:
		msg_template = """{\"test_data\" : { \"thread_id\" : REPLACE_ID}, \"seed\" : \"REPLACE_SEED\", \"message\" : \"REPLACE_MSG\", \"create_date\" : {\"$date\": REPLACE_TS}}"""
		for i in range(1, rounds+1):
			tmp_msg = msg_template
			start_time = datetime.datetime.now()
			tmp_msg = tmp_msg.replace("REPLACE_SEED", str(i))
			tmp_msg = tmp_msg.replace("REPLACE_TS", str(start_time))

			if data_type == 0:
				print("send msg: {}".format(i))
				ret = Producer.send_msg(tmp_msg, "TestProducer_Python")
			else:
				print("send ts msg: {}".format(i))
				ret = Producer.send_ts_msg(tmp_msg)

			end_time = datetime.datetime.now()
			time_delta = end_time - start_time
			delta = int(time_delta.total_seconds() * 1000)
			if 0 != ret or 10 < delta:
				print(i, ret, delta, "send_msg", datetime.datetime.time(datetime.datetime.now()))
			time.sleep(delay/1000)

	if 1 == data_type or data_type == 2:
		dir = "./raw/"
		template_file = os.path.abspath(os.path.join(dir, os.listdir(dir)[0]))
		filename, file_extension = os.path.splitext(template_file)

		for i in range(1, rounds+1):
			clone_file = filename + "{:05d}".format(i) + file_extension
			copyfile(template_file, clone_file)
			start_time = datetime.datetime.now()
			if data_type == 1:
				print("send file: {}".format(clone_file))
				ret = Producer.send_file(clone_file, "TestProducer_Python")
			else:
				print("send log: {}".format(clone_file))
				ret = Producer.send_log(clone_file, "TestProducer_Python")

			end_time = datetime.datetime.now()
			time_delta = end_time - start_time
			delta = int(time_delta.total_seconds() * 1000)
			if 0 != ret or 10 < delta:
				print(i, ret, delta, clone_file, datetime.datetime.time(datetime.datetime.now()))
			time.sleep(delay/1000)

	if 3 == data_type or data_type == 5:
		msg_template = """{\"test_data\" : { \"thread_id\" : REPLACE_ID}, \"seed\" : \"REPLACE_SEED\", \"message\" : \"REPLACE_MSG\", \"create_date\" : {\"$date\": REPLACE_TS}}"""
		dir = "./raw/"
		template_file = os.path.abspath(os.path.join(dir, os.listdir(dir)[0]))
		filename, file_extension = os.path.splitext(template_file)

		for i in range(1, rounds+1):
			tmp_msg = msg_template
			start_time = datetime.datetime.now()
			tmp_msg = tmp_msg.replace("REPLACE_SEED", str(i))
			tmp_msg = tmp_msg.replace("REPLACE_TS", str(start_time))

			clone_file = filename + "{:05d}".format(i) + file_extension
			copyfile(template_file, clone_file)
			start_time = datetime.datetime.now()

			if data_type == 3:
				print("send m2m data: {} / {}".format(clone_file, i))
				ret = Producer.send_m2m_data(clone_file, tmp_msg)
			else:
				print("send ts data: {} / {}".format(clone_file, i))
				ret = Producer.send_ts_data(clone_file, tmp_msg)

			end_time = datetime.datetime.now()
			time_delta = end_time - start_time
			delta = int(time_delta.total_seconds() * 1000)
			if 0 != ret or 10 < delta:
				print(i, ret, delta, clone_file, datetime.datetime.time(datetime.datetime.now()))
			time.sleep(delay/1000)

	if bExit:
		time.sleep(1)
		ret = Producer.destroy()
		print("destroy:", ret, datetime.datetime.time(datetime.datetime.now()))
		return ret

if __name__ == '__main__':
	sys.exit(main ())
