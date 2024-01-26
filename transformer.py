from lark import Transformer
from classes import (
    Var,
    ApplyPred,
    DefinePred,
    Transition,
    Typing,
    Program,
    Block,
    Rs,
    Ro,
    Rt,
    Code
)


class OptimusPirme(Transformer):
    def PY(self, c):
        return str(c[1:-1])

    def ID(self, c):
        return str(c)

    def STR(self, c):
        return str(c)

    def I(self, c):
        return int(c)

    def rawnamed(self, c):
        return str(c[0])[:-1]

    def rsp(self, c):
        return str(c[0])

    def s(self, c):
        id = None if "_" not in str(c[0]) else str(c[0][3:])
        return Var('s', id)

    def g(self, c):
        id = None if "_" not in str(c[0]) else str(c[0][3:])
        return Var('G', id)

    def c(self, c):
        return c[0]

    def ap(self, c):
        id, i, input, output = c[0], 1, list(), list()
        while (c[i] != "|" and i < len(c)):
            if c[i] is not None:
                input.append(c[i])
            i += 1
        i += 1 # "|"
        while (i < len(c)):
            if c[i] is not None:
                output.append(c[i])
            i += 1
        return ApplyPred(id, input, output)

    def d(self, c):
        id, i, input, output = c[0], 1, list(), list()
        while (c[i] != "|" and i < len(c) - 1):
            if c[i] is not None:
                input.append(c[i])
            i += 1
        i += 1 # "|"
        while (i < len(c) - 1):
            if c[i] is not None:
                output.append(c[i])
            i += 1
        code = c[-1]
        return DefinePred(id, input, output, code)

    def tr(self, c):
        c1, c2 = c[0], c[2]
        s1, s2 = c[1], c[3]
        return Transition(s1, s2, c1, c2)

    def trend(self, c):
        c1 = c[0]
        s1, s2 = c[1], c[2]
        return Transition(s1, s2, c1)

    def uo(self, c):
        return c

    def REL(self, c):
        return str(c)

    def ty(self, c):
        [g, c1, r, c2] = c
        return Typing(g, c1, r, c2)

    def ut(self, c):
        return c

    def p(self, c):
        return Program(list(c))

    def bp(self, c):
        return Block(c[0])

    def inneroption(self, c):
        return list(c)

    def code(self, c):
        return Code(c[0])

    def rs(self, c):
        name_id = c[0]
        id = c[1]
        number = c[2]
        inneroptions = c[3:]
        return Rs(name_id, id, number, inneroptions)

    def ro(self, c):
        name_id = c[0]
        uo = c[1]
        tr = c[2]
        return Ro(name_id, uo, tr)

    def rt(self, c):
        name_id = c[0]
        ut = c[1]
        ty = c[2]
        return Rt(name_id, ut, ty)
