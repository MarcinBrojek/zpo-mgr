## Structure visualization:

```
.
├── LICENSE
├── README.md
├── debugger
│   ├── debug_config.yaml
│   └── debugger.py
├── docs
│   ├── config.md
│   ├── debug.md
│   ├── semantics.md
│   ├── structure.md
│   └── tutorial.md
├── main.py
├── programs/
├── requirements.txt
├── run_tests.py
├── src
│   ├── base_grammar.lark
│   ├── base_parser.py
│   ├── base_transformer.txt
│   ├── classes.py
│   ├── converter.py
│   ├── grammar.lark
│   ├── interpreter.py
│   ├── interpreter_config.yaml
│   ├── run.py
│   └── transformer.py
└── tmp
```

## Description

- ### [debugger/](../debugger/)
    - [`debug_config.yaml`](../debugger/debug_config.yaml): Configuration file for debugging.
    - [`debugger.py`](../debugger/debugger.py): Main class for debugging.

- ### [docs/](../docs)
    - [`config.md`](./config.md) : Describes configuration files and their usage
    - [`debug.md`](./debug.md) : Explains how to use debug mode and its features.
    - [`semantics.md`](./semantics.md) : Semantics for the Tool.
    - [`structure.md`](./structure.md) : This file - structure of the project.
    - [`tutorial.md`](./tutorial.md) : Showcases tool usage with examples.

- [`main.py`](../main.py) : Main file - to run single program.

- ### [programs/](../programs/)
    - `test_<number>` : Example programs written for tool. 

- [`run_test.py`](../run_tests.py) : Group run for choosen tests - programs.

- ### [src/](../src/)
    - [`base_grammar.lark`](../src/base_grammar.lark) : Fundation of grammar in lark created by user.
    - [`base_parser.py`](../src/base_parser.py) : Parser, that cooperates with base grammar and transformer.
    - [`base_transformer.txt`](../src/base_transformer.txt) : Fundation of lark transformer in txt for user's program.
    - [`classes.py`](../src/classes.py) : Contains most classes existing in other files.
    - [`converter.py`](../src/converter.py) : Simple converter of construction into LaTeX code.
    - [`grammar.lark`](../src/grammar.lark) : Grammar for main language.
    - [`interpreter.py`](../src/interpreter.py) : Interpreter for main language.
    - [`interpreter_config.yaml`](../src/interpreter_config.yaml) : Configuration file for interpreter.
    - [`run.py`](../src/run.py) : Helper file for interpreter, with prover funtions.
    - [`transformer.py`](../src/transformer.py) : Lark transformer for main language.

- ### [tmp/](../tmp/) - empty at repositiory
    - `tmp_convert.pdf` : Generated pdf for choosen construction.
    - `tmp_transforer.py` : Generated lark transformer for user's program.
