#!/usr/bin/env sh

origDir=$PWD
manageScript=`find $origDir -maxdepth 1 -type f -name 'manage.py'`

for subdir in `find $origDir -type d -name 'locale'`
do
	cd `dirname $subdir`
	python $manageScript compilemessages
	cd $origDir
done
