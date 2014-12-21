<?php
$fileName = "/etc/pure-ftpd.conf";
$myfile = fopen($fileName, "r");
if($myfile){
	$content = '';
	While(($line = fgets($myfile)) !== false){
		if(strpos($line, 'CallUploadScript')!==false)
		{
			$content.="CallUploadScript yes".PHP_EOL;
		}
		else {
			$content.= $line;
		}
	}
}
fclose($myfile);
file_put_contents('/etc/pure-ftpd.conf', $content);
?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>.::A-AST Realtime File Upload Scanner(v1.0.1)::.</title>
<link rel="stylesheet" href="css/master.css" type="text/css" media="screen" />
</head>
<body>
<!--header start here-->
<div id="header-top-main"></div>
<!--header end here-->
<div id="main-body-bg">
<div class="main-body-inner fleft">
<div class="header-inner"><img src="images/logo.png"  alt="Admin.ahead server technology" />
<div class="plan-version-bg fright">A-AST Realtime File Upload Scanner(v1.0.1)</div>
</div>
<div class="fclear"></div>
<!--menu button start here-->
<div class="button-menu-bg">
		<!--menu-->
		<div class="buttun-menu-main">
        <div class="buttun-menu-main1">
          <ul>
          <a href="addon_uploadmonitor.php" title="Home">  <li class="button-bcreate-backup"></li></a>
          		<a href="scan.php" title="Scan"> <li class="button-history-backup"></li></a>
                <a href="http.php" title="HTTP"> <li class="button-timeedit" id="active"></li></a>
          		<a href="ftp.php" title="FTP"> <li class="button-timeedit"></li></a>
          		<a href="rejected.php" title="Rejected Files"> <li class="button-rejected"></li></a>
            <a href="settings.php" title="Settings"><li class="button-restore"></li></a>
            </ul>
            </div>
            </div>
            <!--menu-->
             
            </div>
            <!--menu button end here-->
            <div class="fclear"></div>
            <div class="title-block">LAST 100 UPLOADED FILES</div>
            <div class="fclear"></div>
    <!--content body start here-->
    <div id="content-body-main">
    <?php 
    system ("chmod 777  /usr/local/apache/logs/modsec_audit.log");
    $modsec = exec('httpd -M|grep security2');
    if($modsec=='')
    {
        echo "Please install mod security";
    }
    else { ?>
    <div style="margin:0 auto;">
      <div class="table-main" style="margin:0 auto !important;">
        <div class="CSSTableGenerator" >
                <table >
                    <tr>
                        <td>
                            DATE
                        </td>
                        <td>
                            UPLOADED FILE
                        </td>
                        <td>
                           STATUS
                        </td>
                    </tr>
        <?php 
        
            #read scan log
            error_reporting(E_ALL);
            $scans = file('/usr/local/cpanel/whostmgr/docroot/cgi/httpupload/scanlog') or die('not accessible');
            $scans = array_reverse($scans);
            $i = 1;
            foreach($scans as $line){
                if($i <= 100){
                    $var = explode('>>',$line);
                    ?>
                     <tr>
                          <td><?php echo date('d F Y',strtotime($var[0]));?></td>
                          <td><?php echo $var[2];?></td>
                          <td><?php echo (strtolower(trim($var[1])) == 'ok')?'File OK':'Rejected';?></td>  
                     </tr>   
                    <?php 
                    $i++;
                }else{
                    break;
                }    
               
            }
        ?>
        </table>
            </div>
      </div>
      <!--table-->
    
      </div>
      <div class="fclear"></div>
    <?php }
    ?>
    </div>
    <!--content body end herer-->
  </div>
</div>
</body>
</html>