# Copyright (C) 2012 Bob Bowles <bobjohnbowles@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
import time
from gi.repository import Gtk, Gdk
from constants import UI_BUILD_FILE, UI_CSS_FILE, TOOL_SIZE, BUTTON_PAD
from getImage import initializeImages, getImage, updateImage
from gridWindow import GridWindow


def getAllocatedSize(allocation):
    """Obtain the width and height from a Gtk.Allocation as a tuple.
    Returns a tuple (width, height)."""
    return allocation.width, allocation.height



class UXBgtk:
    """The main game UI"""


    def __init__(self):
        """Load the main UI elements from the .glade file."""

        self.builder = Gtk.Builder()
        self.builder.add_from_file(UI_BUILD_FILE)
        self.builder.connect_signals(self)

        # these are the toolbar widgets
        self.startButton = self.builder.get_object('startButton')
        self.startImage = getImage('Start')
        updateImage(self.startImage, 'Start', TOOL_SIZE)
        self.startButton.add(self.startImage)

        self.hintButton = self.builder.get_object('hintButton')
        self.hintImage = getImage('Hint')
        updateImage(self.hintImage, 'Hint', TOOL_SIZE)
        self.hintButton.add(self.hintImage)
        self.hintButton.set_sensitive(False)

        # the configurationBox and its model
        self.configurations = self.builder.get_object('configurations')
        self.configurationBox = self.builder.get_object('configurationBox')

        self.quitButton = self.builder.get_object('quitButton')
        self.quitImage = getImage('Quit')
        updateImage(self.quitImage, 'Quit', TOOL_SIZE)
        self.quitButton.add(self.quitImage)

        # these are the status bar widgets
        self.exposedCount = self.builder.get_object('exposedCount')
        self.exposedLabel = self.builder.get_object('exposedLabel')
        self.flagCount = self.builder.get_object('flagCount')
        self.flagLabel = self.builder.get_object('flagLabel')

        # the game grid (blank for now)
        self.gridContainer = self.builder.get_object('gridContainer')
        self.gameGrid = None
        self.imageSize = None
        self.initializeGeometry()

        # get references to the toolbar and status bar for size data.
        self.toolbar = self.builder.get_object('toolBox')
        self.statusbar = self.builder.get_object('statusBox')

        # get a reference to the main window itself and display the window
        self.resize = True # resizing toggle
        self.window = self.builder.get_object('window')
        self.window.show_all()


    def initializeGeometry(self):
        """Initialize the geometry hints for the main window."""

        self.geometry = Gdk.Geometry()
        self.geometry.base_height = -1
        self.geometry.base_width = -1
        self.geometry.min_height = -1
        self.geometry.min_width = -1
        self.geometry.min_aspect = 1.0
        self.geometry.max_aspect = 1.0


    def start(self):
        """Start a new game."""

        # reset the start button image
        updateImage(self.startImage, 'Start', TOOL_SIZE)

        # get the grid information from the configuration box.
        activeConfiguration = self.configurationBox.get_active_iter()
        cols, rows, nMines = tuple(self.configurations[activeConfiguration])[2:]

        mines = [True] * nMines
        mines.extend([False] * (cols * rows - nMines))
        random.shuffle(mines)

        # reset the status bar
        self.exposedCount.set_text('0')
        self.exposedLabel.set_text('/ ' + str(cols * rows - nMines))
        self.flagCount.set_text('0')
        self.flagLabel.set_text('/ ' + str(nMines))

        # destroy any pre-existing game
        if self.gameGrid != None: self.gameGrid.destroy()

        # make the new game
        self.gameGrid = GridWindow(parent=self,
                                   cols=cols, rows=rows, mines=mines)
        self.gridContainer.add_with_viewport(self.gameGrid)

        # impose geometry constraints on the window depending on cols and rows
        print('Imposing aspect ratio ' + str(cols / rows))
        self.geometry.min_aspect = cols / rows
        self.geometry.max_aspect = cols / rows
        self.window.set_geometry_hints(self.gridContainer,
                                       self.geometry,
                                       Gdk.WindowHints.ASPECT)

        # start the game
        self.hintButton.set_sensitive(True)
        self.gameGrid.start()
        self.window.show_all()


    def on_window_destroy(self, widget):
        """Handler for closing window."""

        Gtk.main_quit()


    def on_startButton_clicked(self, widget):
        """Handler for the start button."""

        self.start()


    def on_hintButton_clicked(self, widget):
        """Handler for the hint button."""

        self.gameGrid.giveHint()


    def on_quitButton_clicked(self, widget):
        """Handler for the quit button."""

        # obtain the size of the playing area
        size = (self.gridContainer.get_allocated_width(),
                self.gridContainer.get_allocated_height())

        # get rid of the old game
        if self.gameGrid != None: self.gameGrid.destroy()

        # flash up an image
        image = getImage('Explosion')
        updateImage(image, 'Explosion', size)
        self.gridContainer.add_with_viewport(image)
        self.window.show_all()

        # wait a short time without blocking the Gtk event loop...
        for milliseconds in range(2000):
            while Gtk.events_pending():
                Gtk.main_iteration()
            time.sleep(.001)

        # ...now kill the app
        self.window.destroy()


    def on_configurationBox_changed(self, widget):
        """Reset stuff that needs to be reset for creating the game grid."""

        self.imageSize = None
#
#
#    def resizeWindow(self): # TODO maybe don't need this...
#        """Make the window conform to square button geometry."""
#
#        newWidth = (self.imageSize + BUTTON_PAD) * self.gameGrid.cols
#        newHeight = (self.imageSize + BUTTON_PAD) * self.gameGrid.rows
#
#        newWinWidth = newWidth
#        newWinHeight = newHeight + 80
##        \
##                       + self.toolbar.get_allocated_height() \
##                       + self.statusbar.get_allocated_height()
#        newWinSize = newWinWidth, newWinHeight
#        requestedSize = self.window.get_size_request()
#
#        # handle expansion and contraction differently...
#        if requestedSize[0] > newWinWidth or requestedSize[1] > newWinHeight:
#            print('New Win size is BIGGER:  ' + str(newWinSize))
#            self.window.resize(newWinWidth, newWinHeight)
#        else:
#            print('New Win size is SMALLER: ' + str(newWinSize))
#            self.window.set_default_size(newWinWidth, newWinHeight)
#
#
#    def resizeGame(self, allocation): # TODO maybe don't need this
#        """Implement resizing of the window and grid on request. The allocation
#        has already been tested for the correct square button geometry."""
#
#        # resize the game grid...
#        print('New allocation            ('
#              + str(allocation.width) + ',' + str(allocation.height) + ')')
#        self.gameGrid.set_allocation(allocation)
#
#        # ...and then the buttons and images
#        print('Images size requested is ' + str(self.imageSize))
#        self.gameGrid.resizeButtons(self.imageSize)


    def on_window_check_resize(self, widget):
        """Handler for resizing the game grid images. """

        # do nothing if the game grid is not ready
        if not self.gameGrid: return

        # work out the container's allocation
        allocation = self.gridContainer.get_allocation()

        # try to make the allocation fit the rows and columns of the grid
        imageWidth = allocation.width // self.gameGrid.cols - BUTTON_PAD
        imageHeight = allocation.height // self.gameGrid.rows - BUTTON_PAD

        # use the mean of the test sizes
        self.imageSize = (imageWidth, imageHeight)

#        print('New allocation            ('
#              + str(allocation.width) + ',' + str(allocation.height) + ')')
        self.gameGrid.set_allocation(allocation)

        # ...and then the buttons and images
#        print('Images size requested is ' + str(self.imageSize))
        self.gameGrid.resizeButtons(self.imageSize)


# load the image pixbuf cache
initializeImages()

# configure themed styles for the grid buttons
cssProvider = Gtk.CssProvider()
cssProvider.load_from_path(UI_CSS_FILE)
screen = Gdk.Screen.get_default()
styleContext = Gtk.StyleContext()
styleContext.add_provider_for_screen(screen, cssProvider,
                                     Gtk.STYLE_PROVIDER_PRIORITY_USER)

app = UXBgtk()
Gtk.main()

