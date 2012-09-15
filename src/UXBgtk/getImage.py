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

from gi.repository import Gtk, Gdk, GdkPixbuf
import os
from constants import UI_GRAPHICS_PATH, IMAGE_NAMES


# initialize the image cache data structure
imageCache = dict.fromkeys(IMAGE_NAMES)


def initializeImages():
    """Initialize the cache of pixbufs."""

    for key in imageCache.keys():
        file = os.path.join(UI_GRAPHICS_PATH, IMAGE_NAMES[key])
        print('Caching ' + key + ' from file ' + file + '...')
        imageCache[key] = GdkPixbuf.Pixbuf().new_from_file(file)
        

def getImage(name):
    """Obtain an image from a pre-cached pixbuf."""

    return Gtk.Image().new_from_pixbuf(imageCache[name])


def updateImage(image, name, size):
    """Update an image using the file database via an image name key. The image 
    is sized according to the size tuple."""
    
    x = size[0]
    y = size[1]
    #print('Scaling image ' + name + ' to (' + str(x) + ',' + str(y) + ')')
    pixbuf = imageCache[name].scale_simple(x, y,
                                           GdkPixbuf.InterpType.BILINEAR)
    image.set_from_pixbuf(pixbuf)
