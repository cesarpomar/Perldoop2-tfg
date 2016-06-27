my @a=();#<array><10><string>
my @l=();#<list><string>
my @h=();#<hash><string>
my @aa=();#<array><10><array><10><string>
my @ll=();#<list><list><string>
my @hh=();#<hash><hash><string>

my $s;#<string>

$s=$a[0];
$s=$l[0];
$s=$h{"hola"};
$s=$aa[0][0];
$s=$hh{"hola"}{"adios"};