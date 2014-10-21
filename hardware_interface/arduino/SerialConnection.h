#ifndef __SerialConnection_h__
#define __SerialConnection_h__

#include <Arduino.h>
#define SWBUFMAX    512
#define SWDIGITAL   1
#define SWANALOG    2
#define SWPWM       3

class SerialConnection {
public:
  SerialConnection(char *device_name, int baudrate);
  void update(void);
  int addOutput(char *name, char type);
  int addInput(char *name, char type);
  void sendMessage(char *message);

  char id[256];
  int *input_value;
  int input_length;
  int *output_value;
  int output_length;
private:
  void parseMessage(char *message);
  void getInfo(void);
  void getValues(void);
  void setValues(char *msg);

  char readbuf[SWBUFMAX];
  int buflen;

  char **input_name;
  char *input_type;
  char **output_name;
  char *output_type;
};

#endif
