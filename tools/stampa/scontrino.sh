#!/bin/bash

iconv -c -t 437 $1 > /dev/usb/lp0 #| lpr -P text-only
