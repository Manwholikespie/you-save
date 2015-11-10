import os, os.path
import sys
import subprocess

#setting path to manipulate files in the directory later
path = os.getcwd()

os.system("xxd -p file.zip > file.binary")
os.system("perl -pi -e 'chomp if eof' file.binary") #deletes pesky line return so I can fit data across all 45 lines.
fileLineNumber = sum(1 for line in open('file.binary'))
print fileLineNumber


#Going to leave commented for now, just in case.
"""
def equalizeFile():
    characterCount = int(subprocess.check_output("wc -c file.binary | awk '{print $1}'", shell=True))
#    print characterCount #uncomment for Debugging
    characterCountRange = 60 - (characterCount % (fileLineNumber - 1))
#    print characterCountRange #uncomment for Debugging
    for character in range(0,characterCountRange):
        os.system('printf "x" >> file.binary')

    equalNumber = (45 % fileLineNumber) + 1 #needs to be 45 lines
    for i in range (0,equalNumber):
        os.system('printf "\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx">> file.binary')
"""


def encodeToQR():
    lineNumber = 1
    fileNumber = 1
    endNumber = 45

    while lineNumber <= fileLineNumber:

        if(not os.path.isdir(os.getcwd() + "/decoded")):
            print "Making directory"
            os.makedirs(os.getcwd() + "/decoded")

        # sed -n 16224,16482p filename > newfile
        #sed -n 3781,3825p file.binary | qrencode -o decoded/85.png
        encodeCommand = "sed -n " + str(lineNumber) + "," + str(endNumber) + "p file.binary | qrencode -o decoded/" + str(fileNumber) + ".png"

        # for debugging
        print(encodeCommand)

        os.system(encodeCommand)

        #this endNumber will sometimes run over the actual line number, but sed doesn't care.
        endNumber += 45
        lineNumber += 45
        fileNumber += 1

        encodeCommand = None

    fileNumber -= 1 #to account for the extra incrementation.
    if (fileNumber % 3) != 0:
        fileNumberRange = 3 - (fileNumber % 3)
    else:
        fileNumberRange = 0
    fileNumber += 1 #the name of the next .png file

    #this if statement is redundant, however it improves readability imo.
    if fileNumberRange != 0:
        for i in range(0, fileNumberRange):
            os.system("printf x | qrencode -o decoded/" + str(fileNumber) + ".png")
            fileNumber += 1

def decodeQR():
    os.system("rm newFile.binary; touch newFile.binary") #to clean up any past uses
    #thank you James, for your inumfiles code
    inumfiles = len([f for f in os.listdir(path + "/decoded/")if os.path.isfile(os.path.join(path + "/decoded/", f)) and os.path.join(path + "/decoded/", f).split(".")[-1] == "png"])
    fileNumber = 1
    print("\nNumber of files is: " + str(inumfiles) + "\n")
    while fileNumber <= inumfiles:
        #example: zbarimg --raw -q decoded/627.png | sed '$d'>> newFile.binary
        decodeCommand = "zbarimg --raw -q decoded/" + str(fileNumber) + ".png | sed '$d'>> newFile.binary"
        print(decodeCommand)

        os.system(decodeCommand)
        fileNumber += 1
        decodeCommand = None
    os.system("xxd -r -p newFile.binary newFile.zip")

    print("QR code count:" + str(fileNumber - 1))

def cleanUp():
    os.system("""
    rm *.png;
    rm *.binary;
    rm -r decoded/;
    """)


encodeToQR()
decodeQR()
#cleanUp() #leave commented during debugging.


#Check to make sure the files match
print("\nChecksums:")
os.system("md5 -q *.zip")

#Post-program information
print("""------
Stats:
------
\nFile size:
""")

os.system("wc -c file.zip")

print("\nQR Code count:")
inumfiles = len([f for f in os.listdir(path + "/decoded/")if os.path.isfile(os.path.join(path + "/decoded/", f)) and os.path.join(path + "/decoded/", f).split(".")[-1] == "png"])
print inumfiles
