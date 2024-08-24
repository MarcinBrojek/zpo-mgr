from pathlib import Path
from lark import Lark
from src.interpreter import Interpreter
from src.transformer import OptimusPirme
from io import StringIO
import sys


GRAMMAR_PATH = Path(__file__).parent / "src/grammar.lark"

EMPTY_DATA_RESET = {
    "start_gamma": dict(),
    "start_store": dict(),
    "reset_program_state": True,
    "unit_nonterminal": "sp",
    "unit_name": "unit"
}

EMPTY_DATA_NO_RESET = {
    "start_gamma": dict(),
    "start_store": dict(),
    "reset_program_state": False,
    "unit_nonterminal": "sp",
    "unit_name": "unit"
}

TESTS = [
    {
        "name": "original_02-EMPTY_DATA_RESET",
        "program": "original_02.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "original_02-EMPTY_DATA_NO_RESET",
        "program": "original_02.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "test_01-EMPTY_DATA_RESET",
        "program": "test_01.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, 3],
    },
    {
        "name": "test_01-EMPTY_DATA_NO_RESET",
        "program": "test_01.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, 7],
    },
    {
        "name": "test_02-EMPTY_DATA_RESET",
        "program": "test_02.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "test_02-EMPTY_DATA_NO_RESET",
        "program": "test_02.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "test_03-EMPTY_DATA_RESET",
        "program": "test_03.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, '"23"'],
    },
    {
        "name": "test_03-EMPTY_DATA_NO_RESET",
        "program": "test_03.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{},  '"23"'],
    },
    {
        "name": "test_04-EMPTY_DATA_RESET",
        "program": "test_04.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, {"cnt": 1}],
    },
    {
        "name": "test_04-EMPTY_DATA_NO_RESET",
        "program": "test_04.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, {"cnt": 3}],
    },
    {
        "name": "test_05-EMPTY_DATA_NO_RESET",
        "program": "test_05.txt",
        "data": EMPTY_DATA_NO_RESET,
        "error": "Max steps exceed"
    },
    {
        "name": "test_06-EMPTY_DATA_NO_RESET",
        "program": "test_06.txt",
        "data": EMPTY_DATA_NO_RESET,
        "error": "Max steps exceed"
    },
    {
        "name": "test_07-EMPTY_DATA_RESET",
        "program": "test_07.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "test_07-EMPTY_DATA_NO_RESET",
        "program": "test_07.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "test_08-EMPTY_DATA_RESET",
        "program": "test_08.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{'z': 'int'}, {"z": 0}],
    },
    {
        "name": "test_08-EMPTY_DATA_NO_RESET",
        "program": "test_08.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{"z": "int", "y": "int"}, {"z": 0, "y": 3}],
    },
    {
        "name": "test_09-EMPTY_DATA_NO_RESET",
        "program": "test_09.txt",
        "data": EMPTY_DATA_NO_RESET,
        "error": "Max depth exceed"
    },
    {
        "name": "test_10-EMPTY_DATA_NO_RESET",
        "program": "test_10.txt",
        "data": EMPTY_DATA_NO_RESET,
        "error": "Max depth exceed"
    },
    {
        "name": "test_11-EMPTY_DATA_RESET",
        "program": "test_11.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, 3],
    },
    {
        "name": "test_11-EMPTY_DATA_NO_RESET",
        "program": "test_11.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, 7],
    },
    {
        "name": "test_12-EMPTY_DATA_RESET",
        "program": "test_12.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "test_12-EMPTY_DATA_NO_RESET",
        "program": "test_12.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, {}],
    },
    {
        "name": "test_13-EMPTY_DATA_RESET",
        "program": "test_13.txt",
        "data": EMPTY_DATA_RESET,
        "last_final_state": [{}, 23],
    },
    {
        "name": "test_13-EMPTY_DATA_NO_RESET",
        "program": "test_13.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [{}, 23],
    },
    {
        "name": "test_20-EMPTY_DATA_NO_RESET",
        "program": "test_20.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [2, {'transitions': [('c', '1', 'a'), ('a', '0', 'c')], 'accept_states': ['a', 'b'], 'current_state': 'a'}],
    },
    {
        "name": "test_21-EMPTY_DATA_NO_RESET",
        "program": "test_21.txt",
        "data": EMPTY_DATA_NO_RESET,
        "last_final_state": [[{'y': 'T', 'x': 'F'}, {'y': 'T', 'x': 'F', 'z': 'F'}], {'y': 'T', 'x': 'F', 'z': 'F'}],
    },
    {
        "name": "test_22-EMPTY_DATA_RESET",
        "program": "test_22.txt",
        "data": {
            "start_gamma": dict(),
            "start_store": dict(),
            "reset_program_state": True,
            "unit_nonterminal": "t",
            "unit_name": "unit"
        },
        "last_final_state": [{}, 4]
    },
    {
        "name": "test_22-EMPTY_DATA_NO_RESET",
        "program": "test_22.txt",
        "data": {
            "start_gamma": dict(),
            "start_store": dict(),
            "reset_program_state": False,
            "unit_nonterminal": "t",
            "unit_name": "unit"
        },
        "last_final_state": [{}, 4]
    },
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
    for test in TESTS:
        try:
            test_name, program_name, data = test["name"], test["program"], test["data"]
            test_path = Path(__file__).parent / "programs" / program_name

            print(f"{test_name} ", end='')

            with open(GRAMMAR_PATH, "r") as grammar_file, open(test_path, "r") as input_code_file, Capturing() as output:

                grammar_text = grammar_file.read()
                input_code = input_code_file.read()
                parser = Lark(grammar=grammar_text, start="p", parser="earley")

                tree = parser.parse(input_code)
                optimused_tree = OptimusPirme().transform(tree)

                interpreter = Interpreter(data=data)
                interpreter.run(optimused_tree)

                if interpreter.state.program_state != test["last_final_state"]:
                    raise Exception("incorrect final state: ", str(
                        interpreter.state.program_state))

                grammar_file.close()
                input_code_file.close()

            print("OK")

        except Exception as e:

            if ("error" in test) and (test["error"] == str(e)):
                print("OK")

            else:
                print("BAD")
                output = ''.join(output)

                print("\n____________OUTPUT______________\n")
                print(output)  # output contain last output - error

                print("\n____________ERROR_______________\n")
                raise e  # stop testing at first error

    print("all tests passed!")


if __name__ == "__main__":
    main()
