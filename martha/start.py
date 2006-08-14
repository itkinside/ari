#! /usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

class Martha:
    ui = '''<ui>
    <menubar name="MenuBar">
      <menu action="File">
        <menuitem action="Open socket"/>
        <menuitem action="Quit"/>
      </menu>
      <menu action="Help">
        <menuitem action="About"/>
      </menu>
    </menubar>
    </ui>'''

    def __init__(self):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_title('Martha')
        window.connect('delete_event', self.close_application)
        window.set_size_request(525, 150)
        window.show()

        # Vertical container
        main_vbox = gtk.VBox(False, 1)
        window.add(main_vbox)
        main_vbox.show()

        # Menu v2
        uimanager = gtk.UIManager()
        accelgroup = uimanager.get_accel_group()
        window.add_accel_group(accelgroup)
        actiongroup = gtk.ActionGroup('Martha')
        actiongroup.add_actions([('Quit', gtk.STOCK_QUIT, '_Quit', None,
                                  'Quit', self.close_application),
                                 ('About', gtk.STOCK_QUIT, '_Above', None,
                                  'Quit', self.close_application),
                                 ('File', None, '_File'),
                                 ('Help', None, '_Help')])
        uimanager.insert_action_group(actiongroup, 0)
        uimanager.add_ui_from_string(self.ui)
        menubar = uimanager.get_widget('/MenuBar')
        main_vbox.pack_start(menubar, False)

        # Menu
#        menu_items = (
#            ( "/_File",         None,         None, 0, "<Branch>" ),
#            ( "/File/_New",     "<control>N", self.print_hello, 0, None ),
#            ( "/File/_Open",    "<control>O", self.print_hello, 0, None ),
#            ( "/File/_Save",    "<control>S", self.print_hello, 0, None ),
#            ( "/File/Save _As", None,         None, 0, None ),
#            ( "/File/sep1",     None,         None, 0, "<Separator>" ),
#            ( "/File/Quit",     "<control>Q", gtk.main_quit, 0, None ),
#            ( "/_Options",      None,         None, 0, "<Branch>" ),
#            ( "/Options/Test",  None,         None, 0, None ),
#            ( "/_Help",         None,         None, 0, "<LastBranch>" ),
#            ( "/_Help/About",   None,         None, 0, None ),
#            )
#        menubar = self.get_main_menu(window, menu_items)
#        main_vbox.pack_start(menubar, False, True, 0)
#        menubar.show()

        # Drawing area
        area = gtk.DrawingArea()
        area.set_size_request(75, 150)
        main_vbox.add(area)
        area.show()

        drawable = area.window
        style = area.get_style()
        gc = style.fg_gc[gtk.STATE_NORMAL]

        colormap = area.get_colormap()
        white = colormap.alloc_color('#ffffff', True, True)
        black = colormap.alloc_color('#000000', True, True)
        gc.set_foreground(white)
        gc.set_background(black)

        drawable.draw_line(gc, 0, 0, 75, 150)

    def main(self):
        gtk.main()
        return 0

    def close_application(self, widget, event = None, data = None):
        gtk.main_quit()
        return False

    def get_main_menu(self, window, menu_items):
        accel_group = gtk.AccelGroup()
        item_factory = gtk.ItemFactory(gtk.MenuBar, "<main>", accel_group)
        item_factory.create_items(menu_items)
        window.add_accel_group(accel_group)
        self.item_factory = item_factory
        return item_factory.get_widget("<main>")

if __name__ == '__main__':
    martha = Martha()
    martha.main()
