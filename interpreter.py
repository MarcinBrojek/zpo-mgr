from base_parser import BaseParser
from classes import (
    DefinePred,
    Block,
    Rs,
    Ro,
    Rt,
)
from run import Prover


class IEnv:
    def __init__(self, rs_all=None, ro_all=None, rt_all=None, d_all=None):
        self.rs_all = rs_all or dict()
        self.ro_all = ro_all or dict()
        self.rt_all = rt_all or dict()
        self.d_all = d_all or dict()

    def copy(self):
        return IEnv(
            self.rs_all.copy(),
            self.ro_all.copy(),
            self.rt_all.copy(),
            self.d_all.copy(),
        )


class IState:
    def __init__(self, envs=None, store=None, gamma=None):
        self.envs = envs or list([IEnv()])
        self.program_state = [store or dict(), gamma or dict()]


class Interpreter:
    def __init__(self, state=None, base_parser=None):
        self.state = state or IState()
        self.c = None
        self.base_parser = base_parser or BaseParser()

    def run(self, p):
        name = type(p).__name__
        self.base_parser.update_rs_all(self.state.envs[-1].rs_all.values())

        if name in ["Ro", "Rt", "DefinePred"]:
            p.translate(self.base_parser)

        if name == "list":  # p
            for sub_p in p:
                self.run(sub_p)

        elif name == "Block":
            self.state.envs.append(self.state.envs[-1].copy())
            self.run(p.p)
            self.state.envs.pop()

        elif name == "Rs":
            self.state.envs[-1].rs_all[p.name_id] = p

        elif name == "Ro":
            self.state.envs[-1].ro_all[p.name_id] = p

        elif name == "Rt":
            self.state.envs[-1].rt_all[p.name_id] = p

        elif name == "DefinePred":
            self.state.envs[-1].d_all[p.id] = p

        elif name == "str":  # rsp
            self.c = self.base_parser.run("sp", p)
            prover = Prover(self.base_parser, self.state.envs[-1], self.state.program_state, self.c)
            while prover.try_perform_any_transition():
                pass
            print(f"\nstate: {prover.s}, \nconstr: {prover.c}\n\n")
            if prover.c is not None: # final state
                raise Exception("Stuck in sos")
            self.program_state = prover.s

