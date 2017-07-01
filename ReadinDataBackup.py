import os

def importTestData(filename):
    ForceData = ["ForceDataHex"]
    PosData = ["PosDataHex"]
    with open(filename, "r") as file:
        for line in file:
            cleanedLine = line.strip()
            if cleanedLine:
                linelist = line.split()
                firststring = linelist[0]
                if len(firststring) > 2 and firststring[2] == 'S':
                    colonsplit = linelist[0].split(":")

                    for i in range(len(colonsplit)):
                        if colonsplit[i] == '250,"ForceRawData"':
                            commasplit = colonsplit[i+1].split(",")
                            forcehexdata = commasplit[0]
                            ForceData.append(forcehexdata)

                        if colonsplit[i] == '250,"PosnRawData"':
                            commasplit = colonsplit[i+1].split("}")
                            poshexdata = commasplit[0]
                            PosData.append(poshexdata)

    return [filename, ForceData, PosData]

def importMethodFileNames(directory):
    """Given the location of a log directory, returns all of the Method logs in a list to have their
    data imported."""

    allfileNames = os.listdir(directory)
    methodsRunList = []

    for filename in allfileNames:
        if "_MethodRunLog_" in filename:
            methodsRunList.append(filename)
    return methodsRunList



def importAllLogData(directory):
    """Given a log directory by the user returns lists of all the recorded data from
    the logs resulting log is a three dimensional array"""

    listofRunData = []
    filenames = importMethodFileNames(directory)

    for name in filenames:
        listofRunData.append(importTestData(directory +'/' + name))

    return listofRunData

if __name__ == '__main__':

    RunData = importAllLogData(raw_input("Please enter the directory = "))






