import sys
from pathlib import Path
from lark import Lark
from transformer import OptimusPirme
from interpreter import Interpreter

GRAMMAR_PATH = Path(__file__).parent / "grammar.lark"


def main(argv):
    input_code_path = argv[0]
    with open(GRAMMAR_PATH, "r") as grammar_file, open(
        input_code_path, "r"
    ) as input_code_file:
        grammar_text = grammar_file.read()
        input_code = input_code_file.read()
        parser = Lark(grammar=grammar_text, start="p", parser="earley")
        tree = parser.parse(input_code)
        optimused_tree = OptimusPirme().transform(tree)
        # print(str(optimused_tree))

        interpreter = Interpreter()
        interpreter.run(optimused_tree)
        # print(optimused_tree)


if __name__ == "__main__":
    main(sys.argv[1:])
