from __future__ import absolute_import, print_function, unicode_literals
import Live
from ableton.v3.base import sign
from ableton.v3.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v3.control_surface.controls import ButtonControl, EncoderControl, ToggleButtonControl
from ableton.v3.live import move_current_song_time


class TransportComponent(TransportComponentBase):
    __events__ = ('transport_event', )
    arrangement_position_encoder = EncoderControl()
    metronome_button = ToggleButtonControl(color='Transport.MetronomeOff',
                                           on_color='Transport.MetronomeOn')
    delete_button = ButtonControl(color='Transport.DeleteOff',
                                  pressed_color='Transport.DeleteOn')

    @arrangement_position_encoder.value
    def arrangement_position_encoder(self, value, _):
        move_current_song_time(self.song, sign(value))
        self.notify_transport_event(
            '', str(self.song.get_current_smpte_song_time(Live.Song.TimeFormat.smpte_25)))

    @metronome_button.toggled
    def metronome_button(self, toggled, _):
        self.song.metronome = toggled
        self.notify_transport_event(
            'Metronome', 'ON' if toggled else 'OFF')

    @delete_button.pressed
    def delete_button(self, *_):
        slot1 = self.song.view.highlighted_clip_slot
        if slot1.has_clip:
            slot1.delete_clip()
        self.notify_transport_event(
            'Delete Clip', ':-X')
