#Varios a constante

#<$s1><$s2><string>
(my $s1, my $s2)=('hola',"4");

#Variables a variables
($s1, $s2)=($s2,$s1);

#Varaibles a array de funcion

($s1,$s2)=split(",","1,2");

#Varaibles a array variable

my @array=@{["1","2"]};#<array><string>

($s1,$s2)=@array;