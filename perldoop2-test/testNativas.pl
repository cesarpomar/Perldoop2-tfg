my @xs;#<array><string>
my @ls;#<list><string>
my %hash=();#<hash><string>
my $s;#<string>

print("hola");
say("hola");
@xs=split(",","1,2,3,4,5,6");
chop($s);
$s=chop($s);
chomp($s);
$s=chomp($s);
defined($s);
system("ls");
sort (@xs);
#<$a><$b><string>
sort {$b cmp $a}(@xs);
uc($s);
lc($s);
ucfirst($s);
lcfirst($s);
delete $hash{"key"};
$s=join(",",@xs);
@xs=keys(%hash);
@xs=values(%hash);
length($s);
substr($s,1);
substr($s,1,2);
substr($s,1,2,$s);
$s=substr($s,1);
$s=substr($s,1,2);
$s=substr($s,1,2,$s);
splice(@ls,1);
splice(@ls,1,2);
splice(@ls,1,2,@ls);
splice(@ls,1,2,@ls);
@ls=splice(@ls,1);
@ls=splice(@ls,1,2);
@ls=splice(@ls,1,2,@ls);
@ls=splice(@ls,1,2,@ls);
splice(@xs,1);
splice(@xs,1,2);
splice(@xs,1,2,@xs);
splice(@xs,1,2,@xs);
@xs=splice(@xs,1);
@xs=splice(@xs,1,2);
@xs=splice(@xs,1,2,@xs);
@xs=splice(@xs,1,2,@xs);
pop(@ls);
shift(@ls);
push(@ls,$s);
unshift(@ls,$s);
$s=pop(@ls);
$s=shift(@ls);
$s=push(@ls,$s);
$s=unshift(@ls,$s);
pop(@xs);
shift(@xs);
push(@xs,$s);
unshift(@xs,$s);
$s=pop(@xs);
$s=shift(@xs);
$s=push(@xs,$s);
$s=unshift(@xs,$s);

