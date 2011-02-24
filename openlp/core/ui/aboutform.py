# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Jonathan Corwin, Michael      #
# Gorven, Scott Guerrieri, Meinert Jordan, Armin Köhler, Andreas Preikschat,  #
# Christian Richter, Philip Ridout, Maikel Stuivenberg, Martin Thompson, Jon  #
# Tibble, Carsten Tinggaard, Frode Woldsund                                   #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################

from PyQt4 import QtCore, QtGui

from aboutdialog import Ui_AboutDialog
from openlp.core.lib import translate

class AboutForm(QtGui.QDialog, Ui_AboutDialog):
    """
    The About dialog
    """

    def __init__(self, parent, applicationVersion):
        """
        Do some initialisation stuff
        """
        QtGui.QDialog.__init__(self, parent)
        self.applicationVersion = applicationVersion
        self.setupUi(self)
        about_text = self.aboutTextEdit.toPlainText()
        about_text = about_text.replace(u'<version>',
            self.applicationVersion[u'version'])
        if self.applicationVersion[u'build']:
            build_text = unicode(translate('OpenLP.AboutForm', ' build %s')) % \
                self.applicationVersion[u'build']
        else:
            build_text = u''
        about_text = about_text.replace(u'<revision>', build_text)
        self.aboutTextEdit.setPlainText(about_text)
        QtCore.QObject.connect(self.contributeButton,
            QtCore.SIGNAL(u'clicked()'), self.onContributeButtonClicked)

    def onContributeButtonClicked(self):
        """
        Launch a web browser and go to the contribute page on the site.
        """
        import webbrowser
        url = u'http://www.openlp.org/en/documentation/introduction/' \
            + u'contributing.html'
        webbrowser.open_new(url)
