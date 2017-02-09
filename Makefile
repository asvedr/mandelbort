CC=gcc -O2 -shared -Wall

all:
	$(CC) calc.c -o libcalc.so
