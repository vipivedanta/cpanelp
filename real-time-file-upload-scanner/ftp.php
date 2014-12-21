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
          <a href="addon_uploadmonitor.php" title="Home">  <li id="active" class="button-bcreate-backup"></li></a>
          		<a href="scan.php" title="Scan"> <li class="button-history-backup"></li></a>
                <a href="http.php" title="HTTP"> <li class="button-timeedit"></li></a>
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
    $pureftp=exec('pgrep pure');
    if($pureftp=='')
    {
    	echo 'PureFTP is not installed or not running. Please refer <a href="http://docs.cpanel.net/twiki/bin/view/AllDocumentation/WHMDocs/FtpSelect" target="_blank">Switch FTP Server</a> to switch your FTP from cPanel or contact support <a href="https://admin-ahead.com/portal/submitticket.php?step=2&deptid=3" target="_blank">Submit Ticket</a>';
    }
    else {?>
    <div style="margin:0 auto;">
      <div class="table-main" style="margin:0 auto !important;">
        <div class="CSSTableGenerator" >
                <table >
                    <tr>
                        <td>
                            DATE
                        </td>
                        <td >
                            UPLOADER IP
                        </td>
                        <td>
                            USERNAME
                        </td>
                        <td>
                            LOCATION
                        </td>
                        <td>
                            FILE SIZE
                        </td>
                        <td>
                           STATUS
                        </td>
                    </tr>
    <?php 	
    	system ("tac /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/upload.txt > /usr/local/cpanel/whostmgr/docroot/cgi/httpupload/upload.txt.aast");
    	$fileName = "/usr/local/cpanel/whostmgr/docroot/cgi/httpupload/upload.txt.aast";
    	$myfile = fopen($fileName, "r");
    	if($myfile){
    		while(($line = fgets($myfile)) !== false){
    			$line = trim($line);
    			if($line!='')
    			{
	    			$data = explode(',,,',$line);
	    			$time = trim($data[0]);
	    			$uploadedip = trim($data[1]);
	    			$username = trim($data[2]);
	    			$location = trim($data[3]);
	    			$filesize = trim($data[4]);
	    			$status = trim($data[5]); ?>
	    			<tr>
						<td><div><?php echo $time;?></div></td>
					  	<td><div><?php echo $uploadedip; ?></div></td>          
					  	<td><div><?php echo $username;?></div></td>
						<td><div><?php echo $location;?></div></td>
						<td><div><?php echo $filesize;?></div></td>
						<td><div><?php echo $status;?></div></td>
					</tr>
	    		<?php	
	    		}
    		}
    	}
    	fclose($myfile); ?>
    	</table>
            </div>
      </div>
      <!--table-->
    
      </div>
      <div class="fclear"></div>
    <?php
    }
    ?>
    </div>
    <!--content body end herer-->
  </div>
</div>
</body>
</html>