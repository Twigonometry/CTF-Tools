#!/bin/bash
filepath=$1
echo -n -e '\xff\xd8\xff\xe0' > jpegged
cat "$filepath" >> jpegged
