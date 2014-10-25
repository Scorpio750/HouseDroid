#include "stdlib.h"
#include "string.h"
#include "bufser.h"

/* Custom class for the Serial communication */

BufferredSerial::BufferredSerial(char *device_name, int baudrate) {
  strcpy(name, device_name);
  memset(readbuf, 0, BUFMAX * sizeof(char));
  buflen = 0;

  Serial.begin(baudrate);
}

void BufferredSerial::update(void) {
  int bytestoread;
  char *s, *e;

  while ((bytestoread = Serial.available()) > 0) {
    /* Check buffer overflow */
    if (buflen + bytestoread >= BUFMAX) {
      buflen -= BUFMAX / 2;
      memmove(readbuf,
          &readbuf[BUFMAX / 2],
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
    strncpy(message, readbuf, (int)(e - s));
    message[(int)(e - s)] = '\0';
    if (strstr(message, "getinfo") == 0)
      Serial.println(name);
    else
      newMessage = 1;
  }
}

char *BufferredSerial::read(void) {
  if (newMessage) {
    newMessage = 0;
    return message;
  } else {
    return NULL;
  }
}

void BufferredSerial::write(char *message) {
  Serial.print(message);
}
