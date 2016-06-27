sub funcion{
}

#<args><string>
sub funcion2{
	#<$s1><string>
	(my $s1,)=@_;
}

#<args><string><string>
sub funcion3{
	#<$s1><$s2><string>
	(my $s1,my $s2)=@_;
}

#<returns><string>
sub funcion4{
return "";
}

#<returns><string><string>
sub funcion5{
return "","";
}

#<args><string>
#<returns><string>
sub funcion6{
	#<$s1><string>
	(my $s1,)=@_;
	return "";
}



{
	my $s;#<string>
	funcion();
	funcion2("");
	funcion3("","");
	$s = funcion4();
	($s,$s)=funcion5();
	$s=funcion6("");
	
}