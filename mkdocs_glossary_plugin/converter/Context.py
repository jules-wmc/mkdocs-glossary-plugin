from typing import List
from collections import namedtuple

from mkdocs.config import Config

Word = namedtuple("Word", ["name", "source_path"])


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