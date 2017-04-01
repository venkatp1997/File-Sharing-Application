import socket
import subprocess
import time
from datetime import datetime
import os		

def IndexGet(string):
	if "longlist" in string:
		return reply
	elif "shortlist" in string:
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
				if(":" in t[2]):
					temp=" ".join(t)
					temp=datetime.strptime(temp, "%b %d %H:%M")
					if(temp>=stime and temp<=etime):
						out+=file
						out+='\n'
		return out
	elif "regex" in string:
		temp=subprocess.check_output("ls " + directory +" | egrep "+"\""+string.split()[2]+"\"", shell=True)
		tlist=temp.split('\n')
		flist=reply.split('\n')
		out=""
		for tname in tlist:
			for fname in flist:
				if tname and tname in fname and tname not in out:
					out+=fname
					out+='\n'
		return out
	else:
		return "Invalid Command"
def FileHash(string):
	out=""
	if "checkall" in string:
		flist=reply.split('\n')
		for file in flist:
			if (len(file.split())>4):
				fname=file.split()[8:]
				tname=fname[:]
				fname="\ ".join(fname)
				tname=" ".join(tname)
				checksum=""
				checksum+=tname
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
				out+=checksum
				out+='\n'
		return out
	elif "verify" in string:
		flist=string.split()[2:]
		tlist=flist[:]
		tname=" ".join(flist)
		flist=reply.split('\n')
		for file in flist:
			if (len(file.split())>4 and tname in file):
				fname=file.split()[8:]
				checksum=""
				print tname
				checksum+=tname
				checksum+=" "
				print directory+tname,directory+"/"+tname
				if(directory.endswith('/')):
					if(os.path.isfile(directory+tname)):
						t1=subprocess.check_output("md5sum " +directory+tname, shell=True)
						checksum+=t1.split()[0]
				elif(os.path.isfile(directory+"/"+tname)):
					t1=subprocess.check_output("md5sum " +directory+"/"+tname, shell=True)
					checksum+=t1.split()[0]
				else:
					checksum+="directory"
				checksum+=" "
				checksum+=" ".join(file.split()[5:8])
				return checksum
		return "Not Found"	
	else:
		return "Invalid Command"

s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))

s.listen(5)
while True:
	try:
		global directory
		directory=raw_input("Enter the absolute path of the directory you want to share: ")
		global reply
		reply=subprocess.check_output("ls -l " + directory, shell=True)
		break
	except subprocess.CalledProcessError:
		print "Please enter a valid directory's path."
while True:
	c, addr = s.accept()
	mess=c.recv(1024)
	if mess:
		if("Index" in mess):
			c.send(IndexGet(mess))
		elif("FileHash" in mess):
			c.send(FileHash(mess))
		elif("FileDownload" in mess):
			filename=mess.split()[1]
			if directory.endswith("/"):
				f = open(directory+filename,'rb')
			else:
				f = open(directory+"/"+filename,'rb')
			l = f.read(1024)
			while (l):
				c.send(l)
				l=f.read(1024)
			f.close()
	c.close()