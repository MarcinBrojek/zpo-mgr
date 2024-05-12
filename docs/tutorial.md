## Introduction

In this document, we will briefly describe how to write and use your own language. It will cover potential issues or difficulties in crafting language syntax, defining custom small-step semantics, and typing rules. In this tutorial, we will create a simple example, taking the opportunity to explain the significance of each element.

## Program structure

The program consist of:
- modifications to the user's language:
    - 1 - syntax rules,
    - 2 - predicates' definition,
    - 3 - rules of small-step operational semantics,
    - 4 - typing rules,
- 5 - executed user code,
- 6 - block with program.

Therefore, when creating a program, it's important for the syntax rules (1) to come first.
Thanks to them, we can process the specified syntax, i.e., language constructs that are part of semantic and typing rules or predicate definitions (2, 3, 4).
<br><br>
By establishing an appropriate set of rules, the executed user code (5) becomes entirely comprehensible from their standpoint. Let's describe the syntax of individual program elements and their meaning (1, 2, 3, 4, 5, 6). (example taken from [test_01.txt](../programs/test_01.txt))

## Syntax rules

❗ It's important to note that the syntax rules in this tool are based on Lark grammar rules, and thus, their appearance and behavior have been retained. The interpreter was not intended to focus on the parser but rather on the ability to modify / edit syntax rules - hence the use of a pre-existing parser. (here is used "earley") ❗

Sample syntax rules look as follows:
<pre>
@syntax(sp){sp: e | t}
@syntax(e){e: /0/ | /s/ "(" e ")" | e /\+/ e}
@syntax(t){t: /unit/}
</pre>

Above, we have three syntax rules. The first one states that the non-terminal `sp` can be reduced to either `e` or `t.`
The second rule states that the non-terminal `e` can be reduced to the terminal string '0' or to a composition: 's', '(', non-terminal `e`, ')' or to a composition: non-terminal `e`, '+', non-terminal `e`. The third rule states that the non-terminal `t` is always the terminal 'unit'.

To create a rule, you need to write a text in the form:
<pre>
@syntax( < name of syntax rule > ) { < non-terminal name > : < option 1 > | ... | < option n > }
</pre>

Each option is a composition of terminals and non-terminals. To better understand how they are processed, it's worth taking a look at the [grammar.lark](../src/grammar.lark). However, from the user's perspective, they initially have access to an almost empty grammar - [base_grammar.lark](../src/base_grammar.lark). So, the user has access to the non-terminals: `ID` - a name composed of uppercase and lowercase alphabet letters and underscores '_', `STR` - an escaped string, `I` - integer numbers. Moreover, they can also use terminals: regex syntax enclosed in '/' '/' and any string enclosed in '"' '"'. The first ones are considered in the parsing tree, while the latter are ignored.

## Predicates' definition

An example predicate definition looks like this:
<pre>
update(`s(@e)`, @s_1 | `@e`, @s_2)`
s_2 = s_1
if type(s_2[1]) != int:
    s_2[1] = 1
else:
    s_2[1] += 1
`
</pre>

The idea of a predicate arises from the need for handling basic translations of simple expressions, such as arithmetic, and the need to store a new value for the program state. These predicates will be used (applied) in the upper parts of the semantic and typing rules. The implementation of such a predicate will be based on the provided Python code in the predicate definition body.

The above predicate definition example should be interpreted as follows: the predicate is satisfied if it has two input parameters in the form: \`s(@e)\` - a composition of 's', '(', @e - any non-terminal `e` with an empty index, ')' and \`@s_1\` - program state `s_1` with index 1. It also has two output parameters: \`@e\` - any non-terminal `e`, and \`@s_2\` - program state `s_2` with index 2. 

ℹ️ The same symbols used for non-terminals in parameters in the definition must match, so in this case, the first input parameter is essentially 's(< first output parameter >)'.

ℹ️ However, before the output parameters are checked, Python code is executed, which, as a side effect, sets variables that may have an impact on the output parameters. Therefore, we have the order: input parameters -> code -> output parameters, essentially behaving like a function.

The predicate definition takes the form of:

<pre>
< name of predicate > ( 
    < input_par 1 >, ..., < input_par n > 
    | < output_par 1 >, ..., < output_par m > 
) `
< Python code > 
`
</pre>

### Construction

All input / output parameters are constructions that are divided into:
- @s - Program state,
- @G - Context / Gamma,
- \`raw - unprocessed text\` - A construction that will be parsed by user rules.

ℹ️ When a user creates a construction, they may want to include variables - undefined non-terminals (those introduced by the user in syntax rules). In that case, they create them by adding '@' at the beginning of the name. You can add an index to distinguish the same non-terminals but different variables by adding '_' and then a name, such as @e_1.

### Apply predicate

To apply predicate one must follow form:

<pre>
< name of predicate > ( 
    < input_par 1 >, ..., < input_par n > 
    | < output_par 1 >, ..., < output_par m > 
)
</pre>

ℹ️ In this case, the predicate definition is retrieved from memory, and an alignment must occur: input parameters of the apply $\equiv$ input parameters of the definition, and output parameters of the definition $\equiv$ output parameters of the apply. For better understanding, read [semantics.md](semantics.md)

## Small-step operatioanl semantics rules

An example rule looks like:
<pre>
@semantics(oe3){
    <`@e_1`, @s> => <`@e_3`, @s>
    ---
    <`@e_1 + @e_2`, @s> => <`@e_3 + @e_2`, @s>
}
</pre>
And it originated from the following form:
<pre>
@semantics(< rule name >){
    < transition 1 / apply predicate 1 >
    ...
    < transition n / apply predicate n >
    ---
    < main transition >
}
</pre>

where the transition has one of 2 forms: (here extenal symbols '<', '>' are not ignored)
<pre>
'<' < construction 1 > , < program state 1 > '>' => '<' < construction 2 > , < program state 2 > '>'
'<' construction 1 > , < program state 1 '>' => < program state 2 >
</pre>
First transition is from configuration to configuration, second to only program state. 
Therefore, we can say that the example rule indicates the occurrence of a transition under the condition of another one happening in the upper part of the rule. In this case, it is simplifying the first argument in the construction notation as addition.

## Typing rules

An example rule looks like:
<pre>
@typing(te1){
    ---
    @G |- `@e` : `unit`
}
</pre>

And it originated from the following form:
<pre>
@typing(< rule name >){
    < typing 1 / apply predicate 1 >
    ...
    < typing n / apply predicate n >
    ---
    < main typing >
}
</pre>

where the typing has forms:
<pre>
< Gamma > |- < construction 1 > < rel > < construction 2 >
</pre>

Typing is an important aspect of a programming language and here is checked for every encountered syntactic construction. This is done by checking whether a given construction is of type \`unit\`. The example presented above states that from any context, we know that any non-terminal `e` is of type 'unit'.

## Important facts

Before we consider the last elements of the language, let's discuss a few more important pieces of information about the interpreter to have a greater awareness.

- You can set certain interpreter / debugger values to make it work according to your preferences, more information at [config.md](./config.md).
- You can instruct the parser to read an unprocessed construction as a specific non-terminal by using the notation: <pre>< non-terminal name >\`unprocessed construction\` </pre> By default, it always reads from the 'sp' non-terminal, so make sure that all your unprocessed constructions in the program have a fully derivable parsing tree so that they can become constructions.
- Elements of the program are processed sequentially, ensure that during processing, syntax is defined before its use in rules, and the executed code runs after the definition of used predicates and rules.
- Program state is [< store >, < Gamma >] 
- If you want to have better understanding of interpreter, read other documents in [docs](../docs/).

## Code

Example:

<pre>
@code`s(s(0)) + s(0) + 0 + s(0)`
</pre>

And it originated from the following form:

<pre>
@code`unprocessed construction`
</pre>

The code is processed to construction, and then rules from operational semantics are applied to it until reaching the final configuration.

## Block

A block allows isolating fragments of the program so that they have separate syntax, semantic, typing rules, and predicate definitions. When opening a block, we have a copy of existing rules, and when exiting it, we restore the state of rules at the entrance. This removes the influence of rules created inside the block on program elements outside the block.

Form of block:
<pre>
{
    < program >
}
</pre>

Easy example of use: [test_02.txt](../programs/original_02.txt).

## Full example and interpretation

<pre>
@syntax(sp){sp: e | t}
@syntax(e){e: /0/ | /s/ "(" e ")" | e /\+/ e}
@syntax(t){t: /unit/}

@typing(te1){
    ---
    @G |- `@e` : `unit`
}

@typing(te2){
    ---
    @G |- `@sp` : `unit`
}

@semantics(oe1){
    ---
    <`@e_1 + s(@e_2)`, @s> => <`s(@e_1) + @e_2`, @s>
}

@semantics(oe2){
    ---
    <`@e_1 + 0`, @s> => <`@e_1`, @s>
}

@semantics(oe3){
    <`@e_1`, @s> => <`@e_3`, @s>
    ---
    <`@e_1 + @e_2`, @s> => <`@e_3 + @e_2`, @s>
}

@semantics(oe4){
    <`@e_2`, @s> => <`@e_3`, @s>
    ---
    <`@e_1 + @e_2`, @s> => <`@e_1 + @e_3`, @s>
}

update(`s(@e)`, @s_1 | `@e`, @s_2)`
s_2 = s_1
if type(s_2[1]) != int:
    s_2[1] = 1
else:
    s_2[1] += 1
`
@semantics(transferOneToken){
    update(`@e_1`, @s_1 | `@e_2`, @s_2)
    ---
    <`@e_1`, @s_1> => <`@e_2`, @s_2>
}

@semantics(end){
    ---
    <`0`, @s> => @s
}

@code`s(s(0)) + s(0) + 0 + s(0)`
@code`0 + s(s(s(0)))`
</pre>

1. Add the syntax rule sp: `sp - subprogram` can be either `e - expression` or `t - type`.
2. Add the syntax rule e: `e - expression` can be `0 - zero`, `s(e) - successor of e` or `e + e - addition of two expressions`
3. Add the syntax rule t: `t - type` is always `unit - the most general type`
4. Add typing rule te1: All expressions are unit type.
5. Add typing rule te2: All subprograms are unit type.
6. Add semantics rule oe1: If the second operand of addition is the successor function, move it to the left operand.
7. Add semantics rule oe2: If the second operand of addition is zero, keep only the left operand.
8. Add semantics rule oe3: Simplify the left operand of addition if possible.
9. Add semantics rule oe4: Simplify the right operand of addition if possible.
10. Add predicate definition: Retrieve the value from the state and increment it by 1, also taking away one successor from the input parameter in the process.
11. Add semantics rule transferOneToken: Simplify the expression if possible using the 'update' predicate - take away one successor and increment the value from state.
12. Add semantics rule end: When the construction is 0, terminate.
13. Perform the code `s(s(0)) + s(0) + 0 + s(0)`.
14. Perform the code `0 + s(s(s(0)))`.

### Results

😎 Below, we will present the output states of the program by inserting prints into the source code. However, the presented program itself does not output anything.

state: [{}, {}], 
constr: ('sp', [('e', [('e', [('e', [('e', ['s', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['0'])]), '+', ('e', ['s', ('e', ['0'])])])])

state: [{}, {}], 
constr: ('sp', [('e', [('e', ['s', ('e', [('e', [('e', ['s', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['0'])])]), '+', ('e', ['0'])])])

state: [{}, {}], 
constr: ('sp', [('e', ['s', ('e', [('e', [('e', ['s', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['0'])])])])

state: [{}, 1], 
constr: ('sp', [('e', [('e', [('e', ['s', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['0'])])])

state: [{}, 1], 
constr: ('sp', [('e', [('e', ['s', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['s', ('e', ['0'])])])])

state: [{}, 1], 
constr: ('sp', [('e', [('e', ['s', ('e', ['s', ('e', ['s', ('e', ['0'])])])]), '+', ('e', ['0'])])])

state: [{}, 1], 
constr: ('sp', [('e', ['s', ('e', ['s', ('e', ['s', ('e', ['0'])])])])])

state: [{}, 2], 
constr: ('sp', [('e', ['s', ('e', ['s', ('e', ['0'])])])])

state: [{}, 3], 
constr: ('sp', [('e', ['s', ('e', ['0'])])])

state: [{}, 4], 
constr: ('sp', [('e', ['0'])])

state: [{}, 4], 
constr: None

state: [{}, {}], 
constr: ('sp', [('e', [('e', ['0']), '+', ('e', ['s', ('e', ['s', ('e', ['s', ('e', ['0'])])])])])])

state: [{}, {}], 
constr: ('sp', [('e', [('e', ['s', ('e', ['0'])]), '+', ('e', ['s', ('e', ['s', ('e', ['0'])])])])])

state: [{}, {}], 
constr: ('sp', [('e', [('e', ['s', ('e', ['s', ('e', ['0'])])]), '+', ('e', ['s', ('e', ['0'])])])])

state: [{}, {}], 
constr: ('sp', [('e', [('e', ['s', ('e', ['s', ('e', ['s', ('e', ['0'])])])]), '+', ('e', ['0'])])])

state: [{}, {}], 
constr: ('sp', [('e', ['s', ('e', ['s', ('e', ['s', ('e', ['0'])])])])])

state: [{}, 1], 
constr: ('sp', [('e', ['s', ('e', ['s', ('e', ['0'])])])])

state: [{}, 2], 
constr: ('sp', [('e', ['s', ('e', ['0'])])])

state: [{}, 3], 
constr: ('sp', [('e', ['0'])])

state: [{}, 3], 
constr: None