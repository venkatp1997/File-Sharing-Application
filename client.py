import socket
import subprocess
import time
from datetime import datetime
import os

def IndexGet(string):
	if "longlist" in string:
		print reply
	else:
		t=reply
		tlist=reply.split('\n')
		t1=string.split()[2:5]
		t2=string.split()[5:8]
		stime=" ".join(t1)
		etime=" ".join(t2)
		stime=datetime.strptime(stime, "%d %b %H:%M")
		etime=datetime.strptime(etime, "%d %b %H:%M")
		out=""
		for file in tlist:
			if len(file.split())>7:
				t=file.split()[5:8]
				temp=" ".join(t)
				temp=datetime.strptime(temp, "%b %d %H:%M")
				if(temp>=stime and temp<=etime):
					out+=file
					out+='\n'
		print out
def FileHash(string):
	out=""
	if "checkall" in string:
		flist=reply.split('\n')
		for file in flist:
			if (len(file.split())>4):
				fname=file.split()[8:]
				fname=" ".join(fname)
				checksum=""
				checksum+=fname
				checksum+=" "
				if(directory.endswith('/')):
					if(os.path.isfile(directory+fname)):
						t1=subprocess.check_output("md5sum " + directory+fname, shell=True)
						checksum+=t1.split()[0]
				elif(os.path.isfile(directory+"/"+fname)):
					t1=subprocess.check_output("md5sum " + directory+"/"+fname, shell=True)
					checksum+=t1.split()[0]
				else:
					checksum+="Directory"
				checksum+=" "
				checksum+=" ".join(file.split()[5:8])
				print checksum
	elif "verify" in string:
		fname=" ".join(string.split()[2:])
		flist=reply.split('\n')
		for file in flist:
			if (len(file.split())>4 and fname in file):
				fname=file.split()[8:]
				fname=" ".join(fname)
				checksum=""
				checksum+=fname
				checksum+=" "
				if(directory.endswith('/')):
					if(os.path.isfile(directory+fname)):
						t1=subprocess.check_output("md5sum " + directory+fname, shell=True)
						checksum+=t1.split()[0]
				elif(os.path.isfile(directory+"/"+fname)):
					t1=subprocess.check_output("md5sum " + directory+"/"+fname, shell=True)
					checksum+=t1.split()[0]
				else:
					checksum+="Directory"
				checksum+=" "
				checksum+=" ".join(file.split()[5:8])
				print checksum

# while True:
# 	try:
# 		directory=raw_input("Enter the absolute path of the directory you want to share: ")
# 		global reply
# 		reply=subprocess.check_output("ls -l " + directory, shell=True)
# 		break
# 	except subprocess.CalledProcessError:
# 		print "Please enter a valid directory's path."
while True:
	s=socket.socket()
	host=socket.gethostname()
	port=12345
	s.connect((host, port))
	command=raw_input("$> ")
	s.send(command)
	if "IndexGet" in command or "FileHash" in command:
		mess=s.recv(10000)	
		print mess
	else:
		with open("newfile_"+command.split()[1], 'wb') as f:
			while True:
				data = s.recv(1024)
				if not data:
					break
				f.write(data)
		f.close()
	s.close()