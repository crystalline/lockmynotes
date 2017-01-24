#!/usr/bin/env python

import os
from Tkinter import *
from tkMessageBox import *
from tkFileDialog import *

from reedsolo import RSCodec, ReedSolomonError
from simplecrypt import encrypt, decrypt, DecryptionException

class Notepad:

    #variables
    __root = Tk()
    
    #Reed - Solomon codec for error detection and correction
    #Enough to correct the file even if 15% of characters are corrupted
    __rs = RSCodec(120)
    
    #default window width and height
    __thisWidth = 300
    __thisHeight = 300
        
    __thisFileFrame = Frame(__root, borderwidth=1)
    __thisFileFrame.pack(fill=X)
    
    __thisOpenFile = Button(__thisFileFrame, text="Select File", width=10, font=("TkDefaultFont", 10))
    __thisOpenFile.pack(side=LEFT);

    __thisClearFile = Button(__thisFileFrame, text="Clear", width=10, font=("TkDefaultFont", 10))
    __thisClearFile.pack(side=LEFT);
    
    __noFile = "[no file selected]"
    
    __thisFileLabelText = StringVar();
    __thisFileLabelText.set(__noFile)
    
    __thisFileLabel = Label(__thisFileFrame, textvariable=__thisFileLabelText, font=("TkDefaultFont", 10))
    __thisFileLabel.pack(side=LEFT, expand=True, fill=BOTH);    
    
    __thisCmdFrame = Frame(__root, borderwidth=1)
    __thisCmdFrame.pack(fill=X)
    
    __thisPassLabel = Label(__thisCmdFrame, text="Enter Key: ", width=13, font=("TkDefaultFont", 10))
    __thisPassLabel.pack(side=LEFT);
    __thisPassEntry = Entry(__thisCmdFrame, show='*', font=("TkFixedFont", 14))
    __thisPassEntry.pack(side=LEFT, expand=True, fill=BOTH);
    
    __thisSaveFile = Button(__thisCmdFrame, text="Save", font=("TkDefaultFont", 10))
    __thisSaveFile.pack(side=LEFT);
    __thisLoadFile = Button(__thisCmdFrame, text="Load", font=("TkDefaultFont", 10))
    __thisLoadFile.pack(side=LEFT);
        
    __thisTextArea = Text(__root, font=("TkFixedFont", 12), undo=TRUE)
    
    __thisScrollBar = Scrollbar(__thisTextArea)
    __file = None
        
    def __init__(self,**kwargs):
        #initialization

        #set icon
        try:
            appdir = os.path.dirname(os.path.abspath(__file__))
            self.__root.tk.call('wm','iconphoto',self.__root._w, PhotoImage(file=os.path.join(appdir, "icon.png")))
        except:
            pass

        #set window size (the default is 300x300)

        try:
            self.__thisWidth = kwargs['width']
        except KeyError:
            pass

        try:
            self.__thisHeight = kwargs['height']
        except KeyError:
            pass

        #set the window text
        self.__root.title(self.__noFile + " - CryptoNotepad")

        #center the window
        screenWidth = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        left = (screenWidth / 2) - (self.__thisWidth / 2)
        top = (screenHeight / 2) - (self.__thisHeight /2)

        self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth, self.__thisHeight, left, top))

        #add controls (widget)
        
        self.__thisTextArea.pack(fill=BOTH, expand=True)
        
        self.__thisScrollBar.pack(side=RIGHT, fill=Y)
        self.__thisScrollBar.config(command=self.__thisTextArea.yview)
        self.__thisTextArea.config(yscrollcommand=self.__thisScrollBar.set, wrap=CHAR)
    
        self.__thisOpenFile.config(command=self.__openFile)
        self.__thisClearFile.config(command=self.__clearFile)
        self.__thisSaveFile.config(command=self.__saveFile)
        self.__thisLoadFile.config(command=self.__loadFile)
  
        
    def __quitApplication(self):
        self.__root.destroy()
        #exit()

    def __showAbout(self):
        showinfo("CryptoNotepad", "Created by an unnamed programmer")
    
    def __openFile(self):
        self.__file = askopenfilename(defaultextension=".bin",filetypes=[("Encrypted Text Files","*.bin"),("All Files","*.*")])
        if self.__file == "":
            #no file to open
            self.__file = None
        else:
            self.__root.title(self.__noFile + " - CryptoNotepad")
            self.__thisFileLabelText.set(self.__file)
    
    def __clearFile(self):
        self.__file = None
        self.__root.title(self.__noFile + " - CryptoNotepad")
        self.__thisFileLabelText.set(self.__noFile)
        
    def __encodeFile(self, filestr):
        #Encrypt with AES-256
        encrypted = bytearray(encrypt(self.__getKey(), filestr))
        #Encode with Reed-Solomon codec capable of correcting 15% of byte errors
        #And test the decoding on encoded file to be sure
        encoded = self.__rs.encode(encrypted)
        
        try:
            decoded = self.__rs.decode(encoded)
            decrypted = decrypt(self.__getKey(), buffer(decoded)).decode('utf-8')
            if decoded == encrypted and filestr == decrypted:
                return encoded
            else:
                showerror("Weird Encoding Error", "This error should never happen. Sorry, cannot save your file, try other programs. There is something wrong with reedsolo.py or simplecrypt.py")
                return None
        except:
            print sys.exc_info()[0]
            return None
    
    def __decodeFile(self, filestr):
        #decode RS code
        decodedText = ''
        try:
            decodedText = self.__rs.decode(bytearray(filestr))
        except ReedSolomonError:
            showerror("Decoding Error", "The program cannot decode your file because it is corrupted beyond repair. Be careful and don't forget to make backups")
            return ''
        #decrypt
        try:
            decryptedText = decrypt(self.__getKey(), buffer(decodedText))
        except DecryptionException as d:
            print "DecryptionException: ", d
            showerror("Decryption Error", "The program cannot decrypt contents of your file. Either your key is invalid or the password is corrupted. There is no way to decrypt your data if you lose the password. Be careful and don't forget to make backups")
            decryptedText = ''
        return decryptedText
    
    def __getKey(self):
        return self.__thisPassEntry.get()
    
    def __loadFile(self):
        if (len(self.__getKey()) > 0 and self.__file):
            file = open(self.__file,"rb")
            ftext = file.read()
            text = self.__decodeFile(ftext);
            
            self.__thisTextArea.delete(1.0,END)
            self.__thisTextArea.insert(1.0, text)
        else:
            if not self.__file:
                showerror("Error", "No file selected.")
            if len(self.__thisPassEntry.get()) == 0:
                showerror("Error", "No key entered.")
    
    def __saveFile(self):  
        if self.__file == None:
            self.__file = asksaveasfilename(initialfile='text.bin',defaultextension=".bin",filetypes=[("Encrypted Text Files","*.bin"),("All Files","*.*")])
            self.__thisFileLabelText.set(self.__file)
            
        if (len(self.__getKey()) > 0):
            #try to save the file, note 'end-1c' insted of END to get rid of last newline
            text = self.__thisTextArea.get(1.0, 'end-1c')
            encodedText = self.__encodeFile(text);
            
            file = open(self.__file, "wb")
            if (encodedText != None): file.write(encodedText)
            file.close()
            #change the window title
            self.__root.title(os.path.basename(self.__file) + " - CryptoNotepad")
        else:
            if not len(self.__thisPassEntry.get()) > 0:
                showerror("Error", "No key entered.")
    
    def __cut(self):
        self.__thisTextArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__thisTextArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__thisTextArea.event_generate("<<Paste>>")

    def run(self):
        #run main application
        self.__root.mainloop()



#run main application
notepad = Notepad(width=600,height=400)
notepad.run()


