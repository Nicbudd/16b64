# 16b64

**16b64** is a work-in-progress esoteric joke programming language designed to question the
fundamentality of constants in programming.

Please visit [the website](https://www.nicbudd.com/16b64.html) for details, a reference guide, and an online interpreter.

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
