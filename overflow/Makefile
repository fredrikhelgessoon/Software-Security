all:
	sudo gcc -o overflow overflow.c -fno-stack-protector -m32  -no-pie -z execstack
	sudo chmod 4755 overflow
aslr_off:
	echo 0 | sudo tee /proc/sys/kernel/randomize_va_space
aslr_on:
	echo 2 | sudo tee /proc/sys/kernel/randomize_va_space
