from lark import Transformer
from classes import (
    State,
    Gamma,
    ApplyPred,
    DefinePred,
    Transition,
    # MyType,
    Typing,
    Block,
    Rs,
    Ro,
    Rt,
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

    def rsp(self, c):
        return str(c[0][1:-1])

    def s(self, c):
        id = None if "_" not in str(c[0]) else str(c[0][2:])
        return State(id)

    def g(self, c):
        id = None if "_" not in str(c[0]) else str(c[0][2:])
        return Gamma(id)

    # def t(self, c):
    #     print(c)
    #     if isinstance(c, list):
    #         print([type(c_) for c_ in c])
    #     if c[0][0] == "@":
    #         id = None if "_" not in str(c[0]) else str(c[0][2:])
    #         return MyType(id=id)
    #     return MyType(raw_type=c[0])

    def c(self, c):
        return c[0]

    def ap(self, c):
        id = c[0]
        l = c[1:]
        return ApplyPred(id, l)

    def d(self, c):
        id = c[0]
        input, output = list(), list()
        for i in range(1, len(c) - 1, 2):
            if c[i] == "+":
                input.append(c[i + 1])
            elif c[i] == "-":
                output.append(c[i + 1])
            else:
                assert False, c[i]
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
        # return list(c)
        return c

    def REL(self, c):
        return str(c)

    def ty(self, c):
        [g, c1, r, c2] = c
        return Typing(g, c1, r, c2)

    def ut(self, c):
        # return list(c)
        return c

    def p(self, c):
        return list(c)

    def bp(self, c):
        return Block(c)

    def inneroption(self, c):
        return list(c)

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
