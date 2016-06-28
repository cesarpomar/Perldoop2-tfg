#!/usr/bin/perl -w

#<mapper_code>
{
	my $line;			#<string>
	my @words;			#<array><string>
	my $key;			#<string>
	my $valueNum = "1";	#<string>
	my $val;			#<string>

	#<mapper_loop>
	while ($line = <STDIN>) { 
		chomp ($line);
		@words = split (" ",$line);
		foreach my $w (@words) {
			$key = $w; 
			$val = $valueNum;

			#<hadoop_print>
			print ($key,"\t",$val,"\n");
		}
	} 
}