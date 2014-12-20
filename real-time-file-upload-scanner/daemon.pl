use warnings;
use Proc::Daemon;

Proc::Daemon::Init;

my $continue = 1;
$SIG{TERM} = sub { $continue = 0 };

while ($continue) {

open($o,">>/root/inlog");
open($in,"</var/log/inotify");
$pos = 0;
if (-e "/root/position") { $pos=`cat /root/position`; }
seek($in,$pos,0);
open($out,">/var/log/inotify1");
while(<$in>){
print $out $_;
}
$pos=tell($in);
system("echo $pos > /root/position");
close $in;
close $out;
open($intemp,"</var/log/inotify1");
while(<$intemp>) {
print $o $_;
if ($_ =~ /CREATE/ or /MOVED_TO/) {
($dir,$act,$file) = ($_ =~ /(.+?)\s+(CREATE|MOVED_TO)\s+(.+)/);
$temp=$dir.$file;
print $o "\n$temp\n";
}
}
close $in;
close $o;
#print $o "\n\n-------------------\ncurrent position--$pos\n\n";
#system("sed -i '1,\'$pos\'d' /var/log/inotify");
#sleep 2;
}
