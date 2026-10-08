from .BaseConverter import BaseConverter, CONVERTER_TABLE, Context, Word
from typing import Any, List

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Subscript
except:
    Subscript = Any


class SubscriptConverter(BaseConverter):
    support_flatten_conversion = True

    def __init__(self: "SubscriptConverter") -> None:
        pass


CONVERTER_TABLE[Subscript] = SubscriptConverter()
