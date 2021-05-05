<?php
//ini_set('display_errors', 1);
//ini_set('display_startup_errors', 1);
//error_reporting(E_ALL);

$body = $_GET['body'];
$phone = $_GET['phone'];
$phone = str_replace('-', '', $phone);
$phone = str_replace('(', '', $phone);
$phone = str_replace(')', '', $phone);
$phone = str_replace(' ', '', $phone);
function sms($phone, $body)
{
	$sms_login = 'agreator_login';
	$sms_passw = 'agregator_passw';
	$url = 'http://apisms.expecto.me/messages/v2/send/';
	$data = array('login' => $sms_login, 'password' => $sms_passw, 'phone' => $phone, 'text' => $body);
	$options = array(
    'http' => array(
        'header'  => "Content-type: application/x-www-form-urlencoded\r\n",
        'method'  => 'POST',
        'content' => http_build_query($data)
		)
	);
	$context  = stream_context_create($options);
	$result = file_get_contents($url, false, $context);
	return $result;
}
$do = sms($phone, $body);
if ($do) { echo "sms worker ok";} else {echo "sms worker err";};