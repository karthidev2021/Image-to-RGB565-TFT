import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os



class TFT_IMG_RAWFILE_MAKER:
    
    def __init__(self,outputFileName,outputFolderPath,imgFolderPath):
        self.list_of_Images=[]
        self.outputFileName=outputFileName
        self.outFolderPath=outputFolderPath
        self.imgFolderPath=imgFolderPath

    def writeToFile(self,data,mode='a'):
        path=self.outFolderPath+"/"+self.outputFileName+".h"
        with open(path,mode) as file:
            file.write(data)
        
    def initialWrite(self):
        self.list_of_Images=os.listdir(self.imgFolderPath)
        code="int frames="+str(len(self.list_of_Images))+";\n"
        code+="const unsigned short load[][16384] PROGMEM={\n"
        self.writeToFile(code)

    def finalWrite(self):
        code="};"
        self.writeToFile(code)


    def imageToHexSeq(self):
        for imgName in self.list_of_Images:
            code="{\n"
            self.writeToFile(code)

            image=Image.open(self.imgFolderPath+"/"+imgName)
            frame=[]
            newLine=False
            width,height=image.size

            for y in range(height):
                for x in range(width):
                    r,g,b=image.getpixel((x,y))
                    imgInHex=hex(self.rgb_to_rgb565(r,g,b))
                    # imgInHex="0x{:2X}{:2X}{:2X}".format(r,g,b)
                    if newLine: 
                        imgInHex="\n"+imgInHex
                        newLine=False
                    frame.append(imgInHex)

                newLine=True
            code=",".join(frame)
            code+="\n},\n"
            self.writeToFile(code)
            print(imgName+" done..")
    

    def rgb_to_rgb565(self,r,g,b):
        r565=(r*31)//255
        g565=(g*63)//255
        b565=(b*63)//255

        return (r565<<11)| (g565<<5) | b565

    def clearFile(self):
        self.writeToFile("",'w')

    def start(self):
        self.clearFile()
        self.initialWrite()
        self.imageToHexSeq()
        self.finalWrite()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.withdraw()

        # self.mainloop()

        try:

            OutFileName=input("Output FileName : ")
            print("File path : ",end="")
            OutFolderPath=filedialog.askdirectory()
            if OutFolderPath=="": raise Exception
            print(OutFolderPath)

            imgFolderPath=filedialog.askdirectory()
            if imgFolderPath=="": raise Exception
            print(imgFolderPath + " is Selected")

            converter=TFT_IMG_RAWFILE_MAKER(OutFileName,OutFolderPath,imgFolderPath)
            if(input("start process?? (yes/no)")=="yes"): converter.start()
            
        except:print("Error occured!!")

        self.quit()
        print("See you next time ;)")



root=App()