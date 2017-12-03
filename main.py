"""
Author: Gidalti Lourenço Junior
Contact: gidaltijunior@gmail.com
Description: A program to help to control pharmacy prescriptions in Pequeno Cotolengo NGO.

Copyright (C) 2017  Gidalti Lourenço Junior

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from login import Login

if __name__ == "__main__":
    usuario = None
    login = Login()
    Gtk.main()
