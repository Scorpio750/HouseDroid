#ifndef __BufferredSerial_h__
#define __BufferredSerial_h__

#include <Arduino.h>
#define BUFMAX    512

class BufferredSerial {
public:
  BufferredSerial(char *device_name, int baudrate);
  void update(void);
  char *read(void);
  void write(char *message);

  char name[BUFMAX / 2];
  char message[BUFMAX / 2];

private:
  char readbuf[BUFMAX];
  int buflen;
};

#endif
