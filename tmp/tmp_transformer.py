from lark import Token, Transformer
from classes import Var

class OptimusPirme(Transformer):
    def ID(self, c):
        return str(c)

    def STR(self, c):
        return str(c)

    def I(self, c):
        return int(c)

    
    def sp(self, c):
        return ("sp", Var(c[0].ntm, c[0].id) if (len(c) == 1) and isinstance(c[0], Var) and (c[0].to_correct == 1) else [el if not isinstance(el, Token) else el.value for el in c])

    def varsp(self, c):
        return Var(c[0], (c[1] or "")[1:], 1)

    def e(self, c):
        return ("e", Var(c[0].ntm, c[0].id) if (len(c) == 1) and isinstance(c[0], Var) and (c[0].to_correct == 1) else [el if not isinstance(el, Token) else el.value for el in c])

    def vare(self, c):
        return Var(c[0], (c[1] or "")[1:], 1)

    def t(self, c):
        return ("t", Var(c[0].ntm, c[0].id) if (len(c) == 1) and isinstance(c[0], Var) and (c[0].to_correct == 1) else [el if not isinstance(el, Token) else el.value for el in c])

    def vart(self, c):
        return Var(c[0], (c[1] or "")[1:], 1)
