# -*- coding: utf-8 -*-
import hashlib
import os
import shutil
import platform
import datetime


PathFinal

PathNameEnd  	= "FINAL" #Name of the backup folder
PathFinal    	= PathFinal+PathNameEnd

PathFirst		= "ORIGINAL PATH" #put your path that you want to backup 
PathSecond		= "COPY PATH" #path  where you want to save the new backup by year

PathChangeName     	= "PATH CHANGE NAME" #disabled by default
PathGlobal = "GLOBAL PATH FOR TEST"

extEnabled   	  = True
EnabledCopy 	  = True
EnabledStartCopy  = False
EnabledShaCompare = True
EnabledRM    	  = True
EnabledYear       = True
EnabledAllFiles   = False

ArrayExtension  = []
ArrayYears      = []
ArrayAllFiles   = []
ArraySHAFiles   = []



extDocs      = [".doc",".mdb",".xls",".htm",".html",".docx",".txt",".swf",".ppt",".pps",".zip",".pub",".rar",".pdf"]
extVideos    = [".mpg",".avi","mpeg",".3gp",".webm"]
extImgs      = [".jpg",".JPG",".bmp",".gif",".img",".jpeg",".BMP",".GIF"]


# extSelected  = extImgs
extSelected  = extDocs
# extSelected  = extVideos

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()
def readAllEndExtension ():
	for dirpath, subdirs, files in os.walk(PathGlobal):
		for x in files:
			posExtension    = x.rfind(".")
			localExtension  = x[posExtension:]
			# print x[posExtension:]
			# print localExtension
			if not localExtension in ArrayExtension:
				ArrayExtension.append(localExtension)
				# print localExtension
	if extEnabled:
		for x in ArrayExtension:
			print x 
def getDataTimeFile (filename):
    if platform.system() == 'Windows':
        return os.path.getmtime(filename)
    else:
        stat = os.stat(filename)
        try:
            return stat.st_birthtime
        except AttributeError:
            return stat.st_mtime
def makeYearsFolder ():
	print "creating years folder"
	print "years availables:"
	if  os.path.exists(PathFinal) and EnabledRM:
		shutil.rmtree(PathFinal) 
	for dirpath, subdirs, files in os.walk(unicode(PathGlobal)):		
		for x in files:
			# print x
			localFileName = x
			localFile     = os.path.join(dirpath, x)
			localSHAFile  = sha256sum(localFile)
			localYear = datetime.datetime.fromtimestamp(getDataTimeFile (localFile)).strftime('%Y')

			if not localYear in ArrayYears:
				ArrayYears.append(localYear)
				print localYear			
	for x in ArrayYears:
		if not os.path.exists(PathFinal):
			if EnabledYear:
				os.makedirs(PathFinal)
		if not os.path.exists(PathFinal+"\\"+x):
			if EnabledYear:
				os.makedirs(PathFinal+"\\"+x)
			#print PathFinal
def copyFiles ():
	print "reading all folders"
	FileLocalArray = []
	temp = 0
	for dirpath, subdirs, files in os.walk(unicode(PathGlobal)):
		
		for x in files :
			print "ARCHIVO: "+x
			print "END"
				
			localFileName = x	
			localPathFile     = os.path.join(dirpath, localFileName)
			localYear = datetime.datetime.fromtimestamp(getDataTimeFile (localPathFile)).strftime('%Y')
			localSHAFile  = sha256sum(localPathFile)
			EndLocalPath = PathFinal+"\\"+localYear
			EndLocalCopy = EndLocalPath+"\\COPY"
			print localSHAFile
			print localFileName
			positionPoint = localFileName.rfind(".")
			print localFileName[positionPoint:]
			if EnabledCopy:
				if EnabledAllFiles or localFileName[positionPoint:] in extSelected:
					if not localSHAFile in ArraySHAFiles:
						if not os.path.exists(EndLocalPath+"\\"+localFileName):
							shutil.copy2(localPathFile,EndLocalPath)
						else:
							shutil.copy2(localPathFile,EndLocalPath+"\\_ORIGINAL_"+str(temp)+"_"+localFileName)
						ArraySHAFiles.append(localSHAFile)
					else:
						if not os.path.exists(EndLocalCopy):
							print localYear
							os.makedirs(EndLocalCopy)
						shutil.copy2(localPathFile,EndLocalCopy+"\\_COPY_"+localFileName)
			temp = temp + 1
			print temp
def changeName ():
	FileLocalArray = []
	temp = 0
	for dirpath, subdirs, files in os.walk(unicode(PathChangeName)):
		for x in files:
			LocalOnlyName =  x
			localPathFile = os.path.join(dirpath, LocalOnlyName)
			os.rename(localPathFile,str(temp)+"_"+LocalOnlyName)
			temp = temp +1
def compareSha ():
	print "compareSha Started..."
	LocalArrayFirst    = []  #original local path
	LocalArraySecond   = []  #copy local path	
	LocalArraySha1     = []  #first path sha
	LocalArraySha2     = []  #second path sha
	LocalArraySame     = []
	LocalArrayDiff     = []
	
	
	
	tempFirst   = 0
	tempSecond  = 0

	tempSame	= 0
	tempDiff    = 0	

	print "compareSha: add all local file path to the array"
	for dirpath, subdirs, files in os.walk(unicode(PathFirst)):
		for x in files:
			localPath1  = os.path.join(dirpath, x)
			LocalArrayFirst.append(localPath1)
			LocalArraySha1.append(sha256sum(localPath1))
	for x in LocalArrayFirst:
		tempFirst = tempFirst +1
		# print x
	print "adding all files folder from PathSecond to the array localPath2"
	for dirpath, subdirs, files in os.walk(unicode(PathSecond)):
		for x in files:
			localPath2  = os.path.join(dirpath, x)
			LocalArraySecond.append(localPath2)
			LocalArraySha2.append(sha256sum(localPath2))

	for x in LocalArraySecond:
		tempSecond = tempSecond +1
		# print x
	for couunt2, x1 in enumerate(LocalArraySha1):
		tempSha2 = "B3EACB15A0436A4829A6E4D85840638A39B3ADBBF22D7DF81D383AD5D0EE1BC3"
		if x1 == tempSha2.lower() or x1 == tempSha2 :
			print "file found: "+LocalArrayFirst[couunt2]

	print "compareSha: starting method for find and compare local SHA"
	for count, x in enumerate(LocalArraySha2):
		tempSha = "B3EACB15A0436A4829A6E4D85840638A39B3ADBBF22D7DF81D383AD5D0EE1BC3"
		if x == tempSha.lower() or x == tempSha :
			print "file found: "+LocalArraySecond[count]

		if x in LocalArraySha1:
			# print x
			# if x.find("258141B27C5951164C9CD2BCC975C01AD62FF57A2C005D075419BF2454DAA907"):
			# 	print "done"
			tempSame = tempSame  + 1 
		else:
			tempDiff = tempDiff + 1


	print "Archivos encontrados en First : "+str(tempFirst) 
	print "Archivos encontrados en Second: "+str(tempSecond)

	print "\n"
	print "Tamaño de arreglo First : "+str(len(LocalArrayFirst))
	print "Tamaño de arreglo Second: "+str(len(LocalArraySecond))
	
	print "\n"


	print "Archivos encontrados en Same : "+str(tempSame) 
	print "Archivos encontrados en Diff: "+str(tempDiff)		

	# print 



# readAllEndExtension();	
if EnabledStartCopy:
	makeYearsFolder()	
	copyFiles()

if EnabledShaCompare:
	compareSha()
# changeName()