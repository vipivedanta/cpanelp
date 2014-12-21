#!/usr/local/cpanel/3rdparty/bin/php-cgi

<?php 

	$hostname_v = `hostname`;
	$hostname_v = trim($hostname_v);

	#license checking
	function check_license($licensekey,$localkey="") {

		#print_r($_SERVER);
		global $hostname_v;
	    $whmcsurl = "http://admin-ahead.com/portal/";
	    $licensing_secret_key = "ArShIIMQlunPQ"; # Unique value, should match what is set in the product configuration for MD5 Hash Verification
	    $check_token = time().md5(mt_rand(1000000000,9999999999).$licensekey);
	    $checkdate = date("Ymd"); # Current date
	    $usersip = isset($_SERVER['SERVER_ADDR']) ? $_SERVER['SERVER_ADDR'] : $_SERVER['LOCAL_ADDR'];

	    $usersip = `ifconfig | grep "inet addr"`;
	    $usersip = trim($usersip);
	    preg_match('/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/', $usersip, $match);
	    $usersip = trim($match[0]);

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
	                    if (!in_array($$hostname_v, $validdomains)) {
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
	                    if ($results["validdirectory"]!='/usr/local/cpanel/whostmgr/docroot/cgi/aast_ddos_mitigator') {
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
	        #$postfields["domain"] = $_SERVER['SERVER_NAME'];
	        #$postfields["domain"] = "cpanel.samurais.admin-ahead.com";
	        $postfields["domain"] = `hostname`;
	        $postfields["domain"] = trim($postfields["domain"]);
	        $postfields["ip"] = $usersip;
	        $postfields["dir"] = '/usr/local/cpanel/whostmgr/docroot/cgi/aast_ddos_mitigator';
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
	#print_r($results);die;

	
	if ($results["status"]=="Active") {
    	 $licenseinvalid=false;
 	}

 	
 	if($licenseinvalid) {

 		#should not run the ban process
 		die("Invalid license\n");
 	}
	

	#get the pre-set ban interval
	$conf = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos.conf');
	$var = trim($conf[0]);
	$var = explode('=',$var);
	$ban_interval = trim($var[1]);


	#get ip-details from banned-ip-list
	$banned = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list');

	#open banned list
	$b_fp = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list','r');
	#open ignore list
	$i_fp = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list','r');

	#get contents of ignored list & banned list
	$b_ips = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list');
	$i_ips = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list');
	
	$current_time = time();

	#print_r($banned);

	#split to ip & banned time
	foreach($banned as $line){

		$var = explode(':',$line);
		$ip = $var[1];
		$time = $var[2];
		

		#time diffrnce
		$t_diff = $current_time - $time;

		echo $t_diff.'='.$current_time.'-'.$time.' --->'.$ban_interval;
		
		
		#check whether ban period exceeds
		if($t_diff > $ban_interval){

		
			#exceeded,unban it
			$unbanned = false;

			#with csf
			if(file_exists('/etc/init.d/csf')){
				system ("/usr/sbin/csf -dr ".$ip);
				$unbanned = true;
			}else if(file_exists('/etc/init.d/apf')){
				system("/usr/local/sbin/apf -u ".$ip);
				$unbanned = true;
			}else{
				system("iptables -D INPUT -s ".$ip." -j DROP");
				$unbanned = true;
			}

			if($unbanned){
				#system("sed -i '/".$line."/d' /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list");
				#system("sed `-i '/".$ip."/d' /usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list");

				#remove ip from both ignored.ip.list and banned.ip.list

				#update banned.ip.list
				$b_fp_w = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/banned.ip.list','w+');
				$b_content = '';
				foreach($b_ips as $b_line){
					$var = explode(':',$b_line);
					$b_line_ip = trim($var[1]);
					$b_line = trim($b_line);
					if($b_line_ip != $ip){
						$b_content .= $b_line.PHP_EOL;
					}
				}
				fwrite($b_fp_w,$b_content);
				fclose($b_fp_w);

				#update ignored.ip.list
				#open ignore list
				/*$i_fp_w = fopen('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list','w+');
				$i_content = '';
				foreach($i_ips as $i_line){
					$i_line = trim($i_line);
					if($i_line != $ip){
						$i_content .= $i_line.PHP_EOL;
					}
				}
				fwrite($i_fp_w,$i_content);
				fclose($i_fp_w);*/
			}
		}


		
	}

	fclose($b_fp);
	fclose($i_fp);

	
?>