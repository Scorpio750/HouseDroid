#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#define BAUDRATE  57600
#define MAXBUFLEN 512

#define ID "chassis"
#define MOTOR_NUM 3

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
  int num;
  char numbuf[4];
  numbuf[3] = '\0';
  if (strlen(message) != MOTOR_NUM * 3 + 2)
    return;
  for (i = 0; i < MOTOR_NUM; i++) {
    strncpy(numbuf, &message[i * 3 + 1], 3);
    num = atoi(numbuf);
    if (num > 100)
      num = -(num - 100);
    if (num < -100)
      num = 0;
    vec[i] = num;
  }
}

static void clientread() {
  int bytestoread;
  if ((bytestoread = Serial.available()) > 0) {
    char message[32];
    char *s, *e;
    int i;
    
    // Check buffer overflow
    if (bytestoread + buflen >= MAXBUFLEN) {
      // let's be real, the message won't be in the first part
      buflen -= MAXBUFLEN / 2;
      memmove((void *)readbuf,
        (void *)&readbuf[MAXBUFLEN / 2], buflen);
    }
    
    // Read buffer bytes
    Serial.readBytes(&readbuf[buflen], bytestoread);
    buflen += bytestoread;
    readbuf[buflen] = '\0';
    
    // Parse message
    e = strrchr(readbuf, ']');
    for (s = e; s >= readbuf && s[0] != '['; s--) ;
    if (s < readbuf)
      return;
    if (s[0] == '[') {
      buflen -= (int)(s - readbuf);
      memmove((void *)readbuf, (void *)s, buflen);
      readbuf[buflen] = '\0';
      strncpy(message, readbuf, (int)(e - s + 1));
      message[(int)(e - s + 1)] = '\0';
      evalspeeds(message);
    }
  }
}

static void clientwrite() {
  int i;
  int p;
  char writebuf[512];
  i = 0;
  writebuf[i++] = '[';
  if (MOTOR_NUM == 0) // create mock data
    writebuf[i++] = '0';
  else
    for (p = 0; p < MOTOR_NUM; p++) {
      int num = vec[p];
      if (num < 0)
        num = -num + 100;
      writebuf[i++] = num / 100 + '0';
      writebuf[i++] = num % 100 / 10 + '0';
      writebuf[i++] = num % 10 + '0';
      writebuf[i++] = ',';
    }
  writebuf[i - 1] = ']';
  writebuf[i] = '\0';
  Serial.print(writebuf);
}

static void handleId() {
  delay(1000);// bug
  Serial.print("[\"" ID "\"]");
}

void setup() {
  // SET UP YOUR MOTORS HERE
  motor2pin(0, 3, 5);
  motor2pin(1, 6, 9);
  motor2pin(2, 10, 11);
  
  Serial.begin(BAUDRATE);
  handleId();
}

void loop() {
  int i;
  clientread();
  for (i = 0; i < MOTOR_NUM; i++) {
    int mag_vel;
    mag_vel = vec[i] * 255 / 100;
    if (mag_vel > 0) {
      analogWrite(pinmap[i * 2 + 0], mag_vel);
      analogWrite(pinmap[i * 2 + 1], 0);
    } else if (mag_vel < 0) {
      analogWrite(pinmap[i * 2 + 0], 0);
      analogWrite(pinmap[i * 2 + 1], -mag_vel);
    } else {
      analogWrite(pinmap[i * 2 + 0], 0);
      analogWrite(pinmap[i * 2 + 1], 0);
    }
  }
  //clientwrite();
  //Serial.print("\n");
}

