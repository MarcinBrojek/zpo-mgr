## Existing Configuration Files

Here, we will describe the impact of each configuration file and how they influence the tool.

### - [debug_config.yaml](../debugger/debug_config.yaml)

The Debugger class responsible for holding debugging information at runtime relies on a configuration file. In this file, you can specify which program elements will be traced and which keys will correspond to executing specific actions.

### - [interpreter_config.yaml](../src/interpreter_config.yaml)

The Interpreter class, responsible for interpreting the program, initially establishes, upon creation, the initial state of the program and its behavior between subsequent code executions based on the configuration file.