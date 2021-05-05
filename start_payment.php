<?php
include('superpower/database.php');
include('functions.php');
include('super_sesurity.php');
date_default_timezone_set("Europe/Moscow"); 

$uuid = work_status();
//$uuid = $_GET['uuid'];
$receipt = $_GET['status'];


if ($receipt == 'accept'){
	
if (!payment_db($uuid) and ($receipt == 'accept')){
	
	echo "pay not in db so launcher";
	header("Location:" . launch($client->createPayment(prepare_payment($uuid))->id, $uuid));
}

if (payment_db($uuid)){
	$payment = $client->getPaymentInfo(payment_db($uuid)['pay_id'])->status;
	echo $payment;
	switch ($payment){
		case "pending":
			echo "pay status =  pending";
			$url = "https://yoomoney.ru/api-pages/v2/payment-confirm/epl?orderId=" . payment_db($uuid)['pay_id'];
			header("Location:" . $url);
		break;
		case "canceled":
			echo "pay status = canceled";
			header("Location:" . launch_canceled($client->createPayment(prepare_payment($uuid))->id, $uuid));
		break;
		case "succeeded":
			echo "pay status =  succeeded";
			header("Location:era_action.php");
		break;
	}

}
} else {
	header("Location:custom_pay/light_receipt_auto.php?uuid=" . $uuid);
}
