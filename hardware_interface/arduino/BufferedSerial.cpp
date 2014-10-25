#include "stdlib.h"
#include "string.h"
#include "SerialConnection.h"

/* Custom class for the Serial communication */

SerialConnection::SerialConnection(char *device_name, int baudrate) {
  strcpy(id, device_name);
  memset(readbuf, 0, SWBUFMAX * sizeof(char));
  buflen = 0;

  input_name = NULL;
  input_type = NULL;
  input_value = NULL;
  input_length = 0;

  output_name = NULL;
  output_type = NULL;
  output_value = NULL;
  output_length = 0;

  Serial.begin(baudrate);
}

void SerialConnection::update(void) {
  int bytestoread;
  char *s, *e;
  char *message;

  while ((bytestoread = Serial.available()) > 0) {
    /* Check buffer overflow */
    if (buflen + bytestoread >= SWBUFMAX) {
      buflen -= SWBUFMAX / 2;
      memmove(readbuf,
              &readbuf[SWBUFMAX / 2],
              buflen);
    }
    
    /* Read buffer bytes */
    Serial.readBytes(&readbuf[buflen], bytestoread);
    buflen += bytestoread;
    readbuf[buflen] = '\0';

    /* Parse message */
    e = strrchr(readbuf, "\n");
    if (e == NULL)
      continue;
    for (s = e; s > readbuf, && s[0] != '\n'; s--) ;
    if (s[0] == '\n')
      s++;
    buflen -= (int)(s - readbuf)
    memmove(readbuf, s, buflen);
    readbuf[buflen] = '\0';
    message = (char *)malloc((int)(e - s + 1) * sizeof(char));
    strncpy(message, readbuf, (int)(e - s));
    message[(int)(e - s)] = '\0';
    parseMessage(message);
    free(message);
  }
}

int SerialConnection::addOutput(char *name, char type) {
  char **old_name;
  char *old_type;
  int *old_value;
  old_name = output_name;
  old_type = output_type;
  old_value = output_value;
  output_length++;
  output_name = (char **)malloc(output_length * sizeof(char *));
  output_type = (char *)malloc(output_length * sizeof(char));
  output_value = (int *)malloc(output_length * sizeof(int));
  if (old_name) free(old_name);
  if (old_type) free(old_type);
  if (old_value) free(old_value);
  output_name[output_length - 1] = name;
  output_type[output_length - 1] = type;
  output_value[output_length - 1] = 0;
  return output_length - 1;
}

int SerialConnection::addInput(char *name, char type) {
  char **old_name;
  char *old_type;
  int *old_value;
  old_name = input_name;
  old_type = input_type;
  old_value = input_value;
  input_length++;
  input_name = (char **)malloc(input_length * sizeof(char *));
  input_type = (char *)malloc(input_length * sizeof(char));
  input_value = (int *)malloc(input_length * sizeof(int));
  if (old_name) free(old_name);
  if (old_type) free(old_type);
  if (old_value) free(old_value);
  input_name[input_length - 1] = name;
  input_type[input_length - 1] = type;
  input_value[input_length - 1] = 0;
  return input_length - 1;
}

void SerialConnection::sendMessage(char *message) {
  Serial.print(message);
}

void SerialConnection::parseMessage(char *message) {
  char *msg;
  if (strstr(message, "info")) {
    getInfo();
  } else if ((msg = strstr(message, "get")) != NULL) {
    getValues();
  } else if ((msg = strstr(message, "set")) != NULL) {
    setValues(&msg[4]);
  }
}

void SerialConnection::getInfo(void) {
  char buffer[128];
  int i;
  sprintf(buffer, "{\"id\":\"%s\"", id);
  Serial.print(buffer);
  Serial.print(",\"outputs\":[");
  for (i = 0; i < output_length; i++) {
    sprintf(buffer, "[\"%s\",%d]",
        outputs[i], output_type[i]);
    if (i < output_length - 1)
      strcat(buffer, ",");
    Serial.print(buffer);
  }
  Serial.print("],\"inputs\":[");
  for (i = 0; i < input_length; i++) {
    sprintf(buffer, "[\"%s\",%d]",
        inputs[i], input_type[i]);
    if (i < input_length - 1)
      strcat(buffer, ",");
    Serial.print(buffer);
  }
  Serial.print(buffer, "]}\n");
}

void SerialConnection::getValues(void) {
  int i;
  int numbytes;
  char *buffer;
  char temp[16];
  numbytes = 0;
  for (i = 0; i < input_length; i++) {
    switch (input_type[i]) {
      case SWDIGITAL:
        numbytes++;
        break;
      case SWANALOG:
        numbytes += 5;
        break;
      case SWPWM:
        numbytes += 5;
        break;
    }
  }
  buffer = (char *)malloc(numbytes + 2);
  for (i = 0; i < input_length; i++) {
    switch (input_type[i]) {
      case SWDIGITAL:
        sprintf(temp, "%1d", input_value[i]);
        strcat(buffer, temp);
        break;
      case SWANALOG:
        sprintf(temp, "%5d", input_value[i]);
        strcat(buffer, temp);
        break;
      case SWPWM:
        sprintf(temp, "%5d", input_value[i]);
        strcat(buffer, temp);
        break;
    }
  }
  strcat(buffer, "\n");
  Serial.print(buffer);
  free(buffer);
}

void SerialConnection::setValues(char *msg) {
  int i;
  int numbytes;
  char temp[16];
  for (i = 0; i < output_length; i++) {
    switch (output_type[i]) {
      case SWDIGITAL:
        numbytes++;
        break;
      case SWANALOG:
        numbytes += 5;
        break;
      case SWPWM:
        numbytes += 5;
        break;
    }
  }
  if (strlen(msg) < numbytes)
    return;
  for (i = 0; i < output_length; i++) {
    switch (output_type[i]) {
      case SWDIGITAL:
        strncpy(temp, msg, 1);
        temp[1] = '\0';
        output_value[i] = atoi(temp);
        msg++;
        break;
      case SWANALOG:
        strncpy(temp, msg, 5);
        temp[4] = '\0';
        output_value[i] = atoi(temp);
        msg += 4;
        break;
      case SWPWM:
        strncpy(temp, msg, 5);
        temp[4] = '\0';
        output_value[i] = atoi(temp);
        msg += 4;
        break;
    }
  }
}
