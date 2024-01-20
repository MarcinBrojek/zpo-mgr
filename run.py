from classes import Var, ApplyPred, Typing, Transition
from copy import deepcopy
# !for now: constrution is None / var / string / list / dict of constructions


# c - construction, m - maping for vars
# returns: success?, new_c
def try_update_constr(c, m):
    if isinstance(c, dict):
        if not c:
            return True, dict()
        b1, c_keys = zip(*[try_update_constr(el, m) for el in c.keys()])
        b2, c_values = zip(*[try_update_constr(el, m) for el in c.keys()])
        return (True, dict(list(zip(list(c_keys), list(c_values))))) if all(b1) and all(b2) else (False, None)
    if isinstance(c, list):
        if not c:
            return True, list()
        b, new_c = zip(*[try_update_constr(el, m) for el in c])
        return (True, list(new_c)) if all(b) else (False, None)
    if isinstance(c, str):
        return True, c
    if isinstance(c, Var):
        return (True, m[c]) if c in m else (False, None)
    if c is None:
        return True, None
    return False, None


# c1 - full known, c2 - with vars
# returns: success?, maping for vars in c2
def try_unify_constrs(c1, c2): 
    m = dict()
    if isinstance(c1, list) and isinstance(c2, list):
        b, m = zip(*[try_unify_constrs(e1, e2) for e1, e2 in zip(c1, c2)])
        if (not all(b)) or (len(c1) != len(c2)):
            return False, None
        m_or = dict()
        for m_e in m:
            if (m_or | m_e) != (m_e | m_or):
                return False, None
            m_or = m_or | m_e
        return True, m_or
    if isinstance(c1, str) and isinstance(c2, str):
        return (c1 == c2), m
    if (not isinstance(c1, Var)) and isinstance(c2, Var):
        m[c2] = deepcopy(c1)
        return True, m
    if (c1 is None) and (c2 is None):
        return True, m
    return False, None


class Prover:

    def __init__(self, parser, env, program_state, c):
        self.d_all, self.rt_all, self.ro_all = env.d_all, env.rt_all, env.ro_all
        self.unit = parser.run("sp", "unit")
        self.s = program_state # TODO: deep copy needed for s and c - check if needed?
        self.c = c

    def try_perform_any_transition(self):
        for ro_id in self.ro_all:
            ro = self.ro_all[ro_id]
            b, m = try_unify_constrs([self.s, self.c], [ro.tr.s1, ro.tr.c1])
            # print("obecnie:", [self.s, self.c])
            # print("propozycja przyjeta:", [ro.tr.s1, ro.tr.c1])
            if not b:
                continue

            res = self.try_prove_transition([ro.tr], m)
            if res:
                self.s, self.c = res # s2, c2
                return True
        return False

    # ap - apply predicate, m_in - maping for ap.input
    # returns: success?, maping for vars in d.output
    def apply_pred(self, ap, m_in):
        # 0. find d in d_all
        if ap.id not in self.d_all:
            return False, None
        d = self.d_all[ap.id]

        # 1. update all c in ap.input to get each full known with m_in
        b, ap_input = try_update_constr(ap.input, m_in)
        if not b:
            return False, None

        # 2. unify input from ap.input and d.input -> m
        b, m = try_unify_constrs(ap_input, d.input)
        if not b:
            return False, None

        # 3. execute code from d with m as locals variables
        locals = dict()
        for var in m:
            locals[var.ntm + "_" + var.id] = m[var] # default representation
        exec(d.code, {}, locals)
        for local in locals:
            pos_ = local.find("_")
            if pos_ != -1:
                ntm = local[0:pos_]
                id = local[(pos_ + 1):]
                var = Var(ntm, id)
                m[var] = locals[local]

        # 4. with new locals variables (m) -> set d.output (now full known)
        b, d_output = try_update_constr(d.output, m)
        if not b:
            return False, None

        # 5. unify output from d.output and ap.output -> return m_out | m_in
        b, m_out = try_unify_constrs(d_output, ap.output)
        if (not b) or ((m_in | m_out) != (m_out | m_in)):
            return False, None

        return True, (m_out | m_in)

    # tys - list of ty/ap to "prove", m - temporal maping, unique_suf - unique change of var names in rules
    # returns: success?
    def try_prove_typing(self, tys, m, unique_suf=0):
        if not tys: # empty - no more typing to prove
            return True

        unique_suf += 1
        my_tys = tys.copy()
        current = my_tys.pop()
        # print(" <" * unique_suf + f"DEBUG: top tys = {current}\n")

        if isinstance(current, ApplyPred):
            b, new_m = self.apply_pred(current, m)
            if not b:
                return False
            return self.try_prove_typing(my_tys, new_m, unique_suf)
        
        # 0. update all c in current typing
        if not isinstance(current, Typing):
            return False
        b, current_l = try_update_constr([current.g, current.c1, current.r, current.c2], m)
        if not b:
            return False
        
        # 1. iterate through all rt rules to find matching
        for rt_id in self.rt_all:
            # 1a. set new vars in maybe matching rule
            rt = self.rt_all[rt_id].override_vars(unique_suf)
            ut, ty = rt.ut, rt.ty
            # print(" :" * unique_suf + f"DEBUG: top tys = {rt.ty}\n")
            
            # 1b. try match with rule (ty)
            b, m_ty = try_unify_constrs(current_l, [ty.g, ty.c1, ty.r, ty.c2])
            if b and self.try_prove_typing(my_tys + ut[::-1], m | m_ty, unique_suf):
                return True

        return False            

    # trs - list of tuple/tr/ap to "prove", m - maping, unique_suf - unique change of var names in rules
    # returns: last (s2, c2) from single small step
    def try_prove_transition(self, trs, m, unique_suf=0): # expected: trs not empty
        unique_suf += 1
        my_trs = trs.copy()
        current = my_trs.pop()
        # print(" >" * unique_suf + f"DEBUG: top trs = {current}\n")

        if isinstance(current, ApplyPred):
            b, new_m = self.apply_pred(current, m)
            if not b:
                return False
            return self.try_prove_transition(my_trs, new_m, unique_suf)
        
        if isinstance(current, tuple): # (s2-unify, c2-unify, s2-known, c2-known)
            b, [s2, c2] = try_update_constr([current[2], current[3]], m)
            if not b:
                return False
            
            b, m_tu = try_unify_constrs([s2, c2], [current[0], current[1]])
            if (not b) or ((m_tu | m) != (m | m_tu)):
                return False
            
            # check if used constr in prove is well typed (not in final state)
            if (c2 is not None) and (not self.try_prove_typing([Typing(s2[0], c2, ":", self.unit)], dict())):
                return False

            if not my_trs:
                return (s2, c2)

            return self.try_prove_transition(my_trs, m | m_tu, unique_suf)

        if not isinstance(current, Transition):
            return False
        
        b, current_l = try_update_constr([current.s1, current.c1], m)
        if not b:
            return False
        
        for ro_id in self.ro_all:
            ro = self.ro_all[ro_id].override_vars(unique_suf)
            uo, tr = ro.uo, ro.tr
            b, m_tr = try_unify_constrs(current_l, [tr.s1, tr.c1])
            # print(f"DEBUG: current:{current_l}")
            # print(f"DEBUG: left side,tr:{[tr.s1, tr.c1]}")
            if not b:
                continue
            # print(f"DEBUG: udane unify:{m_tr}")
            
            last_s2c2 = self.try_prove_transition(my_trs + [(current.s2, current.c2, tr.s2, tr.c2)] + uo[::-1], m | m_tr, unique_suf)
            if last_s2c2:
                return last_s2c2
            
        return False