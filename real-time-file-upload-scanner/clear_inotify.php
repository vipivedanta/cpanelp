<?php 

	#read inotify
	#$fp_inot = fopen('/var/log/inotify') or die('Could not access inotify');

	#get position file
	if(file_exists('position_v')){

		$pos = file_get_contents('position_v');
		$pos = (int)$pos;

		$op = exec("tail -c +".$pos." /var/log/inotify > /var/log/inotify.bak && mv /var/log/inotify.bak /var/log/inotify");
		#echo $op." -- for ".$pos;

		$fp_pos = fopen('position_v','w+');
		fwrite($fp_pos,'0');
		fclose($fp_pos);

	}
?>