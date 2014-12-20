<?php 

	error_reporting(E_ALL);
	
	$continue = 1;
	while($continue){

		#open inlog
		$fp_inlog = fopen('inlog','a+') or die('could not connect inlog');

		#open inotify
		$fp_inotify = fopen('inotify_1','r') or die('could not connect inotify');

		#define default pos
		$pos = 0;

		#get position if already in file
		if(file_exists('position')){
			$pos = file_get_contents('position');
		}

		#set position
		fseek($fp_inotify,$pos) or die("Could not go for seek");

		#open copy log
		$fp_inotifycp = fopen('inotify1','w+') or die('could not access inotify1');

		#read inotify
		while(($line = fgets($fp_inotify)) !== false){
			fwrite($fp_inotifycp,$line) or die("Couldnt write");
		}
		

		#get the current pointer
		$pos = ftell($fp_inotify);
		$fp_pos = fopen('position','w+') or die('could not access position');
		fwrite($fp_pos,$pos);

		#close unused handlers
		fclose($fp_inotify);
		fclose($fp_inotifycp);
		fclose($fp_pos);

		#loop through inotify copy
		$fp_inotifycp = fopen('inotify1','r');

		#write scan results
		$fp_scanlog = fopen('scanlog','a+') or die("Could not access scanlog");

		while(($line = fgets($fp_inotifycp)) !== false){

			#check for CREATE
			$var = false;
			if (strpos($line,'CREATE') !== false) {
				$var = explode('CREATE',$line);
			}else if (strpos($line,'MOVED_TO') !== false) {
				$var = explode('MOVED_TO',$line);
			}

			if($var){
				
				echo $file_path = trim($var[0]).trim($var[1]); echo '<br/>';
				fwrite($fp_inlog,$file_path.PHP_EOL);

					if(file_exists($file_path)){

						#scan the file path
						exec('clamscan --stdout --no-summary '.$file_path,$op,$status);

						#look for FOUND
						if(strpos($op,'FOUND') !== false){
							fwrite($fp_scanlog,'FOUND >>'.$file_path.PHP_EOL);
						}else if(strpos($op,'OK') !== false){
							fwrite($fp_scanlog,'OK >>'.$file_path.PHP_EOL);
						}

					}else{
						fwrite($fp_scanlog,'No such file found >> '.$file_path.PHP_EOL);
					}
			}else{
				fwrite($fp_scanlog,'Invalid line >>'.$line);
			}
		}

		fclose($fp_inlog);
		fclose($fp_inotifycp);
	}

?>