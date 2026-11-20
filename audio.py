import pygame
import math  #copilot2
import struct  #copilot2
import wave  #copilot2
from io import BytesIO  #copilot2

# Write one event per line as exact beat number, a pipe, then lane 1-4. #copilot2
# Use decimal beats for subdivisions (for example 2.5); REST marks a pause. #copilot2
# Lines starting with # are comments, and blank lines are ignored. #copilot2
BPM = 70  #copilot2 #copilot3
SONG_CHART = """ #copilot2
# beat | lane (or REST) #copilot2
0 | 1 #copilot2
0.5 | 2 #copilot2
1 | 3 #copilot2
2 | 4 #copilot2
2.5 | REST #copilot2
3 | 1 #copilot2
3.5 | 2 #copilot2
4 | 3 #copilot2
5 | 4 #copilot2
5.5 | REST #copilot2
6 | 1 #copilot2
6.5 | 2 #copilot2
7 | 3 #copilot2
7.5 | 3 #copilot2
8 | 4 #copilot2
9 | 1 #copilot2
10 | 2 #copilot2
11 | 3 #copilot2
13 | 4 #copilot2
"""  #copilot2

# Melody pitches and durations, in beat units, for the synthesized sample. #copilot2
_MELODY = [ #copilot2
    (0, 0.5, 392.00), (0.5, 0.5, 392.00), (1, 1, 440.00), (2, 1, 392.00), #copilot2
    (3, 0.5, 523.25), (3.5, 0.5, 493.88), (4, 0.5, 392.00), (5, 0.5, 392.00), #copilot2
    (6, 0.5, 440.00), (6.5, 0.5, 392.00), (7, 0.5, 587.33), (7.5, 0.5, 523.25), #copilot2
    (8, 1, 392.00), (9, 0.5, 392.00), (10, 0.5, 440.00), (11, 0.5, 392.00), #copilot2
    (13, 1.5, 523.25), #copilot2
] #copilot2

_chart_notes = []  #copilot2
for _line in SONG_CHART.splitlines():  #copilot2
    _line = _line.split("#", 1)[0].strip()  #copilot2
    if not _line:  #copilot2
        continue  #copilot2
    _beat_text, _lane_text = _line.split("|", 1)  #copilot2
    _beat = float(_beat_text.strip())  #copilot2
    _lane_text = _lane_text.strip().upper()  #copilot2
    if _lane_text != "REST":  #copilot2
        _chart_notes.append({"beat": _beat, "lane": int(_lane_text)})  #copilot2
_chart_notes.sort(key=lambda _note: _note["beat"])  #copilot2

_PRACTICE_CHART = """ #copilot5
0 | 1 #copilot5
1 | 1 #copilot5
2 | 2 #copilot5
3 | 2 #copilot5
4 | 3 #copilot5
5 | 3 #copilot5
6 | 2 #copilot5
7 | REST #copilot5
9 | 4 #copilot5
10 | 4 #copilot5
11 | 3 #copilot5
12 | 3 #copilot5
13 | 2 #copilot5
14 | 2 #copilot5
15 | 1 #copilot5
"""  #copilot5
_PRACTICE_MELODY = [(beat, 0.75, frequency) for beat, frequency in [(0, 329.63), (1, 329.63), (2, 392.00), (3, 392.00), (4, 440.00), (5, 440.00), (6, 392.00), (9, 523.25), (10, 523.25), (11, 440.00), (12, 440.00), (13, 392.00), (14, 392.00), (15, 329.63)]]  #copilot5
_practice_chart_notes = []  #copilot5
for _line in _PRACTICE_CHART.splitlines():  #copilot5
    _line = _line.split("#", 1)[0].strip()  #copilot5
    if not _line:  #copilot5
        continue  #copilot5
    _beat_text, _lane_text = _line.split("|", 1)  #copilot5
    _lane_text = _lane_text.strip().upper()  #copilot5
    if _lane_text != "REST":  #copilot5
        _practice_chart_notes.append({"beat": float(_beat_text.strip()), "lane": int(_lane_text)})  #copilot5
_practice_chart_notes.sort(key=lambda _note: _note["beat"])  #copilot5

_sample_rate = 22050  #copilot2
_song_sound = {}  #copilot2 #copilot3
_song_channel = None  #copilot2
_start_ticks = None  #copilot2
_scheduled_start_ticks = None  #copilot5
_song_duration = (max(_beat + _duration for _beat, _duration, _frequency in _MELODY) + 1) * 60 / BPM  #copilot2
SONG_NAMES = ["Happy Birthday", "Practice Melody"]  #copilot3
SONG_METADATA = {"Happy Birthday": {"difficulty": "Medium", "description": "A familiar birthday tune with a varied rhythm."}, "Practice Melody": {"difficulty": "Easy", "description": "A gentle two-part melody for practicing the lanes."}}  #copilot5
_selected_song = 0  #copilot3


def get_song_names():  #copilot3
    return list(SONG_NAMES)  #copilot3


def get_song_metadata(song=None):  #copilot5
    song_name = SONG_NAMES[_selected_song] if song is None else str(song)  #copilot5
    return dict(SONG_METADATA.get(song_name, {"difficulty": "Unknown", "description": "No description available."}))  #copilot5


def select_song(index):  #copilot3
    global _selected_song  #copilot3
    _selected_song = int(index) % len(SONG_NAMES)  #copilot3


def _selected_chart_notes():  #copilot5
    return _chart_notes if _selected_song == 0 else _practice_chart_notes  #copilot5


def _selected_melody():  #copilot5
    return _MELODY if _selected_song == 0 else _PRACTICE_MELODY  #copilot5


def _selected_song_duration():  #copilot5
    return (max(_beat + _duration for _beat, _duration, _frequency in _selected_melody()) + 1) * 60 / BPM  #copilot5


def _build_song_sound():  #copilot2
    global _song_sound  #copilot2
    if _selected_song in _song_sound:  #copilot3
        return _song_sound[_selected_song]  #copilot3
    if not pygame.mixer.get_init():  #copilot2
        pygame.mixer.init(frequency=_sample_rate, size=-16, channels=1)  #copilot2
    melody = _selected_melody()  #copilot5
    total_samples = int(_selected_song_duration() * _sample_rate)  #copilot5
    samples = [0] * total_samples  #copilot2
    for beat, duration, frequency in melody:  #copilot2 #copilot3
        start = int(beat * 60 / BPM * _sample_rate)  #copilot2
        length = int(duration * 60 / BPM * _sample_rate * 0.92)  #copilot2
        for offset in range(length):  #copilot2
            envelope = min(1.0, offset / 180, (length - offset) / 800)  #copilot2
            value = int(11000 * envelope * math.sin(2 * math.pi * frequency * offset / _sample_rate))  #copilot2
            if start + offset < total_samples:  #copilot2
                samples[start + offset] += value  #copilot2
    pcm = struct.pack("<" + "h" * total_samples, *(max(-32768, min(32767, sample)) for sample in samples))  #copilot2
    audio_file = BytesIO()  #copilot2
    with wave.open(audio_file, "wb") as wav_file:  #copilot2
        wav_file.setnchannels(1)  #copilot2
        wav_file.setsampwidth(2)  #copilot2
        wav_file.setframerate(_sample_rate)  #copilot2
        wav_file.writeframes(pcm)  #copilot2
    audio_file.seek(0)  #copilot2
    _song_sound[_selected_song] = pygame.mixer.Sound(file=audio_file)  #copilot3
    return _song_sound[_selected_song]  #copilot3


def start_playback(delay=0.0):  #copilot5
    """Start playback now or schedule it after a delay in seconds."""  #copilot5
    global _song_channel, _start_ticks, _scheduled_start_ticks  #copilot5
    if _song_channel is not None:  #copilot4
        _song_channel.stop()  #copilot4
    sound = _build_song_sound()  #copilot4
    _song_channel = None  #copilot5
    _start_ticks = None  #copilot5
    _scheduled_start_ticks = pygame.time.get_ticks() + int(max(0.0, delay) * 1000)  #copilot5
    if delay <= 0.0:  #copilot5
        _song_channel = sound.play()  #copilot4
        _start_ticks = pygame.time.get_ticks() if _song_channel else None  #copilot4
        _scheduled_start_ticks = None  #copilot5
    return _scheduled_start_ticks is not None or _start_ticks is not None  #copilot5


def current_time():  #copilot4
    """Return elapsed playback time in seconds (zero before playback starts)."""  #copilot4
    global _song_channel, _start_ticks, _scheduled_start_ticks  #copilot5
    if _scheduled_start_ticks is not None and pygame.time.get_ticks() >= _scheduled_start_ticks:  #copilot5
        _song_channel = _build_song_sound().play()  #copilot5
        _start_ticks = pygame.time.get_ticks() if _song_channel else None  #copilot5
        _scheduled_start_ticks = None  #copilot5
    if _start_ticks is None:  #copilot4
        return 0.0  #copilot4
    return min((pygame.time.get_ticks() - _start_ticks) / 1000.0, _selected_song_duration())  #copilot5


def current_beat():  #copilot2
    """Return the current position in beats, capped at the song's end."""  #copilot2
    return current_time() * BPM / 60  #copilot2


def get_visible_notes(lookahead_beats=5.0):  #copilot2
    """Return notes within the visible beat window, with their beat and lane."""  #copilot2
    beat_now = current_beat()  #copilot2
    return [dict(note) for note in _selected_chart_notes() if beat_now - 0.2 <= note["beat"] <= beat_now + lookahead_beats]  #copilot5


def get_chart_notes():  #copilot4
    """Return a stable copy of all notes in this song's chart."""  #copilot4
    return [dict(note) for note in _selected_chart_notes()]  #copilot5


def get_song_duration():  #copilot4
    """Return the synthesized song duration in seconds."""  #copilot4
    return _selected_song_duration()  #copilot5


def stop_playback():  #copilot4
    """Stop current playback and clear its timing state before a replay."""  #copilot4
    global _song_channel, _start_ticks, _scheduled_start_ticks  #copilot5
    if _song_channel is not None:  #copilot4
        _song_channel.stop()  #copilot4
    _song_channel = None  #copilot4
    _start_ticks = None  #copilot4
    _scheduled_start_ticks = None  #copilot5

