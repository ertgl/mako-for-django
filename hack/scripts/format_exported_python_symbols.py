# MIT License
#
# Copyright (c) 2024 Ertuğrul Keremoğlu <ertugkeremoglu@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Source: https://gist.github.com/ertgl/b675bdc97e2396f0eb8cf8a226e33e65

__all__ = ["main"]

import operator
import re
import sys

from contextlib import suppress
from pathlib import Path
from typing import (
    Iterable,
    TextIO,
    cast,
)


WORK_DIR = Path.cwd()

VENV_DIR_NAME = ".venv"

VENV_DIR_SEGMENT_REGEX_PATTERN = rf"[\\/]{re.escape(VENV_DIR_NAME)}[\\/]"

VENV_DIR_SEGMENT_REGEX = re.compile(
    VENV_DIR_SEGMENT_REGEX_PATTERN,
    re.IGNORECASE | re.UNICODE,
)


def read(buffer: TextIO) -> str:
    return buffer.read()


def get_export_expression_span(
    source: str,
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    line_no = 1
    column_no = 0
    start_line_no = -1
    start_column_no = -1
    start_offset = -1
    end_line_no = -1
    end_column_no = -1
    end_offset = -1
    lookbehind: list[tuple[tuple[int, int, int], str]] = []
    prefix = "__all__=["
    prefix_chars = list(prefix)
    for char_index, char in cast(Iterable[tuple[int, str]], enumerate(source)):
        if char == "\n":
            line_no += 1
            column_no = 0
        else:
            column_no += 1
        if start_offset == -1:
            if not (char.isspace() or char == "\\"):
                lookbehind.append(((line_no, column_no, char_index), char))
                if len(lookbehind) > len(prefix_chars):
                    lookbehind.pop(0)
            if len(lookbehind) > 0:
                lookbehind_value = list(map(operator.itemgetter(1), lookbehind))
                found_prefix = lookbehind_value == prefix_chars
                is_prefix_at_start = lookbehind[0][0][1] == 1
                if found_prefix and is_prefix_at_start:
                    lookbehind.clear()
                    start_line_no = line_no
                    start_column_no = column_no
                    start_offset = char_index
        if start_offset != -1 and char == "]":
            end_line_no = line_no
            end_column_no = column_no
            end_offset = char_index
            break
    start = start_line_no, start_column_no, start_offset
    end = end_line_no, end_column_no, end_offset
    return start, end


def collect_existing_exported_symbols(source: str) -> set[tuple[int, str]]:
    existing_exported_symbols: set[tuple[int, str]] = set()
    start, end = get_export_expression_span(source)
    if start[2] == -1 or end[2] == -1:
        return existing_exported_symbols
    lines = source[start[2] + 1 : end[2]].split("\n")
    for line_no, line in enumerate(lines):
        for raw_string in line.split(","):
            symbol_line_no = start[0] + line_no
            symbol_name = raw_string.strip()[1:-1].strip()
            if not symbol_name:
                continue
            symbol = (symbol_line_no, symbol_name)
            existing_exported_symbols.add(symbol)
    return existing_exported_symbols


def collect_imported_symbols(source: str) -> set[tuple[int, str]]:
    imported_symbols: set[tuple[int, str]] = set()
    lines = list(map(lambda line: line.strip(), source.split("\n")))
    for line_no, line in enumerate(lines):
        if line.startswith("from"):
            parts = line.split(" ", maxsplit=3)
            if len(parts) != 4:
                continue
            if parts[2] != "import":
                continue
            if parts[-1] == "(":
                index_of_tuple_end = line_no + lines[line_no:].index(")")
                section = "\n".join(lines[line_no + 1 : index_of_tuple_end])
                symbol_names = [
                    symbol_name.strip()
                    for symbol_name in section.split(",")
                    if symbol_name.strip()
                ]
                for symbol_name_index, symbol_name in enumerate(symbol_names):
                    symbol = (line_no + symbol_name_index + 1, symbol_name)
                    imported_symbols.add(symbol)
            elif "," in parts[-1]:
                symbol_names = [
                    symbol_name.strip()
                    for symbol_name in parts[-1].split(",")
                    if symbol_name.strip()
                ]
                for symbol_name_index, symbol_name in enumerate(symbol_names):
                    symbol = (line_no + symbol_name_index + 1, symbol_name)
                    imported_symbols.add(symbol)
            else:
                symbol = (line_no, parts[-1])
                imported_symbols.add(symbol)
    return imported_symbols


def replace_exported_symbols(
    source: str,
    start: tuple[int, int, int],
    end: tuple[int, int, int],
    symbols: set[tuple[int, str]],
) -> str:
    exported_symbols = sorted(set(map(operator.itemgetter(1), symbols)))
    prefix = ""
    suffix = ""
    indent = ""
    if len(exported_symbols) > 1:
        prefix = "\n"
        suffix = ",\n"
        indent = "    "
    inner = ",\n".join(
        [f'{indent}"{symbol}"' for symbol in exported_symbols],
    )
    rendered = f"{prefix}{inner}{suffix}"
    source_chars = list(source)
    source_chars[start[2] + 1 : end[2]] = list(rendered)
    code = "".join(source_chars)
    return code


def write(
    buffer: TextIO,
    output: str,
) -> None:
    buffer.write(output)
    buffer.flush()


def process_stdin(argv: list[str]) -> int:
    source = read(sys.stdin)
    start, end = get_export_expression_span(source)
    if -1 in (start[2], end[2]):
        write(sys.stdout, source)
        return -1
    existing_exported_symbols = collect_existing_exported_symbols(source)
    imported_symbols: set[tuple[int, str]]
    if "-export-all" in argv:
        imported_symbols = collect_imported_symbols(source)
    else:
        imported_symbols = set()
    output = replace_exported_symbols(
        source,
        start,
        end,
        existing_exported_symbols.union(
            imported_symbols,
        ),
    )
    try:
        write(sys.stdout, output)
    except Exception as error:
        write(sys.stderr, f"{str(error)}\n")
        with suppress(Exception):
            write(sys.stdout, source)
        return 1
    return 0


def process_source_file(source_file_path: Path) -> int:
    source = source_file_path.read_text()
    start, end = get_export_expression_span(source)
    if -1 in (start[2], end[2]):
        return -1
    existing_exported_symbols = collect_existing_exported_symbols(source)
    imported_symbols: set[tuple[int, str]]
    if source_file_path.name == "__init__.py":
        imported_symbols = collect_imported_symbols(source)
    else:
        imported_symbols = set()
    output = replace_exported_symbols(
        source,
        start,
        end,
        existing_exported_symbols.union(
            imported_symbols,
        ),
    )
    try:
        with source_file_path.open("w") as source_file:
            write(source_file, output)
    except Exception as error:
        write(sys.stderr, f"{str(error)}\n")
        with suppress(Exception):
            with source_file_path.open("w") as source_file:
                write(source_file, source)
        return 1
    return 0


def process_source_files() -> int:
    reformatted: set[str] = set()
    unchanged: set[str] = set()
    errored: set[str] = set()
    ignored: set[str] = set()

    for source_file_path in WORK_DIR.rglob("*.py"):
        source_file_path_str = str(source_file_path)
        relative_file_path = source_file_path.relative_to(WORK_DIR)
        relative_file_path_str = str(relative_file_path)
        if VENV_DIR_SEGMENT_REGEX.search(source_file_path_str):
            ignored.add(relative_file_path_str)
            continue
        status = process_source_file(source_file_path)
        if status == -1:
            unchanged.add(relative_file_path_str)
        elif status != 0:
            errored.add(relative_file_path_str)
        else:
            reformatted.add(relative_file_path_str)

    output = ""
    sep = ""
    if len(reformatted) == 1:
        output += "1 file reformatted"
        sep = ", "
    elif len(reformatted) > 1:
        output += f"{len(reformatted)!s} files reformatted"
        sep = ", "
    if len(unchanged) == 1:
        output += f"{sep}1 file left unchanged"
        sep = ", "
    elif len(unchanged) > 1:
        output += f"{sep}{len(unchanged)!s} files left unchanged"
        sep = ", "
    if len(errored) == 1:
        output += f"{sep}1 file errored"
        sep = ", "
    elif len(errored) > 1:
        output += f"{sep}{len(errored)!s} files errored"
        sep = ", "
    if len(ignored) == 1:
        output += f"{sep}1 file ignored"
    elif len(ignored) > 1:
        output += f"{sep}{len(ignored)!s} files ignored"

    if not output:
        output = f"{len(unchanged)!s} files left unchanged"

    write(sys.stderr, f"{output}\n")

    if errored:
        return 1

    return 0


def main(
    argv: list[str] | None = None,
) -> int:
    if argv is None:
        argv = sys.argv.copy()
    if "-stdin" in argv:
        return process_stdin(argv)
    return process_source_files()


if __name__ == "__main__":
    sys.exit(main(argv=sys.argv.copy()))
