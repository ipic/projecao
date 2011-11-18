# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=80 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2011 Raoul Snyman                                        #
# Portions copyright (c) 2008-2011 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Michael Gorven, Scott Guerrieri, Matthias Hub, Meinert Jordan,      #
# Armin Köhler, Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias     #
# Põldaru, Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,    #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Frode Woldsund             #
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

from openlp.core.lib import build_icon, translate
from openlp.core.lib.ui import UiStrings

class Ui_AboutDialog(object):
    def setupUi(self, aboutDialog):
        aboutDialog.setObjectName(u'aboutDialog')
        aboutDialog.setWindowIcon(build_icon(u':/icon/openlp-logo-16x16.png'))
        self.aboutDialogLayout = QtGui.QVBoxLayout(aboutDialog)
        self.aboutDialogLayout.setObjectName(u'aboutDialogLayout')
        self.logoLabel = QtGui.QLabel(aboutDialog)
        self.logoLabel.setPixmap(
            QtGui.QPixmap(u':/graphics/openlp-about-logo.png'))
        self.logoLabel.setObjectName(u'logoLabel')
        self.aboutDialogLayout.addWidget(self.logoLabel)
        self.aboutNotebook = QtGui.QTabWidget(aboutDialog)
        self.aboutNotebook.setObjectName(u'aboutNotebook')
        self.aboutTab = QtGui.QWidget()
        self.aboutTab.setObjectName(u'aboutTab')
        self.aboutTabLayout = QtGui.QVBoxLayout(self.aboutTab)
        self.aboutTabLayout.setObjectName(u'aboutTabLayout')
        self.aboutTextEdit = QtGui.QPlainTextEdit(self.aboutTab)
        self.aboutTextEdit.setReadOnly(True)
        self.aboutTextEdit.setObjectName(u'aboutTextEdit')
        self.aboutTabLayout.addWidget(self.aboutTextEdit)
        self.aboutNotebook.addTab(self.aboutTab, u'')
        self.creditsTab = QtGui.QWidget()
        self.creditsTab.setObjectName(u'creditsTab')
        self.creditsTabLayout = QtGui.QVBoxLayout(self.creditsTab)
        self.creditsTabLayout.setObjectName(u'creditsTabLayout')
        self.creditsTextEdit = QtGui.QPlainTextEdit(self.creditsTab)
        self.creditsTextEdit.setReadOnly(True)
        self.creditsTextEdit.setObjectName(u'creditsTextEdit')
        self.creditsTabLayout.addWidget(self.creditsTextEdit)
        self.aboutNotebook.addTab(self.creditsTab, u'')
        self.licenseTab = QtGui.QWidget()
        self.licenseTab.setObjectName(u'licenseTab')
        self.licenseTabLayout = QtGui.QVBoxLayout(self.licenseTab)
        self.licenseTabLayout.setObjectName(u'licenseTabLayout')
        self.licenseTextEdit = QtGui.QPlainTextEdit(self.licenseTab)
        self.licenseTextEdit.setReadOnly(True)
        self.licenseTextEdit.setObjectName(u'licenseTextEdit')
        self.licenseTabLayout.addWidget(self.licenseTextEdit)
        self.aboutNotebook.addTab(self.licenseTab, u'')
        self.aboutDialogLayout.addWidget(self.aboutNotebook)
        self.buttonBox = QtGui.QDialogButtonBox(aboutDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(u'buttonBox')
        self.contributeButton = QtGui.QPushButton()
        self.contributeButton.setIcon(
            build_icon(u':/system/system_contribute.png'))
        self.contributeButton.setObjectName(u'contributeButton')
        self.buttonBox.addButton(self.contributeButton,
            QtGui.QDialogButtonBox.ActionRole)
        self.aboutDialogLayout.addWidget(self.buttonBox)
        self.retranslateUi(aboutDialog)
        self.aboutNotebook.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(u'rejected()'),
            aboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(aboutDialog)

    def retranslateUi(self, aboutDialog):
        aboutDialog.setWindowTitle(u'%s OpenLP' % UiStrings().About)
        self.aboutTextEdit.setPlainText(translate('OpenLP.AboutForm',
            'OpenLP <version><revision> - Open Source Lyrics '
            'Projection\n'
            '\n'
            'OpenLP is free church presentation software, or lyrics '
            'projection software, used to display slides of songs, Bible '
            'verses, videos, images, and even presentations (if '
            'Impress, PowerPoint or PowerPoint Viewer is installed) '
            'for church worship using a computer and a data projector.\n'
            '\n'
            'Find out more about OpenLP: http://openlp.org/\n'
            '\n'
            'OpenLP is written and maintained by volunteers. If you would '
            'like to see more free Christian software being written, please '
            'consider contributing by using the button below.'
        ))
        self.aboutNotebook.setTabText(
            self.aboutNotebook.indexOf(self.aboutTab), UiStrings().About)
        lead = u'Raoul "superfly" Snyman'
        developers = [u'Tim "TRB143" Bentley', u'Jonathan "gushie" Corwin',
            u'Michael "cocooncrash" Gorven',
            u'Andreas "googol" Preikschat', u'Raoul "superfly" Snyman',
            u'Martin "mijiti" Thompson', u'Jon "Meths" Tibble']
        contributors = [u'Gerald "jerryb" Britton',
            u'Scott "sguerrieri" Guerrieri',
            u'Matthias "matthub" Hub', u'Meinert "m2j" Jordan',
            u'Armin "orangeshirt" K\xf6hler', u'Joshua "milleja46" Miller',
            u'Stevan "ElderP" Pettit', u'Mattias "mahfiaz" P\xf5ldaru',
            u'Christian "crichter" Richter', u'Philip "Phill" Ridout',
            u'Simon "samscudder" Scudder', u'Jeffrey "whydoubt" Smith',
            u'Maikel Stuivenberg', u'Frode "frodus" Woldsund']
        testers = [u'Philip "Phill" Ridout', u'Wesley "wrst" Stout',
            u'John "jseagull1" Cegalis (lead)']
        packagers = ['Thomas "tabthorpe" Abthorpe (FreeBSD)',
            u'Tim "TRB143" Bentley (Fedora and Android)',
            u'Matthias "matthub" Hub (Mac OS X)',
            u'Stevan "ElderP" Pettit (Windows)',
            u'Raoul "superfly" Snyman (Ubuntu)']
        translators = {
            u'af': [u'Johan "nuvolari" Mynhardt'],
            u'de': [u'Patrick "madmuffin" Br\xfcckner',
                u'Meinert "m2j" Jordan', u'Andreas "googol" Preikschat',
                u'Christian "crichter" Richter'],
            u'en_GB': [u'Tim "TRB143" Bentley', u'Jonathan "gushie" Corwin'],
            u'en_ZA': [u'Raoul "superfly" Snyman'],
            u'et': [u'Mattias "mahfiaz" P\xf5ldaru'],
            u'fr': [u'Stephan\xe9 "stbrunner" Brunner'],
            u'hu': [u'Gyuris Gell\xe9rt'],
            u'ja': [u'Kunio "Kunio" Nakamaru'],
            u'nb': [u'Atle "pendlaren" Weibell', u'Frode "frodus" Woldsund'],
            u'nl': [u'Arjen "typovar" van Voorst'],
            u'pt_BR': [u'Rafael "rafaellerm" Lerm', u'Gustavo Bim',
                u'Simon "samscudder" Scudder'],
            u'ru': [u'Sergey "ratz" Ratz']
        }
        documentors = [u'Wesley "wrst" Stout',
            u'John "jseagull1" Cegalis (lead)']
        self.creditsTextEdit.setPlainText(unicode(translate('OpenLP.AboutForm',
            'Project Lead\n'
            '    %s\n'
            '\n'
            'Developers\n'
            '    %s\n'
            '\n'
            'Contributors\n'
            '    %s\n'
            '\n'
            'Testers\n'
            '    %s\n'
            '\n'
            'Packagers\n'
            '    %s\n'
            '\n'
            'Translators\n'
            '    Afrikaans (af)\n'
            '        %s\n'
            '    German (de)\n'
            '        %s\n'
            '    English, United Kingdom (en_GB)\n'
            '        %s\n'
            '    English, South Africa (en_ZA)\n'
            '        %s\n'
            '    Estonian (et)\n'
            '        %s\n'
            '    French (fr)\n'
            '        %s\n'
            '    Hungarian (hu)\n'
            '        %s\n'
            '    Japanese (ja)\n'
            '        %s\n'
            '    Norwegian Bokm\xe5l (nb)\n'
            '        %s\n'
            '    Dutch (nl)\n'
            '        %s\n'
            '    Portuguese, Brazil (pt_BR)\n'
            '        %s\n'
            '    Russian (ru)\n'
            '        %s\n'
            '\n'
            'Documentation\n'
            '    %s\n'
            '\n'
            'Built With\n'
            '    Python: http://www.python.org/\n'
            '    Qt4: http://qt.nokia.com/\n'
            '    PyQt4: http://www.riverbankcomputing.co.uk/software/pyqt/'
            'intro\n'
            '    Oxygen Icons: http://oxygen-icons.org/\n'
            '\n'
            'Final Credit\n'
            '    "For God so loved the world that He gave\n'
            '    His one and only Son, so that whoever\n'
            '    believes in Him will not perish but inherit\n'
            '    eternal life."  -- John 3:16\n\n'
            '    And last but not least, final credit goes to\n'
            '    God our Father, for sending His Son to die\n'
            '    on the cross, setting us free from sin. We\n'
            '    bring this software to you for free because\n'
            '    He has set us free.')) % (lead, u'\n    '.join(developers),
            u'\n    '.join(contributors), u'\n    '.join(testers),
            u'\n    '.join(packagers), u'\n        '.join(translators[u'af']),
            u'\n        '.join(translators[u'de']),
            u'\n        '.join(translators[u'en_GB']),
            u'\n        '.join(translators[u'en_ZA']),
            u'\n        '.join(translators[u'et']),
            u'\n        '.join(translators[u'fr']),
            u'\n        '.join(translators[u'hu']),
            u'\n        '.join(translators[u'ja']),
            u'\n        '.join(translators[u'nb']),
            u'\n        '.join(translators[u'nl']),
            u'\n        '.join(translators[u'pt_BR']),
            u'\n        '.join(translators[u'ru']),
            u'\n    '.join(documentors)))
        self.aboutNotebook.setTabText(
            self.aboutNotebook.indexOf(self.creditsTab),
            translate('OpenLP.AboutForm', 'Credits'))
        copyright = unicode(translate('OpenLP.AboutForm',
            'Copyright \xa9 2004-2011 %s\n'
            'Portions copyright \xa9 2004-2011 %s')) % (u'Raoul Snyman',
            u'Tim Bentley, Jonathan Corwin, Michael Gorven, Gerald Britton, '
            u'Scott Guerrieri, Matthias Hub, Meinert Jordan, Armin K\xf6hler, '
            u'Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias '
            u'P\xf5ldaru, Christian Richter, Philip Ridout, Simon Scudder, '
            u'Jeffrey Smith, Maikel Stuivenberg, Martin Thompson, Jon Tibble, '
            u'Frode Woldsund')
        licence = translate('OpenLP.AboutForm',
            'This program is free software; you can redistribute it and/or '
            'modify it under the terms of the GNU General Public License as '
            'published by the Free Software Foundation; version 2 of the '
            'License.')
        disclaimer = translate('OpenLP.AboutForm',
            'This program is distributed in the hope that it will be useful, '
            'but WITHOUT ANY WARRANTY; without even the implied warranty of '
            'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See below '
            'for more details.')
        gpltext = ('GNU GENERAL PUBLIC LICENSE\n'
            'Version 2, June 1991\n'
            '\n'
            'Copyright (C) 1989, 1991 Free Software Foundation, Inc., 51 '
            'Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. '
            'Everyone is permitted to copy and distribute verbatim copies of '
            'this license document, but changing it is not allowed.\n'
            '\n'
            'Preamble\n'
            '\n'
            'The licenses for most software are designed to take away your '
            'freedom to share and change it. By contrast, the GNU General '
            'Public License is intended to guarantee your freedom to share '
            'and change free software--to make sure the software is free for '
            'all its users. This General Public License applies to most of '
            'the Free Software Foundation\'s software and to any other '
            'program whose authors commit to using it. (Some other Free '
            'Software Foundation software is covered by the GNU Lesser '
            'General Public License instead.) You can apply it to your '
            'programs, too.\n'
            '\n'
            'When we speak of free software, we are referring to freedom, not '
            'price. Our General Public Licenses are designed to make sure '
            'that you have the freedom to distribute copies of free software '
            '(and charge for this service if you wish), that you receive '
            'source code or can get it if you want it, that you can change '
            'the software or use pieces of it in new free programs; and that '
            'you know you can do these things.\n'
            '\n'
            'To protect your rights, we need to make restrictions that forbid '
            'anyone to deny you these rights or to ask you to surrender the '
            'rights. These restrictions translate to certain responsibilities '
            'for you if you distribute copies of the software, or if you '
            'modify it.\n'
            '\n'
            'For example, if you distribute copies of such a program, whether '
            'gratis or for a fee, you must give the recipients all the rights '
            'that you have. You must make sure that they, too, receive or '
            'can get the source code. And you must show them these terms so '
            'they know their rights.\n'
            '\n'
            'We protect your rights with two steps: (1) copyright the '
            'software, and (2) offer you this license which gives you legal '
            'permission to copy, distribute and/or modify the software.\n'
            '\n'
            'Also, for each author\'s protection and ours, we want to make '
            'certain that everyone understands that there is no warranty for '
            'this free software. If the software is modified by someone else '
            'and passed on, we want its recipients to know that what they '
            'have is not the original, so that any problems introduced by '
            'others will not reflect on the original authors\' reputations.\n'
            '\n'
            'Finally, any free program is threatened constantly by software '
            'patents. We wish to avoid the danger that redistributors of a '
            'free program will individually obtain patent licenses, in effect '
            'making the program proprietary. To prevent this, we have made '
            'it clear that any patent must be licensed for everyone\'s free '
            'use or not licensed at all.\n'
            '\n'
            'The precise terms and conditions for copying, distribution and '
            'modification follow.\n'
            '\n'
            'GNU GENERAL PUBLIC LICENSE\n'
            'TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION\n'
            '\n'
            '0. This License applies to any program or other work which '
            'contains a notice placed by the copyright holder saying it may '
            'be distributed under the terms of this General Public License. '
            'The "Program", below, refers to any such program or work, and a '
            '"work based on the Program" means either the Program or any '
            'derivative work under copyright law: that is to say, a work '
            'containing the Program or a portion of it, either verbatim or '
            'with modifications and/or translated into another language. '
            '(Hereinafter, translation is included without limitation in the '
            'term "modification".) Each licensee is addressed as "you".\n'
            '\n'
            'Activities other than copying, distribution and modification are '
            'not covered by this License; they are outside its scope. The '
            'act of running the Program is not restricted, and the output '
            'from the Program is covered only if its contents constitute a '
            'work based on the Program (independent of having been made by '
            'running the Program). Whether that is true depends on what the '
            'Program does.\n'
            '\n'
            '1. You may copy and distribute verbatim copies of the Program\'s '
            'source code as you receive it, in any medium, provided that you '
            'conspicuously and appropriately publish on each copy an '
            'appropriate copyright notice and disclaimer of warranty; keep '
            'intact all the notices that refer to this License and to the '
            'absence of any warranty; and give any other recipients of the '
            'Program a copy of this License along with the Program.\n'
            '\n'
            'You may charge a fee for the physical act of transferring a '
            'copy, and you may at your option offer warranty protection in '
            'exchange for a fee.\n'
            '\n'
            '2. You may modify your copy or copies of the Program or any '
            'portion of it, thus forming a work based on the Program, and '
            'copy and distribute such modifications or work under the terms '
            'of Section 1 above, provided that you also meet all of these '
            'conditions:\n'
            '\n'
            'a) You must cause the modified files to carry prominent notices '
            'stating that you changed the files and the date of any change.\n'
            '\n'
            'b) You must cause any work that you distribute or publish, that '
            'in whole or in part contains or is derived from the Program or '
            'any part thereof, to be licensed as a whole at no charge to all '
            'third parties under the terms of this License.\n'
            '\n'
            'c) If the modified program normally reads commands interactively '
            'when run, you must cause it, when started running for such '
            'interactive use in the most ordinary way, to print or display an '
            'announcement including an appropriate copyright notice and a '
            'notice that there is no warranty (or else, saying that you '
            'provide a warranty) and that users may redistribute the program '
            'under these conditions, and telling the user how to view a copy '
            'of this License. (Exception: if the Program itself is '
            'interactive but does not normally print such an announcement, '
            'your work based on the Program is not required to print an '
            'announcement.)\n'
            '\n'
            'These requirements apply to the modified work as a whole. If '
            'identifiable sections of that work are not derived from the '
            'Program, and can be reasonably considered independent and '
            'separate works in themselves, then this License, and its terms, '
            'do not apply to those sections when you distribute them as '
            'separate works. But when you distribute the same sections as '
            'part of a whole which is a work based on the Program, the '
            'distribution of the whole must be on the terms of this License, '
            'whose permissions for other licensees extend to the entire '
            'whole, and thus to each and every part regardless of who wrote '
            'it.\n'
            '\n'
            'Thus, it is not the intent of this section to claim rights or '
            'contest your rights to work written entirely by you; rather, the '
            'intent is to exercise the right to control the distribution of '
            'derivative or collective works based on the Program.\n'
            '\n'
            'In addition, mere aggregation of another work not based on the '
            'Program with the Program (or with a work based on the Program) '
            'on a volume of a storage or distribution medium does not bring '
            'the other work under the scope of this License.\n'
            '\n'
            '3. You may copy and distribute the Program (or a work based on '
            'it, under Section 2) in object code or executable form under the '
            'terms of Sections 1 and 2 above provided that you also do one of '
            'the following:\n'
            '\n'
            'a) Accompany it with the complete corresponding machine-readable '
            'source code, which must be distributed under the terms of '
            'Sections 1 and 2 above on a medium customarily used for software '
            'interchange; or,\n'
            '\n'
            'b) Accompany it with a written offer, valid for at least three '
            'years, to give any third party, for a charge no more than your '
            'cost of physically performing source distribution, a complete '
            'machine-readable copy of the corresponding source code, to be '
            'distributed under the terms of Sections 1 and 2 above on a '
            'medium customarily used for software interchange; or,\n'
            '\n'
            'c) Accompany it with the information you received as to the '
            'offer to distribute corresponding source code. (This '
            'alternative is allowed only for noncommercial distribution and '
            'only if you received the program in object code or executable '
            'form with such an offer, in accord with Subsection b above.)\n'
            '\n'
            'The source code for a work means the preferred form of the work '
            'for making modifications to it. For an executable work, '
            'complete source code means all the source code for all modules '
            'it contains, plus any associated interface definition files, '
            'plus the scripts used to control compilation and installation of '
            'the executable. However, as a special exception, the source '
            'code distributed need not include anything that is normally '
            'distributed (in either source or binary form) with the major '
            'components (compiler, kernel, and so on) of the operating system '
            'on which the executable runs, unless that component itself '
            'accompanies the executable.\n'
            '\n'
            'If distribution of executable or object code is made by offering '
            'access to copy from a designated place, then offering equivalent '
            'access to copy the source code from the same place counts as '
            'distribution of the source code, even though third parties are '
            'not compelled to copy the source along with the object code.\n'
            '\n'
            '4. You may not copy, modify, sublicense, or distribute the '
            'Program except as expressly provided under this License. Any '
            'attempt otherwise to copy, modify, sublicense or distribute the '
            'Program is void, and will automatically terminate your rights '
            'under this License. However, parties who have received copies, '
            'or rights, from you under this License will not have their '
            'licenses terminated so long as such parties remain in full '
            'compliance.\n'
            '\n'
            '5. You are not required to accept this License, since you have '
            'not signed it. However, nothing else grants you permission to '
            'modify or distribute the Program or its derivative works. These '
            'actions are prohibited by law if you do not accept this '
            'License. Therefore, by modifying or distributing the Program '
            '(or any work based on the Program), you indicate your acceptance '
            'of this License to do so, and all its terms and conditions for '
            'copying, distributing or modifying the Program or works based on '
            'it.\n'
            '\n'
            '6. Each time you redistribute the Program (or any work based on '
            'the Program), the recipient automatically receives a license '
            'from the original licensor to copy, distribute or modify the '
            'Program subject to these terms and conditions. You may not '
            'impose any further restrictions on the recipients\' exercise of '
            'the rights granted herein. You are not responsible for enforcing '
            'compliance by third parties to this License.\n'
            '\n'
            '7. If, as a consequence of a court judgment or allegation of '
            'patent infringement or for any other reason (not limited to '
            'patent issues), conditions are imposed on you (whether by court '
            'order, agreement or otherwise) that contradict the conditions of '
            'this License, they do not excuse you from the conditions of this '
            'License. If you cannot distribute so as to satisfy '
            'simultaneously your obligations under this License and any other '
            'pertinent obligations, then as a consequence you may not '
            'distribute the Program at all. For example, if a patent license '
            'would not permit royalty-free redistribution of the Program by '
            'all those who receive copies directly or indirectly through you, '
            'then the only way you could satisfy both it and this License '
            'would be to refrain entirely from distribution of the Program.\n'
            '\n'
            'If any portion of this section is held invalid or unenforceable '
            'under any particular circumstance, the balance of the section is '
            'intended to apply and the section as a whole is intended to '
            'apply in other circumstances.\n'
            '\n'
            'It is not the purpose of this section to induce you to infringe '
            'any patents or other property right claims or to contest '
            'validity of any such claims; this section has the sole purpose '
            'of protecting the integrity of the free software distribution '
            'system, which is implemented by public license practices. Many '
            'people have made generous contributions to the wide range of '
            'software distributed through that system in reliance on '
            'consistent application of that system; it is up to the '
            'author/donor to decide if he or she is willing to distribute '
            'software through any other system and a licensee cannot impose '
            'that choice.\n'
            '\n'
            'This section is intended to make thoroughly clear what is '
            'believed to be a consequence of the rest of this License.\n'
            '\n'
            '8. If the distribution and/or use of the Program is restricted '
            'in certain countries either by patents or by copyrighted '
            'interfaces, the original copyright holder who places the Program '
            'under this License may add an explicit geographical distribution '
            'limitation excluding those countries, so that distribution is '
            'permitted only in or among countries not thus excluded. In such '
            'case, this License incorporates the limitation as if written in '
            'the body of this License.\n'
            '\n'
            '9. The Free Software Foundation may publish revised and/or new '
            'versions of the General Public License from time to time. Such '
            'new versions will be similar in spirit to the present version, '
            'but may differ in detail to address new problems or concerns.\n'
            '\n'
            'Each version is given a distinguishing version number. If the '
            'Program specifies a version number of this License which applies '
            'to it and "any later version", you have the option of '
            'following the terms and conditions either of that version or of '
            'any later version published by the Free Software Foundation. If '
            'the Program does not specify a version number of this License, '
            'you may choose any version ever published by the Free Software '
            'Foundation.\n'
            '\n'
            '10. If you wish to incorporate parts of the Program into other '
            'free programs whose distribution conditions are different, write '
            'to the author to ask for permission. For software which is '
            'copyrighted by the Free Software Foundation, write to the Free '
            'Software Foundation; we sometimes make exceptions for this. Our '
            'decision will be guided by the two goals of preserving the free '
            'status of all derivatives of our free software and of promoting '
            'the sharing and reuse of software generally.\n'
            '\n'
            'NO WARRANTY\n'
            '\n'
            '11. BECAUSE THE PROGRAM IS LICENSED FREE OF CHARGE, THERE IS NO '
            'WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY APPLICABLE '
            'LAW. EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT '
            'HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT '
            'WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, '
            'BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY '
            'AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE '
            'QUALITY AND PERFORMANCE OF THE PROGRAM IS WITH YOU. SHOULD THE '
            'PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF ALL NECESSARY '
            'SERVICING, REPAIR OR CORRECTION.\n'
            '\n'
            '12. IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO '
            'IN WRITING WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY '
            'MODIFY AND/OR REDISTRIBUTE THE PROGRAM AS PERMITTED ABOVE, BE '
            'LIABLE TO YOU FOR DAMAGES, INCLUDING ANY GENERAL, SPECIAL, '
            'INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OR '
            'INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS '
            'OF DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY '
            'YOU OR THIRD PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH '
            'ANY OTHER PROGRAMS), EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN '
            'ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.\n'
            '\n'
            'END OF TERMS AND CONDITIONS\n'
            '\n'
            'How to Apply These Terms to Your New Programs\n'
            '\n'
            'If you develop a new program, and you want it to be of the '
            'greatest possible use to the public, the best way to achieve '
            'this is to make it free software which everyone can redistribute '
            'and change under these terms.\n'
            '\n'
            'To do so, attach the following notices to the program. It is '
            'safest to attach them to the start of each source file to most '
            'effectively convey the exclusion of warranty; and each file '
            'should have at least the "copyright" line and a pointer to where '
            'the full notice is found.\n'
            '\n'
            '<one line to give the program\'s name and a brief idea of what '
            'it does.>\n'
            'Copyright (C) <year> <name of author>\n'
            '\n'
            'This program is free software; you can redistribute it and/or '
            'modify it under the terms of the GNU General Public License as '
            'published by the Free Software Foundation; either version 2 of '
            'the License, or (at your option) any later version.\n'
            '\n'
            'This program is distributed in the hope that it will be useful, '
            'but WITHOUT ANY WARRANTY; without even the implied warranty of '
            'MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the '
            'GNU General Public License for more details.\n'
            '\n'
            'You should have received a copy of the GNU General Public '
            'License along with this program; if not, write to the Free '
            'Software Foundation, Inc., 51 Franklin Street, Fifth Floor, '
            'Boston, MA 02110-1301 USA.\n'
            '\n'
            'Also add information on how to contact you by electronic and '
            'paper mail.\n'
            '\n'
            'If the program is interactive, make it output a short notice '
            'like this when it starts in an interactive mode:\n'
            '\n'
            'Gnomovision version 69, Copyright (C) year name of author\n'
            'Gnomovision comes with ABSOLUTELY NO WARRANTY; for details type '
            '"show w".\n'
            'This is free software, and you are welcome to redistribute it '
            'under certain conditions; type "show c" for details.\n'
            '\n'
            'The hypothetical commands "show w" and "show c" should show '
            'the appropriate parts of the General Public License. Of course, '
            'the commands you use may be called something other than "show '
            'w" and "show c"; they could even be mouse-clicks or menu items--'
            'whatever suits your program.\n'
            '\n'
            'You should also get your employer (if you work as a programmer) '
            'or your school, if any, to sign a "copyright disclaimer" for the '
            'program, if necessary. Here is a sample; alter the names:\n'
            '\n'
            'Yoyodyne, Inc., hereby disclaims all copyright interest in the '
            'program "Gnomovision" (which makes passes at compilers) written '
            'by James Hacker.\n'
            '\n'
            '<signature of Ty Coon>, 1 April 1989\n'
            'Ty Coon, President of Vice\n'
            '\n'
            'This General Public License does not permit incorporating your '
            'program into proprietary programs. If your program is a '
            'subroutine library, you may consider it more useful to permit '
            'linking proprietary applications with the library. If this is '
            'what you want to do, use the GNU Lesser General Public License '
            'instead of this License.')
        self.licenseTextEdit.setPlainText(u'%s\n\n%s\n\n%s\n\n\n%s' %
            (copyright, licence, disclaimer, gpltext))
        self.aboutNotebook.setTabText(
            self.aboutNotebook.indexOf(self.licenseTab),
            translate('OpenLP.AboutForm', 'License'))
        self.contributeButton.setText(translate('OpenLP.AboutForm',
            'Contribute'))
