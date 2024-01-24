# returns: translated rsp into sp (list of rsp into list of sp)
def translate_c(base_parser, start, c):
    if isinstance(c, str):
        return base_parser.run(start, c)
    if isinstance(c, list):
        return [translate_c(base_parser, start, el) for el in c]
    return c


# returns: new c (copy) witch changed vars' names 
def override_vars(c, unique_suf):
    if isinstance(c, dict):
        c_keys = override_vars(list(c.keys()), unique_suf)
        c_values = override_vars(list(c.values()), unique_suf)
        return dict(zip(c_keys, c_values))
    if isinstance(c, tuple):
        return tuple(override_vars(list(c), unique_suf))
    if isinstance(c, list):
        return [override_vars(el, unique_suf) for el in c]
    if isinstance(c, str):
        return c
    if isinstance(c, Var):
        ntm = c.ntm + "#" + str(unique_suf)
        var = c.id
        return Var(ntm, var)
    return None


class Var:
    def __init__(self, ntm, id, to_correct=0):
        self.ntm = ntm
        self.id = id or ""
        self.to_correct = to_correct

    def __str__(self):
        return f"@{self.ntm}_{self.id}"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, another):
        return isinstance(another, Var) and self.ntm == another.ntm and self.id == another.id

    def __hash__(self):
        return hash((self.ntm, self.id))


class ApplyPred:
    def __init__(self, id, input, output):
        self.id = id
        self.input = input
        self.output = output

    def __str__(self):
        return f"@apply ({self.id}) ({self.input} | {self.output})"

    def __repr__(self):
        return self.__str__()

    def translate(self, base_parser):
        self.input = translate_c(base_parser, "sp", self.input)
        self.output = translate_c(base_parser, "sp", self.output)

    def override_vars(self, suf):
        return ApplyPred(
            override_vars(self.id, suf),
            [override_vars(el, suf) for el in self.input],
            [override_vars(el, suf) for el in self.output]
        )


class DefinePred:
    def __init__(self, id, input, output, code):
        self.id = id
        self.input = input
        self.output = output
        self.code = code

    def __str__(self):
        return f"@define ({self.id}) ({self.input} | {self.output}) {self.code}\n"

    def __repr__(self):
        return self.__str__()

    def translate(self, base_parser):
        self.input = translate_c(base_parser, "sp", self.input)
        self.output = translate_c(base_parser, "sp", self.output)


class Transition:
    def __init__(self, s1, s2, c1, c2=None):
        self.c1 = c1
        self.c2 = c2
        self.s1 = s1
        self.s2 = s2
        self.ending = c2 is None

    def __str__(self):
        if self.ending:
            return f"<{self.c1}, {self.s1}> => {self.s2}"
        else:
            return f"<{self.c1}, {self.s1}> => <{self.c2}, {self.s2}>"

    def __repr__(self):
        return self.__str__()

    def translate(self, base_parser):
        self.c1 = translate_c(base_parser, "sp", self.c1)
        if not self.ending:
            self.c2 = translate_c(base_parser, "sp", self.c2)

    def override_vars(self, suf):
        return Transition(
            override_vars(self.s1, suf),
            override_vars(self.s2, suf),
            override_vars(self.c1, suf),
            override_vars(self.c2, suf)
        )


class Typing:
    def __init__(self, g, c1, r, c2):
        self.g = g
        self.c1 = c1
        self.r = r
        self.c2 = c2

    def __str__(self):
        return f"{self.g} |- {self.c1} {self.r} {self.c2}"

    def __repr__(self):
        return self.__str__()

    def translate(self, base_parser):
        self.c1 = translate_c(base_parser, "sp", self.c1)
        self.c2 = translate_c(base_parser, "sp", self.c2)

    def override_vars(self, suf):
        return Typing(
            override_vars(self.g, suf),
            override_vars(self.c1, suf),
            override_vars(self.r, suf),
            override_vars(self.c2, suf)
        )


class Block:
    def __init__(self, p):
        self.p = p

    def __str__(self):
        return "{\n" + str(self.p) + "\n}"

    def __repr__(self):
        return self.__str__()


class Rs:
    def __init__(self, name_id, id, number, inneroptions):
        self.name_id = name_id
        self.id = id
        self.number = number
        self.inneroptions = inneroptions

    def __str__(self):
        return (
            f"@syntax({self.name_id})"
            + "{\n"
            + f"{self.id}.{self.number} : {self.inneroptions}"
            + "\n}\n"
        )

    def __repr__(self):
        return self.__str__()


class Ro:
    def __init__(self, name_id, uo, tr):
        self.name_id = name_id
        self.uo = uo
        self.tr = tr

    def __str__(self):
        return (
            f"@semantics({self.name_id})" + "{\n" + f"{self.uo}\n---\n{self.tr}" + "\n}\n"
        )

    def __repr__(self):
        return self.__str__()

    def translate(self, base_parser):
        for c in self.uo:
            c.translate(base_parser)
        self.tr.translate(base_parser)

    def override_vars(self, suf):
        return Ro(
            override_vars(self.name_id, suf),
            [el.override_vars(suf) for el in self.uo],
            self.tr.override_vars(suf)
        )


class Rt:
    def __init__(self, name_id, ut, ty):
        self.name_id = name_id
        self.ut = ut
        self.ty = ty

    def __str__(self):
        return f"@typing({self.name_id})" + "{\n" + f"{self.ut}\n---\n{self.ty}" + "\n}\n"

    def __repr__(self):
        return self.__str__()

    def translate(self, base_parser):
        for c in self.ut:
            c.translate(base_parser)

        self.ty.translate(base_parser)

    def override_vars(self, suf):
        return Rt(
            override_vars(self.name_id, suf),
            [el.override_vars(suf) for el in self.ut],
            self.ty.override_vars(suf)
        )
