#Funciones disponibles:
#  'CHOMP', 'CHOP', 'CLOSE', 'DEFINED', 'DELETE', 'DIE', 'EACH', 'EXISTS', 'EXIT', 'JOIN', 
#  'KEYS', 'LC', 'LCFIRST', 'LENGTH', 'OPEN', 'POP', 'PRINT', 'PUSH', 'SAY', 'SHIRFT', 
#  'SORT', 'SPLICE', 'SPLIT', 'SUBSTR', 'SYSTEM', 'UC', 'UCFIRST', 'UNSHIFT', 'VALUES'

#Si tienen solo un argumento, no hace falta parentesis.(El analizador tiene un parametro que solucione esta problema)

print "hola";

lc "hola";

#Pueden anidarse

print uc "hola";

#La funcion each es la unica excepcion (#var1,#var2) = each %has

my %hash=%{{"hola"=>"1"}};#<hash><string>
my $key;#<string>;
my $value;#<string>;

while(($key,$value) = each %hash){
	print $key.$value;
}

#Las funciones con varios argumentos pueden usarse con cualquier numero

my $cadena="hola mundo";#<string>

print substr($cadena,1);
print substr($cadena,1,5);