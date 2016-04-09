#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ../static/archivio
name=`date +"Report %Y-%m-%d delle ore %H e %M"`
wget -k -p http://localhost/report
cd localhost
mv report "$name".html
