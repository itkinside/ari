import sys

try:
    import pygtk
    pygtk.require("2.0")

    import gtk
    import gtk.glade
except:
    print "Missing dependecy: pygtk"
    sys.exit(1)

class AngelicaGUI:
    def __init__(self):  
        gladefile = "angelica/angelica.glade"  
        self.windowname = "Anglica"  
        self.wTree = gtk.glade.XML(gladefile, self.windowname)  
        dic = { "on_window1_destroy" : gtk.main_quit,  
                #"on_button1_clicked" : self.submitDB,  
                #"on_button3_clicked" : self.fillTree,  
                #"on_notebook1_switch_page" : self.selectNotebookPage,  
                #"on_treeview1_button_press_event" : self.clickTree,  
                #"on_button2_clicked" : self.createProjectGraph  
                } 
        self.wTree.signal_autoconnect(dic)


window = AngelicaGUI()
gtk.main()
