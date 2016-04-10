#Declaracion de ficheros
my $fi;#<file>
my $fo;#<file>

my $line;#<string>

#La funcion nativa open, '<' entrada, '>' salida borrando fichero, '>>' añadir a fichero
open($fi,'<','in.txt');
open($fo,'>>','out.txt');

#Leer linea a linea fichero(si fuera un array imitaria el comportamiento de perl de poner una linea por fila)
while($line = <$fi>){
	#El descriptor de salida no se incluye en los parentesis
	print $fo ($line);
}

#Los ficheros deben cerrarse
close $fi;
close $fo;

#Tambien se puede leer de teclado
$line=<STDIN>;

print $line;
