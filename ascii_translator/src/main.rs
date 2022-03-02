use std::env;
use std::fs;
use regex::Regex;

fn firstCodeBit(s: String) {
    let bytes = s
    .split(", ")
    .nth(0)
    .expect("Number has no code")
    .as_bytes();
}

fn main() {

    let mut constants: [&str; 1 << 16] = [""; 1 << 16];

    let contents = fs::read_to_string("16b64constants.txt")
        .expect("Could not read file. Oops!");

    let mut lines = contents.lines();

    let RE = Regex::new(r".{9}([^,\s]),").unwrap();

    for line in lines.enumerate() {
        let first_code_bit = RE.captures_iter().nth(0).except("Did not find code.");

        constants[line.0] = first_code_bit;
        println!("{}", constants[line.0]);
    }

}
