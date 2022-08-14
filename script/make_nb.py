"""
Create a notebook containing code from a script.

Based on https://github.com/williamjameshandley/py2nb/blob/master/py2nb
"""

import argparse
import os

import nbformat
from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


MARKDOWN_CHARS = ["#|", "# |"]
ACCEPTED_CHARS = ["#-", "# -", *MARKDOWN_CHARS]


def new_cell(nb: NotebookNode, cell: str, markdown: bool = False) -> str:
    """
    Create a new cell

    Parameters
    ----------
    nb: NotebookNode
        Notebook to write to, as produced by nbformat.v4.new_notebook()

    cell: str
        String to write to the cell

    markdown: bool, default False
        Whether to create a markdown cell, or a code cell

    Returns
    -------
    empty string
    """

    if cell := cell.rstrip().lstrip():
        cell = new_markdown_cell(cell) if markdown else new_code_cell(cell)
        nb.cells.append(cell)

    return ""


def str_starts_with(string, options) -> bool:
    return any(string.startswith(opt) for opt in options)


def convert(script_name):
    """Convert the python script to jupyter notebook"""

    with open(script_name) as f:
        markdown_cell = code_cell = ""
        nb = new_notebook()
        for line in f:
            if str_starts_with(line, ACCEPTED_CHARS):
                code_cell = new_cell(nb, code_cell)
                if str_starts_with(line, MARKDOWN_CHARS):
                    # find the first occurence of |
                    # and add the rest of the line to the markdown cell
                    markdown_cell += line[line.index("|") + 1 :]
                else:
                    markdown_cell = new_cell(nb, markdown_cell, markdown=True)
            else:
                markdown_cell = new_cell(nb, markdown_cell, markdown=True)
                code_cell += line

        markdown_cell = new_cell(nb, markdown_cell, markdown=True)
        code_cell = new_cell(nb, code_cell)

        notebook_name = f"{os.path.splitext(script_name)[0]}.ipynb"
        nbformat.write(nb, notebook_name)


def parse_args():
    """Argument parsing for py2nb"""

    parser = argparse.ArgumentParser(
        description="Convert a python script to a jupyter notebook"
    )
    parser.add_argument(
        "script_name",
        help="name of script (.py) to convert to jupyter notebook (.ipynb)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    convert(args.script_name)
