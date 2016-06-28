my $b=1;#<boolean>
my $i=1;#<integer>
my $l=1;#<long>
my $f=1;#<float>
my $d=1;#<double>
my $s="";#<string>
my $file=undef;#<file>
my @array=undef;#<array><integer>
my @list=undef;#<list><integer>
my %hash=undef;#<hash><integer>
my %ref=undef;#<ref><hash><integer>

#Casting a boolean
$b = 1;
$b = 1.1;
$b = "1";
$b = $i;
$b = $l;
$b = $f;
$b = $d;
$b = $s;
$b = $file;
$b = @array;
$b = @list;
$b = %hash;
$b = $ref;

#Casting a integer
$i = 1;
$i = 1.1;
$i = "1";
$i = $b;
$i = $l;
$i = $f;
$i = $d;
$i = $s;
$i = $file;
$i = @array;
$i = @list;
$i = %hash;
$i = $ref;

#Casting a long
$i = 1;
$i = 1.1;
$l = "1";
$l = $b;
$l = $i;
$l = $f;
$l = $d;
$l = $s;
$l = $file;
$l = @array;
$l = @list;
$l = %hash;
$l = $ref;

#Casting a float
$f = 1;
$f = 1.1;
$f = "1";
$f = $b;
$f = $i;
$f = $l;
$f = $d;
$f = $s;
$f = $file;
$f = @array;
$f = @list;
$f = %hash;
$f = $ref;

#Casting a double
$f = 1;
$f = 1.1;
$d = "1";
$d = $b;
$d = $i;
$d = $l;
$d = $f;
$d = $s;
$d = $file;
$d = @array;
$d = @list;
$d = %hash;
$d = $ref;

#Casting a string
$s = 1;
$s = 1.1;
$s = "1";
$s = $b;
$s = $i;
$s = $l;
$s = $f;
$s = $d;
$s = $file;
$s = @array;
$s = @list;
$s = %hash;
$s = $ref;

#Casting a array
@array = @list;

#Casting a list
@list = @array;
