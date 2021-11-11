# 16b64

**16b64** is an esoteric joke programming language designed to question the fundamentality of constants in programming. 

There are 10 two-byte constants in 16b64 that must be manipulated to generate other numbers. They are numbered `0-9` and are based on the first 20 bytes of the SHA-256 hash of "16b64". 

Operations are done to a stack with 16 bit words in reverse polish notation. The language has 64 instructions, each written with single characters. The operations include the characters `A-Z, a-z` and loops are done with `()`, giving 64 possible instructions

## Constants:

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

## Examples:
`7` - Puts `0x445a` on the stack.  
`9` - Puts `0x25e5` on the stack.  
`r` - Rotates previous stack item right by one.  
`A` - logical AND two previous stack items.  
`79rA` - puts `0x005a` on stack.  
`79rAC` - puts "R" (ASCII `0x5a`) to <stdout>.  
