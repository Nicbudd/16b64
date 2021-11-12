# 16b64

**16b64** is an esoteric joke programming language designed to question the
fundamentality of constants in programming.

There are 10 two-byte constants in 16b64 that must be manipulated to generate
other numbers. They are numbered `0-9` and are based on the first 20 bytes of
the SHA-256 hash of "16b64".

Operations are done to a stack with 16 bit words in reverse polish notation.
The language has 64 instructions, each written with single characters. The
operations include the characters `A-Z, a-z` and loops are done with `()`,
giving 64 possible instructions.

## Examples

`5` - Puts `0x4fda` on the stack.
`2` - Puts `0xfc26` on the stack.
`N` - Bitwise NOT previous item on stack.
`a` - Add together previous two items on stack (ignore overflow).
`X` - Bitwise XOR previous two items on stack.
`5N` - Puts `0xb025` (NOT `0x4fda`) on the stack.
`22a` - Puts `0xf84c` (`0xfc26` + `0xfc26`)
`5N22aX` - Puts `0x4869` (`0xb025` XOR `0xf84c`) on the stack.
`C` - Print previous two bytes on stack to STDOUT in two 1-byte characters.
`5N22aXC` - Prints "Hi".

# Installation

## Linux

1. Clone this repo in a safe place. This can be done as follows:  
`git clone https://github.com/Nicbudd/16b64` or `gh repo clone Nicbudd/16b64`
2. Edit 16b64.sh to include the path to the *i16b64.py* file  
3. **Rename your file** to just `16b64` and move it to /usr/local/bin

## Windows

lol idk

# Usage

The interpreter can be called on terminal to run source code directly or by
reading a file.

`16b64 5r61lAaC3l33RAC7N92XlaC081lXlXC585raNXC042lANaC015AaC` -> `"Hello, World!"`
`16b64 examples/"hello world.16b"` -> `"Hello, World!"`

The interpreter ignores all whitespace and comments in the source files.
Comments are written with `#`.

The `-d` flag shows a debug mode, which prints each instruction out line by line
to show the instruction and the stack when the instruction is read.

# Reference

## Constants

`"0"` = `0x1c72`  
`"1"` = `0x14bc`  
`"2"` = `0xfc26`  
`"3"` = `0x7e37`  
`"4"` = `0xb53f`  
`"5"` = `0x4fda`  
`"6"` = `0x20fe`  
`"7"` = `0x445a`  
`"8"` = `0xb76a`  
`"9"` = `0x25e5`  

## Instructions

Where `x` and `y` are referenced, `x` is the first item on the stack and `y` is
the second item on the stack. Instructions are case sensitive.

`A`	x AND y
`B`
`C`	push x to STDOUT as two ASCII char
`D`	duplicate x
`E`
`F`	find value x positions down in the stack and move it to the top
`G`
`H`
`I`	push STDIN to stack
`J`
`K`
`L`	x cyclic shift left by y places
`M`
`N`	NOT x
`O`	x OR y
`P`
`Q`
`R`	x cyclic shift right by y places
`S`	swaps x, y on stack
`T`
`U`	push x to STDOUT as Unicode
`V`	push yx to STDOUT as Unicode
`W`
`X`	x XOR y
`Y`	Pull bottom of stack to top of stack
`Z`	Push x to bottom of stack
`a`	x + y, set flag true if overflow
`b`	flag = LSB of x
`c`	x < y, set flag to result
`d`	delete x
`e`	x == y, set flag to result
`f`	find value x%16 positions down in the stack and move it to the top (4 bit version of F)
`g`	x > y, set flag to result
`h`
`i`	invert flag
`j`
`k`
`l`	x cyclic shift left by 1
`m`
`n`
`o`
`p`
`q`
`r`	x cyclic shift right by 1
`s`
`t`
`u`
`v`
`w`
`x`
`y`
`z`
`(`	start of loop
`)`	loop if flag == TRUE
