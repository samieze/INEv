#!/bin/bash
echo -e "\
pi_6 | joystick | 0.1 | 10004.10\n \
pi_6 | joystick | 1.0 | 10003.10\n \
pi_6 | joystick | 1.0 | 10002.10\n \
pi_6 | joystick | 0.1 | 10001.10\n \
pi_6 | joystick | 0.1 | 10010.10 \
" > /dev/udp/127.0.0.1/5005


