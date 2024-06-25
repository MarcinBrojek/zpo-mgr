from src.base_parser import BaseParser
from src.run import Prover
from debugger.debugger import Debugger
from pathlib import Path
import yaml
from copy import deepcopy


CONFIG_PATH = Path(__file__).parent / "interpreter_config.yaml"


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
    def __init__(self, data=None, envs=None):
        self.envs = envs or list([IEnv()])
        self.start_store = data["start_store"]
        self.start_gamma = data["start_gamma"]
        self.reset_program_state = data["reset_program_state"]
        self.unit_nonterminal = data["unit_nonterminal"]
        self.unit_name = data["unit_name"]
        self.program_state = [deepcopy(self.start_store), deepcopy(self.start_gamma)]

    def try_reset_program_state(self):
        if self.reset_program_state:
            self.program_state = [deepcopy(self.start_store), deepcopy(self.start_gamma)]


class Interpreter:
    def __init__(self, state=None, base_parser=None, debugger=None, data=None, path=CONFIG_PATH):
        self.c = None
        self.base_parser = base_parser or BaseParser()
        self.debugger = debugger or Debugger(debug=False)

        if data is None:
            with open(path, "r") as file:
                data = yaml.safe_load(file)

        self.state = state or IState(data=data)

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
            p.translate(self.base_parser) # should be moved?

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
            self.c = p.rsp # sp, after transtlate

            self.debugger.in_prove = True # DEBUG
            self.debugger.incr_action_depth() # DEBUG - avoid influence of skip all / abort all on program from transition

            prover = Prover(self.base_parser, self.state.envs[-1], self.state.program_state, self.c, self.debugger, self.state.unit_nonterminal, self.state.unit_name)

            b = True
            # perform sos
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

                # print(f"\nstate: {prover.s}, \nconstr: {prover.c}\n\n")
                b = prover.try_perform_any_transition() # is performed transition

                self.debugger.decr_action_depth() # DEBUG

            self.debugger.decr_action_depth() # DEBUG
            self.debugger.in_prove = False # DEBUG

            if prover.c is not None: # final state
                raise Exception("Stuck in sos")
            
            self.state.program_state = prover.s
            self.state.try_reset_program_state()
        
        elif name == "Breakpoint":
            # DEBUG
            self.debugger.read_action("Breakpoint - id:" + p.id, "breakpoint")
            if self.debugger.is_aborted():
                return
            # DEBUG
