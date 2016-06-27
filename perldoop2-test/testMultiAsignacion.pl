#<$a><$b><$c><$d><integer>
#<@xs><array><10><integer>

my $a=0;
my $b=0;
my $c=0;
my $d=0;
my @xs=();

($a,$b)=(1,2);
($a,$b)=($b,$a);
($c,$d)=($a,$b);
($a,$b,$c,$d)=@xs;
