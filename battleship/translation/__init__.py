import gettext
from battleship.util import Config
import battleship.resources as resources


def _(string):
    global _ru
    if LANGUAGE == "Русский":
        return _ru(string)
    return string


def setLang(language):
    global LANGUAGE
    LANGUAGE = language


if "LANGUAGE" not in globals():
    LANGUAGE = Config.get()["language"]
    ruTrans = gettext.translation(
        "messages", resources.translation, languages=("ru",)
    )
    _ru = ruTrans.gettext
