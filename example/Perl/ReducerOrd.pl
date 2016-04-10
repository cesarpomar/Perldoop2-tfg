#!/usr/bin/perl -w

#Modelo de reducer con menos codigo para entradas ya ordenadas, a efectos del analizador, el codigo etiquetado es el mismo.

#<reducer_code><string><string><string><string>
{
	#<reducer_var>
	my $newKey;			#<string><reducer_key>
	my $value;			#<string><reducer_value>
	my $count=0;		#<integer>
	#<reducer_var>
	my $oldkey=undef;	#<string>
	my $line;			#<string>

	while ($line = <STDIN>) {
		chomp ($line);
		($newKey, $value) = split ("\t",$line); 

		if (!(defined($oldkey))) {
			$oldkey = $newKey;
			$count  = $value;
		}elsif ($oldkey eq $newKey){
			#<reducer_op>
			{
				$count = $count + $value;
			}
		}else{
			print ($oldkey,'\t',$count,'\n');#<reducer_print>
			
			$oldkey = $newKey;
			$count  = $value;
		}
	}
	#<reducer_change>
	{
		print ($oldkey,'\t',$count,'\n');#<reducer_print>
	}

}



