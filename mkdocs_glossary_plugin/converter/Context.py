from typing import List, Optional
from collections import namedtuple

from mkdocs.config import Config

# is_case_sensitive overrides the global is_case_sensitive setting for this word when not None
Word = namedtuple("Word", ["name", "source_path", "is_case_sensitive"], defaults=[None])


class Context:
    def __init__(
        self: "Context", config: Config, glossary: List[Word], current_dir: str
    ) -> None:
        self.glossary: List[Word] = glossary
        self.current_dir: str = current_dir

        self.is_case_sensitive: bool = config["is_case_sensitive"]
        self.enable_toc: bool = config["enable_toc"]
        self.replace_emphasized_text: bool = config["replace_emphasized_text"]
        self.replace_header: bool = config["replace_header"]
        self.replace_table_header: bool = config["replace_table_header"]
        self.replace_table_body: bool = config["replace_table_body"]
        self.replace_math_element: bool = config["replace_math_element"]