#!/usr/bin/bash
##############################################################################################
# This bash script builds up several simulation in different themodynamics conditions
#	 ITS IMPORTANT TO CHANE THE LINES THAT CONTAIN "{PATH TO THE SCRIPT}"
# Also, this script build the runner.sh (that gives us the faculty to send all the simulation
#	from one script) and the results.sh ( that read all the results and save them in a
#	xlsx file. You must use the data_obtainer.py file and the simulation builder.py file.
#
##############################################################################################

# Choose all the temperatures where simulation will be runned
temp=( "450" "500" "550" "600" "650" "700" "750" "800" "850")
# Choose all the partial pressure where simulation will be runned
#	In this case Pressure and Pressure2 are relationed as  1= Pressure + Pressure 2
#	But you cand modify this script add or remove parameter to be passed
Pressure=("0.01"  "0.1" "0.25" "0.5" "0.75" "0.99")
Pressure2=("0.99"  "0.9" "0.75" "0.5" "0.25" "0.01")
#echo $temp
ORIGINAL=$PWD
# In this repository you cand find the simulation builder .py script
script="{PATH TO THE SCRIPT} /simulation_builder.py"
# This builds the runner.sh a script that send all hte jobs to a queque.
#	IN THE SECTION BUILDING THE RUNNER SCRIPT CHANGE THE INFORMATION OF THE QUEQUE TO ADAPT IT
#	TO THE QUEQUE DISTRIBUTION THAT YOU USES.
touch runner.sh
echo "" > runner.sh

touch results.sh
echo "#!/usr/bin/bash" > results.sh
echo "counter=2" >> results.sh
# iterate over temperature and the over pressure
for i in ${!temp[@]} 
do
	for j in ${!Pressure[@]} #
	do
		# BUILDING THE RUNNER SCRIPT
		echo "element $i is ${temp[$i]} with PCO2 ${Pressure[$j]} and PH2 ${Pressure2[$j]}"
	       	DIR="./data3/short_1/Temp${temp[$i]}/PCO2_${Pressure[$j]}"
		echo "orig=\$PWD">>runner.sh
		# 
		echo "cd ${DIR}">>/{PATH TO THE SCRIPT}/data_obtainer.py>>runner.sh
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


