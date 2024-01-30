from pathlib import Path
from src.converter import gen_tex
import yaml


CONFIG_PATH = Path(__file__).parent / "debug_config.yaml"


inf = 1000000


class Debugger:
    def __init__(self, stdscr=None, debug=False, path=CONFIG_PATH):

        self.depth = 0 # actual depth of action

        # global action -> action_depth = -1
        # action_all -> action_depth = depth - 1
        # action -> action_depth = depth

        # we store at skip / abort the depth of last used that action
        # if actual depth is >= skip /abort, we "perform" that stored action
        self.skip = inf
        self.abort = inf 

        if not debug:
            self.debug = False
            return # empty debug
        
        self.debug = True
        self.stdscr = stdscr
        self.stdscr.scrollok(1)

        with open(path, "r") as file:
            data = yaml.safe_load(file)
        self.data = data
        self.in_prove = False

    def addstr(win, text):
        y, x = win.getyx()
        win.addstr(y, x, text)
        win.move(y + 1, 0)

    def add_window_info(self, c):
        self.stdscr.addstr("\n")
        self.stdscr.addstr(f"--------------------------------------------------------------------------------\n")
        self.stdscr.addstr(f"                            DEBUG - {type(c).__name__} - depth({self.depth})\n")
        self.stdscr.addstr(f"--------------------------------------------------------------------------------\n\n")
        self.stdscr.addstr(str(c))
        self.stdscr.refresh()

    def incr_action_depth(self):
        self.depth += 1

    def decr_action_depth(self):
        self.depth -= 1

    def is_skipped(self):
        return self.depth >= self.skip
    
    def is_aborted(self):
        return self.depth >= self.abort
    
    def try_skip_reset(self):
        if self.depth <= self.skip:
            self.skip = inf

    def try_abort_reset(self):
        if self.depth <= self.abort:
            self.abort = inf

    def read_action(self, c, place):
        if (not self.debug) or self.is_skipped() or self.is_aborted():
            return
        
        read = not (self.data["follow"][place])
        if read:
            return
        
        if self.data["clear_window"] == True:
            self.stdscr.clear()
            self.stdscr.refresh()

        self.add_window_info(c)
        depth = self.depth

        while(not read):
            key = self.stdscr.getch()

            if key == self.data["keys"]["refresh"]:
                if self.data["clear_window"] == True:
                    self.stdscr.clear()
                    self.stdscr.refresh()
                self.add_window_info(c)

            elif key == self.data["keys"]["print_pdf"]:
                gen_tex(c)

            elif key == self.data["keys"]["global_skip"]:
                self.skip, read = -1, True
            elif key == self.data["keys"]["global_abort"]:
                self.abort, read = -1, True

            elif self.in_prove: # transition, typing
                if key == self.data["keys"]["prove_next"]:
                    read = True
                elif key == self.data["keys"]["prove_skip"]:
                    self.skip, read = depth, True
                elif key == self.data["keys"]["prove_abort"]:
                    self.abort, read = depth, True
                elif key == self.data["keys"]["prove_skip_all"]:
                    self.skip, read = depth - 1, True
                elif key == self.data["keys"]["prove_abort_all"]:
                    self.abort, read = depth - 1, True

            else: # program (block), breakpoints, call
                if key == self.data["keys"]["next"]:
                    read = True
                elif key == self.data["keys"]["skip"]:
                    self.skip, read = depth, True
                elif key == self.data["keys"]["abort"]:
                    self.abort, read = depth, True
                elif key == self.data["keys"]["skip_all"]:
                    self.skip, read = depth - 1, True
                elif key == self.data["keys"]["abort_all"]:
                    self.abort, read = depth - 1, True
