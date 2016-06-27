my $f;#<file>
my $line;#<string>
my @lines;#<array><string>

open($f,'<','in.txt');

$line = <$f>;
@lines = <$f>;

close ($f);

open($f,'>','out.txt');

print $f ($line);

close ($f);

$line=<STDIN>;

