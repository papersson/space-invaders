#!/bin/sh
# A build where main.c includes util.h, but the Makefile only lists main.c as a prerequisite.
# Change util.h and run make: make sees nothing out of date, and the program keeps the old value.
# Then declare the header (or let the compiler record it with -MMD) and run again.
set -e
D=$(mktemp -d); cd "$D"
printf '#define SHIPPING_THRESHOLD 65\n' > util.h
printf '#include <stdio.h>\n#include "util.h"\nint main(void){printf("free shipping from $%%d\\n", SHIPPING_THRESHOLD);return 0;}\n' > main.c
printf 'app: main.c\n\tcc -o app main.c\n' > Makefile
echo "--- Makefile: app depends on main.c only"; cat Makefile
make -s; ./app
sleep 1; printf '#define SHIPPING_THRESHOLD 75\n' > util.h
echo "--- util.h changed to 75; make:"; make; ./app
printf 'app: main.c util.h\n\tcc -o app main.c\n' > Makefile
echo "--- Makefile now also lists util.h; make:"; make; ./app
