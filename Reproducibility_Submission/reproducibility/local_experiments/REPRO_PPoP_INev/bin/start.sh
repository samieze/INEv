#!/bin/sh

cd result/
rm result.csv
cp result_plain.csv result.csv
cd ..
for file in PP_config_big/* ;
do
		a=0
		while [ $a -lt 1 ]
		do
		java -cp commons-math3-3.5.jar: Optimizer_Main "$file" true true
		a=`expr $a + 1`
		done
		
done
cd result/
mv result.csv result_PPoP_big.csv
cp result_plain.csv result.csv
cd ..
#rename resultfiles etc

for file in PP_config_small/* ;
do
		a=0
		while [ $a -lt 1 ]
		do
		java -cp commons-math3-3.5.jar: Optimizer_Main "$file" true true
		a=`expr $a + 1`
		done
		
done

cd result/
mv result.csv result_PPoP_small.csv
cd ..
