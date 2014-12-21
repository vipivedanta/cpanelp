<?php 
	
	error_reporting(E_ALL);
	ini_set('error_reporting',1);	

	$confs = $_POST;
	$fp_conf = fopen('configuration_1.conf','w') or die('Could not access the configuration.conf');

	$content = '';
	foreach($confs as $key=>$value){
		$content .= $key.':'.$value.PHP_EOL;
	}

	#echo $content;
	fwrite($ffp_conf,$content) or die('Could not write to the conf file');
	fclose($fp_conf);

	#echo '<pre>'; print_r($confs);

	#for watcher mod
	if($confs['mode'] == 'watcher'){

		#1-->clear all cron associated with filter mode
		exec("crontab -l | grep -v checker.sh | sed '' | crontab -");
		#print ("starting daemon now");

		
		#2-->start daemon script
		#sleep(10);
		system("/usr/local/cpanel/3rdparty/bin/php-cgi  /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/daemon_q.php &");
		#exec('php /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/daemon_q.php ');
		

		#3-->start inotify - If already started,kill it and start again
		$op = exec('ps aux | grep -v grep | grep "inotifywait"');
		preg_match_all('!\d+!', $op, $matches);
		exec("kill -9 ".$matches[0][0]);

		$watch = ($confs['watch_what'] == 'home')?"/home/*":"/home/*/public_html/";
		exec('inotifywait -d -e moved_to -e create -r '.$watch.' --outfile /var/log/inotify');

		#4-->kill ftp_parser process
		$op = exec('ps aux | grep -v grep | grep "httpupload/ftp_parser.php"');
		preg_match_all('!\d+!', $op, $matches);
		exec("kill -9 ".$matches[0][0]);

		#start inotify cleaner cron
		$clear_cron = exec("crontab -l | grep clear_inotify.php");	
		#start inotify_clearing cron only if clear cron is not set
		if($clear_cron == ''){
			system('crontab -l | { cat; echo "* * * * * /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/clear_inotify.php"; } | crontab -');
		}

		#remove pro_ftp_parser.php 
		exec("crontab -l | grep -v pro_ftp_parser.php | sed '' | crontab -");

	}else if($confs['mode'] == 'filter'){

		#in case of filter mode
		
		#1-->kill the daemon script
		$op = exec('ps aux | grep -v grep | grep "httpupload/daemon_q.php"');
		preg_match_all('!\d+!', $op, $matches);
		exec("kill -9 ".$matches[0][0]);


		#2-->kill the cron - inotify clear
		$clear_cron = exec("crontab -l | grep clear_inotify.php");
		if($clear_cron != ''){
			exec("crontab -l | grep -v clear_inotify | sed '' | crontab -");
		}

		

		if($confs['filter_what'] == 'pure'){

			#pureFTP
			#3-->start checker.sh cron
			$cron = exec("crontab -l | grep checker.sh");	
			if($cron == ''){
				system('crontab -l | { cat; echo "* * * * * /bin/sh /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/checker.sh"; } | crontab -');
			}

			#remove pro_ftp_parser.php 
			exec("crontab -l | grep -v pro_ftp_parser.php | sed '' | crontab -");

			
		}else if($confs['filter_what'] == 'pro'){
			#proFTP

			#disable checker.sh
			exec("crontab -l | grep -v checker.sh | sed '' | crontab -");

			#run pro_ftp_parser cron in 10s interval
			$cron = exec("crontab -l | grep pro_ftp_parser.php");
			if($cron == ''){
				system('crontab -l | { cat; echo "* * * * * /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/pro_ftp_parser.php"; } | crontab -');
				system('crontab -l | { cat; echo "* * * * * sleep 10; /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/pro_ftp_parser.php"; } | crontab -');
				system('crontab -l | { cat; echo "* * * * * sleep 20; /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/pro_ftp_parser.php"; } | crontab -');
				system('crontab -l | { cat; echo "* * * * * sleep 30; /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/pro_ftp_parser.php"; } | crontab -');
				system('crontab -l | { cat; echo "* * * * * sleep 40; /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/pro_ftp_parser.php"; } | crontab -');
				system('crontab -l | { cat; echo "* * * * * sleep 50; /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/pro_ftp_parser.php"; } | crontab -');
			}
		}	


	}

?>
