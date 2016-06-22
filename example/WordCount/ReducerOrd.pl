#!/usr/bin/perl -w

#Modelo de reducer con menos codigo para entradas ya ordenadas, a efectos del analizador, el codigo etiquetado es el mismo.

#<reducer_code><string><string><string><string>
{
	#<reducer_var>
	my $value;			#<string><reducer_value>
	my $count=0;		#<integer>
	my $oldkey=undef;	#<string><reducer_key>
	#<reducer_var>	
	my $newKey;			#<string>
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
			print ($oldkey,'\t',$count,'\n');
			
			$oldkey = $newKey;
			$count  = $value;
		}
	}
	#<reducer_change>
	{
		#<hadoop_print>
		print ($oldkey,'\t',$count,'\n');
	}

}



