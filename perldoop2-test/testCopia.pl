my @array=();#<array><10><string>
my @list=();#<list><10><string>
my %hash=();#<hash><10><string>
my $rarray;#<ref><array><string>
my $rlist;#<ref><list><string>
my $rhash;#<ref><hash><string>

@array=@array;
@list=@list;
%hash=%hash;

$rarray=\@array;
$rlist=\@list;
$rhash=\%hash;

@array=@{$rarray};
@list=@{$rlist};
%hash=%{$rhash};

$rarray=$rarray;
$rlist=$rlist;
$rhash=$rhash;
