from .BaseConverter import BaseConverter, CONVERTER_TABLE, Context, Word
from typing import Any, List

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Span
except:
    Span = Any


class SpanConverter(BaseConverter):
    support_flatten_conversion = True

    def __init__(self: "SpanConverter") -> None:
        pass


CONVERTER_TABLE[Span] = SpanConverter()
