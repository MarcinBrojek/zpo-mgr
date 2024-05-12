from pathlib import Path
from lark import Lark
from src.interpreter import Interpreter
from src.transformer import OptimusPirme
from io import StringIO
import sys


GRAMMAR_PATH = Path(__file__).parent / "src/grammar.lark"

EMPTY_DATA_RESET = {"start_gamma": dict(), "start_store": dict(), "reset_program_state": True}
EMPTY_DATA_NO_RESET = {"start_gamma": dict(), "start_store": dict(), "reset_program_state": False}

TESTS = [
    {"name": "original_02.txt", "data": EMPTY_DATA_RESET},
    {"name": "original_02.txt", "data": EMPTY_DATA_NO_RESET},

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
    {"name": "test_21.txt", "data": EMPTY_DATA_NO_RESET},
]


# https://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue())
        del self._stringio
        sys.stdout = self._stdout


def main():
    test_name, data = None, None
    try:
        for test in TESTS:
            test_name, data = test["name"], test["data"]
            test_path = Path(__file__).parent / "programs" / test_name
            with open(GRAMMAR_PATH, "r") as grammar_file, open(test_path, "r") as input_code_file, Capturing() as output:

                grammar_text = grammar_file.read()
                input_code = input_code_file.read()
                parser = Lark(grammar=grammar_text, start="p", parser="earley")

                tree = parser.parse(input_code)
                optimused_tree = OptimusPirme().transform(tree)
                Interpreter(data=data).run(optimused_tree)

                grammar_file.close()
                input_code_file.close()
            
            print(f"{test_name} OK")

    except Exception as e:
        print(f"{test_name} BAD")
        output = ''.join(output)
        print(output) # output contain last output - error
        raise e # stop testing at first error

    print("all tests passed!")


if __name__ == "__main__":
    main()