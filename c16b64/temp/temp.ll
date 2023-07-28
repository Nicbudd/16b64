define i16 @main() {
	%1 = xor i16 46954, u0xFFFF
	%2 = and i16 46399, %1
	%3 = lshr i16 %2, 15
	%4 = shl i16 %2, 1
	%5 = or i16 %3, %4
	ret i16 %5
}