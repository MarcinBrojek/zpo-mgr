import argparse
from pathlib import Path
from lark import Lark
from src.transformer import OptimusPirme
from src.interpreter import Interpreter
from src.converter import gen_tex
from debugger.debugger import Debugger
import curses


GRAMMAR_PATH = Path(__file__).parent / "src/grammar.lark"


def main(stdscr=None, args=None):
    with open(GRAMMAR_PATH, "r") as grammar_file, open(args.code_path, "r") as input_code_file:
        
        grammar_text = grammar_file.read()
        input_code = input_code_file.read()
        parser = Lark(grammar=grammar_text, start="p", parser="earley")

        tree = parser.parse(input_code)
        optimused_tree = OptimusPirme().transform(tree)

        # print(str(optimused_tree))

        debugger = Debugger(stdscr=stdscr, debug=args.debug)

        interpreter = Interpreter(debugger=debugger)

        interpreter.run(optimused_tree)

        # print(optimused_tree)

        # gen_tex(optimused_tree)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("code_path", help="Code file with path")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    if args.debug:
        curses.wrapper(main, args)
    else:
        main(None, args)
