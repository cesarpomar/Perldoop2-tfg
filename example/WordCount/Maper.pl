#!/usr/bin/perl -w

#Hay que indicar la region del mapper, opcionalmete se pueden especificar el tipo de valorEntrada,ClaveSalida,ValorSalida con en este ejemplo
#<mapper_code><string><string><string>
{
	my $line;			#<string>
	my @words;			#<array><string>
	my $key;			#<string>
	my $valueNum = "1";	#<string>
	my $val;			#<string>

	#Tambien hay que indicar el bucle que debe tener la plantilla while( $var = <STDIN>)
	#<mapper_loop>
	while ($line = <STDIN>) { 
		chomp ($line);
		@words = split (" ",$line);
		foreach my $w (@words) {
			$key = $w; 
			$val = $valueNum;

			#Hay que diferenciar las impresiones por pantalla y en el contexto
			#<hadoop_print>
			print ($key,"\t",$val,"\n");
		}
	} 
}