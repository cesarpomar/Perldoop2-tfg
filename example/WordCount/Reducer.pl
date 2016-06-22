#!/usr/bin/perl -w
#El reducer tiene un comportamiento mas abierto que el resto, solo las regiones etiquetadas seran traducidas. Solo las regiones entiquetadas dentro del reduccer seran traducidas.

#Region del reducer, opcionalmete se pueden especificar el tipo de ClaveEntrada,valorEntrada,ClaveSalida,ValorSalida con en este ejemplo
#<reducer_code><string><string><string><string>
{
	#Acotar las variables que se usan en las regiones reducer_op y reducer_change
	#<reducer_var>
	#Indicar variable clave
	my $oldkey=undef;	#<string><reducer_key>
	#Indicar variable valor
	my $value;			#<string><reducer_value>
	my $count=0;		#<integer>
	#<reducer_var>
	my $newKey;			#<string>
	my $line;			#<string>
	my %unorder=();		#<hash><array><string>

	while ($line = <STDIN>) {
		chomp ($line);
		($newKey, $value) = split ("\t",$line); 
		push(@{$unorder{$newKey}},$value);
	}

	foreach $newKey (keys(%unorder)){
		foreach $value (@{$unorder{$newKey}}){
			if (!(defined($oldkey))) {
				$oldkey = $newKey;
				$count  = $value;
			}elsif ($oldkey eq $newKey){
				#Operacion que se llevara acabo para cada reduccion
				#<reducer_op>
				{
					$count = $count + $value;
				}
			}else{
				print ($oldkey,'\t',$count,'\n');
				
				$oldkey = $newKey;
				$count  = $value;
			}
		}
	}
	#Operacion a realizar antes de terminar
	#<reducer_change>
	{
		#Hay que diferenciar las impresiones por pantalla y en el contexto
		#<hadoop_print>
		print ($newKey,'\t',$count,'\n');
	}

}



