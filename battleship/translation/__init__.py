"""Translation module."""

import gettext
from battleship.util import Config
import battleship.resources as resources


def _(string):
    global _ru
    if LANGUAGE == "Русский":
        return _ru(string)
    return string


def setLang(language):
    """Set translation language."""
    global LANGUAGE
    LANGUAGE = language


def get_translation():
    """Define translations."""
    if "LANGUAGE" not in globals():
        global LANGUAGE
        LANGUAGE = Config.get()["language"]
        ruTrans = gettext.translation(
            "messages", resources.translation, languages=("ru",)
        )
        global _ru
        _ru = ruTrans.gettext
