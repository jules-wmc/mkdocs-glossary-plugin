from .BaseConverter import BaseConverter, CONVERTER_TABLE, Context, Word
from typing import Any, List

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Quoted
except:
    Quoted = Any


class QuotedConverter(BaseConverter):
    support_flatten_conversion = True

    def __init__(self: "QuotedConverter") -> None:
        pass


CONVERTER_TABLE[Quoted] = QuotedConverter()
