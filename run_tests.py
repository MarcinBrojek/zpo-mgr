from pathlib import Path
from lark import Lark
from src.interpreter import Interpreter
from src.transformer import OptimusPirme


GRAMMAR_PATH = Path(__file__).parent / "src/grammar.lark"

EMPTY_DATA_RESET = {"start_gamma": dict(), "start_store": dict(), "reset_program_state": True}
EMPTY_DATA_NO_RESET = {"start_gamma": dict(), "start_store": dict(), "reset_program_state": False}

TESTS = [
    {"name": "test_01.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_02.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_03.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_04.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_07.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_08.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_11.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_12.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_13.txt", "data": EMPTY_DATA_RESET},
    {"name": "test_20.txt", "data": EMPTY_DATA_NO_RESET},
]


def main():
    for test in TESTS:
        test_name, data = test["name"], test["data"]
        test_path = Path(__file__).parent / "programs" / test_name
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