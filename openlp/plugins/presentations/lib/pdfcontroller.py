# -*- coding: utf-8 -*-

##########################################################################
# OpenLP - Open Source Lyrics Projection                                 #
# ---------------------------------------------------------------------- #
# Copyright (c) 2008-2020 OpenLP Developers                              #
# ---------------------------------------------------------------------- #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <https://www.gnu.org/licenses/>. #
##########################################################################
import logging
import re
from shutil import which
from subprocess import CalledProcessError, check_output

from openlp.core.common import check_binary_exists, is_win
from openlp.core.common.registry import Registry
from openlp.core.common.applocation import AppLocation
from openlp.core.display.screens import ScreenList
from openlp.plugins.presentations.lib.presentationcontroller import PresentationController, PresentationDocument


if is_win():
    from subprocess import STARTUPINFO, STARTF_USESHOWWINDOW

try:
    import fitz
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

log = logging.getLogger(__name__)

PDF_CONTROLLER_FILETYPES = ['pdf', 'xps', 'oxps', 'epub', 'cbz', 'fb2']


class PdfController(PresentationController):
    """
    Class to control PDF presentations
    """
    log.info('PdfController loaded')

    def __init__(self, plugin):
        """
        Initialise the class

        :param plugin: The plugin that creates the controller.
        """
        log.debug('Initialising')
        super(PdfController, self).__init__(plugin, 'Pdf', PdfDocument)
        self.process = None
        self.supports = ['pdf']
        self.also_supports = []
        # Determine whether mudraw or ghostscript is used
        self.check_installed()

    @staticmethod
    def process_check_binary(program_path):
        """
        Function that checks whether a binary is either ghostscript or mudraw or neither.
        Is also used from presentationtab.py

        :param pathlib.Path program_path: The full path to the binary to check.
        :return: Type of the binary, 'gs' if ghostscript, 'mudraw' if mudraw, None if invalid.
        :rtype: str | None
        """
        program_type = None
        runlog = check_binary_exists(program_path)
        # Analyse the output to see it the program is mudraw, ghostscript or neither
        for line in runlog.splitlines():
            decoded_line = line.decode()
            found_mudraw = re.search('usage: mudraw.*', decoded_line, re.IGNORECASE)
            if found_mudraw:
                program_type = 'mudraw'
                break
            found_mutool = re.search('usage: mutool.*', decoded_line, re.IGNORECASE)
            if found_mutool:
                # Test that mutool contains mudraw
                if re.search(r'draw\s+--\s+convert document.*', runlog.decode(), re.IGNORECASE | re.MULTILINE):
                    program_type = 'mutool'
                    break
            found_gs = re.search('GPL Ghostscript.*', decoded_line, re.IGNORECASE)
            if found_gs:
                program_type = 'gs'
                break
        log.debug('in check_binary, found: {text}'.format(text=program_type))
        return program_type

    def check_available(self):
        """
        PdfController is able to run on this machine.

        :return: True if program to open PDF-files was found, otherwise False.
        """
        log.debug('check_available Pdf')
        return self.check_installed()

    def check_installed(self):
        """
        Check the viewer is installed.

        :return: True if program to open PDF-files was found, otherwise False.
        """
        log.debug('check_installed Pdf')
        self.mudrawbin = None
        self.mutoolbin = None
        self.gsbin = None
        self.also_supports = []
        # Use the user defined program if given
        if Registry().get('settings').value('presentations/enable_pdf_program'):
            program_path = Registry().get('settings').value('presentations/pdf_program')
            program_type = self.process_check_binary(program_path)
            if program_type == 'gs':
                self.gsbin = program_path
            elif program_type == 'mudraw':
                self.mudrawbin = program_path
            elif program_type == 'mutool':
                self.mutoolbin = program_path
        elif PYMUPDF_AVAILABLE:
            self.also_supports = ['xps', 'oxps', 'epub', 'cbz', 'fb2']
            return True
        else:
            # Fallback to autodetection
            application_path = AppLocation.get_directory(AppLocation.AppDir)
            if is_win():
                # for windows we only accept mudraw.exe or mutool.exe in the base folder
                if (application_path / 'mudraw.exe').is_file():
                    self.mudrawbin = application_path / 'mudraw.exe'
                elif (application_path / 'mutool.exe').is_file():
                    self.mutoolbin = application_path / 'mutool.exe'
            else:
                # First try to find mudraw
                self.mudrawbin = which('mudraw')
                # if mudraw isn't installed, try mutool
                if not self.mudrawbin:
                    self.mutoolbin = which('mutool')
                    # Check we got a working mutool
                    if not self.mutoolbin or self.process_check_binary(self.mutoolbin) != 'mutool':
                        self.gsbin = which('gs')
                # Last option: check if mudraw or mutool is placed in OpenLP base folder
                if not self.mudrawbin and not self.mutoolbin and not self.gsbin:
                    application_path = AppLocation.get_directory(AppLocation.AppDir)
                    if (application_path / 'mudraw').is_file():
                        self.mudrawbin = application_path / 'mudraw'
                    elif (application_path / 'mutool').is_file():
                        self.mutoolbin = application_path / 'mutool'
        if self.mudrawbin or self.mutoolbin:
            self.also_supports = ['xps', 'oxps', 'epub', 'cbz', 'fb2']
            return True
        elif self.gsbin:
            return True
        return False

    def kill(self):
        """
        Called at system exit to clean up any running presentations
        """
        log.debug('Kill pdfviewer')
        while self.docs:
            self.docs[0].close_presentation()


class PdfDocument(PresentationDocument):
    """
    Class which holds information of a single presentation.
    This class is not actually used to present the PDF, instead we convert to
    image-serviceitem on the fly and present as such. Therefore some of the 'playback'
    functions is not implemented.
    """
    def __init__(self, controller, document_path):
        """
        Constructor, store information about the file and initialise.

        :param pathlib.Path document_path: Path to the document to load
        :rtype: None
        """
        log.debug('Init Presentation Pdf')
        super().__init__(controller, document_path)
        self.presentation = None
        self.blanked = False
        self.hidden = False
        self.image_files = []
        self.num_pages = -1
        # Setup startupinfo options for check_output to avoid console popping up on windows
        if is_win():
            self.startupinfo = STARTUPINFO()
            self.startupinfo.dwFlags |= STARTF_USESHOWWINDOW
        else:
            self.startupinfo = None

    def gs_get_resolution(self, size):
        """
        Only used when using ghostscript
        Ghostscript can't scale automatically while keeping aspect like mupdf, so we need
        to get the ratio between the screen size and the PDF to scale

        :param size: Size struct containing the screen size.
        :return: The resolution dpi to be used.
        """
        # Use a postscript script to get size of the pdf. It is assumed that all pages have same size
        gs_resolution_script = AppLocation.get_directory(
            AppLocation.PluginsDir) / 'presentations' / 'lib' / 'ghostscript_get_resolution.ps'
        # Run the script on the pdf to get the size
        runlog = []
        try:
            runlog = check_output([str(self.controller.gsbin), '-dNOPAUSE', '-dNODISPLAY', '-dBATCH',
                                   '-sFile={file_path}'.format(file_path=self.file_path), str(gs_resolution_script)],
                                  startupinfo=self.startupinfo)
        except CalledProcessError as e:
            log.debug(' '.join(e.cmd))
            log.debug(e.output)
        # Extract the pdf resolution from output, the format is " Size: x: <width>, y: <height>"
        width = 0.0
        height = 0.0
        for line in runlog.splitlines():
            try:
                width = float(re.search(r'.*Size: x: (\d+\.?\d*), y: \d+.*', line.decode()).group(1))
                height = float(re.search(r'.*Size: x: \d+\.?\d*, y: (\d+\.?\d*).*', line.decode()).group(1))
                break
            except AttributeError:
                continue
        # Calculate the ratio from pdf to screen
        if width > 0 and height > 0:
            width_ratio = size.width() / width
            height_ratio = size.height() / height
            # return the resolution that should be used. 72 is default.
            if width_ratio > height_ratio:
                return int(height_ratio * 72)
            else:
                return int(width_ratio * 72)
        else:
            return 72

    def load_presentation(self):
        """
        Called when a presentation is added to the SlideController. It generates images from the PDF.

        :return: True is loading succeeded, otherwise False.
        """
        log.debug('load_presentation pdf')
        temp_dir_path = self.get_temp_folder()
        # Check if the images has already been created, and if yes load them
        if (temp_dir_path / 'mainslide001.png').is_file():
            created_files = sorted(temp_dir_path.glob('*'))
            for image_path in created_files:
                if image_path.is_file():
                    self.image_files.append(image_path)
            self.num_pages = len(self.image_files)
            return True
        size = ScreenList().current.display_geometry
        # Generate images from PDF that will fit the frame.
        runlog = ''
        try:
            if not temp_dir_path.is_dir():
                temp_dir_path.mkdir(parents=True)
            # The %03d in the file name is handled by each binary
            if self.controller.mudrawbin:
                log.debug('loading presentation using mudraw')
                runlog = check_output([str(self.controller.mudrawbin), '-w', str(size.width()),
                                       '-h', str(size.height()),
                                       '-o', str(temp_dir_path / 'mainslide%03d.png'), str(self.file_path)],
                                      startupinfo=self.startupinfo)
            elif self.controller.mutoolbin:
                log.debug('loading presentation using mutool')
                runlog = check_output([str(self.controller.mutoolbin), 'draw', '-w', str(size.width()),
                                       '-h', str(size.height()), '-o', str(temp_dir_path / 'mainslide%03d.png'),
                                       str(self.file_path)],
                                      startupinfo=self.startupinfo)
            elif self.controller.gsbin:
                log.debug('loading presentation using gs')
                resolution = self.gs_get_resolution(size)
                runlog = check_output([str(self.controller.gsbin), '-dSAFER', '-dNOPAUSE', '-dBATCH', '-sDEVICE=png16m',
                                       '-r{res}'.format(res=resolution), '-dTextAlphaBits=4', '-dGraphicsAlphaBits=4',
                                       '-sOutputFile={output}'.format(output=temp_dir_path / 'mainslide%03d.png'),
                                       str(self.file_path)], startupinfo=self.startupinfo)
            elif PYMUPDF_AVAILABLE:
                log.debug('loading presentation using PyMuPDF')
                pdf = fitz.open(str(self.file_path))
                for i, page in enumerate(pdf, start=1):
                    src_size = page.bound().round()
                    # keep aspect ratio
                    scale = min(size.width() / src_size.width, size.height() / src_size.height)
                    m = fitz.Matrix(scale, scale)
                    page.getPixmap(m, alpha=False).writeImage(str(temp_dir_path / 'mainslide{:03d}.png'.format(i)))
                pdf.close()
            created_files = sorted(temp_dir_path.glob('*'))
            for image_path in created_files:
                if image_path.is_file():
                    self.image_files.append(image_path)
        except Exception:
            log.exception(runlog)
            return False
        self.num_pages = len(self.image_files)
        # Create thumbnails
        self.create_thumbnails()
        return True

    def create_thumbnails(self):
        """
        Generates thumbnails
        """
        log.debug('create_thumbnails pdf')
        if self.check_thumbnails():
            return
        # use builtin function to create thumbnails from generated images
        index = 1
        for image in self.image_files:
            self.convert_thumbnail(image, index)
            index += 1

    def close_presentation(self):
        """
        Close presentation and clean up objects. Triggered by new object being added to SlideController or OpenLP being
        shut down.
        """
        log.debug('close_presentation pdf')
        self.controller.remove_doc(self)

    def is_loaded(self):
        """
        Returns true if a presentation is loaded.

        :return: True if loaded, False if not.
        """
        log.debug('is_loaded pdf')
        if self.num_pages < 0:
            return False
        return True

    def is_active(self):
        """
        Returns true if a presentation is currently active.

        :return: True if active, False if not.
        """
        log.debug('is_active pdf')
        return self.is_loaded() and not self.hidden

    def get_slide_count(self):
        """
        Returns total number of slides

        :return: The number of pages in the presentation..
        """
        return self.num_pages
