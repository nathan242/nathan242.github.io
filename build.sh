#!/bin/bash

if [ ! -e "build-site.py" ]
then
	echo "build-site.py is not in this dir."
	echo "Abort!"
	exit 1
fi

rm *.html

./build-site.py

if [ $? -eq 0 ]
then
	mv ./build/*.html .
fi

