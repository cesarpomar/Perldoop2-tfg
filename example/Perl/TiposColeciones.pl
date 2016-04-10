#Tipos de colecciones: array, hash, list

#La diferencia entre list y array es que con operaciondes de lectura/escritura es mas rapido el array, pero si hay operaciones para añadir o eliminar
#	se debe usar list para un mayor rendimiento. 

#Las colecciones deben ser inicializadas antes de su uso, para ello la igualamos a '()'

#Declaracion sin inicializar:

my @array;#<array><integer>

#Declaracion con inicializacion:

#El array necesita obligatoriamente un tamaño, para los otros es opcional para mejorar el rendimiento.

my @array2=();#<array><2><integer>
my @list=();#<array><integer>

#No tiene que reservarse en la declaración:
@array2=();#<10>
@list=();

#Pueden usarse variables para especificar el tamaño

my $tam=2;#<integer>
@array2=();#<$tam>

#Se puede usar la declaracion adelantada

#<$array3><array><10><string>

my @array3;

#Si se uso declaracion adelantada, en caso de lo espacificar el tamaño coge el de su declaracion

@array3=();#<10>
@array3=();

#Puedes igualar lista y array, el analizador se encarga de la transformacion

@list=@array2;

#Multidimensiones, las colecciones se pueden anidar. Cada subdimension debe inicializarse por cada dimension. En caso de <array> pueden acerse juntas

my @matrix=();#<array><10><array><8><string>

