<?php if(isset($_GET['b'])):
$success = 'Selected IP is banned permanently!';
elseif(isset($_GET['ub'])):
$success = 'Selected IP is removed from permanent ban list.';
endif;?>


<?php if(isset($err)):?>
<div class="alerte"><?php echo $err;?></div>
<?php endif;?>

<?php if(isset($success)):?>
<div class="alertm"><?php echo $success;?></div>
<?php endif;?>

<?php 
    $db = new SQLite3('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/ddos.db');
    $sql = "SELECT count(*) AS total FROM (SELECT ip,MAX(conn) conn,dt,count(ip) total FROM bann GROUP BY ip) AS ips";
    #$sql = 'SELECT * FROM bann';
    $result = $db->query($sql) or die('Cant access db');
    $row = $result->fetchArray(SQLITE3_ASSOC);

    $totalRows = $row['total'];
    $rowsPerPage = PER_PAGE;
    $totalPages = ceil($totalRows / $rowsPerPage);

    #current page
    if(isset($_GET['cp']) && is_numeric($_GET['cp'])){
        $cp = (int)$_GET['cp'];
    }else{
        $cp = 1;
    }

    if($cp > $totalPages){ 
        $cp = $totalPages;
    }else if($cp < 1){ 
        $cp = 1;
    }

    #offset
    $offset = ($cp - 1)*$rowsPerPage;

    
    #range
    $range = 3;
    ?>

    <!--Pagination-->
<div class="pagination">
<ul>
    <?php if($cp > 1):?>
    <li><a href="addon_aast_ddos_mitigator.cgi?do=ipbh&cp=1">First</a></li>
    <?php $prev_page = $cp - 1;?>
    <li><a href="addon_aast_ddos_mitigator.cgi?do=ipbh&cp=<?php echo $prev_page;?>">Prev</a></li>     
    <?php endif;?>
    
    <?php if($totalPages > 1):?>
    <?php for($x = ($cp-$range); $x<(($cp+$range)+1); $x++):?>
    <?php if($x > 0 && $x <= $totalPages):?>
    <?php if($x == $cp):?>
    <li class="current"><strong><?php echo $x;?></strong></li>
    <?php else:?>
    <li><a href="addon_aast_ddos_mitigator.cgi?do=ipbh&cp=<?php echo $x;?>"><?php echo $x;?></a></li>
    <?php endif;?>
    <?php endif;?>
    <?php endfor;?>
    <?php endif;?>

    <?php if($cp != $totalPages):?>
    <?php $next_page = $cp + 1;?>
    <li><a href="addon_aast_ddos_mitigator.cgi?do=ipbh&cp=<?php echo $next_page;?>">Next</a></li>
    <li><a href="addon_aast_ddos_mitigator.cgi?do=ipbh&cp=<?php echo $totalPages;?>">Last</a></li>
    <?php endif;?>

</ul>
</div>
<div class="fclear"></div>

<?php 
    
    #get permanently banned IPS
    $perma_banned = file('/usr/local/cpanel/whostmgr/cgi/aast_ddos_mitigator/permanent.ip.ban.list',FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    $perma_banned = array_map('trim',$perma_banned);

?>

<?php 
    $sql = "SELECT ip,MAX(conn) conn,dt,count(ip) total FROM bann GROUP BY ip ORDER BY dt DESC LIMIT $offset,$rowsPerPage";
    $result = $db->query($sql) or die("Couldn't connect to db");
?>
<ul>
<li></li>
<li>
<table class="tftable" border="1" >
<tr>
    <th>#</th><th>IP</th><th>No of Connections</th><th>Date</th><th>Action</th>
</tr>    
<?php $count = $offset; while($row = $result->fetchArray(SQLITE3_ASSOC)):?>
<tr>
    <td><?php echo ++$count;?></td>
    <td><?php echo $row['ip'];?></td>
     <td><?php echo $row['conn'];?></td>
    <td><?php echo date('M d,Y h:i:s',$row['dt']);?></td>
    <td class="action">
    <?php if(in_array($row['ip'],$perma_banned)):?>
    <a href="addon_aast_ddos_mitigator.cgi?do=unban&ip=<?php echo $row['ip'];?>&cp=<?php echo $cp;?>">Unban</a>   
    <?php else:?>
    <a href="addon_aast_ddos_mitigator.cgi?do=do_perma_ban&ip=<?php echo $row['ip'];?>&cp=<?php echo $cp;?>">Ban permanently</a> 
    <?php endif;?>
    </td>
</tr>
<?php endwhile;?>
</table>
</li></ul>




