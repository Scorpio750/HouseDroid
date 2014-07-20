#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define BAUDRATE  38400
#define MAXBUFLEN 512
#define OFF       0
#define FW        1
#define BW        2

#define MOTOR_NUM 6

static int vec[MOTOR_NUM];
static int pinmap[MOTOR_NUM * 2];
static char readbuf[MAXBUFLEN];
static int buflen;

static void motor2pin(char m, char p1, char p2) {
  pinMode(p1, OUTPUT);
  pinMode(p2, OUTPUT);
  pinmap[m * 2 + 0] = p1;
  pinmap[m * 2 + 1] = p2;
}

static void evalspeeds(char *message) {
  int i;
  if (strlen(message) != MOTOR_NUM + 2)
    return;
  for (i = 0; i < MOTOR_NUM; i++)
    vec[i] = message[i + 1] - '0';
}

static int getmsgind(char *buf, int *sp, int *ep) {
  int s, e;
  int i;
  s = -1;
  e = -1;
  for (i = strlen(buf); i >= 0; i--)
    if (buf[i] == ']') { e = i; break; }
  if (e == -1) return -1;
  for (; i >= 0; i--)
    if (buf[i] == '[') { s = i; break; }
   if (s == -1) return -1;
   *sp = s;
   *ep = ++e;
   return 0;
}

static void syncserial() {
  int bytestoread;
  while ((bytestoread = Serial.available()) > 0) {
    char message[32];
    int i;

    // Check buffer overflow
    if (bytestoread + buflen >= MAXBUFLEN) {
      buflen -= MAXBUFLEN / 2;
      memmove((void *)readbuf,
      (void *)&readbuf[MAXBUFLEN / 2], buflen);
    }
    
    // Read buffer bytes
    Serial.readBytes(&readbuf[buflen], bytestoread);
    buflen += bytestoread;
    readbuf[buflen] = '\0';
    
    // Check for handshake
    if ((i = strstr(readbuf, "[[REQ]]")) != 0) {
      buflen -= i + 7;
      memmove((void *)readbuf,
        (void *)&readbuf[i + 7], buflen);
      break;
    }
  } 
}

static void clientread() {
  int bytestoread;
  if ((bytestoread = Serial.available()) > 0) {
    char message[32];
    int s, e;
    
    // Check buffer overflow
    if (bytestoread + buflen >= MAXBUFLEN) {
      buflen -= MAXBUFLEN / 2;
      memmove((void *)readbuf,
        (void *)&readbuf[MAXBUFLEN / 2], buflen);
    }
    
    // Read buffer bytes
    Serial.readBytes(&readbuf[buflen], bytestoread);
    buflen += bytestoread;
    readbuf[buflen] = '\0';
    
    // Parse message
    if (getmsgind(readbuf, &s, &e) == 0) {
      buflen -= s;
      memmove((void *)readbuf,
        (void *)(&readbuf[s]), buflen);
      readbuf[buflen] = '\0';
      e -= s;
      strncpy(message, readbuf, e);
      message[e] = '\0';
      evalspeeds(message);
    }
  }
}

static void clientwrite() {
  int i, p;
  char writebuf[512];
  writebuf[i++] = '\[';
  if (MOTOR_NUM == 0) // create mock data
    writebuf[i++] = '0';
  else
    for (p = 0; p < MOTOR_NUM; p++) {
      writebuf[i++] = vec[p] + '0';
      writebuf[i++] = ',';
    }
  writebuf[i - 1] = '\]';
  writebuf[i] = '\0';
  Serial.print(writebuf);
}

void setup() {
  // SET UP YOUR MOTORS HERE
  motor2pin(0, 2, 3);
  motor2pin(1, 4, 5);
  motor2pin(2, 6, 7);
  motor2pin(3, 8, 9);
  motor2pin(4, 10, 11);
  motor2pin(5, 12, 13);
  
  Serial.begin(BAUDRATE);
  // synchronize serial
  syncserial();
}

void loop() {
  int i;
  clientread();
  for (i = 0; i < MOTOR_NUM; i++) {
    switch (vec[i]) {
      case OFF:
        digitalWrite(pinmap[i * 2 + 0], LOW);
        digitalWrite(pinmap[i * 2 + 1], LOW);
        break;
      case FW:
        digitalWrite(pinmap[i * 2 + 0], HIGH);
        digitalWrite(pinmap[i * 2 + 1], LOW);
        break;
      case BW:
        digitalWrite(pinmap[i * 2 + 0], LOW);
        digitalWrite(pinmap[i * 2 + 1], HIGH);
        break;
      default:
        digitalWrite(pinmap[i * 2 + 0], LOW);
        digitalWrite(pinmap[i * 2 + 1], LOW);
    }
  }
  //clientwrite();
}
