from .BaseConverter import BaseConverter, CONVERTER_TABLE, Context, Word
from typing import Any, List

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Underline
except:
    Underline = Any


class UnderlineConverter(BaseConverter):
    support_flatten_conversion = True

    def __init__(self: "UnderlineConverter") -> None:
        pass


CONVERTER_TABLE[Underline] = UnderlineConverter()
