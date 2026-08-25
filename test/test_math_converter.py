import unittest

import pandoc
import mkdocs_glossary_plugin.converter  # noqa: F401
from mkdocs_glossary_plugin.converter.BaseConverter import Context, Word
from mkdocs_glossary_plugin.converter.DisplayMathConverter import DisplayMathConverter
from mkdocs_glossary_plugin.converter.InlineMathConverter import InlineMathConverter
from mkdocs_glossary_plugin.converter.PandocConverter import PandocConverter
from pandoc.types import DisplayMath, InlineMath, Link, Math


class TestMathConverters(unittest.TestCase):
    def setUp(self) -> None:
        self.context = Context(
            {
                "is_case_sensitive": True,
                "enable_toc": True,
                "replace_emphasized_text": True,
                "replace_header": True,
                "replace_table_header": True,
                "replace_table_body": True,
            },
            [Word("test", "/docs/foo/test.md")],
            "/docs",
        )

    def test_display_math_type_converter_returns_target(self) -> None:
        target = DisplayMath()
        converted = DisplayMathConverter().convert(self.context, target)
        self.assertIs(target, converted[0])

    def test_inline_math_type_converter_returns_target(self) -> None:
        target = InlineMath()
        converted = InlineMathConverter().convert(self.context, target)
        self.assertIs(target, converted[0])

    def test_math_converter_keeps_math_text_unlinked(self) -> None:
        doc = pandoc.read(
            "test $$test$$ after\n\n$$\ntest\n$$\n",
            format="markdown_phpextra+tex_math_dollars",
        )

        converted = PandocConverter().convert(self.context, doc)[0]
        first_para = converted[1][0]
        second_para = converted[1][1]

        self.assertIsInstance(first_para[0][0], Link)
        self.assertIsInstance(first_para[0][2], Math)
        self.assertEqual(first_para[0][2][1], "test")
        self.assertIsInstance(second_para[0][0], Math)
        self.assertEqual(second_para[0][0][1], "\ntest\n")


if __name__ == "__main__":
    unittest.main()
