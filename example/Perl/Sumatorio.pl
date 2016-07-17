#<args><string>
#<returns><float>
sub sumatorio{
	(my $cadena,)=@_;#<string>
	my @numeros = split(",",$cadena);#<array><string>
    my $suma = 0;#<float>
	for my $n (@numeros){
		$suma += $n;
	}
	return $suma;
}

my $input = <STDIN>;#<string>
print sumatorio($input);