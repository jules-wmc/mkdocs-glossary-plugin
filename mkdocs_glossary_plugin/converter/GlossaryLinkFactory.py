from typing import Any, List
import os

from .Context import Context, Word

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Link
except:
    Link = Any


def make_glossary_link(context: Context, word: Word, content: List[Any]) -> Link:
    relative_path: str = os.path.relpath(word.source_path, context.current_dir)
    return Link(("", [], []), content, (relative_path, ""))  # type: ignore
