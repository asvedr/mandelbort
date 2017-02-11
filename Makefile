CC=gcc -fPIC -std=c99 -O2 -shared -Wall

all:
	$(CC) calc.c -o libcalc.so
