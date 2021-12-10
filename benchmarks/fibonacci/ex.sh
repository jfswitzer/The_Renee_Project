#!/bin/bash
powerstat -z -d 0 0.5 960 >> pstat.out &
sleep 60;
./main.sh;
sleep 60
pkill powerstat;
