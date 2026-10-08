from typing import Any, List, Dict, Tuple

from .Context import Context, Word
from .MergeableInlineConverter import is_mergeable_inline, mergeable_inline_converter


class BaseConverter:
    CONVERTER_TABLE: dict = {}
    support_flatten_conversion: bool = False

    def __init__(self: "BaseConverter") -> None:
        pass

    def convert(self: "BaseConverter", context: Context, target: Any) -> List[Any]:
        if self.support_flatten_conversion:
            return self.__convert_flattened(context, target)
        return self.__convert_default(context, target)

    def __convert_default(self: "BaseConverter", context: Context, target: Any) -> List[Any]:
        converted_list: List[Tuple[int, List[Any]]] = []

        for child_index, child in enumerate(target):
            if child is None:
                continue
            converted: List[Any] = CONVERTER_TABLE[type(child)].convert(context, child)
            if len(converted) == 1 and child == converted[0]:
                continue
            converted_list.append((child_index, converted))

        for child_index, converted in reversed(converted_list):
            target[child_index] = converted[0]
            target[child_index + 1 : child_index + 1] = converted[1:]

        return [target]

    def __convert_flattened(self: "BaseConverter", context: Context, target: Any) -> List[Any]:
        # a pandoc node with a single [Inline] field exposes it as one list argument, not as individual siblings
        for argument in target:
            if isinstance(argument, list):
                self.__convert_inline_run(context, argument)

        return [target]

    def __convert_inline_run(self: "BaseConverter", context: Context, inline_children: List[Any]) -> None:
        splices: List[Tuple[int, int, List[Any]]] = []
        mergeable_run: List[Any] = []
        mergeable_run_start_index: int = 0

        for child_index, child in enumerate(inline_children):
            # buffer consecutive Str/Space/SoftBreak children so glossary words containing spaces can be matched
            if is_mergeable_inline(context, child):
                if not mergeable_run:
                    mergeable_run_start_index = child_index
                mergeable_run.append(child)
                continue
            self.__flush_mergeable_run(
                context, mergeable_run, mergeable_run_start_index, child_index, splices
            )

            converted_child: List[Any] = CONVERTER_TABLE[type(child)].convert(context, child)
            if len(converted_child) == 1 and child == converted_child[0]:
                continue
            splices.append((child_index, child_index + 1, converted_child))

        self.__flush_mergeable_run(
            context, mergeable_run, mergeable_run_start_index, len(inline_children), splices
        )

        for start_index, end_index, converted in reversed(splices):
            inline_children[start_index:end_index] = converted

    def __flush_mergeable_run(
        self: "BaseConverter",
        context: Context,
        mergeable_run: List[Any],
        mergeable_run_start_index: int,
        mergeable_run_end_index: int,
        splices: List[Tuple[int, int, List[Any]]],
    ) -> None:
        if mergeable_run:
            converted_run: List[Any] = mergeable_inline_converter.convert(context, list(mergeable_run))
            if converted_run != mergeable_run:
                splices.append((mergeable_run_start_index, mergeable_run_end_index, converted_run))
            mergeable_run.clear()


CONVERTER_TABLE: Dict[Any, BaseConverter] = {}
