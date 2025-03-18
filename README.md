# 16b64

**16b64** is a work-in-progress esoteric joke programming language designed to question the
fundamentality of constants in programming.

Please visit [the website](https://www.nicbudd.com/16b64.html) for details, a reference guide, and an online interpreter.

# Installation

The interpreter is a command line program that has been compiled into (hopefully) statically linked binaries for both Windows and Linux. You may use those or compile the source code yourself. The interpreter is written in Rust.

There used to be a Python version of the interpreter, however it is now depreciated, the Rust interpreter is the latest version.

## From Binaries

Download the latest version from the [releases tab](https://github.com/Nicbudd/16b64/releases).

1. Download the proper executable or binary for your system (`i16b64_x86_64-pc-windows-msvc.exe` for Windows, `i16b64_x86_64-unknown-linux-musl` for Linux).

2. Rename to `i16b64` (recommended)

3. Move `i16b64` to $PATH (for example, ~/.cargo/bin or /usr/local/bin on Linux, or C:/Users/(username)/.cargo/bin on Windows).

4. Test: Open a terminal or command prompt and type `i16b64 7C`. It should print `DZ`.

## From Source Code

1. Install rust at the rust-lang.org website.

2. Download the source code: either clone this repo (`git clone https://github.com/Nicbudd/16b64` or `gh repo clone Nicbudd/16b64`) or download it from the releases tab.  

3. Compile the program in the `i16b64` folder with `cargo`. Cargo should come preinstalled with `rustup` automatically:  
`cd 16b64/i16b64`  
`cargo build --release`  

4. Copy `i16b64` to $PATH (for example, ~/.cargo/bin or /usr/local/bin on Linux, or C:/Users/(username)/.cargo/bin on Windows):  
(Linux) `sudo cp target/release/i16b64 /usr/local/bin`  


### Windows / MacOS

lol figure it out idk


# Usage

The interpreter can be called on terminal to run source code directly or by
reading a file.  

`16b64 5r61lAaC3l33RAC7N92XlaC081lXlXC585raNXC042lANaC015AaC` -> "Hello, World!"  
`i16b64 5r61lAaC3l33RAC7N92XlaC081lXlXC585raNXC042lANaC015AaC` -> "Hello, World!"  

`16b64 examples/helloWorld.16b` -> "Hello, World!"  
`i16b64 -f examples/helloWorld.16b` -> "Hello, World!"  

Options:  

```
  -d, --debug       - debug mode: prints debug information for each step of the execution
  -f, --file [file] - read file and execute as code
  -s, --safe        - safe mode: prevents infinite loops, loops greater than 10,000 iterations.
  -h, --help        - prints help message
```

Please note that flags can't currently be combined, such as `-ds`. This will hopefully be fixed soon.  

The interpreter ignores all whitespace and comments in the source files.
Comments are written with `#`.
