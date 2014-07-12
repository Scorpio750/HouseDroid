#!/bin/bash
cvlc --sout '#rtp{sdp=rtsp://127.0.0.1:8080/test.sdp}' -vvv file:///home/grippier/rtsp/${1}
