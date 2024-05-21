import sys
from math import ceil
from PyQt6.QtGui import QAction, QFont, QTextCharFormat
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QStatusBar, QToolBar, QTextEdit, QGridLayout, QWidget, QFileDialog, QComboBox, QFontComboBox

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.parsercheck = 0
        self.setWindowTitle("Andy's Scratchpad V2") #change the title of the window
        self.textbox = QTextEdit() #create textbox
        self.textbox.setFixedSize(700, 800) #set the size of the textbox
        self.textbox.setAutoFillBackground(True)
        self.textbox.setStyleSheet("background-color: white") #change the paper color of the textbox to white
        self.setStyleSheet("background-color: lightgrey") #change the background of the programm to lightgrey
        self.formatting_text = [] #list used to save the changes made in the programm, such as font or font_size

        self.setStatusBar(QStatusBar(self)) #create statusbar
        self.file_name_label = QLabel("Unsaved File") #at the beginning of the programm, set the text in the statusbar to "unsaved file"
        self.statusBar().addWidget(self.file_name_label) #add the label to the statusbar
        self.statusBar().setStyleSheet("background-color: grey") #set the color of the statusbar to grey

        self.clear_button = QAction("Clear", self) #create the "clear" button
        self.new_button = QAction("New", self) #create the "new" button
        self.save_as_button = QAction("Save as", self) #create the "save as" button
        self.save_button = QAction("Save", self) #create the "save" button
        self.open_button = QAction("Open", self) #create the "open" button

        self.clear_button.triggered.connect(self.clearText) #add the clearText() function to the clear button
        self.new_button.triggered.connect(self.newFile) #add the newFile() function to the clear button
        self.save_button.triggered.connect(lambda x=0: self.saveText(x)) #add the saveText() function to the save button
        self.save_as_button.triggered.connect(lambda x=0: self.saveText(x+1)) #add the saveText() function to the save as button
        self.open_button.triggered.connect(self.openText) #add the openText() function to the open button
        self.save_button.setShortcut("Ctrl+S") #add shortcut to the save button
        self.save_as_button.setShortcut("Ctrl+Alt+S") #add shortcut to the save as button
        
        menubar = self.menuBar() #innitiate menubar
        menubar.setStyleSheet("background-color: grey") #set the color of the menubar to grey
        file_menu = menubar.addMenu("&File") #add the "file" menu to the menubar
        edit_menu = menubar.addMenu("&Edit") #add the "edit" menu to the menubar
        file_menu.addAction(self.new_button) #add the new button the file menu
        file_menu.addAction(self.save_button) #add the save button to the file menu
        file_menu.addAction(self.save_as_button) #add the save as button to the file menu
        file_menu.addAction(self.open_button) #add the open button to the file menu
        edit_menu.addAction(self.clear_button) #add the clear button to the edit menu

        toolbar = QToolBar() #create toolbar
        toolbar.setFixedHeight(40) #set the height of the toolbar
        self.addToolBar(toolbar) #innitiate the toolbar
        self.font_dropdown = QFontComboBox() #create dropdown menu in toolbar
        self.font_dropdown.setFixedHeight(25) #set height of the dropdown menu
        self.font_dropdown.currentFontChanged.connect(self.changeFontDropDown) #add the changeFontDropDown() function to the dropdown menu

        self.font_size_dropdown = QComboBox() #create dropdown menu in toolbar
        self.font_size_dropdown.setFixedHeight(25) #set height of the dropdown menu
        self.font_size_dropdown.addItems(["8", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30"]) #add items to drop down menu
        self.font_size_dropdown.setCurrentText("12") #set size 12 on programm boot
        self.font_dropdown.setCurrentFont(QFont("Arial", int(self.font_size_dropdown.currentText()))) #set font Arial on programm boot
        self.font_size_dropdown.currentTextChanged.connect(self.changeFontDropDown) #add changeFontDropDown() function to the dropdown menu
        
        if self.parsercheck == 0: #if you start the programm by opening a file, set the text of the textbox to the files content
            try:
                file = open(sys.argv[1], "r+")
                self.textbox.append(file.read())
                self.file_name_label.setText(file.name)
                file.close()
                self.AFEformatting()
                self.parsercheck = 1
            except:
                pass
            
        #add dropdown menus to toolbar
        toolbar.addWidget(self.font_dropdown) #put the font dropdown menu into the toolbar
        toolbar.addWidget(self.font_size_dropdown) #put the font size dropdown menu into the toolbar

        layout = QGridLayout() #create layout
        layout.addWidget(self.textbox) #add the textbox to the layout

        widget = QWidget() #create widget
        widget.setLayout(layout) #set widget layout to the previously created layout
        self.setCentralWidget(widget) #setting the central widget of the window to the previously created widget
        self.showMaximized() #maximize the window

    def clearText(self): #clear the text in the textbox 
        self.textbox.clear() #clears the text in the textbox

    def newFile(self): #opens new file / clears file
        self.textbox.clear() #clear the text in the textbox
        self.file_name_label.setText("Unsaved File") #set the filename in the statusbar into "unsaved file"
        self.font_dropdown.setCurrentText("Arial") #set the font to arial
        self.font_size_dropdown.setCurrentText("12") #set the font size to 12

    def saveText(self, x): #save file with filedialog
        if self.file_name_label.text() == "Unsaved File" or x == 1: #if currently there is no file opened
            #choose where to save the file, the file name and the file type
            name = QFileDialog.getSaveFileName(caption="Save File As", directory="Text", initialFilter="Andy's File Extension (*.afe)", filter="All Files (*);;Python Files (*.py);;Text Files (*.txt);;Andy's File Extension (*.afe)")
            try:
                file = open(name[0], "w") #create the file with the parameters from name
                self.file_name_label.setText(name[0]) #set the file name in the statusbar to the chosen file name
                file.write(self.textbox.toPlainText()) #write the content of the textbox into the file
                file.close() #close the file
            except:
                pass
        else:
            try:
                file = open(self.file_name_label.text(), "w") #open the file with the file name from the statusbar
                file.write(self.textbox.toPlainText()) #write the content of the textbox into the file
                file.close() #close the file
            except:
                pass
            
    def openText(self): #open file with filedialog
        #choose which file to open
        name = QFileDialog.getOpenFileName(caption="Open File", directory="Text", initialFilter="All Files (*)", filter="All Files (*);;Andy's File Extension (*.afe)")
        try:
            file = open(name[0], "r") #open the file with the parameters from name
            self.file_name_label.setText(name[0]) #change the file name in the statusbar to the name of the opened file
            self.textbox.clear() #clear the textbox
            self.textbox.append(file.read()) #add the content from the file to the textbox
            file.close() #close the file
        except:
            pass
    
    def changeFontDropDown(self): #change font with dropdown menu
       Cursor = self.textbox.textCursor() #get the Cursor of the textbox
       word0 = Cursor.selectedText() #get the initial selected text
       cursor_char_format = QTextCharFormat() #create char format
       cursor_char_format.setFontFamily(self.font_dropdown.currentText()) #set fontfamily
       cursor_char_format.setFontPointSize(float(int(self.font_size_dropdown.currentText()))) # set pointsize
       if self.textbox.toPlainText() == "": # if the textbox/file is empty, immediatly change the font for the whole document
           self.textbox.setFontFamily(cursor_char_format.fontFamily()) #set the font of the textbox with the font of the cursor char format
           self.textbox.setFontPointSize(cursor_char_format.fontPointSize()) #set the font size of the textbox with the font of the cursor char format

       else: #if the textbox is not empty
            if word0 != "": #if the textbox is not empty, and something is selected, change the font of the selected text
                Cursor.removeSelectedText() #remove the selected text
                Cursor.insertText(word0, cursor_char_format) #insert the previously selected text with the cursor char format
            if word0 == "": #if there is no word behind the cursor, change the font of the word before the cursor instead
                Cursor.movePosition(Cursor.MoveOperation.PreviousWord, Cursor.MoveMode.KeepAnchor) #select the word before the cursor
                word = Cursor.selectedText()
                Cursor.removeSelectedText() #remove the selected text
                Cursor.insertText(word, cursor_char_format) #insert word with the cursor char format
                Cursor.movePosition(Cursor.MoveOperation.NextWord, Cursor.MoveMode.KeepAnchor)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()