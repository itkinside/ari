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
