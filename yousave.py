import os, os.path
import time
import sys
import subprocess

#setting path to manipulate files in the directory later
path = os.getcwd()



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
    os.system("xxd -p file.zip > file.binary")
    os.system("perl -pi -e 'chomp if eof' file.binary") #deletes pesky line return so I can fit data across all 45 lines.
    fileLineNumber = sum(1 for line in open('file.binary'))

    lineNumber = 1
    fileNumber = 1
    endNumber = 45

    incrementProgress = 10 # percent of lines encoded in QR codes.

    print("\nEncoding to regular QR codes...")
    while lineNumber <= fileLineNumber:

        if(not os.path.isdir(os.getcwd() + "/codes")):
            print "Making directory"
            os.makedirs(os.getcwd() + "/codes")

        # reads a portion (45 lines) of a file (file.binary), and then pipes that
        # reading to qrencode to create a new QR image in the /codes directory.
        # example: sed -n 3781,3825p file.binary | qrencode -o codes/85.png
        encodeCommand = "sed -n " + str(lineNumber) + "," + str(endNumber) + "p file.binary | qrencode -o codes/" + str(fileNumber) + ".png"

        #Progress bar
        if round((float(lineNumber) / fileLineNumber) * 100) >= incrementProgress:
            print str(incrementProgress) + '% (' + str(lineNumber) + '/' + str(fileLineNumber) + ')'
            incrementProgress += 10



        os.system(encodeCommand)

        #this endNumber will sometimes run over the actual line number, but sed doesn't care.
        endNumber += 45
        lineNumber += 45
        fileNumber += 1

        encodeCommand = None #free up space


    incrementProgress = None #free up space, and get ready for next progress bar.

    fileNumber -= 1 #to account for the extra incrementation.
    if (fileNumber % 3) != 0:
        fileNumberRange = 3 - (fileNumber % 3)
    else:
        fileNumberRange = 0
    fileNumber += 1 #the name of the next .png file

    #this if statement is redundant, however it improves readability imo.
    if fileNumberRange != 0:
        for i in range(0, fileNumberRange):
            os.system("printf x | qrencode -o codes/" + str(fileNumber) + ".png")
            fileNumber += 1

def decodeQR():
    os.system("rm newFile.binary; touch newFile.binary") #to clean up any past uses

    #thank you James, for your inumfiles code
    #gets the number of files in the /decoded directory
    inumfiles = len(
    [f for f in os.listdir(path + "/decoded/")
    if os.path.isfile(os.path.join(path + "/decoded/", f))
    and os.path.join(path + "/decoded/", f).split(".")[-1] == "png"]
    )

    incrementProgress = 10 # % QR codes in /decoded read to newFile.binary

    fileNumber = 1
    print("\nNumber of files is: " + str(inumfiles) + "\n")
    print("Decoding standard QR...")
    while fileNumber <= inumfiles:
        #example: zbarimg --raw -q decoded/627.png | sed '$d' | head -n45 >> newFile.binary
        #the head is to cut out the random gibberish that has a 3% chance of being outputted
        #thanks to zbarimg's poor engineering.
        decodeCommand = "zbarimg --raw -q decoded/" + str(fileNumber) + ".png | sed '$d' | head -n45 >> newFile.binary"

        #print(decodeCommand) #keep this for when zbarimg messes it all up.
        if round((float(fileNumber) / inumfiles) * 100) >= incrementProgress:
            print str(incrementProgress) + '% (' + str(fileNumber) + '/' + str(inumfiles) + ')'
            incrementProgress += 10

        os.system(decodeCommand)
        fileNumber += 1
        decodeCommand = None

    print("QR code count:" + str(fileNumber - 1))





def recompileBinary():
    os.system("xxd -r -p newFile.binary newFile.zip")


def cleanUp():
    os.system("""
    rm *.png;
    rm *.binary;
    rm -r decoded/;
    """)

def encodeRGB():

    #Set up a shortcut to the directory of non-RGB, plain QR codes
    path = os.getcwd() + "/codes"

    #Check if the decoded directory exists. If not, exit, because if it doesn't exist,
    #Then there is no point to running the program, because there are no files.
    if not os.path.isdir(path):
        print "Directory not found"
        exit()
    else:
        print "Directory found"

    #Get number of files (Removed string version to declutter code)
    numfiles = len(
    [f for f in os.listdir(path)
    if os.path.isfile(os.path.join(path, f))
    and os.path.join(path, f).split(".")[-1] == "png"])

    #Check if there are any files in the decoded directory If not, exit, because if
    #there are none, then there is no point to running the program, because there
    #is nothing to encode.
    if numfiles == 0:
        print "No files found"
        exit()
    else:
        if numfiles == 1:
            print "Found " + str(numfiles) + " file"
        else:
            print "Found " + str(numfiles) + " files"

    #Check if there are enough codes to create a 3 dimensional code. If there are
    #less than 3, then exit, and if the number of codes is not divisible by 3, then
    #exit.
    if numfiles < 3:
        print "Not enough files to create a 3 dimensional code"
        exit()
    if numfiles%3 != 0:
        print "Number of files must be divisible by 3"
        exit()
    if numfiles == 3:
        print "I can make " + str(numfiles/3) + " compressed code"
    elif numfiles >= 3:
        print "I can make " + str(numfiles/3) + " compressed codes"


    #Look for the encoded directory. If it doesn't exist, create it. Since we don't
    #depend on anything in this directory, only put files into it, we can just
    #create it if it doesn't exist
    if(not os.path.isdir(os.getcwd() + "/encoded")):
        print "Making directory"
        os.makedirs(os.getcwd() + "/encoded")

    decfiles = os.listdir(os.getcwd() + "/codes")
    index = 1
    #Image resolution changing

    print "\nFixing image resolutions..."

    incrementProgress = 10

    for file in decfiles:
        if file.split(".")[-1] == "png":
            os.system("convert " + path + "/" + file + " -resize 543x543 " + path + "/" + file)

            # Progress bar
            if round((float(index) / numfiles)*100) >= incrementProgress:
                print str(incrementProgress) + '% (' + str(index) + '/' + str(numfiles) + ')'
                incrementProgress += 10
            index += 1


    print "Image resolutions fixed."

    incrementProgress = 10 #reset it back to 10


    #Marks the beginning of the compression
    print "\nCompressing..."
    encodednum = 1 #1.png
    #Go through each file and compress every 3 files
    for x in range(0, numfiles, 3):

        os.system("convert " + (path + "/" + str(x + 1) + ".png") + " " + (path + "/" + str(x + 2) + ".png") + " " + (path + "/" + str(x + 3) + ".png") + " -set colorspace RGB -combine -set colorspace sRGB " + os.getcwd() + "/encoded/" + str(encodednum) + ".png")

        # Progress bar
        if round((float(encodednum) / (numfiles / 3))*100) >= incrementProgress:
            print str(incrementProgress) + '% (' + str(encodednum) + '/' + str(numfiles / 3) + ')'
            incrementProgress += 10

        encodednum += 1

    incrementProgress = None #clear the memory
    print "All images are now RGB."




def decodeRGB():
    #Set up a shortcut to the current directory
    dirpath = os.getcwd()

    #Set up a shortcut to the encoded directory
    encpath = dirpath + "/encoded"

    #Check if the encoded directory exists. If not, exit, because if it doesn't exist,
    #Then there is no point to running the program, because there are no files.
    if not os.path.isdir(encpath):
        print "Directory not found"
        exit()

    #Get number of files (Removed string version to declutter code)
    numfiles = len(
    [f for f in os.listdir(encpath)
    if os.path.isfile(os.path.join(encpath, f))
    and os.path.join(encpath, f).split(".")[-1] == "png"])

    #for debugging.
    print "\nFiles to decode: " + str(numfiles)

    # make the /decoded directory
    # again, this is assuming that the person takes the video full of RGB codes,
    # then decodes them, and then stores those decoded ones in a new folder.
    if(not os.path.isdir(os.getcwd() + "/decoded")):
        print "Making directory.\n"
        os.makedirs(os.getcwd() + "/decoded")


    print "Decoding RGB to standard QR..."
    #Go through each image in the encoded directory, convert it, then dump the decoded
    #files into the decoded directory

    incrementProgress = 10
    for x in range(0, numfiles):
        if round((float(x + 1) / numfiles) * 100) >= incrementProgress:
            print str(incrementProgress) + '% (' + str(x+1) + '/' + str(numfiles) + ')'
            incrementProgress += 10
        os.system("convert " + encpath + "/" + str(x + 1) + ".png -separate " + os.getcwd() + "/decoded/" + str(x + 1) + ".png")

    #Get list of decoded files (This is just for renaming)
    decfiles = os.listdir(os.getcwd() + "/decoded")
    index = 0
    #Go through each file and rename it
    for file in decfiles:
        if file.split(".")[-1] == "png":
            index += 1

    filename = 1
    print index
    for x in range(0, index / 3, 1):
        for y in range(0, 3, 1):
            os.rename(dirpath + "/decoded/" + str(x + 1) + "-" + str(y) + ".png", dirpath + "/decoded/" + str(filename) + ".png")
            filename += 1

### MISC FUNCTIONS

def progressPrintout(numerator,denominator):
    if round((float(numerator) / (denominator / 3))*100) >= incrementProgress:
        print str(incrementProgress) + '% (' + str(numerator) + '/' + str(denominator / 3) + ')'
        incrementProgress += 10

def showStats():
    # Check to make sure the files match
    print("\nChecksums:")
    os.system("md5 -q *.zip")

    # Post-program information
    print("""------
    Stats:
    ------
    \nFile size:
    """)

    os.system("wc -c file.zip")

    print("\nQR Code count:")

    inumfiles = len(
    [f for f in os.listdir(path + "/decoded/")
    if os.path.isfile(os.path.join(path + "/decoded/", f))
    and os.path.join(path + "/decoded/", f).split(".")[-1] == "png"])

    print inumfiles

def clean(choice):
    if choice == 1:
        os.system("""
        rm -r codes/;
        rm file.binary;
        """)
    elif choice == 2:
        os.system("""
        rm -r codes/;
        rm -r decoded/;
        rm -r encoded/;
        rm *.binary;
        """)


def mainMenu():
    os.system("clear")
    print """
__   __          ____
\ \ / /__  _   _/ ___|  __ ___   _____
 \ V / _ \| | | \___ \ / _` \ \ / / _ \\
  | | (_) | |_| |___) | (_| |\ V /  __/
  |_|\___/ \__,_|____/ \__,_| \_/ \___|
----------------------------------------
          Welcome to YouSave.
Please select what you would like to do.
----------------------------------------
    """
    print """    [1] Encode a file.
    [2] Decode a file.
    [3] Exit.
    """
    try:
        choice = int(raw_input("Choose wisely.\n > "))
    except:
        print("\n\nSomething went wrong.\nLet's try this again\n")
        time.sleep(3)
        mainMenu()

    if choice == 1:
        encodeToQR()    #works
        encodeRGB()     #works
        clean(choice)
        print("\nSuccess!\n")
        time.sleep(3)
        mainMenu()
    elif choice == 2:
        decodeRGB() #works
        decodeQR()  #occasionally works (thanks to zbarimg)
        recompileBinary() #works
        showStats() #keeping md5's here for debugging.
        clean(choice)
        print("\nSuccess!\n")
        exit()
    elif choice == 3:
        print "Thank you for using YouSave. Goodbye."
        exit()
    elif choice != 1 or 2 or 3:
        print "\nImproper option. Try again.\n"
        time.sleep(2)
        mainMenu()

mainMenu()
