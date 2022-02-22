# 16b64

**16b64** is a work-in-progress esoteric joke programming language designed to question the
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
`22a` - Puts `0xf84c` (`0xfc26` + `0xfc26`) on the stack.  
`5N22aX` - Puts `0x4869` (`0xb025` XOR `0xf84c`) on the stack.  
`C` - Print previous two bytes on stack to STDOUT in two 1-byte characters.  
`5N22aXC` - Prints "Hi".  

## Versions

For now there are two implementations of the interpreter with slightly different actions: one in **Rust** and one in **Python**. The Python version is the original, but it's now a little behind and is being depreciated soon. If you can install the Rust version, please do so.  

# Installation

## Linux

1. Clone this repo. This can be done as follows:  
`git clone https://github.com/Nicbudd/16b64` or `gh repo clone Nicbudd/16b64`  

### Rust

2. Install `rustup`. Currently the preferred method by the rust-lang.org website is:  
`curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh`  
3. Compile the program in the `i16b64` folder with `cargo`. Cargo should come preinstalled with `rustup` automatically:  
`cd 16b64/i16b64`  
`cargo build --release`  

4. Copy `i16b64` to /usr/local/bin:  
`sudo cp target/release/i16b64 /usr/local/bin`  

### Python

2. Edit 16b64.sh to include the path to the *i16b64.py* file.  
3. **Rename 16b64.sh** to just `16b64` and move it to /usr/local/bin  


## Windows / MacOS

lol figure it out idk

# Usage

The Rust version of the interpreter is called as and referred to as `i16b64` and the Python version is `16b64`.  

The interpreter can be called on terminal to run source code directly or by
reading a file.  

`16b64 5r61lAaC3l33RAC7N92XlaC081lXlXC585raNXC042lANaC015AaC` -> "Hello, World!"  
`i16b64 5r61lAaC3l33RAC7N92XlaC081lXlXC585raNXC042lANaC015AaC` -> "Hello, World!"  

`16b64 examples/helloWorld.16b` -> "Hello, World!"  
`i16b64 -f examples/helloWorld.16b` -> "Hello, World!"  

**Python** Options:  

```
  -d - debug mode: prints debug information for each step of the execution
  -s - safe mode: prevents infinite loops, loops greater than 10,000 iterations.
```

**Rust** Options:  

```
  -d, --debug       - debug mode: prints debug information for each step of the execution
  -f, --file [file] - read file and execute as code
  -s, --safe        - safe mode: prevents infinite loops, loops greater than 10,000 iterations.
  -h, --help        - prints help message
```

Please note that flags can't currently be combined, such as `-ds`. This will hopefully be fixed soon.  

The interpreter ignores all whitespace and comments in the source files.
Comments are written with `#`.

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
`P` move y to x positions down in the stack.  
`Q`  
`R`	x cyclic shift right by y places  
`S`	swaps x, y on stack  
`T`  
`U`	push x to STDOUT as Unicode  
`V`	push yx to STDOUT as Unicode  
`W`  
`X`	x XOR y  
`Y`  
`Z`  
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
`p` move y to x%16 positions down in the stack. (4 bit version of P)  
`q` randomly set flag to true or false  
`r`	x cyclic shift right by 1  
`s`  
`t`  
`u`  
`v`  
`w`  
`x`  
`y`	pull bottom of stack to top of stack  
`z`	push x to bottom of stack  
`(`	start of loop  
`)`	loop if flag == TRUE  
