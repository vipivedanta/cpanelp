
<!--DEFAULTS-->
<?php 
    
    $freq = 1;$conn = 150;$time_to_block = 600;$email = 'admin@admin-ahead.com';

    #$filePath = "/usr/local/ddos/ddos.conf";
    $filePath = "/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos.conf";
    $myfile = fopen($filePath, "r") or die("Unable to open file!Sorry");
   

    #read line by line
    if($myfile){
       
        while(($line = fgets($myfile)) !== false){
            
            
            #frequency
            if(strpos($line,'freq') !== false){ 
                $freq = trim(substr($line,strpos($line, "=") + 1)); 
            }

            #no of connections
            if(strpos($line,'connlimit') !== false){
                 $conn = trim(substr($line,strpos($line, "=") + 1)); 
            }

            #firewal
            /*if(strpos($line,'APF_BAN') !== false && $line[0] != '#'){
                $firewal = trim(substr($line,strpos($line, "=") + 1)); 
            }

            #kill
            if(strpos($line,'KILL') !== false && $line[0] != '#'){
                 $block_ip = trim(substr($line,strpos($line, "=") + 1)); 
            }*/

            #ban period
            if(strpos($line,'email') !== false){
                $email = substr($line,strpos($line, "=") + 1);
                #$email = trim(str_replace('"','',$email));
            }

            #email id   
            if(strpos($line,'baninterval') !== false){
                 $time_to_block = trim(substr($line,strpos($line, "=") + 1)); 
            }
            
        }
    }
    fclose($myfile);
  
?>

<!--PROCESSING FORM-->
<?php 
    if(isset($_POST['save'])){

        $freq = $_POST['freq'];
        $conn = $_POST['conn'];
       $time_to_block = $_POST['time_to_block'];
        $email = $_POST['email'];
        $plugin = $_POST['plugin'];

        if(trim($_POST['freq']) == '' || $_POST['freq'] < 1 || !is_numeric($_POST['freq'])){
            $err = 'Please enter a valid Frequency!';
        }else if(trim($_POST['conn']) == '' || $_POST['conn'] < 1 || !is_numeric($_POST['conn'])){
            $err = 'Please specify a valid No of connections!';
        }else if(trim($_POST['time_to_block']) == '' || $_POST['time_to_block'] < 1 || !is_numeric($_POST['time_to_block'])){
            $err = 'Please specify a time in seconds (Time to block)!';
        }else if(!filter_var($_POST['email'], FILTER_VALIDATE_EMAIL)){ 
            $err = 'The E Mail provided is not valid !';
        }else{

            #All success
            #filePath = "/usr/local/ddos/ddos.conf";
            $filePath = "/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos.conf";
            $myfile = fopen($filePath, "r") or die("Unable to open file!");
            

            #read line by line
            if($myfile){
                
                $content = '';
                while(($line = fgets($myfile)) !== false){
            
            
                #frequency
                if(strpos($line,'freq') !== false){ 
                    $line = 'freq='.$freq. PHP_EOL;
                }

                #no of connections
                if(strpos($line,'connlimit') !== false){
                    $line = 'connlimit='.$conn. PHP_EOL;
                }

                #firewal
               /* if(strpos($line,'APF_BAN') !== false && $line[0] != '#'){
                    $line = 'APF_BAN='.$firewall. PHP_EOL;
                }

                #kill
                if(strpos($line,'KILL') !== false && $line[0] != '#'){
                    $line = 'KILL='.$block_ip. PHP_EOL;
                }*/

                #ban period
                if(strpos($line,'email') !== false){
                    $line = 'email='.$email.''. PHP_EOL;
                }

                #email id   
                if(strpos($line,'baninterval') !== false){
                    $line = 'baninterval='.$time_to_block. PHP_EOL;
                }
            
                $content .= $line;

            }

        }
        fclose($myfile);

        $unban = exec("crontab -l | grep ddos_unban.cgi");
        $ban = exec("crontab -l | grep ddos_ban.cgi");

		if($plugin=='disabled')
		{
	        if($unban != '' && $ban != ''){
	        	//exec('crontab -l | grep -v ddos_unban.cgi | crontab -');
	        	//exec('crontab -l | grep -v ddos_ban.cgi | crontab -');
	        	exec('crontab -l | grep -v aast_ddos_mitigator | crontab -');
	        	
	        	//$test1 = `crontab -l | grep -v ddos_ban.cgi | crontab -`;
        		//$test2 = `crontab -l | grep -v ddos_unban.cgi | grep -v ddos_ban.cgi | crontab -`;
        		//$test2 = `crontab -l | grep -v aast_ddos_mitigator | crontab -`;
				//$test3 = `crontab -l | grep -v aast_ddos_mitigator | crontab -`;

       			#we need to remove from whitelist also
        		$whitelist_file_content_array = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list','r');

        		#unban all temporary banned IPs
        		$ip_file = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list','r') or die("Couldn't access the banned list file");
        		if($ip_file){
			        while(($line = fgets($ip_file)) !== false){
			
			            $var = explode(':',$line);
			            $b_ip = $var[1];
			
			            #check which firewal is present & ban with that firewall.
			            if (file_exists("/etc/init.d/csf")) {
			              exec("/usr/sbin/csf -dr ".$b_ip);
			            }else if (file_exists("/etc/init.d/apf")){
			              exec("/usr/local/sbin/apf -u ".$b_ip);
			            }else { 
			              exec("iptables -D INPUT -s ".$b_ip." -j DROP"); 
			            }
			            #exec("sed -i '/".$b_ip."/d' /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list");
			
			            if(count($whitelist_file_content_array) != 0){
			              exec("sed -i '/".$b_ip."/d' /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list");
			            }  
			        }
        	fclose($ip_file);

	        #remove all IPs from banned.ip.list
	        $ip_file = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list',"w");
	        fwrite($ip_file,'');
	        fclose($ip_file);

	      }else{
	        die("Couldnot access the file!");
	      }
	     }
        }
        if($plugin=='enabled')
		{
	        if($unban == '' && $ban == ''){
	        
	            $unban_cron = "crontab -l | sed '\$a*/1 * * * * /usr/local/cpanel/3rdparty/bin/php-cgi  /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos_unban.cgi >/dev/null 2>&1' | crontab -";
	            $o = `$unban_cron`;
	            exec("crontab -l | grep -v ddos_ban.cgi | sed '\$a*/".$freq." * * * * /usr/local/cpanel/3rdparty/bin/php-cgi /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos_ban.cgi >/dev/null 2>&1' | crontab -");
	        }
        }

        
  

        #write
        $myfile = fopen($filePath, "w") or die("Unable to open file!");
        fwrite($myfile,$content);
        fclose($myfile);

        $success = 'Configuration has been changed!';

        }       
    }
?>  


<?php if(isset($err)):?>
<div class="alerte"><?php echo $err;?></div>
<?php endif;?>

<?php if(isset($success)):?>
<div class="alertm"><?php echo $success;?></div>
<?php endif;?>

<?php
if(!file_exists('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/runstatus'))
{
	$fileName = '/etc/wwwacct.conf';
	$myfile = fopen($fileName, "r");
	if($myfile){
		while(($line = fgets($myfile)) !== false){
			if(strpos($line, 'CONTACTEMAIL ')!==false)
			{
				$email = trim($line);
				$email = explode(' ',$line);
				$email = $email[1];
			}
        }
        fclose($myfile);
	}
	exec("touch /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/runstatus");
}
?>

<!--HTML-->
<form class="config-form" method="post" action="addon_aast_ddos_mitigator.cgi">
<ul>
    <li>
        <label for="freq">Frequency of script execution <span class="descr">(In minutes)</span> <span class="req">*</span></label>
        <input type="text" name="freq" class="freq" align="right" value="<?php echo $freq;?>" />
    </li>

    <li>
        <label for="conn">No. of connections <span class="req">*</span></label>
        <input type="text" name="conn" class="conn"  align="right" value="<?php echo $conn;?>" />
    </li>

  
    <li>
        <label for="time_to_block">Time to block IP<span class="descr"> (In seconds)</span> <span class="req">*</span></label>
        <input type="text" name="time_to_block" class="time-to-block" align="right"  value="<?php echo $time_to_block;?>" />
    </li>

    <li>
        <label for="email">E Mail to notify <span class="req">*</span></label>
        <input type="text" name="email" class="email"  align="right" value="<?php echo $email;?>" />
    </li>
    <?php 
    $unban = exec("crontab -l | grep ddos_unban.cgi");
    $ban = exec("crontab -l | grep ddos_ban.cgi");
	$status = "enabled";
    if($unban != '' && $ban != ''){
        $status = "enabled";
     }else{
        $status = "disabled";
     }
    ?>
    <li>
        <label for="email">Plugin Status <span class="req">*</span></label>
        <div style="float:right;margin-right:20px;">
        <input type="radio" name="plugin" value="enabled" <?php if($status=='enabled') echo "checked";?>> Enabled  &nbsp  &nbsp
		<input type="radio" name="plugin" value="disabled" <?php if($status=='disabled') echo "checked";?>> Disabled<br>
        </div>
    </li>

<li><input type="submit" class="btn-s" name="save" value="Update configuration"></li>
</ul>
</form>
