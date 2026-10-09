from .Context import Context, Word
from .GlossaryLinkFactory import make_glossary_link
from typing import Any, List, Tuple
import logging
import re

import pandoc
from pandoc.types import *

try:
    from pandoc.types import Str, Space, SoftBreak
except:
    Str = Any
    Space = Any
    SoftBreak = Any

log = logging.getLogger("mkdocs.plugins." + __name__)


def is_mergeable_inline(context: Context, child: Any) -> bool:
    if isinstance(child, Str):
        # a literal "[TOC]" token is left alone so StrConverter can replace it with the table of contents
        return not (context.enable_toc and child[0] == "[TOC]")
    return isinstance(child, Space) or isinstance(child, SoftBreak)


def find_whole_word(haystack: str, needle: str) -> int:
    """Find the first occurrence of needle in haystack that isn't part of a larger word."""
    if not needle:
        return -1
    match = re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", haystack)
    return match.start() if match else -1


class MergeableInlineConverter:
    def __init__(self: "MergeableInlineConverter") -> None:
        pass

    def convert(self: "MergeableInlineConverter", context: Context, target: List[Any]) -> List[Any]:
        merged_text, child_text_spans = self.__flatten_inlines(target)
        log.debug("Processing text: %r", merged_text)

        for word in context.glossary:
            haystack_text: str = (
                merged_text if context.is_case_sensitive else merged_text.lower()
            )
            needle_text: str = (
                word.name if context.is_case_sensitive else word.name.lower()
            )

            # context.glossary is sorted longest-name-first, so the first hit found here is the longest match
            match_start_offset: int = find_whole_word(haystack_text, needle_text)
            if match_start_offset == -1:
                continue
            match_end_offset: int = match_start_offset + len(word.name)
            log.debug("Matched word: %r -> %r", merged_text, word.name)

            before_children, matched_children, after_children = self.__split_inlines_at(
                target, child_text_spans, match_start_offset, match_end_offset
            )
            glossary_link: Any = make_glossary_link(context, word, matched_children)

            # recurse on both sides, since more glossary words may still appear before or after this match
            return (
                self.convert(context, before_children)
                + [glossary_link]
                + self.convert(context, after_children)
            )

        log.debug("No match found for text: %r", merged_text)
        return target

    def __flatten_inlines(
        self: "MergeableInlineConverter", inline_children: List[Any]
    ) -> Tuple[str, List[Tuple[int, int]]]:
        merged_text: str = ""
        child_text_spans: List[Tuple[int, int]] = []
        for child in inline_children:
            # Space and SoftBreak carry no text of their own, they always render as a single space character
            child_text: str = child[0] if isinstance(child, Str) else " "
            child_text_spans.append(
                (len(merged_text), len(merged_text) + len(child_text))
            )
            merged_text += child_text
        return merged_text, child_text_spans

    def __split_inlines_at(
        self: "MergeableInlineConverter",
        inline_children: List[Any],
        child_text_spans: List[Tuple[int, int]],
        match_start_offset: int,
        match_end_offset: int,
    ) -> Tuple[List[Any], List[Any], List[Any]]:
        before_children: List[Any] = []
        matched_children: List[Any] = []
        after_children: List[Any] = []

        for child, (child_start_offset, child_end_offset) in zip(
            inline_children, child_text_spans
        ):
            # child entirely precedes the match, keep it untouched on the left side
            if child_end_offset <= match_start_offset:
                before_children.append(child)
            # child entirely follows the match, keep it untouched on the right side
            elif child_start_offset >= match_end_offset:
                after_children.append(child)
            elif isinstance(child, Str):
                # only a Str child can be partially covered by the match, Space/SoftBreak are a single character
                child_text: str = child[0]
                local_start_offset: int = max(0, match_start_offset - child_start_offset)
                local_end_offset: int = min(
                    len(child_text), match_end_offset - child_start_offset
                )
                if local_start_offset > 0:
                    before_children.append(Str(child_text[:local_start_offset]))
                matched_children.append(
                    Str(child_text[local_start_offset:local_end_offset])
                )
                if local_end_offset < len(child_text):
                    after_children.append(Str(child_text[local_end_offset:]))
            else:
                # fully covered by the match (e.g. a Space/SoftBreak between two matched words)
                matched_children.append(child)

        return before_children, matched_children, after_children


mergeable_inline_converter = MergeableInlineConverter()
