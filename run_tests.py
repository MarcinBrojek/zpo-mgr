from pathlib import Path
from lark import Lark
from src.interpreter import Interpreter
from src.transformer import OptimusPirme


GRAMMAR_PATH = Path(__file__).parent / "src/grammar.lark"


TESTS = [
    "test_01.txt",
    "test_02.txt",
    "test_03.txt",
    "test_04.txt",
    "test_07.txt",
    "test_08.txt",
    "test_11.txt",
    "test_12.txt",
    "test_13.txt",
]


def main():

    data = {"start_gamma": dict(), "start_store": dict(), "reset_program_state": False}
    for test in TESTS:
        test_path = Path(__file__).parent / "programs" / test
        with open(GRAMMAR_PATH, "r") as grammar_file, open(test_path, "r") as input_code_file:

            grammar_text = grammar_file.read()
            input_code = input_code_file.read()
            parser = Lark(grammar=grammar_text, start="p", parser="earley")

            tree = parser.parse(input_code)
            optimused_tree = OptimusPirme().transform(tree)
            Interpreter(data=data).run(optimused_tree)

            grammar_file.close()
            input_code_file.close()


if __name__ == "__main__":
    main()