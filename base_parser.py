from pathlib import Path
from lark import Lark

BASE_GRAMMAR_PATH = Path(__file__).parent / "base_grammar.lark"
BASE_TRANSFORMER_PATH = Path(__file__).parent / "base_transformer.txt"


def my_import(name):
    components = name.split(".")
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


class BaseParser:
    def __init__(
        self, grammar_path=BASE_GRAMMAR_PATH, tranformer_path=BASE_TRANSFORMER_PATH
    ):
        self.base_grammar_txt = open(grammar_path).read()
        self.base_tranformer_txt = open(tranformer_path).read()
        self.rs_all = list()

    def update_rs_all(self, rs_all):
        self.rs_all = rs_all

    def run(self, start, input_txt):
        grammar_txt = self.base_grammar_txt
        known_ntm = []
        # print(self.rs_all)
        for rs in self.rs_all:
            if rs.id not in known_ntm:
                grammar_txt += f"{rs.id}: var{rs.id}\n" # name var{rs.id} should be unique
                grammar_txt += f'var{rs.id}: "@" ' + r"/[a-zA-Z]+/ [/_\w+/]" + "\n"
                known_ntm.append(rs.id)

            rule_txt = ""
            for option in rs.inneroptions:
                rule_txt += "| "
                for el in option:
                    rule_txt += el + " "
            grammar_txt += f"%extend {rs.id}.{rs.number or 0} : " + rule_txt[2:] + "\n"

        # print("GRAMMAR", grammar_txt)
        parser = Lark(grammar=grammar_txt, start=start, parser="earley")
        tree = parser.parse(input_txt)

        tranformer_txt = self.base_tranformer_txt
        for ntm in known_ntm:
            tranformer_txt += f"\n    def {ntm}(self, c):\n" + f"        res = [el if not isinstance(el, Token) else el.value for el in c]\n" + f"        return Var(res[0].ntm, res[0].id) if (len(res)) == 1 and isinstance(res[0], Var) and (res[0].to_correct == 1) else res\n"
            tranformer_txt += f"\n    def var{ntm}(self, c):\n" + f"        return Var(c[0], (c[1] or \"\")[1:], 1)\n" # c[1] can be None (id)

        with open("tmp_transformer.py", "w") as tmp_transformer_import:
            tmp_transformer_import.write(tranformer_txt)

        OptimusPirme = my_import("tmp_transformer.OptimusPirme")

        # print(tranformer_txt)
        return OptimusPirme(visit_tokens=True).transform(tree)
