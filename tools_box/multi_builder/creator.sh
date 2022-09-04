#!/usr/bin/bash
# Choose all the temperatures where simulation will be runned
temp=( "450" "500" "550" "600" "650" "700" "750" "800" "850")
# P CO2
Pressure=("0.01"  "0.1" "0.25" "0.5" "0.75" "0.99")
Pressure2=("0.99"  "0.9" "0.75" "0.5" "0.25" "0.01")
#echo $temp
ORIGINAL=$PWD
script="/home/adastra/Documents/TFM/scripts/KMCscr/python_1D/simulation_builder.py"
touch runner.sh
echo "" > runner.sh

touch results.sh
echo "#!/usr/bin/bash" > results.sh
echo "counter=2" >> results.sh
for i in ${!temp[@]} 
do
	for j in ${!Pressure[@]}
	do
		# BUILDING THE RUNNER SCRIPT
		echo "element $i is ${temp[$i]} with PCO2 ${Pressure[$j]} and PH2 ${Pressure2[$j]}"
	       	DIR="./data3/short_1/Temp${temp[$i]}/PCO2_${Pressure[$j]}"
		echo "orig=\$PWD">>runner.sh
		echo "cd ${DIR}">>/home/adastra/Documents/TFM/scripts/KMCscr/python_1D/data_obtainer.py>>runner.sh
		echo "qsub -N T${temp[$i]}_P${Pressure[$j]} script.sub" >>runner.sh
		echo "cd \$orig">> runner.sh

		# BUILDING THE RESULTS SCRIPT
		echo "orig=\$PWD">>results.sh
		echo "cp results.xlsx ${DIR}">>results.sh
		echo "cd ${DIR}">>results.sh
		echo "echo \$PWD">>results.sh
		echo "/home/adastra/Documents/TFM/scripts/KMCscr/python_1D/data_obtainer.py \${counter}">>results.sh
		echo "mv results.xlsx \$orig">>results.sh
		echo "echo \"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\"">>results.sh
		echo "counter=\$((counter+1))">>results.sh
		echo "cd \$orig">>results.sh
		mkdir -p $DIR
		cp script.sub $DIR
		cd $DIR
		${script} ${temp[$i]} ${Pressure[$j]} ${Pressure2[$j]}
		cd $ORIGINAL
	done
done
chmod +x runner.sh
chmod +x results.sh	


