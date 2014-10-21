CCFLAGS = -ansi -Wall -pedantic -Werror -pthread

all: controller.o libcontroller.so.1

controller.o: controller.c
	gcc ${CCFLAGS} -c controller.c

libcontroller.so.1: libcontroller.o
	gcc ${CCFLAGS} -shared libcontroller.o -o libcontroller.so.1

libcontroller.o: controller.c
	gcc ${CCFLAGS} -fPIC -c controller.c -o libcontroller.o

clean:
	rm -f *.o *.so.*
