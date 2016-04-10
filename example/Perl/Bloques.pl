#Sin argumentos ni retorno

#Variable global
my $global;#<integer>
my $var="hola";#<string>

sub funcion{
	#Varaible local
	my $local;#<integer>
	#Variable global
	our $global2;#<integer>
}

sub funcion2{
#	Varaible local que oculta global
	my $var;#<integer>
	$var="adios";
	print $var;
}

funcion();
funcion2();
print $var;