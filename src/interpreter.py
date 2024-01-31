from src.base_parser import BaseParser
from src.run import Prover
from debugger.debugger import Debugger


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
    def __init__(self, state=None, base_parser=None, debugger=None):
        self.state = state or IState()
        self.c = None
        self.base_parser = base_parser or BaseParser()
        self.debugger = debugger or Debugger(debug=False)

    def run(self, p):
        name = type(p).__name__
        self.base_parser.update_rs_all(self.state.envs[-1].rs_all.values())

        # DEBUG - before translate
        if name != "Block":
            self.debugger.try_reset()
            if self.debugger.is_aborted():
                return
        # DEBUG

        if name in ["Ro", "Rt", "DefinePred", "Code"]:
            p.translate(self.base_parser)

        # DEBUG - print translated structure
        if name != "Block" and name != "Breakpoint":
            self.debugger.read_action(p, "program")
            if self.debugger.is_aborted():
                return
        # DEBUG

        if name == "Program":
            # DEBUG - depth update
            self.debugger.incr_action_depth()
            # DEBUG

            for sub_p in p.lst:
                self.run(sub_p)

            # DEBUG - reset all action
            self.debugger.decr_action_depth()
            # DEBUG

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

        elif name == "Code":
            self.c = p.rsp # sp after transtlate

            self.debugger.in_prove = True # DEBUG
            self.debugger.incr_action_depth() # DEBUG - avoid influence of skip all / abort all on program from transition

            prover = Prover(self.base_parser, self.state.envs[-1], self.state.program_state, self.c, self.debugger)

            b = True
            while b:
                # DEBUG
                if self.debugger.debug and self.debugger.data["follow"]["config"]:
                    self.debugger.try_reset()
                    if self.debugger.is_aborted():
                        break # or maybe return?
                    self.debugger.read_action({"s": prover.s, "c": prover.c}, "config")
                    if self.debugger.is_aborted():
                        break # or maybe return?
                # DEBUG
                    
                self.debugger.incr_action_depth() # DEBUG

                b = prover.try_perform_any_transition() # is performed transition
                print(f"\nstate: {prover.s}, \nconstr: {prover.c}\n\n")

                self.debugger.decr_action_depth() # DEBUG

            self.debugger.decr_action_depth() # DEBUG
            self.debugger.in_prove = False # DEBUG

            if prover.c is not None: # final state
                raise Exception("Stuck in sos")
            self.program_state = prover.s
        
        elif name == "Breakpoint":
            # DEBUG
            self.debugger.read_action("Breakpoint - id:" + p.id, "breakpoint")
            if self.debugger.is_aborted():
                return
            # DEBUG
