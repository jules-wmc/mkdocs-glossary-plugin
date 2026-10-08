from .BaseConverter import BaseConverter, CONVERTER_TABLE, Context, Word
from typing import Any, List

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Superscript
except:
    Superscript = Any


class SuperscriptConverter(BaseConverter):
    support_flatten_conversion = True

    def __init__(self: "SuperscriptConverter") -> None:
        pass


CONVERTER_TABLE[Superscript] = SuperscriptConverter()
