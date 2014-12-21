#!/usr/local/cpanel/3rdparty/bin/php-cgi
<?php
$fp = fopen("/tmp/pro_ftp_parser_lock.txt", "w+");
if (flock($fp, LOCK_EX | LOCK_NB)) {
	while(1) {
		$n=0;
		$m =0;
		$emailid = '';
		$myfile = "/usr/local/cpanel/whostmgr/docroot/cgi/httpupload/settings.conf";
		$myfile = fopen($myfile, "r");
		if($myfile){
			while(($line = fgets($myfile)) !== false){
				if(strpos($line, 'firewall=on')!==false)
				{
					$n =1;
				}
				if(strpos($line, 'email=on')!==false)
				{
					$m =1;
				}
				if(strpos($line, 'emailid=')!==false)
				{
					$emailid = explode('=',$line);
					$emailid = trim($emailid[1]);
				}
			}
		}
		fclose($myfile);
		if(file_exists('/etc/httpd/aast_uploadmonitor/position'))
		{
			$position = file_get_contents('/etc/httpd/aast_uploadmonitor/position');
		}
		$data2 = '';
		$infile = fopen('/var/log/ftp.log', "r");
		fseek($infile,$position,0);
		while(($line = fgets($infile)) !== false){
			if(strpos($line, 'STOR')!==false)
			{
				$logdata = explode(' ',$line);
				$time = $logdata[0];
				$ipaddress = $logdata[2];
				$username = $logdata[3];
				$directory = $logdata[4];
				
				$clamscan = `clamscan --remove --stdout  --no-summary $directory`;
				$checkString ='';
				if(strpos($clamscan, ':')!==false)
				{
					$checkString = explode(':',$clamscan);
					if(isset($checkString[1]))
					{
						$checkString = $checkString[1];
					}
					else {
						$checkString = '';
					}
				}
				if(strpos($clamscan, 'Empty file')!==false)
				{
					$output = "Empty file,,,";
				}
				elseif(strpos($checkString, 'ERROR')!==false)
				{
					$output = "Error File,,,";
				}
				elseif(strpos($checkString, 'FOUND')!==false)
				{
					$output = "ClamAV rejected file,,,";
				}
				elseif(strpos($checkString, 'OK')!==false)
				{
					$output = "Status OK,,,";
				}
				else {
					$output = "Status OK,,,";
				}
				file_put_contents('/usr/local/cpanel/whostmgr/docroot/cgi/httpupload/ftpupload.txt', $ipaddress.',,,'.$username.',,,'.$directory.',,,'.$output.$time.PHP_EOL);
				if($output!='Status OK,,,' || $output!='Status OK,,,')
				{
					$data2.= PHP_EOL.$time.',,,'.$ipaddress.',,,'.$username.',,,'.$directory.',,,'.$output;
					if($n==1)
					{
						if(file_exists('/etc/init.d/csf'))
						{
							file_put_contents('/etc/csf/csf.deny', $ipaddress.PHP_EOL);
							system ("/usr/sbin/csf -r > /dev/null 2>&1");
						}
						elseif(file_exists('/etc/init.d/apf') || file_exists('/etc/init.d/apf-firewall')) {
							file_put_contents('/etc/apf/deny_hosts.rules', $ipaddress.PHP_EOL);
							file_put_contents('/etc/apf-firewall/deny_hosts.rules', $ipaddress.PHP_EOL);
							system ("/usr/local/sbin/apf -r > /dev/null 2>&1");
							system ("/usr/sbin/apf -r > /dev/null 2>&1");
						}
						else {
							system ("iptables -A INPUT -p tcp -s $ipaddress -j DROP");
						}
					}
					if($m==1)
					{
						system ("echo \"A uploaded file was blocked which has been uploaded from the IP address $ipaddress. The uploaded username is $username\" | mailx -s \"Alert from A-AST Realtime File Uploader\" $emailid");
					}
				}
			}
		}
		file_put_contents('/usr/local/cpanel/whostmgr/docroot/cgi/httpupload/ftpupload_rejected.txt', $data2);
		$position = ftell($infile);
		fclose($infile);
		file_put_contents('/etc/httpd/aast_uploadmonitor/position', $position);
		sleep(10);
	}
	flock($fp, LOCK_UN); // release the lock
}
fclose($fp);
