##############################################################################
#                                                                            #
#  This file is part of SonSilentSea, a free ships based combatr game.       #
#  Copyright (C) 2014  Jose Luis Cercos Pita <jlcercos@gmail.com>            #
#                                                                            #
#  AQUAgpusph is free software: you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by      #
#  the Free Software Foundation, either version 3 of the License, or         #
#  (at your option) any later version.                                       #
#                                                                            #
#  AQUAgpusph is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU General Public License for more details.                              #
#                                                                            #
#  You should have received a copy of the GNU General Public License         #
#  along with AQUAgpusph.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                            #
##############################################################################

import bge
from bge import logic as g
import os.path as path
import sys


class sssDynamicLoader():
    def __init__(self, obj):
        blend_file = self['blend_file']
        if blend_file == '':
            return
        self.load_blender_file(blend_file)

    def typeName(self):
        return 'sssDynamicLoader'

    def update(self):
        return

    def load_blender_file(self, file_name):
        # Locate the file
        file_path = self._locate_resource(file_name)
        if not file_path:
            print('Failure loading "{}":'.format(file_name))
            print('    File not found')
            return
        loaded = g.LibList()
        print(loaded)
        if file_path in loaded:
            return

        # Load it
        g.LibLoad(file_path, 'Scene', load_actions=True, verbose=True, load_scripts=True)
        loaded = g.LibList()
        print(loaded)

    def _locate_resource(self, file_name):
        if path.isabs(file_name):
            return file_name
        # Default paths
        paths = [path.join(sys.prefix,'share/sonsilentsea/resources'),
                 path.join(path.abspath('./'),'resources'),
                 path.expanduser('~/.sonsilentsea/resources')]
        # Look for the file in the paths
        for p in paths:
            file_path = path.join(p, file_name)
            if path.isfile(file_path):
                return file_path
        return None
