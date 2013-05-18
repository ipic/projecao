# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2013 Raoul Snyman                                        #
# Portions copyright (c) 2008-2013 Tim Bentley, Gerald Britton, Jonathan      #
# Corwin, Samuel Findlay, Michael Gorven, Scott Guerrieri, Matthias Hub,      #
# Meinert Jordan, Armin Köhler, Erik Lundin, Edwin Lunando, Brian T. Meyer.   #
# Joshua Miller, Stevan Pettit, Andreas Preikschat, Mattias Põldaru,          #
# Christian Richter, Philip Ridout, Simon Scudder, Jeffrey Smith,             #
# Maikel Stuivenberg, Martin Thompson, Jon Tibble, Dave Warnock,              #
# Frode Woldsund, Martin Zibricky, Patrick Zimmermann                         #
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
"""
The :mod:`~openlp.core.ui.media.webkit` module contains our WebKit video player
"""
from PyQt4 import QtGui

import logging

from openlp.core.lib import Settings, translate
from openlp.core.ui.media import MediaState
from openlp.core.ui.media.mediaplayer import MediaPlayer

log = logging.getLogger(__name__)

VIDEO_CSS = u"""
#videobackboard {
    z-index:3;
    background-color: %(bgcolor)s;
}
#video {
    background-color: %(bgcolor)s;
    z-index:4;
}
"""

VIDEO_JS = u"""
    function show_video(state, path, volume, loop, variable_value){
        // Sometimes  video.currentTime stops slightly short of video.duration and video.ended is intermittent!

        var video = document.getElementById('video');
        if(volume != null){
            video.volume = volume;
        }
        switch(state){
            case 'load':
                video.src = 'file:///' + path;
                if(loop == true) {
                    video.loop = true;
                }
                video.load();
                break;
            case 'play':
                video.play();
                break;
            case 'pause':
                video.pause();
                break;
            case 'stop':
                show_video('pause');
                video.currentTime = 0;
                break;
            case 'close':
                show_video('stop');
                video.src = '';
                break;
            case 'length':
                return video.duration;
            case 'current_time':
                return video.currentTime;
            case 'seek':
                video.currentTime = variable_value;
                break;
            case 'isEnded':
                return video.ended;
            case 'setVisible':
                video.style.visibility = variable_value;
                break;
            case 'setBackBoard':
                var back = document.getElementById('videobackboard');
                back.style.visibility = variable_value;
                break;
       }
    }
"""

VIDEO_HTML = u"""
<div id="videobackboard" class="size" style="visibility:hidden"></div>
<video id="video" class="size" style="visibility:hidden" autobuffer preload></video>
"""

FLASH_CSS = u"""
#flash {
    z-index:5;
}
"""

FLASH_JS = u"""
    function getFlashMovieObject(movieName)
    {
        if (window.document[movieName]){
            return window.document[movieName];
        }
        if (document.embeds && document.embeds[movieName]){
            return document.embeds[movieName];
        }
    }

    function show_flash(state, path, volume, variable_value){
        var text = document.getElementById('flash');
        var flashMovie = getFlashMovieObject("OpenLPFlashMovie");
        var src = "src = 'file:///" + path + "'";
        var view_parm = " wmode='opaque'" + " width='100%%'" + " height='100%%'";
        var swf_parm = " name='OpenLPFlashMovie'" + " autostart='true' loop='false' play='true'" +
            " hidden='false' swliveconnect='true' allowscriptaccess='always'" + " volume='" + volume + "'";

        switch(state){
            case 'load':
                text.innerHTML = "<embed " + src + view_parm + swf_parm + "/>";
                flashMovie = getFlashMovieObject("OpenLPFlashMovie");
                flashMovie.Play();
                break;
            case 'play':
                flashMovie.Play();
                break;
            case 'pause':
                flashMovie.StopPlay();
                break;
            case 'stop':
                flashMovie.StopPlay();
                tempHtml = text.innerHTML;
                text.innerHTML = '';
                text.innerHTML = tempHtml;
                break;
            case 'close':
                flashMovie.StopPlay();
                text.innerHTML = '';
                break;
            case 'length':
                return flashMovie.TotalFrames();
            case 'current_time':
                return flashMovie.CurrentFrame();
            case 'seek':
//                flashMovie.GotoFrame(variable_value);
                break;
            case 'isEnded':
                //TODO check flash end
                return false;
            case 'setVisible':
                text.style.visibility = variable_value;
                break;
        }
    }
"""

FLASH_HTML = u"""
<div id="flash" class="size" style="visibility:hidden"></div>
"""

VIDEO_EXT = [
    u'*.3gp',
    u'*.3gpp',
    u'*.3g2',
    u'*.3gpp2',
    u'*.aac',
    u'*.flv',
    u'*.f4a',
    u'*.f4b',
    u'*.f4p',
    u'*.f4v',
    u'*.mov',
    u'*.m4a',
    u'*.m4b',
    u'*.m4p',
    u'*.m4v',
    u'*.mkv',
    u'*.mp4',
    u'*.ogv',
    u'*.webm',
    u'*.mpg', u'*.wmv', u'*.mpeg', u'*.avi',
    u'*.swf'
]

AUDIO_EXT = [
    u'*.mp3',
    u'*.ogg'
]


class WebkitPlayer(MediaPlayer):
    """
    A specialised version of the MediaPlayer class, which provides a QtWebKit
    display.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        MediaPlayer.__init__(self, parent, u'webkit')
        self.original_name = u'WebKit'
        self.display_name = u'&WebKit'
        self.parent = parent
        self.can_background = True
        self.audio_extensions_list = AUDIO_EXT
        self.video_extensions_list = VIDEO_EXT

    def get_media_display_css(self):
        """
        Add css style sheets to htmlbuilder
        """
        background = QtGui.QColor(Settings().value(u'players/background color')).name()
        css = VIDEO_CSS % {u'bgcolor': background}
        return css + FLASH_CSS

    def get_media_display_javascript(self):
        """
        Add javascript functions to htmlbuilder
        """
        return VIDEO_JS + FLASH_JS

    def get_media_display_html(self):
        """
        Add html code to htmlbuilder
        """
        return VIDEO_HTML + FLASH_HTML

    def setup(self, display):
        """
        Set up the player
        """
        display.web_view.resize(display.size())
        display.web_view.raise_()
        self.has_own_widget = False

    def check_available(self):
        """
        Check the availability of the media player
        """
        return True

    def load(self, display):
        """
        Load a video
        """
        log.debug(u'load vid in Webkit Controller')
        controller = display.controller
        if display.has_audio and not controller.media_info.is_background:
            volume = controller.media_info.volume
            vol = float(volume) / float(100)
        else:
            vol = 0
        path = controller.media_info.file_info.absoluteFilePath()
        if controller.media_info.is_background:
            loop = u'true'
        else:
            loop = u'false'
        display.web_view.setVisible(True)
        if controller.media_info.file_info.suffix() == u'swf':
            controller.media_info.is_flash = True
            js = u'show_flash("load","%s");' % (path.replace(u'\\', u'\\\\'))
        else:
            js = u'show_video("load", "%s", %s, %s);' % (path.replace(u'\\', u'\\\\'), str(vol), loop)
        display.frame.evaluateJavaScript(js)
        return True

    def resize(self, display):
        """
        Resize the player
        """
        display.web_view.resize(display.size())

    def play(self, display):
        """
        Play a video
        """
        controller = display.controller
        display.web_loaded = True
        length = 0
        start_time = 0
        if self.state != MediaState.Paused and controller.media_info.start_time > 0:
            start_time = controller.media_info.start_time
        self.set_visible(display, True)
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("play");')
        else:
            display.frame.evaluateJavaScript(u'show_video("play");')
        if start_time > 0:
            self.seek(display, controller.media_info.start_time * 1000)
        # TODO add playing check and get the correct media length
        controller.media_info.length = length
        self.state = MediaState.Playing
        display.web_view.raise_()
        return True

    def pause(self, display):
        """
        Pause a video
        """
        controller = display.controller
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("pause");')
        else:
            display.frame.evaluateJavaScript(u'show_video("pause");')
        self.state = MediaState.Paused

    def stop(self, display):
        """
        Stop a video
        """
        controller = display.controller
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("stop");')
        else:
            display.frame.evaluateJavaScript(u'show_video("stop");')
        self.state = MediaState.Stopped

    def volume(self, display, volume):
        """
        Set the volume
        """
        controller = display.controller
        # 1.0 is the highest value
        if display.has_audio:
            vol = float(volume) / float(100)
            if not controller.media_info.is_flash:
                display.frame.evaluateJavaScript(u'show_video(null, null, %s);' % str(vol))

    def seek(self, display, seek_value):
        """
        Go to a position in the video
        """
        controller = display.controller
        if controller.media_info.is_flash:
            seek = seek_value
            display.frame.evaluateJavaScript(u'show_flash("seek", null, null, "%s");' % (seek))
        else:
            seek = float(seek_value) / 1000
            display.frame.evaluateJavaScript(u'show_video("seek", null, null, null, "%f");' % (seek))

    def reset(self, display):
        """
        Reset the player
        """
        controller = display.controller
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("close");')
        else:
            display.frame.evaluateJavaScript(u'show_video("close");')
        self.state = MediaState.Off

    def set_visible(self, display, status):
        """
        Set the visibility
        """
        controller = display.controller
        if status:
            is_visible = "visible"
        else:
            is_visible = "hidden"
        if controller.media_info.is_flash:
            display.frame.evaluateJavaScript(u'show_flash("setVisible", null, null, "%s");' % (is_visible))
        else:
            display.frame.evaluateJavaScript(u'show_video("setVisible", null, null, null, "%s");' % (is_visible))

    def update_ui(self, display):
        """
        Update the UI
        """
        controller = display.controller
        if controller.media_info.is_flash:
            current_time = display.frame.evaluateJavaScript(u'show_flash("current_time");')
            length = display.frame.evaluateJavaScript(u'show_flash("length");')
        else:
            if display.frame.evaluateJavaScript(u'show_video("isEnded");'):
                self.stop(display)
            current_time = display.frame.evaluateJavaScript(u'show_video("current_time");')
            # check if conversion was ok and value is not 'NaN'
            if current_time and current_time != float('inf'):
                current_time = int(current_time * 1000)
            length = display.frame.evaluateJavaScript(u'show_video("length");')
            # check if conversion was ok and value is not 'NaN'
            if length and length != float('inf'):
                length = int(length * 1000)
        if current_time > 0:
            controller.media_info.length = length
            controller.seek_slider.setMaximum(length)
            if not controller.seek_slider.isSliderDown():
                controller.seek_slider.blockSignals(True)
                controller.seek_slider.setSliderPosition(current_time)
                controller.seek_slider.blockSignals(False)

    def get_info(self):
        """
        Return some information about this player
        """
        return(translate('Media.player', 'Webkit is a media player which runs '
            'inside a web browser. This player allows text over video to be '
            'rendered.') +
            u'<br/> <strong>' + translate('Media.player', 'Audio') +
            u'</strong><br/>' + unicode(AUDIO_EXT) + u'<br/><strong>' +
            translate('Media.player', 'Video') + u'</strong><br/>' +
            unicode(VIDEO_EXT) + u'<br/>')
