#!/bin/sh

cd result/
rm result.csv
cp result_plain.csv result.csv
cd ..
a=0
for file in PP_config_table/* ;
do
		echo "Starting $file"		
		java -cp commons-math3-3.5.jar: Optimizer_Main "$file" true true
		a=`expr $a + 1`
		python3.8 add_to_table.py $file $a 
done
		

cd result/
mv result.csv ../result_PPoP.csv


