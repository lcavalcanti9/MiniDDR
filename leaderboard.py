import json
import os

_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".miniddr_leaderboard.json")  #copilot4
_cache = {"attempts": {}, "entries": []}  #copilot4


def _save_cache():  #copilot4
    try:  #copilot4
        with open(_CACHE_FILE, "w", encoding="utf-8") as cache_file:  #copilot4
            json.dump(_cache, cache_file, indent=2)  #copilot4
    except OSError:  #copilot4
        pass  #copilot4


def begin_attempt(song):  #copilot4
    song_key = str(song)  #copilot4
    _cache["attempts"][song_key] = _cache["attempts"].get(song_key, 0) + 1  #copilot4
    _save_cache()  #copilot4
    return _cache["attempts"][song_key]  #copilot4


def record_result(song, player_name, attempt, score, maximum_score, grade):  #copilot4
    result = {"song": str(song), "name": str(player_name), "attempt": int(attempt), "score": int(score), "maximum_score": int(maximum_score), "grade": str(grade)}  #copilot4
    _cache["entries"].append(result)  #copilot4
    _cache["entries"].sort(key=lambda entry: (entry["song"], -entry["score"], entry["attempt"]))  #copilot4
    _save_cache()  #copilot4
    return dict(result)  #copilot4


def get_entries(song=None):  #copilot4
    entries = _cache["entries"] if song is None else [entry for entry in _cache["entries"] if entry["song"] == str(song)]  #copilot4
    return [dict(entry) for entry in entries]  #copilot4


def clear_cache():  #copilot4
    _cache["attempts"].clear()  #copilot4
    _cache["entries"].clear()  #copilot4
    try:  #copilot4
        os.remove(_CACHE_FILE)  #copilot4
    except FileNotFoundError:  #copilot4
        pass  #copilot4
    except OSError:  #copilot4
        pass  #copilot4


clear_cache()  #copilot4

