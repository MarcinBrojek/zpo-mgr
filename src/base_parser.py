from pathlib import Path
from lark import Lark

BASE_GRAMMAR_PATH = Path(__file__).parent / "base_grammar.lark"
BASE_TRANSFORMER_PATH = Path(__file__).parent / "base_transformer.txt"


def import_class(mod, component):
    mod = __import__(mod, fromlist=[None])
    return getattr(mod, component)


class BaseParser:
    def __init__(
        self, grammar_path=BASE_GRAMMAR_PATH, tranformer_path=BASE_TRANSFORMER_PATH
    ):
        self.base_grammar_txt = open(grammar_path).read()
        self.base_tranformer_txt = open(tranformer_path).read()
        self.rs_all = list()
        self.need_update = True
        self.start = str("# No start at the beggining")

    def update_rs_all(self, rs_all):
        if rs_all != self.rs_all:
            self.rs_all = rs_all
            self.need_update = True

    def run(self, start, input_txt):

        if self.need_update:

            grammar_txt = self.base_grammar_txt
            known_ntm = []
            for rs in self.rs_all:
                if rs.id not in known_ntm:
                    grammar_txt += f"{rs.id}: var{rs.id}\n" # name var{rs.id} should be unique
                    grammar_txt += f'var{rs.id}: "@" ' + r"/" + rs.id + r"/" + r" [/_\w+/]" + "\n"
                    known_ntm.append(rs.id)

                rule_txt = ""
                for option in rs.inneroptions:
                    rule_txt += "| "
                    for el in option:
                        rule_txt += el + " "
                grammar_txt += f"%extend {rs.id}.{rs.number or 0} : " + rule_txt[2:] + "\n"

            tranformer_txt = self.base_tranformer_txt
            for ntm in known_ntm:
                tranformer_txt += f"\n    def {ntm}(self, c):\n" + f"        return (\"{ntm}\", Var(c[0].ntm, c[0].id) if (len(c) == 1) and isinstance(c[0], Var) and (c[0].to_correct == 1) else [el if not isinstance(el, Token) else el.value for el in c])\n"
                tranformer_txt += f"\n    def var{ntm}(self, c):\n" + f"        return Var(str(c[0]), (c[1] or \"\")[1:], 1)\n" # c[1] can be None (id)

            with open("tmp/tmp_transformer.py", "w") as tmp_transformer_import:
                tmp_transformer_import.write(tranformer_txt)
                tmp_transformer_import.close()

            self.grammar_txt = grammar_txt
            self.parser = Lark(grammar=grammar_txt, start=start, parser="earley")

        elif self.start != start:
            self.parser = Lark(grammar=self.grammar_txt, start=start, parser="earley")

        # print("GRAMMAR", grammar_txt)
        # print(tranformer_txt)
        self.need_update = False
        self.start = start
        
        tree = self.parser.parse(input_txt)
        self.OptimusPirme = import_class("tmp.tmp_transformer", "OptimusPirme")

        return self.OptimusPirme(visit_tokens=True).transform(tree)
