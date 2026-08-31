import json
import os
import glob


_translations = {}
_current_lang = "es"


def _get_locale_dir():
    return os.path.join(os.path.dirname(__file__), "locales")


def load_language(lang_code):
    global _translations, _current_lang
    path = os.path.join(_get_locale_dir(), f"{lang_code}.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            _translations = json.load(f)
    else:
        _translations = {}
    _current_lang = lang_code


def gettext(text):
    return _translations.get(text, text)


_ = gettext


def current_lang():
    return _current_lang


def available_languages():
    locale_dir = _get_locale_dir()
    files = glob.glob(os.path.join(locale_dir, "*.json"))
    langs = []
    for f in sorted(files):
        code = os.path.splitext(os.path.basename(f))[0]
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
            langs.append((code, data.get("_language_name", code)))
    return langs


load_language("es")
