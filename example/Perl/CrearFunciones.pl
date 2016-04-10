#Sin argumentos ni retorno

sub funcion{
	print "soy 1";
}

#Con un argumentos y sin retorno

#<args><string>
sub funcion2{
	#<$s1><string>
	(my $s1,)=@_;#Cogemos el argumentos, fijarse que aunque es uno hay una coma para forzar modo lista.
	print $s1;
}

#Con dos argumentos y sin retorno

#<args><string><string>
sub funcion3{
	#<$s1><$s2><string>
	my $s1;
	my $s2;
	($s1,$s2)=@_;
	print ($s1.$s2);
}

#Sin argumentos y dos retornos

#<returns><string><string>
sub funcion4{
	return "soy","4";
}

#Completa
#<args><string>
#<returns><string>
sub funcion5{
	#<$s1><string>
	(my $s1,)=@_;
	return $s1;
}

{
	funcion();
	funcion2 "soy 2";
	funcion3("soy ","3");
	#<$s1><$s2><string>
	my $s1;
	my $s2;
	($s1,$s2)=funcion4();
	print ($s1.$s2);
	print funcion5 "soy 5";
	
}

