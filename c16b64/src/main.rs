use clap::Parser;

use std::io::{stdin, Read};
use std::path::PathBuf;
use std::fs::{read_to_string, remove_file};
use std::fs;
use std::process::Command;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The input .16b file that needs to be compiled. If no proper file is provided, uses stdin.
    #[arg(short, long)]
    input_file: Option<PathBuf>,

    /// The name of the executable to be written output
    #[arg(short, long)]
    output_file: PathBuf,
}

fn main() {
    let args = Args::parse();

    // todo: optimization flags for clang

    let code_string = match args.input_file {
        None => {
            let mut buffer = String::new();
            stdin().read_to_string(&mut buffer);
            buffer
        }
        Some(p) => {
            match read_to_string(p) {
                Ok(s) => s,
                Err(_) => {
                    println!("Input file could not be accessed");
                    std::process::exit(1);
                }
            }

        }
    };

    let compiled = compile(code_string.as_str());


    fs::write("temp/temp.ll", compiled).expect("Unable to write to the output file.");

    let output = Command::new("clang")
        .arg("temp/temp.ll")
        .arg("-o")
        .arg(args.output_file)
        .output()
        .expect("Call to clang didn't work. Perhaps it is not installed?");

    let out = output.stdout;
    let out_string = String::from_utf8(out).unwrap();

    let eout = output.stderr;
    let eout_string = String::from_utf8(eout).unwrap();

    println!("{}", out_string);
    eprintln!("{}", eout_string);


    //remove_file("temp/temp.ll").ok();


}

fn constants(c: char) -> u16 {
    match c {
        '0' => 0x1c72,
        '1' => 0x14bc,
        '2' => 0xfc26,
        '3' => 0x7e37,
        '4' => 0xb53f,
        '5' => 0x4fda,
        '6' => 0x20fe,
        '7' => 0x445a,
        '8' => 0xb76a,
        '9' => 0x25e5,
        _ => panic!("Unexpected char in constants.")
    }
}

// stack

#[derive(Clone, Copy)]
enum VirtualReg {
    Constant(u16),
    Register(u32),
}

impl VirtualReg {
    fn allocate_reg(register_num: &mut u32) -> VirtualReg {
        *register_num += 1;
        VirtualReg::Register(*register_num - 1)
    }

    fn name(&self) -> String {
        match self {
            Self::Constant(c) => {c.to_string()},
            Self::Register(r) => {format!("%{}", r)},
        }
    }
}

struct State {
    stack: Vec<VirtualReg>,
    register_num: u32,
}

impl State {

    fn arithmetic_line_gen(&mut self, main_str: &mut String, action: &str) {
        let new_reg = VirtualReg::allocate_reg(&mut self.register_num);
        let a = self.stack.pop().expect("Tried to do operation on empty stack");
        let b = self.stack.pop().expect("Tried to do operation on empty stack");
        self.stack.push(new_reg);

        let new_str = format!("\t{} = {} i16 {}, {}\n", new_reg.name(), action, a.name(), b.name());
        main_str.push_str(new_str.as_str());
    }

    fn modify_line_gen(&mut self, main_str: &mut String, action: &str) {
        let new_reg = VirtualReg::allocate_reg(&mut self.register_num);
        let a = self.stack.pop().expect("Tried to do operation on empty stack");
        self.stack.push(new_reg);

        let new_str = format!("\t{} = {} i16 {}\n", new_reg.name(), action, a.name());
        main_str.push_str(new_str.as_str());
    }

    fn not_line_gen(&mut self, main_str: &mut String) {

        let new_reg = VirtualReg::allocate_reg(&mut self.register_num);
        let a = self.stack.pop().expect("Tried to do operation on empty stack");
        self.stack.push(new_reg);

        let new_str = format!("\t{} = xor i16 {}, u0xFFFF\n", new_reg.name(), a.name());
        main_str.push_str(new_str.as_str());
    }


    fn rotl_line_gen(&mut self, main_str: &mut String) {

        // %10 = lshr i16 %input, 15   ; get first bit and shift it to the last bit
        // %11 = shl i16 %input, 1     ; shift left 1 bit (last bit will be zero)
        // %output = or i16 %10 %11    ; or them

        let temp_reg_1 = VirtualReg::allocate_reg(&mut self.register_num);
        let temp_reg_2 = VirtualReg::allocate_reg(&mut self.register_num);
        let new_reg = VirtualReg::allocate_reg(&mut self.register_num);

        let a = self.stack.pop().expect("Tried to do operation on empty stack");

        self.stack.push(temp_reg_1);
        self.stack.push(temp_reg_2);
        self.stack.push(new_reg);


        let new_str = format!("\t{} = lshr i16 {}, 15\n", temp_reg_1.name(), a.name());
        main_str.push_str(new_str.as_str());

        let new_str = format!("\t{} = shl i16 {}, 1\n", temp_reg_2.name(), a.name());
        main_str.push_str(new_str.as_str());

        let new_str = format!("\t{} = or i16 {}, {}\n", new_reg.name(), temp_reg_1.name(), temp_reg_2.name());
        main_str.push_str(new_str.as_str());
    }


}




// eats in 16b64 and shits out LLVM IR 
fn compile(code_string: &str) -> String {
    
    let mut main_str = String::from("define i16 @main() {\n");
    
    let mut state = State { stack: vec![], register_num: 1 };

    // %1 is going to contain the exit code.
    let mut exit_code_reg = VirtualReg::allocate_reg(&mut state.register_num);
    main_str.push_str("\t%1 = add i16 0, 0\n"); // lmao 

    //8N4Al - 0x002A - dec 42

    // todo: comments

    for c in code_string.chars() {
        match c {
            '0'..='9' => {
                let val = constants(c);
                let virt_reg = VirtualReg::Constant(val);
                state.stack.push(virt_reg);
            }
            'A' => {state.arithmetic_line_gen(&mut main_str, "and");}
            'D' => {
                let a = state.stack.last().expect("Tried to duplicate nothing.").clone();
                state.stack.push(a);
            }
            'E' => {main_str.push_str("\tret i16 0\n")}
            'N' => {state.not_line_gen(&mut main_str);}
            'd' => {state.stack.pop().expect("Unable to delete nothing.");}
            'l' => {state.rotl_line_gen(&mut main_str)}
            error_c => {panic!("unexpected character \"{}\" in input", c)}
        }
    }

    
    
    let last_string = format!("\tret i16 {}\n}}", exit_code_reg.name());
    main_str.push_str(last_string.as_str());

    let st = main_str;        

    println!("{}", st);

    st
}