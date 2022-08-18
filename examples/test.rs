fn main() {
    for n in 0..=65535 {
        let mut q: u16;

        q = (n >> 1) + (n >> 2);
        q = q + (q >> 4);
        q = q + (q >> 8);
        //q = q + (q >> 16);
        q = q >> 3;
        let r: u16 = n - (((q << 2) + q) << 1);
        let out: u16 = q + ((r + 6) >> 4);

        if out != (n / 10) {
            println!("Fails! {} gives {}", n, out);
        }

        //println!("{} gives {}", n, out);
    }

}
