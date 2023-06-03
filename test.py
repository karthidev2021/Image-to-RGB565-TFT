import tkinter as tk
from tkinter import filedialog
from PIL import Image
import os



class TFT_IMG_RAWFILE_MAKER:
    
    def __init__(self,outputFileName,outputFolderPath,imgFolderPath,variable):
        self.list_of_Images=[]
        self.outputFileName=outputFileName
        self.outFolderPath=outputFolderPath
        self.imgFolderPath=imgFolderPath
        self.variable=variable

    def writeToFile(self,data,mode='a'):
        path=self.outFolderPath+"/"+self.outputFileName+".h"
        with open(path,mode) as file:
            file.write(data)
        
    def initialWrite(self):
        self.list_of_Images=os.listdir(self.imgFolderPath)
        image=Image.open(self.imgFolderPath+"/"+self.list_of_Images[0])
        totalPixel=image.size[0]*image.size[1]
        image.close()
        code="int {}_frames={};\n".format(self.variable,len(self.list_of_Images))
        code+="int {}_width={};\n".format(self.variable,image.size[0])
        code+="int {}_height={}\n;".format(self.variable,image.size[1])
        code+="const unsigned short {}[][{}] PROGMEM={{\n".format(self.variable,totalPixel)
        self.writeToFile(code)

    def finalWrite(self):
        code="};"
        self.writeToFile(code)


    def imageToHexSeq(self):
        count=0
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
                    if newLine or count==16: 
                        imgInHex="\n"+imgInHex
                        newLine=False
                        if(count==16): count=0
                    frame.append(imgInHex)
                    count+=1

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

            print("Image File path : ",end="",flush=True)
            imgFolderPath=filedialog.askdirectory(title="Select image folder")
            if imgFolderPath=="": raise Exception
            print(imgFolderPath)

            OutFileName=input("Output FileName : ")
            if OutFileName=="": OutFileName="output"

            print("Outfile File path : ",end="",flush=True)
            outFolderPath=filedialog.askdirectory(title="Select output folder")
            if outFolderPath=="": raise Exception
            print(outFolderPath)

            variableName=input("Output Variable Name : ")
            if variableName=="": variableName="image_var"

            converter=TFT_IMG_RAWFILE_MAKER(OutFileName,outFolderPath,imgFolderPath,variableName)
            if(input("start process?? (yes/no) : ")=="yes"): converter.start()
            
        except Exception as e:print(e)

        self.quit()
        print("See you next time ;)")



root=App()