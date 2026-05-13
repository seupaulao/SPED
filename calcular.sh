receitabruta=30000;
pprolabore=0.25;
prolabore=`echo "$receitabruta * $pprolabore" | bc`;
inss=`echo "$prolabore * 0.11" | bc`;

senhapostgres="asd123zxc";

echo "-----------------SIMPLES NACIONAL------------------";
echo " ";

echo "Receita Bruta:     $receitabruta";
echo "% Prolabore  :     $pprolabore";
echo "Prolabore    :     $prolabore";
echo "INSS         :     $inss"; 

calc() {
    echo "$@" | bc -l
}

anexo=5;
if [ "$(calc "$pprolabore >= 0.28")" -eq 1 ]; then
   anexo=3;
fi;

snc=0.15;
if [ $anexo -eq 3 ]; then
   snc=0.06;
fi;

impostosnc=$(calc "$snc * $receitabruta");  
totalsnc=$(calc "$impostosnc + $inss");

echo "Anexo        :     $anexo";
echo "% Simples Nac:     $snc";
echo "Imposto - DAS:     $impostosnc";
echo " ";
echo "Total        :     $totalsnc";

echo " ";
echo "-----------------LUCRO PRESUMIDO------------------\n"
echo " ";
echo "Receita Bruta:     $receitabruta";
echo "% Prolabore  :     $pprolabore";
echo "Prolabore    :     $prolabore";
echo " ";
base=$(calc "$receitabruta * 0.32");
echo "Base Calculo :     $base";
echo " ";

irpj=$(calc "0.15 * $base");
csll=$(calc "0.09 * $base"); 
pis=$(calc "0.0065 * $receitabruta");
cofins=$(calc "0.03 * $receitabruta");
iss=$(calc "0.05 * $receitabruta")
totallp=$(calc "$irpj + $csll + $pis + $cofins + $iss + $inss");

echo "IRPJ         :     $irpj";
echo "CSLL         :     $csll";
echo "PIS          :     $pis";
echo "COFINS       :     $cofins";
echo "ISS          :     $iss";
echo "INSS         :     $inss";
echo " "
echo "Total        :     $totallp";
echo " ";
echo " ";
melhor="Simples Nacional";
if [ $(calc "$totallp <= $totalsnc") -eq 1 ]; then
	melhor="Lucro Presumido";
fi;
echo "Melhor Opção :     $melhor";



