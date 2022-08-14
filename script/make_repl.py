import json
import sys
from itertools import groupby


IN = ">>> "
IN2 = "... "
EMPTYLINE = "\n"


def handle_output(output: dict) -> str:
    res = []
    if output["output_type"] == "execute_result":
        res = output["data"]["text/plain"]
    elif output["output_type"] == "stream":
        res = output["text"]

    return "".join(res) + "\n"


def handle_source(source: dict) -> str:
    res = []
    for is_key, group in groupby(source, lambda x: x != EMPTYLINE):
        if is_key:
            for i, block in enumerate(group):
                if (
                    i == 0
                    or block.startswith("import")
                    or (block.startswith("from") and "import" in block)
                ):
                    res.append(IN + block)
                else:
                    res.append(IN2 + block)

    return "".join(res) + "\n"


if __name__ == "__main__":
    # 1. python make_nb.py example.py
    # 2. jupyter nbconvert --to notebook --execute example.ipynb
    # 3. python make_repl.py example.nbconvert.ipynb

    with open(sys.argv[1], "r") as fr, open(
        f"{sys.argv[1].split('.')[0]}.repl.py", "w"
    ) as fw:
        nb_json = json.loads(fr.read())
        for cell in nb_json["cells"]:
            if cell["cell_type"] == "code":

                # handle source
                fw.write(handle_source(cell["source"]))

                # handle outputs
                fw.write("".join(handle_output(output) for output in cell["outputs"]))
