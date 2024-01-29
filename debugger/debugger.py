from pathlib import Path
from src.converter import gen_tex
import yaml


CONFIG_PATH = Path(__file__).parent / "debug_config.yaml"


class Debugger:
    def __init__(self, stdscr=None, debug=False, path=CONFIG_PATH):

        self.action_depth = 0 # actual depth of action
        self.saved_action_depth = 0 # saved depth for action like "skip"

        self.skip_global = False
        self.abort_global = False

        self.skip = False
        self.abort = False

        self.skip_all = False
        self.abort_all = False

        if not debug:
            self.skip_global = True
            return # empty debug
        
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
        self.stdscr.addstr(f"                            DEBUG - {type(c).__name__} - depth({self.action_depth})\n")
        self.stdscr.addstr(f"--------------------------------------------------------------------------------\n\n")
        self.stdscr.addstr(str(c))
        self.stdscr.refresh()

    def save_action_depth(self):
        self.saved_action_depth = self.action_depth

    def incr_action_depth(self):
        self.action_depth += 1

    def decr_action_depth(self):
        self.action_depth -= 1

    def is_skipped(self):
        if self.skip_global:
            return True
        skipped = False
        skipped |= self.skip and (self.action_depth > self.saved_action_depth)
        skipped |= self.skip_all and (self.action_depth >= self.saved_action_depth)
        return skipped
    
    def is_aborted(self):
        if self.abort_global:
            return True
        aborted = False
        aborted |= self.abort and (self.action_depth > self.saved_action_depth)
        aborted |= self.abort_all and (self.action_depth >= self.saved_action_depth)
        return aborted

    def read_action(self, c, place):
        if self.is_skipped() or self.is_aborted():
            return
        
        read = not (self.data["follow"][place])
        if read:
            return
        
        self.save_action_depth()
        if self.data["clear_window"] == True:
            self.stdscr.clear()
            self.stdscr.refresh()

        self.add_window_info(c)

        while(not read):
            key = self.stdscr.getch()

            if key == self.data["keys"]["print_pdf"]:
                gen_tex(c)

            elif key == self.data["keys"]["global_skip"]:
                self.skip_global, read = True, True
            elif key == self.data["keys"]["global_abort"]:
                self.abort_global, read = True, True

            elif self.in_prove: # transition, typing
                if key == self.data["keys"]["prove_next"]:
                    self.next, read = True, True
                elif key == self.data["keys"]["prove_skip"]:
                    self.skip, read = True, True
                elif key == self.data["keys"]["prove_abort"]:
                    self.abort, read = True, True
                elif key == self.data["keys"]["prove_skip_all"]:
                    self.skip_all, read = True, True
                elif key == self.data["keys"]["prove_abort_all"]:
                    self.abort_all, read = True, True

            else: # program (block), breakpoints, call
                if key == self.data["keys"]["next"]:
                    self.next, read = True, True
                elif key == self.data["keys"]["skip"]:
                    self.skip, read = True, True
                elif key == self.data["keys"]["abort"]:
                    self.abort, read = True, True
                elif key == self.data["keys"]["skip_all"]:
                    self.skip_all, read = True, True
                elif key == self.data["keys"]["abort_all"]:
                    self.abort_all, read = True, True

    def action_end(self):
        if self.is_skipped() or self.is_aborted():
            return

        self.skip = False
        self.abort = False

    def action_all_end(self):
        if self.is_skipped() or self.is_aborted():
            return

        self.skip = False
        self.abort = False
        self.skip_all = False
        self.abort_all = False