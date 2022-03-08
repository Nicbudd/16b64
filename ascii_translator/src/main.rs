use regex::Regex;
use std::io::{self, BufRead, BufReader};
use std::fs::File;

fn main() {
    // get list of code for each of the constants from file
    let mut constants: Vec<String> = vec![String::new(); 1 << 16];


    let file = File::open("../16b64constants.txt").unwrap();
    let reader = BufReader::new(file);

    let RE = Regex::new(r"^.{9}([^,\s]+).*$").unwrap();

    let mut line_counter = 0;
    for line in reader.lines() {
        let line = line.expect("Could not read line of constants file");
        let first_code_bit = RE
            .captures_iter(&line)
            .nth(0)
            .expect("Did not find code");
        constants[line_counter] = String::from(&first_code_bit[1]);

        line_counter += 1;
    }


    // get phrase
    println!("Phrase to translate:");
    let mut phrase = String::new();
    io::stdin()
        .read_line(&mut phrase)
        .expect("Failed to read input.");

    // ask if user wants to add newline to end of phrase
    println!("Add newline \\n? [Y/n]");
    let mut newline = String::new();
    io::stdin()
        .read_line(&mut newline)
        .expect("Failed to read input.");

    if newline.starts_with('n') {
        phrase = phrase.trim_end_matches('\n').to_string();
    }

    let mut return_string = String::new();

    let mut twobyte = true;

    if phrase.is_ascii() {
        let mut c_counter = 0;
        let mut chars = phrase.chars();

        loop {
            let c1 = match chars.next() {
                Some(c) => c as usize,
                None => break
            };
            let c2 = match chars.next() {
                Some(c) => c as usize,
                None => 0 // return a null character if we run out of chars
            };

            let val = (c1 << 8) + c2; // c1 is top byte
            return_string += &constants[val];
            return_string += "C";
        }

    } else {
        for c in phrase.chars() {
            let val = c as usize;
            return_string += &constants[val];
            return_string += "U";
        }
    }



    println!("{}", return_string)

}
