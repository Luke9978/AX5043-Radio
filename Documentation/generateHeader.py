#!/usr/bin/python
import sys, getopt, os
import time , queue , pprint
from pyexcel_ods import get_data


#NOTE This is for me to sharpen my programing skills and to have some fun with this project, 
#     with that being said this script is not perfect and is a learning experience. 
#     Criticism is welcom though. :)

# Spreadsheet format:               [Hex Code, Name, Dir]

# Data will be loaded into array ex: ["XXX","NAME OF REGISTER","R&|W"] < for now
# then pushed into multiprocessing function to be phrased and constructed into final queue
# rejoined and  then have single function write to disk. The disk is only going to write so fast...

def sortMe(val):
    return val[0]


def loadData(inputfile):
    # Sanity check for input file incase anything happens
    result=[]
    nameLength = 0
    try:    
        data = get_data(inputfile) #Code to read ODS Spreadsheet
        for key,val in enumerate(data["Sheet1"]):
            if val:
                result.append([key,[val[0],val[1],val[2]]])
                if nameLength < len(val[1]):
                    nameLength = len(val[1])
    except IOError as e:
        print(e)
        sys.exit(2)
    
    return(result,nameLength)

def formatData(data): 
    ret = []
    for item in data:
        ret.append([item[0],item[1][0],str(item[1][1].replace(" ","")+"_"+str(item[1][2].replace(" ","")))])
        
    for item in ret:
        if len(str(item[1])) == 1:
            item[1] = "0x00" + str(item[1])
        elif len(str(item[1])) == 2:
            item[1] = "0x0"  + str(item[1])
        elif len(str(item[1])) == 3:
            item[1] = "0x"   + str(item[1])
        else:
            item[1] = "0x"   + str(item[1])
    return ret


def writeData(data,outputFile,nameLength):
    try:
        with open(outputFile,"w") as f:
            f.write("/* AX5043_Radio.  */\n"\
                    "#ifndef AX5043_Radio_SEEN\n"\
                    "#define AX5043_Radio_SEEN\n")
            for item in data:
                x = len(item[2])
                f.write("#define "+str(item[2]))
                while(nameLength>x):
                    f.write(" ")
                    x=x+1
                f.write(item[1]+"\n")
            f.write("\n#endif /* !AX5043_Radio */")
    except IOError as e:
        print(e)
        sys.exit(2)
        
        
def main(argv):
    #Code below is how you phrase arg inputs for use
    inputfile="registers_AX504.ods"  #Assumes my defaults
    outputfile="ax5043.h"            # ^
    nameLength=0
    try:
        opts,args = getopt.getopt(argv,"hi:o:",["inputODS=","output="])
    except getopt.GetoptError:
        print("Error has occurred in argument phrasing...")
        print("Please verify the input file exist and is readable or specify location")
        print("generateHeader.py -i <inputODS> -o <output>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h","--help"): # TODO the long options don't work and I don't know why, something with getopt function i think...
            print("generateHeader.py -i <input> -o <output>")
            sys.exit()
        elif opt in ("-i", "--inputODS"):
            inputfile = arg
        elif opt in ("-o", "-output"):
            outputfile = arg
            
    #Start of the heavy lifting
    
    result,nameLength = loadData(inputfile) # should do work and return Queue
    
    formated = formatData(result)
    
    formated.sort(key=sortMe)
    #pprint.pprint(formated)
    print(nameLength)
    writeData(formated,outputfile,nameLength+4)

    # TODO Maybe check what is in header, so as not to have to generate now "clean" one
    #      this might save some headaches on code writen outside of the registers 

if __name__ == "__main__": 
    main(sys.argv[1:])
        
