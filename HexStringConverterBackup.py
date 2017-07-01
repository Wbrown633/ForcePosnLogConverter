
import unittest
import matplotlib.pyplot as plt
from ReadinData import *
import collections
import time


# Define Constants

ENCODERCONVERSION = 20000 #max encoder counts

ENCODERDISTANCECONVERSION = 10000 #counts/ (mm) actn axis travel

ENCODERFORCECONVERSION = 20000 #counts/ (N) force


def parseHexString(hexString, chars):
    """ Parses a continuous hex string into many strings of len 'chars'
    then converts those strings to decimal and returns the result as a list
    Example: parseHexString("208b208f209a2085", 4) --> [8331, 8335, 8346, 8325] """

    listofHex = [hexString[i:i+chars] for i in range(0, len(hexString), chars)]
    listofDec = []
    for j in listofHex:
        listofDec.append(int(j, 16))
    return listofDec

def plotData(listofForceData, listofPosnData, fileName, actuationnumber):
    """Given two lists, force and position data, and a file name this function uses matplotlib to plot them
    it then saves the output to the folderpath, which is specified in the main namespace. The name of the file
    mirrors that of the .log file that the data was drawn from. """

    plt.plot(listofForceData, linestyle = '-', marker = '.')
    plt.plot(listofPosnData, linestyle = '-', marker = '.')
    plt.ylabel('Force/Posn Data (N : mm)')
    plt.xlabel('Time')
    plt.title(fileName)
    plt.legend(["Force", "Position"])
    plt.savefig(folderpath + "/" + fileName.split(".")[0] + "Actuation_" + str(actuationnumber) + ".png")
    plt.close()

def convertEncoderData(hexList):

    """ Given a string of encoder hex data converts the data to reflect absolute encoder counts"""

    convertedList = [] # to store final values
    revolutions = 0

    # convert the long string of hex data we were given into a list of raw count readings
    hexList = parseHexString(hexList, 4)

    # The purpose of this algorithm is to identify large changes in encoder recordings and identify those
    # as a time when the encoder has exceeded it's maximum count, and record that as a revolution in the proper
    # direction. The scaling constants can be tweaked if the data isn't coming out properly in the graphs.
    # In the future encoder rollover should be handled by the firmware.
    NEGScalingFactor = -.65
    POSITIVEScalingFactor = .56

    for i in range(len(hexList)):

        diffbetweenpoints = (hexList[i] - hexList[i-1])
        if diffbetweenpoints <= NEGScalingFactor * ENCODERCONVERSION:
            if hexList[i] < hexList[i-1]:
                revolutions += 1
            convertedList.append(hexList[i] +revolutions*ENCODERCONVERSION) #convert current count based on tallied revolutions
        elif diffbetweenpoints >= POSITIVEScalingFactor * ENCODERCONVERSION:
            if hexList[i]>hexList[i-1]:
                revolutions -= 1 # next point is less than current point
            convertedList.append(hexList[i] + revolutions*ENCODERCONVERSION) #convert current count based on tallied revolutions
        else:
            convertedList.append(hexList[i] + revolutions*ENCODERCONVERSION)
    return convertedList

def convertRawCountsDistance(listofRawCounts):
    """Given a List of Raw encoder counts and a conversion factor produces a list of converted data"""

    ENCODERDISTANCECONVERSION = 10000 # counts per (mm) actn axis travel

    listofConvertedValues = []
    for count in listofRawCounts:
        count = float(count)/ENCODERDISTANCECONVERSION
        listofConvertedValues.append(count)

    return listofConvertedValues


def convertRawCountsForce(listofRawCounts):
    """Given a list of Raw force transducer data converts to force (N) using defined constants pulled from the
    FDMDX Characteristics file"""

    ENCODERFORCECONVERSION = 19859 #counts/ Volt

    ForceSlope = 2.873 #N/Volt
    ForceIntercept = -1.475 #N

    listofConvertedValues = []

    for count in listofRawCounts:
        count = (float(count) * ForceSlope/ENCODERFORCECONVERSION) + ForceIntercept
        listofConvertedValues.append(round(count, 4)) #Rounds the answer to 4 decimal places

    return listofConvertedValues

def convertOneFile(listofOneFile):
    """Given the two dimensional array corresponding to the Force and Position data
    for one file in a given directory returns the converted data for that file"""

    fileName = listofOneFile[0]

    listofForceDataHex = listofOneFile[1]
    listofPosDataHex = listofOneFile[2]

    # Poping these items from the list w/o saving them to a variable deletes them
    listofForceDataHex.pop(0)
    listofPosDataHex.pop(0)

    # Define list variables
    rawCountsForceData = []
    rawCountsPosData =[]
    listoflistofConvertedForce = []
    listoflistofConvertedPos = []

    # Force data comes wrapped in an extra layer of quotes, this block removes them and converts the hex to raw counts
    for force in listofForceDataHex:
        force = force[1:(len(force)-1)]
        rawCountsForceData.append(parseHexString(force, 4))

    # Same as above for Position
    for pos in listofPosDataHex:
        pos = pos[1:(len(pos)-1)]
        rawCountsPosData.append(convertEncoderData(pos))

    # Using factors from the FDMDX Characteristics file the raw force and position values are converted to (N) and (mm)
    for data in rawCountsForceData:
        listoflistofConvertedForce.append(convertRawCountsForce(data))

    for data in rawCountsPosData:
        listoflistofConvertedPos.append(convertRawCountsDistance(data))


    # Docs on namedtuples: https://docs.python.org/2/library/collections.html#collections.namedtuple
    convertedData = collections.namedtuple("Data", ["Force", "Pos", "Name"])
    convertedData.Force = listoflistofConvertedForce
    convertedData.Pos   = listoflistofConvertedPos
    convertedData.Name  = fileName.split("/")[1] # Ex: C:\temp\Proveris\ISL\Logs\05May2017/11111-141_MethodRunLog_050517051342.log
                                                 # path comes before "/" and the name comes after
    return convertedData




if __name__ == '__main__':

    # ask the user where the directory containing the logs they wish to convert is
    originaldirectory = raw_input("Please enter the directory = ")

    # All plots are stored in the temp drive in a parent folder called "Plots", the folders under that share a name
    # with the folder that holds the logs the user directed us to:
    # Ex: originaldirectory = "C:\temp\Proveris\ISL\Logs\03May2017"
    # we will store our plots in "C:\temp\Plots\03May2017"

    splitdirectory = originaldirectory.split("\\")
    foldername = splitdirectory[-1]
    folderpath = "C:/temp/Plots/" + foldername

    # Check if the directory we want to store our plots in exists, if not make it
    # http://stackoverflow.com/questions/273192/how-to-check-if-a-directory-exists-and-create-it-if-necessary

    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

    # Import the data from the .log files contained in the folder the user has shown us
    listofRunData = importAllLogData(originaldirectory)

    # Each item corresponds to the data created by one file, so we convert each file and plot each set of data
    # one at a time
    for listofOneFile in listofRunData:
        convertedData = convertOneFile(listofOneFile)
        count = 0
        for i in range(len(convertedData.Force)):
            count += 1
            plotData(convertedData.Force[i], convertedData.Pos[i], convertedData.Name, count)













