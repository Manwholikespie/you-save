import os, os.path
import sys

#setting path to manipulate files in the directory later
path = os.getcwd()

os.system("xxd -p file.zip > file.binary")

fileLineNumber = sum(1 for line in open('file.binary'))
print fileLineNumber

def encodeToQR():
    lineNumber = 1
    fileNumber = 1
    endNumber = 45
    #example tail -n+50000000 test.in | head -n10
    while lineNumber <= fileLineNumber:

        if(not os.path.isdir(os.getcwd() + "/decoded")):
            print "Making directory"
            os.makedirs(os.getcwd() + "/decoded")

        # sed -n 16224,16482p filename > newfile
        encodeCommand2 = "sed -n " + str(lineNumber) + "," + str(endNumber) + "p file.binary | qrencode -o decoded/" + str(fileNumber) + ".png"

        # for debugging
        print(encodeCommand2)

        os.system(encodeCommand2)

        #this endNumber will sometimes run over the actual line number, but sed doesn't care.
        endNumber += 45
        lineNumber += 45
        fileNumber += 1

        encodeCommand2 = None




def decodeQR():
    os.system("rm newFile.binary; touch newFile.binary") #to clean up any past uses
    #thank you James, for your inumfiles code
    inumfiles = len([f for f in os.listdir(path + "/decoded/")if os.path.isfile(os.path.join(path + "/decoded/", f)) and os.path.join(path + "/decoded/", f).split(".")[-1] == "png"])
    fileNumber = 1
    print("\nNumber of files is: " + str(inumfiles) + "\n")
    while fileNumber <= inumfiles:
        #still trying to fix this piece. Either command works right now, mainly
        #because the top one doesn't even do anything.
        #decodeCommand = "zbarimg --raw -q " + str(fileNumber) + ".png | sed 's/;$//' >> newFile.binary"
        decodeCommand = "zbarimg --raw -q decoded/" + str(fileNumber) + ".png | sed '$d'>> newFile.binary"
        print(decodeCommand)

        os.system(decodeCommand)
        fileNumber += 1
        decodeCommand = None
    os.system("xxd -r -p newFile.binary newFile.zip")

def cleanUp():
    os.system("""
    rm *.png;
    rm *.binary;
    rm -r decoded/;
    """)



encodeToQR()
decodeQR()
cleanUp() #comment if you want to experiment with the QR codes



#Check to make sure the files match
print("\nChecksums:")
os.system("md5 -q *.zip")
