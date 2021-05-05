<?php
//ini_set('error_reporting', E_ALL);
//ini_set('display_errors', 1);
//ini_set('display_startup_errors', 1);
//set_error_handler('var_dump', 1);
include('superpower/database.php');
$to = $_GET['to'];
$message = $_GET['message'];
$subj = $_GET['subj'];
$fr = 'robot@icstech.ru';
$frback = 'rec@icstech.ru';
$why_you_hate_me = $_POST['whyu'];
use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;
require "PHPMailer.php";
require "SMTP.php";

$mail = new PHPMailer;
$mail->isSMTP(); 
$mail->CharSet = 'UTF-8';
$mail->Host = "smtp.yandex.ru";
$mail->SMTPAuth = true; 
$mail->SMTPSecure = "ssl";
$mail->Port = 465;
$mail->setFrom("robot@icstech.ru");
$mail->isHTML(true); 
$mail->AddEmbeddedImage('img/2u_cs_mini.jpg', 'smiley');		
$mail->Subject = $subj;$mail->addAddress($to);$mail->Body = $message;
if (!$mail->send()) {
echo "Ошибка! почтового воркера";
} else {
header('Location: ' . $_SERVER['HTTP_REFERER']);
}
