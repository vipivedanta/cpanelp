<style>
  fieldset{
    border:solid 1px #ccc;
    padding: 10px;
    margin-top: 25px;
  }
</style>
<?php
$licenseinvalid = false;
if($licenseinvalid) {
	echo "<h2>License status: :".$results['status']."</h2>";
	echo "<h3>License message: ".$results['message']."</h3>";
	echo "<form method='post' action='addon_uploadmonitor.php'><input type='text' name='license' /><input type='submit' /></form>";
}
else {?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>.::A-AST Realtime File Upload Scanner(V1.0.1)::.</title>
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
    <div class="title-block">Configiration</div>
    <div class="fclear"></div>
    <!--content body start here-->
    <div id="content-body-main">	

    <div id="msg"></div>

    <?php 
       if(file_exists('configuration_1.conf')){

          $conf = array();
          $fp = fopen('configuration_1.conf','r');
          while(($line = fgets($fp)) !== false){
            $var = explode(':',$line);
            $confs[trim($var[0])] = trim($var[1]);
          }
          fclose($fp);

       }

       /*$w_checked = $home_checked = $public_checked =  $http_c = $ftp_c = '';
       $f_checked = '';
       $w_class = 'hide';
       $f_class = 'hide';
       $s_class = '';*/

       if(isset($confs)){

          $w_checked = $home_checked = $public_checked = '';
          $f_checked = '';
          $w_class = 'hide';
          $f_class = 'hide';
          $s_class = '';

          if($confs['mode'] == 'watcher'){
            $w_checked = 'checked';
            $w_class = 'show';
            $s_class = 'show';

            #which watcher 
            if($confs['watch_what'] == 'home'){
              $home_checked = 'checked';
            }else{
              $public_checked = 'checked';
            }


          }else{
            $f_class = 'show';
            $f_checked = 'checked';
            $s_class = 'show';

            $f_pure = $f_pro = '';
            if($confs['filter_what'] == 'pure'){
              $f_pure = 'checked';
            }else{
              $f_pro = 'checked';
            }

            $http_c = (isset($confs['http_filter']))?'checked':'';
            $ftp_c = (isset($confs['ftp_filter']))?'checked':'';


          }
       }


    ?>

    <form method="post" action="" id="config-form">
    
    <fieldset>
    <legend>Modes</legend>  
    <input type="radio" name="mode" value="watcher" id="watcher" <?php echo $w_checked;?>/>Watcher Mode<br/>
    <input type="radio" name="mode" value="filter" id="filter" <?php echo $f_checked;?>/>Filter Mode<br/>
    </fieldset>

    <fieldset id="watcher-opt" class="<?php echo $w_class;?>">
    <legend>Watcher Mode Options</legend>
    <input type="radio" name="watch_what" value="home" <?php echo $home_checked;?>/>Entire Home Directory<br/>
    <input type="radio" name="watch_what" value="publichtml" <?php echo $public_checked;?>/>public_html/<br/> 
    </fieldset>

    <fieldset id="filter-opt" class="<?php echo $f_class;?>">
    <legend>Filter Mode Options</legend>
    <input type="radio" name="filter_what" value="pure" <?php echo $f_pure;?>/>PureFTPd<br/>
    <input type="radio" name="filter_what" value="pro" <?php echo $f_pro;?>/>ProFTPd<br/> 
    
  
    <hr/><br/><br/>
    <input type="checkbox" name="http_filter" value="1" <?php echo $http_c;?>>HTTP filter
    <input type="checkbox" name="ftp_filter" value="1" <?php echo $ftp_c;?>>FTP filter
    </fieldset>
    
    <input type="button" name="submit" id="submit" value="Save Configuration" class="btn <?php echo $s_class;?>" />

    </form>

    </div>
    <!--content body end herer-->
  </div>
</div>
</body>
</html>
<?php } ?>

<script src="https://code.jquery.com/jquery-latest.min.js"></script>
<script type="text/javascript">
  
  jq = jQuery.noConflict();
  jq(document).ready(function(){

    jq("#watcher-opt").hide();
    jq("#filter-opt").hide();
    jq("#submit").hide();

    jq(".show").show();
    jq(".hide").hide();

    //when click on watcher
    jq("#watcher").click(function(){
      jq("#watcher-opt").fadeIn(1000);
      jq("#filter-opt").hide();
      jq("#submit").fadeIn(1000);
    });

    //when click on filter
    jq("#filter").click(function(){
      jq("#watcher-opt").hide();
      jq("#filter-opt").fadeIn(1000);
      jq("#submit").fadeIn(1000);
    });

    //when click on submit
    jq("#submit").click(function(){

      jq(this).attr("value","Processing...");
      var data = jq("#config-form").serialize();
      jq.post('update_config.php',data,function(response){
        jq("#msg").html(response);
        jq("#submit").attr("value","Save Configuration");
      });
    });

  });  

</script>
