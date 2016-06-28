
#<reducer_code>
{
	#<reducer_var>
	my $oldkey=undef;	#<string><reducer_key>
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
	#<reducer_change>
	{
		#<hadoop_print>
		print ($newKey,'\t',$count,'\n');
	}

}



