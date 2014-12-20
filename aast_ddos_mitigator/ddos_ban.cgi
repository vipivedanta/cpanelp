#!/usr/local/cpanel/3rdparty/bin/php-cgi

<?php 


	#license checking
	function check_license($licensekey,$localkey="") {
	    $whmcsurl = "http://admin-ahead.com/portal/";
	    $licensing_secret_key = "ArShIIMQlunPQ"; # Unique value, should match what is set in the product configuration for MD5 Hash Verification
	    $check_token = time().md5(mt_rand(1000000000,9999999999).$licensekey);
	    $checkdate = date("Ymd"); # Current date
	    $usersip = isset($_SERVER['SERVER_ADDR']) ? $_SERVER['SERVER_ADDR'] : $_SERVER['LOCAL_ADDR'];
	    $localkeydays = 1; # How long the local key is valid for in between remote checks
	    $allowcheckfaildays = 1; # How many days to allow after local key expiry before blocking access if connection cannot be made
	    $localkeyvalid = false;
	    if ($localkey) {
	        $localkey = str_replace("\n",'',$localkey); # Remove the line breaks
			$localdata = substr($localkey,0,strlen($localkey)-32); # Extract License Data
			$md5hash = substr($localkey,strlen($localkey)-32); # Extract MD5 Hash
	        if ($md5hash==md5($localdata.$licensing_secret_key)) {
	            $localdata = strrev($localdata); # Reverse the string
	    		$md5hash = substr($localdata,0,32); # Extract MD5 Hash
	    		$localdata = substr($localdata,32); # Extract License Data
	    		$localdata = base64_decode($localdata);
	    		$localkeyresults = unserialize($localdata);
	            $originalcheckdate = $localkeyresults["checkdate"];
	            if ($md5hash==md5($originalcheckdate.$licensing_secret_key)) {
	                $localexpiry = date("Ymd",mktime(0,0,0,date("m"),date("d")-$localkeydays,date("Y")));
	                if ($originalcheckdate>$localexpiry) {
	                    $localkeyvalid = true;
	                    $results = $localkeyresults;
	                    $validdomains = explode(",",$results["validdomain"]);
	                    if (!in_array($_SERVER['SERVER_NAME'], $validdomains)) {
	                        $localkeyvalid = false;
	                        $localkeyresults["status"] = "Invalid";
	                        $results = array();
	                    }
	                    $validips = explode(",",$results["validip"]);
	                    if (!in_array($usersip, $validips)) {
	                        $localkeyvalid = false;
	                        $localkeyresults["status"] = "Invalid";
	                        $results = array();
	                    }
	                    if ($results["validdirectory"]!=dirname(__FILE__)) {
	                        $localkeyvalid = false;
	                        $localkeyresults["status"] = "Invalid";
	                        $results = array();
	                    }
	                }
	            }
	        }
	    }
	    if (!$localkeyvalid) {
	        $postfields["licensekey"] = $licensekey;
	        $postfields["domain"] = $_SERVER['SERVER_NAME'];
	        $postfields["ip"] = $usersip;
	        $postfields["dir"] = dirname(__FILE__);
	        if ($check_token) $postfields["check_token"] = $check_token;
	        if (function_exists("curl_exec")) {
	            $ch = curl_init();
	            curl_setopt($ch, CURLOPT_URL, $whmcsurl."modules/servers/licensing/verify.php");
	            curl_setopt($ch, CURLOPT_POST, 1);
	            curl_setopt($ch, CURLOPT_POSTFIELDS, $postfields);
	            curl_setopt($ch, CURLOPT_TIMEOUT, 30);
	            curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	            $data = curl_exec($ch);
	            curl_close($ch);
	        } else {
	            $fp = fsockopen($whmcsurl, 80, $errno, $errstr, 5);
		        if ($fp) {
	        		$querystring = "";
	                foreach ($postfields AS $k=>$v) {
	                    $querystring .= "$k=".urlencode($v)."&";
	                }
	                $header="POST ".$whmcsurl."modules/servers/licensing/verify.php HTTP/1.0\r\n";
	        		$header.="Host: ".$whmcsurl."\r\n";
	        		$header.="Content-type: application/x-www-form-urlencoded\r\n";
	        		$header.="Content-length: ".@strlen($querystring)."\r\n";
	        		$header.="Connection: close\r\n\r\n";
	        		$header.=$querystring;
	        		$data="";
	        		@stream_set_timeout($fp, 20);
	        		@fputs($fp, $header);
	        		$status = @socket_get_status($fp);
	        		while (!@feof($fp)&&$status) {
	        		    $data .= @fgets($fp, 1024);
	        			$status = @socket_get_status($fp);
	        		}
	        		@fclose ($fp);
	            }
	        }
	        if (!$data) {
	            $localexpiry = date("Ymd",mktime(0,0,0,date("m"),date("d")-($localkeydays+$allowcheckfaildays),date("Y")));
	            if ($originalcheckdate>$localexpiry) {
	                $results = $localkeyresults;
	            } else {
	                $results["status"] = "Invalid";
	                $results["description"] = "Remote Check Failed";
	                return $results;
	            }
	        } else {
	            preg_match_all('/<(.*?)>([^<]+)<\/\\1>/i', $data, $matches);
	            $results = array();
	            foreach ($matches[1] AS $k=>$v) {
	                $results[$v] = $matches[2][$k];
	            }
	        }
	        if (isset($results["md5hash"])) {
	            if ($results["md5hash"]!=md5($licensing_secret_key.$check_token)) {
	                $results["status"] = "Invalid";
	                $results["description"] = "MD5 Checksum Verification Failed";
	                return $results;
	            }
	        }
	        if ($results["status"]=="Active") {
	            $results["checkdate"] = $checkdate;
	            $data_encoded = serialize($results);
	            $data_encoded = base64_encode($data_encoded);
	            $data_encoded = md5($checkdate.$licensing_secret_key).$data_encoded;
	            $data_encoded = strrev($data_encoded);
	            $data_encoded = $data_encoded.md5($data_encoded.$licensing_secret_key);
	            $data_encoded = wordwrap($data_encoded,80,"\n",true);
	            $results["localkey"] = $data_encoded;
	        }
	        $results["remotecheck"] = true;
	    }
	    unset($postfields,$data,$matches,$whmcsurl,$licensing_secret_key,$checkdate,$usersip,$localkeydays,$allowcheckfaildays,$md5hash);
	    return $results;
	}

	#dummy flag	
	$licenseinvalid=true;

	#if license.conf exists, get it contents
	if (file_exists('/usr/local/cpanel/whostmgr/docroot/cgi/aast_ddos_mitigator/license.conf'))
 	{
 		$localfile = file_get_contents('/usr/local/cpanel/whostmgr/docroot/cgi/aast_ddos_mitigator/license.conf');
	}
	
	#if license.conf is empty, them set localfile is empty
	if (empty($localfile)) $localfile = '';

	#get license key
	preg_match('/^license=(\S+)\n/',$localfile,$match);
 	if ( ! isset($match[1]))
 	{
    	$match[1] = null;
 	}
 	$license=$match[1];

 	#get localkey
	preg_match('/\nlocalkey=(\S+)\n/',$localfile,$match);
	if ( ! isset($match[1])) {
   	 $match[1] = null;
	}
	$key=$match[1];
	
	#check the license	
	$results = check_license($license,$key);

	
	if ($results["status"]=="Active") {
    	 $licenseinvalid=false;
 	}

 	if($licenseinvalid && isset($_POST['license']) )
 	{
    	 $license=$_POST['license'];
     	$results = check_license($license);
     	if ($results["status"]=="Active")
     	{
       	  $licenseinvalid=false;
       	  $file = fopen("/usr/local/cpanel/whostmgr/docroot/cgi/aast_ddos_mitigator/license.conf","w");
       	  fwrite($file,"license=$license\n");
       	  fwrite($file,"localkey={$results['localkey']}");
       	  fclose($file);
     	}
 	}

 	if($licenseinvalid) {

 		#should not run the ban process
 		die();
 	}

	#open ddos.conf file
	$conf = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos.conf');
	array_pop($conf);

	#get connection limit
	$var = explode('=',$conf[1]);
	$connection_limit = trim($var[1]);
	
	#get ipconfig
	$ipconn = `netstat -ntu | awk '{print $5}' | sed -r 's/(.*?):([0-9]+)$/\\1/' | sort | uniq -c | sort -nr`;
	
	$fp = fopen('ipconn.txt','w');
	fwrite($fp,$ipconn);

	#get IPs and connections as array
	$ips = file('ipconn.txt');
	fclose($fp);

	#filter  out only ipv4 ips
	$c_ips = array(); #for valid ip(v4) entries
	foreach($ips as $ip){
		
		$var = explode(' ',$ip);
		$var = array_values(array_filter($var));

		#$var should not be empty
		if(isset($var[0]) && isset($var[1])){

			#$var[1] probably an IP.Now check for IPv6 format(::ffff:xxx.xxx.xxx.xxx)
			if(strpos($var[1],'::ffff:') == true){
				$ipv4 = trim(str_replace('::ffff:','',$var[1]));
			}else{
				$ipv4 = trim($var[1]);
			}

			#validate IP
			if(filter_var($ipv4,FILTER_VALIDATE_IP)){

				$c_ips[$ipv4] = $var[0];
			}
		}
	
	}

	if(empty($c_ips)){
		die('No valid IPs');
	}

	#now check previously banned ips -> format is conn:ip:time
	$pre_bans_temp = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list');
	$pre_bans = array();
	if(!empty($pre_bans_temp)){
		foreach($pre_bans_temp as $line){
			$var = explode(':',$line);
			$pre_bans[] = $var[1];
		}
	}	


	#open ignore-list files
	$i_fp = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list','a+');
	$igonored_ips = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list');
	$igonored_ips = array_map('trim',$igonored_ips);

	#banned ip-list
	$b_fp = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list','a+');

	#get own ips
	$self_ips = `/sbin/ifconfig | grep "inet addr"`;
	#write to a file
	$s_fp = fopen('self_ips.txt','w');
	fwrite($s_fp,$self_ips);
	#now read
	$self_ips = file('self_ips.txt');

	#get just ips only from the self-ip-elements
	$n_self_ips = array();
	foreach($self_ips as $ip){
		$n_self_ips[] = getStringBetween($ip,'addr:',' ');
	}

	
	#ban ips which is not already banned
	foreach($c_ips as $ip=>$con){

		#only if connection limit exceeded
		if($con > $connection_limit){

			#not already banned
			if(!in_array($ip,$igonored_ips) && !in_array($ip,$n_self_ips) && !in_array($ip,$pre_bans)){

				$banned = false;

				#check for csf
				if(file_exists('/etc/init.d/csf')){
					system ("/usr/sbin/csf -d ".$ip);
					$banned = true;
				}else if(file_exists('/etc/init.d/apf')){
					#ban with apf
					system("/usr/local/sbin/apf -d ".$ip);
					$banned = true;
				}else{
					#ban with iptables
					system("iptables -I INPUT -s ".$ip." -j DROP");
					$banned = true;
				}

				if($banned){

					
					#write to ip-ignore-list
					#if(!in_array($ip,$igonored_ips)){
						#fwrite($i_fp,$ip.PHP_EOL);
					#}	

					$time = time();

					#write to banned-ip-list
					if(!in_array($ip,$pre_bans)){
						fwrite($b_fp,$con.':'.$ip.':'.$time.PHP_EOL);
					}	

					#save to sqlite table
					#exec("/usr/bin/sqlite3 /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos.db \"insert into bann (ip,conn,dt) values ('".$con."','".$ip."','".$time."');\"");

					#via pdo
					$db = new PDO('sqlite:/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos.db');
					$sql = "insert into bann (ip,conn,dt) values ('".$ip."','".$con."','".$time."')";
					$db->query($sql);
				}
			}
		}
	}
	fclose($i_fp);
	fclose($b_fp);


	#get string between two strings/chars
	function getStringBetween($str,$from,$to)
	{
    	$sub = substr($str, strpos($str,$from)+strlen($from),strlen($str));
    	return substr($sub,0,strpos($sub,$to));
	}
	

?>