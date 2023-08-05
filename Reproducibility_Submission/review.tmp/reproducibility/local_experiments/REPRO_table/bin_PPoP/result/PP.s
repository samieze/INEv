#!/bin/sh

for file in ../configFiles/*;
do
		a=0
		while [ $a -lt 5 ]
		do
		java -cp commons-math3-3.5.jar: Optimizer_Main "$file" true true
		a=`expr $a + 1`
		done
		
done
