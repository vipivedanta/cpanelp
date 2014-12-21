<?php 

    define('PLUGIN_NAME','Admin-Ahead DDoS Mitigator v1.0');
    define('PER_PAGE',15);

?>

<!doctype html>
<html>
<head>
<meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />

<title><?php echo PLUGIN_NAME;?></title>
<style>
  @charset "utf-8";
/* CSS Document */

@font-face {
    font-family: 'latoregular';
    src: url('font/lato-reg-webfont.eot');
    src: url('font/lato-reg-webfont.eot?#iefix') format('embedded-opentype'),
         url('font/lato-reg-webfont.woff2') format('woff2'),
         url('font/lato-reg-webfont.woff') format('woff'),
         url('font/lato-reg-webfont.ttf') format('truetype'),
         url('font/lato-reg-webfont.svg#latoregular') format('svg');
    font-weight: normal;
    font-style: normal;

}


.fleft {
    float: left;
}
.fright {
    float: right;
}
.fclear {
    clear: both
}
.fleftclear {
    clear: left
}
.frightclear {
    clear: right
}
* {
    margin: 0px;
    padding: 0px;
    border: 0px;
    text-decoration: none;
    outline: none;
    list-style: none;
}



.mrg-lft{margin-left:10px;}


#main-frame{/*width:900px;*/ max-width:98%; margin:0 auto; }

.mmain-inner{width:99.9%; float:left; border:1px #dfdfdf solid; border-radius:5px; }

.hedr{width:96.9%; padding:20px; float:left; 

background: #ffffff; /* Old browsers */
/* IE9 SVG, needs conditional override of 'filter' to 'none' */
background: url(data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiA/Pgo8c3ZnIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgdmlld0JveD0iMCAwIDEgMSIgcHJlc2VydmVBc3BlY3RSYXRpbz0ibm9uZSI+CiAgPGxpbmVhckdyYWRpZW50IGlkPSJncmFkLXVjZ2ctZ2VuZXJhdGVkIiBncmFkaWVudFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgeDE9IjAlIiB5MT0iMCUiIHgyPSIwJSIgeTI9IjEwMCUiPgogICAgPHN0b3Agb2Zmc2V0PSIwJSIgc3RvcC1jb2xvcj0iI2ZmZmZmZiIgc3RvcC1vcGFjaXR5PSIxIi8+CiAgICA8c3RvcCBvZmZzZXQ9IjQ5JSIgc3RvcC1jb2xvcj0iI2RmZGZkZiIgc3RvcC1vcGFjaXR5PSIxIi8+CiAgICA8c3RvcCBvZmZzZXQ9IjQ5JSIgc3RvcC1jb2xvcj0iI2RmZGZkZiIgc3RvcC1vcGFjaXR5PSIxIi8+CiAgPC9saW5lYXJHcmFkaWVudD4KICA8cmVjdCB4PSIwIiB5PSIwIiB3aWR0aD0iMSIgaGVpZ2h0PSIxIiBmaWxsPSJ1cmwoI2dyYWQtdWNnZy1nZW5lcmF0ZWQpIiAvPgo8L3N2Zz4=);
background: -moz-linear-gradient(top,  #ffffff 0%, #dfdfdf 49%, #dfdfdf 49%); /* FF3.6+ */
background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#ffffff), color-stop(49%,#dfdfdf), color-stop(49%,#dfdfdf)); /* Chrome,Safari4+ */
background: -webkit-linear-gradient(top,  #ffffff 0%,#dfdfdf 49%,#dfdfdf 49%); /* Chrome10+,Safari5.1+ */
background: -o-linear-gradient(top,  #ffffff 0%,#dfdfdf 49%,#dfdfdf 49%); /* Opera 11.10+ */
background: -ms-linear-gradient(top,  #ffffff 0%,#dfdfdf 49%,#dfdfdf 49%); /* IE10+ */
background: linear-gradient(to bottom,  #ffffff 0%,#dfdfdf 49%,#dfdfdf 49%); /* W3C */
filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#ffffff', endColorstr='#dfdfdf',GradientType=0 ); /* IE6-8 */


}




.hedr h1{ font-family: 'latoregular', sans-serif; font-size:1em; color:#E71010; float:right; margin-top:15px; margin-left:10px;  text-align:center; padding:10px; background:#FFF; border-radius:5px;    }
.hedr h1 span{color:#F90;}
.hedr img{border-radius:5px; -moz-border-radius:5px; -webkit-border-radius:5px;}
.sid-menu-man{max-width:180px; float:left;}

.sid-menu-man ul{}

.sid-menu-man ul li{ display:block; background:#f3f3f3; padding:10px 15px;  border: 1px solid #dadada;
  border-left: 0; border-bottom:0; font-family: 'latoregular', sans-serif; font-size:13px; color:#666;}
.sid-menu-man ul li:hover{background:#F90; color:#fff; cursor:pointer; }.sid-menu-man ul li#active{ background:#fff; border-right:0; color:#F90;}


.main-content{width:77.9%; float:left; padding-bottom:10px;}
.main-content h2{font-family: 'latoregular', sans-serif; color:#333; font-weight:bold; font-size:14px; padding:10px 15px; border-bottom:1px #dadada solid;  float:left; width:100%; margin-left:15px;}

.inner-contet{max-width:600px; border:1px #F0F0F0 solid; border-radius:3px; margin:10px 0px 0px 15px;  float:left;   padding-top:20px;}

.inner-contet ul{}
.inner-contet ul li{float:left; width:94%; color:#333; padding:10px 15px; font-family: 'latoregular', sans-serif; font-size:13px;}
.inner-contet ul li span{ color:#F00;}
.inner-contet ul li input[type='text']{padding:5px; float:right; border:1px #CCC solid; border-radius:3px;}
.inner-contet ul li label{ float:left;}
.inner-contet ul li select{padding:5px; float:right; border:1px #CCC solid; border-radius:3px;}


.btn-s {
  background: #ffffff;
  background-image: -webkit-linear-gradient(top, #ffffff, #f4f5f4);
  background-image: -moz-linear-gradient(top, #ffffff, #f4f5f4);
  background-image: -ms-linear-gradient(top, #ffffff, #f4f5f4);
  background-image: -o-linear-gradient(top, #ffffff, #f4f5f4);
  background-image: linear-gradient(to bottom, #ffffff, #f4f5f4);
  -webkit-border-radius: 5;
  -moz-border-radius: 5;
  border-radius: 5px;
  font-family: 'latoregular', sans-serif;
  color: #333333;
  font-size: 13px;
  padding: 2px 20px 2px 20px;
  border: solid #c7c7c7 1px;
  text-decoration: none;
  float:right;
}

.btn-s:hover {
  background: #75db41;
  background-image: -webkit-linear-gradient(top, #75db41, #33d113);
  background-image: -moz-linear-gradient(top, #75db41, #33d113);
  background-image: -ms-linear-gradient(top, #75db41, #33d113);
  background-image: -o-linear-gradient(top, #75db41, #33d113);
  background-image: linear-gradient(to bottom, #75db41, #33d113);
  text-decoration: none;
  color:#fff;
}



.alertm{width:93%; margin:15px auto; text-align:center; padding:10px 15px; background:#6cbd58; border-radius:5px; color:#fff; font-family: 'latoregular', sans-serif; font-size:13px; }

.alertm a{color:#F90;}

.foootr{width:98.8%; float:left; padding:10px; color:#666;  border-top:1px #f2f2f2 solid;  text-align:center; font-family: 'latoregular', sans-serif; font-size:12px; margin-top:20px;}

/*.table-1{width:100%;}.table-1 td{background:#999; padding:5px;}.table-1 tr{border:1px #090 solid;}*/


/*--inner table--*/


.ftabke-input-[type='text']{background-image:-web-kit-gradient(right,#fgnnn,#30F); }


@media screen and (max-width:500px) { 
.ftabke-input- select option{background:-web-kit-gradeint(bottom,#f90,#3f0),-moz-radial-gradeint(right,#550,#500),-o-radial-gradeint(top,#333,#003);

appearance:button; transform:scale(0.1,0.2); transition-duration:.5s;


}
}

/*table*/

.tabl-pagntn {
    float: right;
    margin: -4px 0 10px 0;
    
}
.tabl-pagntn a {
    float: left;
    font-size: 12px;
    color: #5dbffb;
    text-align: center;
    font-family: 'latoregular', sans-serif;
    padding: 2px;
}
.tabl-pagntn a:hover {
    color: #2d2d2d;
}
.tftable {
    font-size: 12px;
    color: #fff;
    width: 100%;
    font-family: 'latoregular', sans-serif;
    border-width: 1px;
    border-color: #729ea5;
    border-collapse: collapse;
    
}
.tftable th {
    font-size: 12px;
    background-color: #999999;
    border-width: 1px;
    padding: 8px;
    font-family: 'latoregular', sans-serif;
    border-style: solid;
    border-color: #fff;
    text-align: left;
    word-break:break-all;
}

.tftable td a{color:#F00;}
.tftable tr {
    background-color: #f2fbfe;
}
.tftable td {
    font-size: 12px;
    border-width: 1px;
    padding: 8px;
    border-style: solid;
    border-color: #E5E5E5;
    word-break: break-all;
    color:#333;
}
.tftable tr:hover {
    background-color: #fff;
}
.tftable tr:nth-child(odd){ background-color:#F5F4F4;}
.tftable tr:nth-child(even){background-color:#fff;}
.alerte{width:93%; margin:15px auto; text-align:center; padding:5px 10px; background:#F09365; border-radius:5px; color:#000; font-family: 'latoregular', sans-serif; font-size:13px; }

/*---inner table---*/
.pagination{float:right;  height:20px; }

.pagination ul{}

.pagination ul li{width:auto;
  font-size: 12px;
  color: #333333;
  padding:2px;
  
  text-align: center;
  font-family: 'latoregular', sans-serif;
  padding: 2px;}

.pagination ul li a{color: #333333;}
.pagination ul li a:hover{color:#F90;}
.pagination ul li#current{color:#F90 !important;}


</style>
</head>

<body>



<div id="main-frame"><!--main frame start-->

<div class="mmain-inner"><!--main inner start-->

<div class="hedr"><!--header-->
<a href="http://www.admin-ahead.com" target="_blank">
<img class="fleft" src="https://admin-ahead.com/wp-content/themes/admin-ahead/images/banner_2.png" alt="Admin.ahead server technology">
</a>

<h1><?php echo PLUGIN_NAME;?></h1>

</div><!--/header-->
<div class="fclear"></div>

<?php 

#echo '<pre>'; print_r($_SERVER);

$domain_v_name = `hostname`;
$domain_v_name = trim($domain_v_name);

function check_license($licensekey,$localkey="") {
    global $domain_v_name;
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
                    if (!in_array($domain_v_name, $validdomains)) {
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
        #$postfields["domain"] = $_SERVER['SERVER_NAME'];
        
        $postfields["domain"] = trim($domain_v_name);
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
 $licenseinvalid=true;
 if (file_exists('license.conf'))
 {
 	$localfile = file_get_contents('license.conf');
 }
 if (empty($localfile)) $localfile = '';
 preg_match('/^license=(\S+)\n/',$localfile,$match);
 if ( ! isset($match[1]))
 {
    $match[1] = null;
 }
 $license=$match[1];
preg_match('/\nlocalkey=(\S+)\n/',$localfile,$match);
if ( ! isset($match[1])) {
    $match[1] = null;
}
$key=$match[1];
	
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
         $file = fopen("license.conf","w");
         fwrite($file,"license=$license\n");
         fwrite($file,"localkey={$results['localkey']}");
         fclose($file);
     }
 }
if($licenseinvalid) {
	echo "<h4>License status:".$results['status']."</h4>";
	echo "<form method='post' action='addon_aast_ddos_mitigator.cgi'><input style='border:1px solid black;' type='text' name='license' /> <input type='submit' name ='submitlicense' value='Submit'/></form>";
}
else { ?>
<!--alert-->
<!--<div class="alertm">(D)DoS is currently enabled.<a href="#">Click to disable it</a></div>-->
<!--alert-->


<div class="fclear"></div>
<div class="sid-menu-man"><!--side menu-->
<ul>
<a href="addon_aast_ddos_mitigator.cgi" title="Configuration"><li <?php echo(!isset($_GET['do']))?'id="active"':'';?>>Configuration</li></a>
<a href="addon_aast_ddos_mitigator.cgi?do=wlip" title="IP whitelisting"><li <?php echo(isset($_GET['do']) && $_GET['do'] == 'wlip')?'id="active"':'';?>>IP Whitelisting</li></a>
<a href="addon_aast_ddos_mitigator.cgi?do=tbip" title="Temporarily banned IPs"><li <?php echo(isset($_GET['do']) && $_GET['do'] == 'tbip')?'id="active"':'';?>>Temporarily Banned IPs</li></a>
<a href="addon_aast_ddos_mitigator.cgi?do=ipbh" title="IP ban history"><li <?php echo(isset($_GET['do']) && $_GET['do'] == 'ipbh')?'id="active"':'';?>>IP ban history</li></a>
</ul>
</div><!--/side menu-->



<div class="main-content"><!---main-content-->

<?php if(!isset($_GET['do'])):?>
   
   <h2>Configuration</h2>
    <div class="fclear"></div>

    <div class="inner-contet">
    <?php require_once 'configuration.cgi';?>
    </div>

<?php elseif($_GET['do'] == 'wlip'):?>
    <h2>IP whitelisting</h2>  
     <div class="fclear"></div>
    <div class="inner-contet">
    <?php require_once 'ip_whitelisting.cgi';?>      
    </div>
        
<?php elseif($_GET['do'] == 'tbip'):?>
    <h2>Temporarily Banned IPs</h2>
     <div class="fclear"></div>
    <div class="inner-contet">
    <?php require_once 'temp_banned_ips.cgi';?>
    </div>

<?php elseif($_GET['do'] == 'ipbh'):?>
    <h2>IP Ban History</h2> 
    <div class="fclear"></div>
    <div class="inner-contet">
    <?php require_once 'ban_history.cgi';?>
    </div>

<?php elseif($_GET['do'] == 'dsbl'):?>
    <?php 

        #remove both the cron files.
        #unlink("/etc/cron.d/ddos.ban");
        #unlink("/etc/cron.d/ddos.unban");
        exec("crontab -l | grep -v ddos_ban.cgi | crontab -");
        exec("crontab -l | grep -v ddos_unban.cgi | crontab -");


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


    ?> 
    <script > window.location.href = 'addon_aast_ddos_mitigator.cgi';</script>     

<?php elseif($_GET['do'] == 'rmvip'):?>
                
                <?php 
                    error_reporting(E_ALL);    
                    $ip = $_GET['ip']; 
                    #$filePath = "/usr/local/ddos/ignore.ip.list";
                    $filePath = "/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ignore.ip.list";
                    $myfile = fopen($filePath, "r") or die("Unable to open file!");

                    #read line by line
                    if($myfile){
                        $content = '';
                        while(($line = fgets($myfile)) !== false){
                               if(trim($line) != $ip){
                                 $content .= trim($line)."\n";
                               }
                        }
                    }
                    fclose($myfile);

                    $myfile = fopen($filePath, "w") or die("Unable to open file!");
                    fwrite($myfile,$content);
                    fclose($myfile);
                    #echo $url = "addon_aast_ddos_deflate.cgi?do=wlip&ipremove=".$ip;
                    #header("Location:addon_aast_ddos_deflate.cgi?do=wlip");
                    ?>
                    <script > window.location.href = 'addon_aast_ddos_mitigator.cgi?do=wlip&ipremove=<?php echo $ip;?>';</script>    
               
                    <?php elseif($_GET['do'] == 'do_perma_ban'):?> 
                    
                    <?php 
                        $filePath = "/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/permanent.ip.ban.list";
                        $myfile = fopen($filePath, "a") or die("Unable to open file!"); 
                        fwrite($myfile,$_GET['ip'].PHP_EOL);
                        fclose($myfile); 


                        #ban process
                        if (file_exists("/etc/init.d/csf")) {
                            exec ("/usr/sbin/csf -d ".$_GET['ip']." 2> /dev/null");
                        }else if(file_exists("/etc/init.d/apf")) {
                            exec(" apf -d ".$_GET['ip']." 2> /dev/null");
                        }else { 
                            exec("iptables -I INPUT -s ".$_GET['ip']." -j DROP 2> /dev/null"); 
                        }
                    ?>   
                    <script > window.location.href = "addon_aast_ddos_mitigator.cgi?do=ipbh&cp=<?php echo $_GET['cp'];?>&b";</script>  
                    
   <?php elseif($_GET['do'] == 'unban'):?>
                    <?php 

                        #unban
                        if (file_exists("/etc/init.d/csf")) {
                            exec ("/usr/sbin/csf -dr ".$_GET['ip']." 2> /dev/null");
                        }else if(file_exists("/etc/init.d/apf")) {
                            exec(" apf -u ".$_GET['ip']." 2> /dev/null");
                        }else { 
                            exec("iptables -D INPUT -s ".$_GET['ip']." -j DROP 2> /dev/null"); 
                        }

                        $filePath = "/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/permanent.ip.ban.list";
                        $file = fopen($filePath,"r");
                        $content = '';
                        while(($line = fgets($file)) !== false){

                            if(trim($line) != $_GET['ip']){
                                $content .= $line;
                            }
                        }
                        fclose($file);
                        $file = fopen($filePath,"w");
                        fwrite($file,$content);
                        fclose($file);
                    ?>
                     <script > window.location.href = "addon_aast_ddos_mitigator.cgi?do=ipbh&cp=<?php echo $_GET['cp'];?>&ub";</script>  

<?php endif;?>

<div class="fclear"></div>

<div style="padding:15px;">
<hr/>   


</div><!---/main-content-->

<?php } ?>

<div class="foootr"><!---footer-->

Copyright © Admin-Ahead Server Technologies 2014 | All Rights Reserved


</div><!---/footer-->




</div><!--main inner end-->


</div><!-- main frame end-->




</body>
</html>
