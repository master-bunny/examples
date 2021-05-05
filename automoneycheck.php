<?php
//error_reporting(-1);
//ini_set('display_errors', 'On');
//set_error_handler("var_dump");
include('super_sesurity.php');
include('superpower/database.php');
include('functions.php');
date_default_timezone_set("Europe/Moscow"); 
$timest = time();

$query = mysql_query("SELECT * FROM payment WHERE step in (2, 23, 24) AND flag1 IS NULL" );


while ($row = mysql_fetch_assoc($query)) {
$uuid = $row['uuid'];
$pay_id = $row['pay_id'];
$status = $client->getPaymentInfo($pay_id)->status;
echo $pay_id . '=' . $status . '///';
if ($status == "succeeded"){
	echo "succeeded";
	accept_payment($uuid);
}

}
?>