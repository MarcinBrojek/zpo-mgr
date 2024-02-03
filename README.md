## General info
The project was developed as part of a master's thesis. It is a tool that enables designing and using a custom programming language by defining syntax rules, operational semantics in small steps, and typing. Subsequently, code can be written in the invented language. Essentially, this tool is a language interpreter that facilitates what was described above. This happens because we assume a constant structure of the written programs - they consist of individual parts, such as syntax modification. These parts are dynamically analyzed and processed, allowing the created language or its part to be used and tested during development. More information about the project's [structure](./docs/structure.md) and operation principles can be found in the [docs](./docs/) folder.
<br><br>
The project requires further testing and development, so please be aware that there may be bugs in it.

## Dependencies & quick set up
The project / interpreter was developed in the Python language and solely relies on Python libraries available at https://pypi.org. Dependencies can be found in the [requirements.txt](./requirements.txt) file.
1. Download repository. (suggested: create virualenv)
2. Download dependecies with pip.
3. You can start work with repository.

## Short example of use.

1. Design your language and use it - all in one file.
<br>
(The contents of the file: [test_02.txt](./programs/test_02.txt))
```
@syntax(sp){sp: /unit/ | /print/ "(" sp ")" | string}
@syntax(string){string: STR}

@typing(t1){
    ---
    @G |- `@sp` : `unit`
}

pred_print(`@sp` |)`
print("OUT: " + sp[0])
`

@semantics(o1){
    pred_print(`@sp` |)
    ---
    <`print(@sp)`, @s> => @s
}

{

    pred_print(`@string` |)`
print("IN: " + string[0])
    `

    @code`print("printed in block")`
}

@syntax(sp){sp: /unit/ | /print/ "(" sp ")" | STR}

@code`print( "printed outside of block" )`

```
2. Run [main.py](./main.py) with one argument - file from point 1.

```console
> python main.py programs/test_02.txt
```
3. Watch the resulsts of calling programs. (on your own)

## Tasks list - todo: move to issues.

- [ ] Add type check at the beggining in sos
- [ ] Modify debug in transition and typing to show more steps
- [ ] Add class - Configuration, for better explanation
- [ ] Add class - Rule, for better explanation
- [ ] Add exceptions for some situations
- [ ] Write up list of lackings for semantics
- [ ] Reformat code + style
- [ ] Make tutorial
- [ ] Complete `README`

