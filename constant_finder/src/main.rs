// Work in Progress
use std::fs::File;
use std::io::prelude::*;

const CONSTS: [u16; 10] = [
0x1c72,
0x14bc,
0xfc26,
0x7e37,
0xb53f,
0x4fda,
0x20fe,
0x445a,
0xb76a,
0x25e5];


fn interpret(code: &str) -> u16 {

    let safe = true;
    let mut stack: Vec<u16> = Vec::new();
    let mut flag = false;

    let mut skip_loop = false;
    let mut loop_stack = vec![];
    let mut loop_iterations = 0;
    let mut parenthesis = 0;

    let mut end_of_loop = false;

    let code_chars: Vec<_> = code.chars().clone().collect(); //cause strings in UTF8 are weird.

    let mut i = -1;

    while !end_of_loop {

        i += 1; // increment loop

        let c = match code_chars.get(i as usize) {
            Some(val) => *val,
            None => break,
        };

        // loop handling
        if c == '(' {
            if !flag {skip_loop = true;} // skip loop if not flag

            if skip_loop {
                parenthesis += 1; // count amount of left parenthesis

            } else {
                loop_stack.push(i); // push current index to loop stack
            }

        } else if c == ')' {
            if skip_loop {
                parenthesis -= 1; // remove right parenthesis

                if parenthesis == 0 { // if out of the nest (amt. left parenthesis == amt. right parenthesis)
                    skip_loop = false; // stop skipping
                }

            // otherwise we're in the loop
            } else if safe && loop_iterations > 10000 { // safe mode infinite loop protection
                    panic!("Safe Mode Error: Too many loop repetitions.");

            // restart loop if flag, otherwise end loop
            } else if flag { // go back to beginning of loop
                loop_iterations += 1; // add to count of amt of loops done
                // loop back
                i = loop_stack.pop().expect("Interpreter Error: No items on loop stack") - 1;

            } else { // end loop
                // remove loop pointer from stack
                loop_stack.pop().expect("Interpreter Error: No items on loop stack");

            }
        }

        if !skip_loop {

            let c_int: isize = c as isize - 48; // convert char to int (for integer instructions)
            if c_int < 10 && c_int >= 0 {
                let c_int: usize = c_int as usize;
                stack.push(CONSTS[c_int]);

            } else {
                match c {
                    'A' => {
                        let x = stack.pop().expect("No items on stack to add.");
                        let y = stack.pop().expect("Not enough items on stack to add.");
                        stack.push(x & y);
                    },

                    'D' => {
                        let x = stack.pop().expect("No items on stack to duplicate.");
                        stack.push(x);
                        stack.push(x);
                    },

                    'L' => {
                        let x = stack.pop().expect("No items on stack to shift.") as u32;
                        let y = stack.pop().expect("Not enough items on stack to shift.");
                        stack.push(y.rotate_left(x));
                    },

                    'M' => {
                        let x = stack.pop().expect("No items on stack to take modulus of.");
                        let y = stack.pop().expect("Not enough items on stack to perform modulo operation.");
                        stack.push(y % x);
                    },

                    'N' => {
                        let x = stack.pop().expect("No items on stack to preform NOT operation on.");
                        stack.push(!x);
                    },

                    'O' => {
                        let x = stack.pop().expect("No items on stack to take modulus of.");
                        let y = stack.pop().expect("Not enough items on stack to perform modulo operation.");
                        stack.push(x | y);
                    },

                    'R' => {
                        let x = stack.pop().expect("No items on stack to shift.") as u32;
                        let y = stack.pop().expect("Not enough items on stack to shift.");
                        stack.push(y.rotate_right(x));
                    },

                    'S' => {
                        let x = stack.pop().expect("No items on stack to take modulus of.");
                        let y = stack.pop().expect("Not enough items on stack to perform modulo operation.");
                        stack.push(x);
                        stack.push(y);
                    },

                    'X' => {
                        let x = stack.pop().expect("No items on stack to XOR.");
                        let y = stack.pop().expect("Not enough items on stack to XOR.");
                        stack.push(x ^ y);
                    },

                    'a' => {
                        let x = stack.pop().expect("No items on stack to add.");
                        let y = stack.pop().expect("Not enough items on stack to add.");
                        let sum = x.overflowing_add(y);
                        flag = sum.1;
                        let sum = sum.0;

                        stack.push(sum);
                    },

                    'b' => {
                        let x = stack.pop().expect("No items on stack to use as flag.");
                        flag = (x % 2) == 1; // will return true if LSB is 1, otherwise will return false
                        stack.push(x);
                    },

                    'c' => {
                        let x = stack.pop().expect("No items on stack to compare.");
                        let y = stack.pop().expect("Not enough items on stack to compare.");
                        flag = x < y;
                        stack.push(y);
                        stack.push(x);
                    },

                    'd' => {
                        let _x = stack.pop().expect("No items on stack to delete.");
                    },

                    'e' => {
                        let x = stack.pop().expect("No items on stack to compare.");
                        let y = stack.pop().expect("Not enough items on stack to compare.");
                        flag = x == y;
                        stack.push(y);
                        stack.push(x);
                    },

                    'f' => {
                        let x = stack.pop().expect("No items on stack to duplicate.");
                        let l = stack.len();
                        let index = l - ((x as usize) % 16) - 1;

                        match stack.get(index) {
                            Some(_) => {
                                let y = stack.remove(index);
                                stack.push(y);
                            },
                            None => {
                                flag = true;
                            }
                        }
                    },

                    'g' => {
                        let x = stack.pop().expect("No items on stack to compare.");
                        let y = stack.pop().expect("Not enough items on stack to compare.");
                        flag = x > y;
                        stack.push(y);
                        stack.push(x);
                    },

                    'i' => {
                        flag = !flag;
                    },

                    'l' => {
                        let x = stack.pop().expect("No items on stack to shift.");
                        stack.push(x.rotate_left(1));
                    },

                    'r' => {
                        let x = stack.pop().expect("No items on stack to shift.");
                        stack.push(x.rotate_right(1));
                    },

                    'p' => {
                        let x = stack.pop().expect("No items on stack to find.");
                        let y = stack.pop().expect("No items on stack to find.");

                        let l = stack.len();
                        let index = l - ((x as usize) % 16);
                        match stack.get(index) {
                            Some(_) => {
                                stack.insert(index, y);
                            },

                            None => {flag = true;}
                        }
                    },

                    '(' | ')' => {}

                    _ => {panic!("Unrecogniz
99rrO64aOed character '{}'", c)},

                }
            }
        }
    }
    stack[stack.len() - 1]
}

fn main() {
    // stats
    let mut generated_consts = 0;
    let mut unique = 0;
    let mut tot_unique = 0;
    let mut new_best = 0;
    const LIST_SIZE: usize = (1 << 16);


    // initialize our list of all constants
    let mut constants_list: Vec<String> = vec![String::from(""); 1 << 16];

    // initialize three constant lists
    let mut prev_constants: Vec<String> = vec![];
    // initialize primitive constants
    for num in 0..10 {
        prev_constants.push(num.to_string());
    }
    let mut new_constants: Vec<String> = vec![];
    let mut all_constants: Vec<String> = prev_constants.clone();

    for depth in 0..2 {


        let mut step1_constants: Vec<String> = vec![];

        println!("{:?}", prev_constants);

        for c in &mut prev_constants.iter() {

            println!("{}", c);

            for char in ["l", "ll", "r", "rr", "N"] {
                let s: String = String::from("") + c + &char.to_string();
                step1_constants.push(s);
                generated_consts += 1;
            }
        }

        new_constants.append(&mut step1_constants.clone());


        let mut first_terms: Vec<String> = step1_constants.clone();
        first_terms.append(&mut prev_constants);

        for c in &mut first_terms.clone().iter() {

            println!("{}", c);

            let mut second_terms: Vec<String> = all_constants.clone();
            second_terms.append(&mut step1_constants);
            let mut second_terms_iter = second_terms.iter();

            let mut step2_constants: Vec<String> = vec![];

            for char in ["a", "A", "X", "O"] {
                for c2 in &mut second_terms_iter.clone() {
                    let s: String = String::from("") + c + &c2 + &char.to_string();
                    step2_constants.push(s);
                    generated_consts += 1;
                }
            }

            new_constants.append(&mut step2_constants);

        }
        
        println!("determining values...");

        for c in &new_constants {
            let value = interpret(c) as usize;

            let mut old_const = &mut constants_list[value];
            let mut old_const_list = old_const.split(", ");
            let best = old_const_list.nth(0).expect("String parse error");

            if best.len() == 0 {
                *old_const = String::from(c);
                unique += 1;

            } else if best.len() > c.len() {
                *old_const = String::from(c);
                new_best += 1;

            } else if best.len() == c.len() {
                old_const.push_str(", ");
                old_const.push_str(c);

            } // else our old result was better
        }
        tot_unique += unique;

        println!("Depth: {}, Unique: {}, Total Unique: {}, Improvements: {}", depth, unique,
        tot_unique, new_best);

        prev_constants = new_constants.clone(); // clone the vector
        all_constants.append(&mut prev_constants.clone()); // clone the vector
        new_constants = vec![]; // clear the vector
        new_best = 0;
        unique = 0;

    }

    let path = "constants.txt";
    let mut output = File::create(path).expect("Could not create file.");

    for c in constants_list.iter().enumerate() {
        let print_str = format!("{:#06X} - {}", c.0, c.1);
        //println!("{}", &print_str);
        write!(&output, "{}\n", &print_str);
    }

    /*

    */

    let code = "01a";

    // main call to interpret

}
