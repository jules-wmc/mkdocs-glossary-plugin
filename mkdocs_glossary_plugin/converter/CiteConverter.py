from .BaseConverter import BaseConverter, CONVERTER_TABLE, Context, Word
from typing import Any, List

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Cite
except:
    Cite = Any


class CiteConverter(BaseConverter):
    support_flatten_conversion = True

    def __init__(self: "CiteConverter") -> None:
        pass


CONVERTER_TABLE[Cite] = CiteConverter()
