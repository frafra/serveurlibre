#!/bin/bash

rm -f log.txt
wget -r http://127.0.0.1 -S -o log.txt
if [ $? -ne 0 ]; then
    echo "Web test failed. Look at log.txt for non 200 HTTP response"
    echo "You could use: grep -C 3 HTTP/1.1 log.txt | less"
else
    echo "Web test succeeded!"
fi
rm -r 127.0.0.1
