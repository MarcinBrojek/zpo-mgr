## Introduction

The small-step semantics allows understanding the behavior, the flow of the language, and the result produced by individual syntactic constructs. This semantics is available at the [link to Overleaf (view mode)](https://www.overleaf.com/read/bkzncfprpdkh#9766c8) and it pertains to this interpreter. It does not precisely describe its behavior, and therefore, this document will include descriptions of this semantics and discrepancies compared to the actual behavior of the tool.

Upload date of [semantics](./semantics/) - 04/02/2024 ❕ all visible screens may be outdated
❕ report bugs in issues - as documentation 

## Syntax description

Base | Construction | Unprocessed contruction
:-:|:-:|:-:
![](./semantics/syntax_base.png) | ![](./semantics/syntax_contruction.png) | ![](./semantics/syntax_base_sp.png)

Apply & Def Predicate | Transition & Typing | Program
:-:|:-:|:-:
![](./semantics/syntax_ap_d.png) | ![](./semantics/syntax_tr_ty.png) | ![](./semantics/syntax_program.png)

## Semantics elements

State, Configuration, Environments | Syntax Environment | Operational Semantics Environment
:-:|:-:|:-:
![](./semantics/sem_info.png) | ![](./semantics/sem_info_s.png) | ![](./semantics/sem_info_o.png)

Typing Environment | Predicate Environment | Predefined predicates
:-:|:-:|:-:
![](./semantics/sem_info_t.png) | ![](./semantics/sem_info_d.png) | ![](./semantics/sem_info_predef.png)

## Semantics description

Parse transition rule | Parse upper part transition rule | Parse transition | Parse transition end
:-:|:-:|:-:|:-:|
![](./semantics/P-RO.png) | ![](./semantics/P-uo12.png) | ![](./semantics/P-tr.png) | ![](./semantics/P-trend.png)

Parse typing rule | Parse upper part typing rule | Parse typing
:-:|:-:|:-:|
![](./semantics/P-RT.png) | ![](./semantics/P-ut12.png) | ![](./semantics/P-ty.png)

Parse predicate definition | Parse construction list | Parse construction | Parse apply predicate
:-:|:-:|:-:|:-:|
![](./semantics/P-d.png) | ![](./semantics/P-cl.png) | ![](./semantics/P-c.png) | ![](./semantics/P-ap.png)

Two programs | Two programs, one program end
:-:|:-:|
![](./semantics/SR-P1P2.png) | ![](./semantics/SR-P1P2end.png)

Syntax rule | Semantics rule | Typing rule | Definition (predicate)
:-:|:-:|:-:|:-:|
![](./semantics/SR-RS.png) | ![](./semantics/SR-RO.png) | ![](./semantics/SR-RT.png) | ![](./semantics/SR-D.png)

Block | Block end
:-:|:-:|
![](./semantics/SR-{P}.png) | ![](./semantics/SR-popEnv.png)

Raw subprogram | Subprogram | Subprogram end | Prove predicate
:-:|:-:|:-:|:-:|
![](./semantics/SR-rsP.png) | ![](./semantics/SR-sP.png) | ![](./semantics/SR-sPend.png) | ![](./semantics/O-sP-ap.png)

Prove upper part rule transition | Prove upper part rule transition - single | Prove empty upper part rule transition
:-:|:-:|:-:|
![](./semantics/O-sP-uo12.png) | ![](./semantics/O-sP-uo.png) | ![](./semantics/O-sP.png) | ![](./semantics/O-sP-ap.png)

Prove upper part rule transition end | Prove upper part rule transition - single end | Prove empty upper part rule transition end
:-:|:-:|:-:|
![](./semantics/O-sP-uo12end.png) | ![](./semantics/O-sP-uoend.png) | ![](./semantics/O-sPend.png) | ![](./semantics/O-sP-ap.png)

Prove upper part rule typing | Prove upper part rule typing - single | Prove empty upper part rule typing
:-:|:-:|:-:|
![](./semantics/T-sP-ut12.png) | ![](./semantics/T-sP-ut.png) | ![](./semantics/T-sP.png)

## Discrepancies in Semantics Compared to the Actual Behavior of the Tool

TODO
