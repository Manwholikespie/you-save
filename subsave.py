import os
import datetime
import base64

def makeBinaryFile():
    os.system("rm file.binary")
    os.system("xxd -p file.zip > file.binary")

def downloadSubs(url):
    os.system("youtube-dl --all-subs --skip-download '" + url + "'")
    os.system("mv *.vtt file.vtt")

def makeSubFile():
    binaryLines = [str(line.replace("\n","")) for line in open("file.binary","r")]

    os.system("rm file.vtt; touch file.vtt") # create a file to store subtitle data

    subFile = open("file.vtt","w")

    # write the header of the file
    subFile.write("""WEBVTT
Kind: captions
Language: en\n\n""")

    # begin writing datetime and lines
    myTime = datetime.datetime(1,1,1,hour=0,minute=0,second=0,microsecond=500000)

    repeatAmt = 20
    for x in xrange(0,len(binaryLines),repeatAmt):
        # make timecode
        nextTime = myTime + datetime.timedelta(microseconds=10000)

        time1 = str(myTime.time()).replace("0000","0")
        time2 = str(nextTime.time()).replace("0000","0")
        if "." not in time1:
            # check if time1 is rounded to a whole second. It needs to be a float
            time1 += ".000"
        elif "." not in time2:
            # otherwise, it will be in the other time string.
            time2 += ".000"

        timeString = time1 + " --> " + time2
        entryString = ""
        for n in range(repeatAmt):
            try: entryString += base64.b64encode(base64.b16decode(binaryLines[x+n].upper())) + "\n"
            except IndexError: pass

        subFile.write(timeString+"\n")
        subFile.write(entryString+"\n\n")
        # print timeString # uncomment for debugging

        myTime = nextTime # increment it

def readSubFile():
    os.system("rm newfile.binary; touch b64.binary newfile.binary")
    os.system("cat file.vtt | grep -iv ':' | grep -v '^$' > b64.binary")
    hexFile = open("newfile.binary","w")

    # take the base64 encoded lines and put them back in hex
    for line in open("b64.binary"):
        if line != "WEBVTT\n":
            hexFile.write(base64.b16encode(base64.b64decode(line.replace("\n",""))).lower()+"\n")

    hexFile.close() # close the file so that we can recompile its output

    os.system("perl -pi -e 'chomp if eof' file.binary") #delete last line return
    os.system("perl -pi -e 'chomp if eof' file.binary") #delete last line return
    os.system("xxd -r -p newfile.binary newfile.zip")

def cleanUp():
    os.system("rm *.binary")
    os.system("md5 *.zip | awk '{print $4}'")

# downloadSubs("https://www.youtube.com/watch?v=eis2JD58_KU")
makeBinaryFile()
makeSubFile()
readSubFile()
cleanUp()
# os.system("open -e file.vtt")
