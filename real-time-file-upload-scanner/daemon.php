<?php 
	error_reporting(E_ALL);	

	while(true){

		#create position file
		if(!file_exists('position.txt')){
			$position = count(file('inotify.txt'));
			$fp_pos = fopen('position.txt','w+') or die('Couldnot create position file');
			fwrite($fp_pos,$position);
			fclose($fp_pos);
		}

		#read inotify
		$fp = fopen('inotify.txt','r') or die('Could not access inotify');

		$position = file_get_contents('position.txt');

		$fp_l = fopen('log.txt','a+') or die('Could not create log file');

		$line_no = if(isset($line_no))?$line_no:0;
		
		while(($line = fgets($fp)) !== false){

			if($line_no >= $position || $position == '0'){
				fwrite($fp_l,$line) or die('Could not write to log file');
			}else{
				echo $line;
				fwrite($fp_l,'---END OF A BLOCK');
				fclose($fp_l);
				break;
			}

			$line_no++;

		}

		#re-write the position file
		$fp_pos = fopen('position.txt','w+') or die('Couldnot create position file');
		$line_no = $line_no+1;
		fwrite($fp_pos,$line_no);
		fclose($fp_pos);
	}	
?>