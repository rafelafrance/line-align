#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

from line_align.pylib import char_sub_matrix as matrix


def main():
    args = parse_args()
    matrix.add_chars(
        args.char_set, args.new_chars, args.image_size, args.font_path, args.font_size
    )


def parse_args() -> argparse.Namespace:
    description = """Add characters to the Line Align utility's character substitution
        matrix. The matrix has the characters along the row and column headers and
        each cell value has a value that is a coarse approximation of how visually
        similar the two characters are."""

    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--char-set",
        default="default",
        metavar="NAME",
        help="""Update this character set matrix. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--new-chars",
        default=matrix.CHARS,
        metavar="CHARS",
        help="""A string containing the characters to add to the matrix. Characters
            here will replace those in the char-set. Default includes a space and
            a newline. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--font-path",
        type=Path,
        metavar="PATH",
        help="""A true type font file to use for calculations.
            (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--font-size",
        type=int,
        metavar="SIZE",
        default=matrix.DEFAULT_FONT_SIZE,
        help="""
            The font size in pixels to use for calculations. (default: %(default)s)""",
    )

    arg_parser.add_argument(
        "--image-size",
        type=int,
        metavar="SIZE",
        default=matrix.DEFAULT_IMAGE_SIZE,
        help="""Size of the image that contains a char. (default: %(default)s)""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
