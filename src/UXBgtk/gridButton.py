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

from gi.repository import Gtk
from getImage import getImage, updateImage
from constants import GRID_BUTTON_SIZE


# grid direction vectors (8 points of the compass)
directions = []
for x in range(-1, 2):
    for y in range(-1, 2):
        # we skip the centre
        if not (x == y == 0): directions.append((x, y))



class GridButton(Gtk.Button):
    """Visual representation of a minefield grid square. Contains all the
    information it needs to display itself and interact with the game."""


    def __init__(self, parent=None, pos=None, mined=False):
        """Do the class initialization and prepare the game-specific
        attributes."""

        super().__init__()

        # the global application parent object and the game grid
        self.parent = parent

        # this button's grid position.
        self.pos = pos

        # is this button mined?
        self.mined = mined
        self.exploded = False

        # is this button flagged? - initialize to False
        self.flagged = False

        # TODO initialize the mine count to zero
        self.neighbourMines = 0

        # TODO need to convert from ttk
#        self['textvariable'] = self.neighbourMines
#        self['width'] = 2 # width of the text field

        # initialize the neighbour flag count to zero
        self.neighbourFlags = 0

        # flag to emulate disabled when mines are exposed
        self.exposed = False

        # TODO  Convert from ttk: initialize the image to empty at 20 pixels
#        self.imageSize = 20
#        self.imageKey = 'Empty'
#        self.setImage()
#        self['compound'] = 'image'
        self.imageKey = 'Explosion'
        self.image = getImage(self.imageKey)
        self.add(self.image)
        updateImage(self.image, self.imageKey,
                    (GRID_BUTTON_SIZE, GRID_BUTTON_SIZE))

        # TODO convert from ttk: initialize the font key to 10 pixels (half image size).
#        self.fontKey = '.'.join([str(self.imageSize // 2), 'TButton'])

#        # TODO these are the TK bindings: set up the event bindings
#        self.bind('<ButtonRelease-1>', self.leftMouse)  # Left-Mouse
#        self.bind('<ButtonRelease-3>', self.rightMouse) # Right-Mouse
#        self.bind('<ButtonPress-1>',
#                  lambda event, \
#                         button=self._root().gameWindow.toolbar.startButton, \
#                         key='Click':\
#                         self._root().gameWindow.toolbar.setImage(button, key))

        # set up the GTK event handlers
        self.connect("button_press_event", self.on_button_press_event)
        self.connect("button_release_event", self.on_button_release_event)



    def updateNeighbourMines(self):
        """Update the number of neighbouring mines after initialization. This
        only happens at the start of each game, but the cache of neighbours is
        used later."""

        # initialize the list of neighbours
        self.neighbourList = []
        for dir in directions:
            x = self.pos[0] + dir[0]
            y = self.pos[1] + dir[1]
            if x < 0 or x >= self.parent.cols or \
               y < 0 or y >= self.parent.rows: continue
            neighbour = self.parent.btnLookup[(x, y)]
            self.neighbourList.append(neighbour)

            # count the neighbours that are mined
            if neighbour.mined: self.neighbourMines += 1


    def updateNeighbourFlags(self, increment):
        """Increment or decrement the count of neighbour flags when notified of
        a change. The Boolean increment argument determines whether we add or
        remove from the tally."""

        if increment: self.neighbourFlags += 1
        else: self.neighbourFlags -= 1


    def setImage(self):
        """Set the image on the button using the key. """

        # TODO need to convert from ttk
        pass

#        self['image'] = getImage(self, self.imageSize, self.imageKey)


    def setFont(self):
        """Set up the font to use for text. This also changes the background
        colour of the button. Different styles for different numbers of mines
        gives the numbers different foreground colours."""

        # TODO we need to convert this from ttk
        pass
#        # use a different background if the button has not been exposed
#        if self.exposed:
#            self['style'] = '.'.join([str(self.neighbourMines.get()),
#                                      self.fontKey])
#        else:
#            self['style'] = self.fontKey


    def setStyle(self, fontKey):
        """Choose the style to use according to the font key passed, and set
        the image size to match."""

        # TODO need to convert from ttk
        pass
#        
#        self.fontKey = fontKey
#        self.setFont()
#
#        # configure the image to match the font size
#        self.imageSize = int(fontKey.split('.')[0]) * 2
#        self.setImage()

    def resize(self, size):
        """Resize the grid button's child (image or text) to match the current
        window size. (The button looks after itself.)"""

        # TODO something goes in here to replace setStyle, setFont, setImage.
        allocation = self.get_allocation()
        allocation.width = size[0]
        allocation.height = size[1]
        self.set_allocation(allocation)

        updateImage(self.image, self.imageKey, size)


    def on_button_press_event(self, widget, event):
        """Event handler for button presses. The handler must decide which
        mouse button was clicked and forward the invocation to leftMouse() or
        rightMouse()."""
        # TODO need some functionality here
        print('Pressed Event! pos=' + str(self.pos))
        print('Widget is ' + str(widget))
        print('Event is ' + str(event))
        print('Event button # is ' + str(event.get_button()))


    def on_button_release_event(self, widget, event):
        """Event handler for button releases. The handler must decide which
        mouse button was clicked. We are only interested in leftMouse clicks."""
        # TODO need some functionality here
        print('Released Event! pos=' + str(self.pos))
        print('Widget is ' + str(widget))
        print('Event is ' + str(event))
        print('Event button # is ' + str(event.get_button()))


    def leftMouse(self, widget):
        """Left-Mouse handler. We use this to clear the area."""

        # exclusions
        if self.exposed: return False
        if self.flagged: return False

        exposedNeighbours = 0

        # end game - we hit a mine - lose
        if self.mined:
            self.imageKey = 'Explosion' # lose
#            # TODO cleardown mode - not working - threading problem?
#            if self.master.exploded:
#                self.imageKey = 'UXB'

            self.setImage()
            self.exploded = True
            self.master.exploded = True

        else: # expose the button, display the number of neighbour mines
            self.expose(self)

            # propagate exposure to the neighbours if mines = flags
            if self.neighbourFlags == self.neighbourMines.get():
                for neighbour in self.neighbourList:

                    exposedNeighbours += neighbour.leftMouse(widget)

            # TODO reset the start button image
            self._root().gameWindow.toolbar.setImage(
                self._root().gameWindow.toolbar.startButton, 'Start')

        # update count of exposed buttons - potential win end game
        exposedNeighbours += 1 # add self to the count
        if widget == self:
            self.master.incrementExposedCount(exposedNeighbours)
        else: return exposedNeighbours


    def expose(self, widget):
        """Reveal the number of neighbour mines for this button."""

        # disable the button and change its colour once it has been clicked
        self.exposed = True
        self.setFont()

        self.imageKey = 'Empty'
        self.setImage()
        if self.neighbourMines.get() > 0:
            self['compound'] = 'center'

        # this is for when invoked by the game grid when giving hints
        if widget != self:
            self.master.incrementExposedCount(1)


    def rightMouse(self):
        """Right-Mouse handler. We use this to toggle mine flags."""

        if self.exposed: return

        if self.flagged:
            self.imageKey = 'Empty'
            self.setImage()
        else:
            self.imageKey = 'Flag'
            self.setImage()
        self.flagged = not self.flagged

        # notify neighbours and parent of the change
        self.master.updateFlags(self.flagged)
        for neighbour in self.neighbourList:
            neighbour.updateNeighbourFlags(self.flagged)
