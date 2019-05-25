<?php

$strJson = '{"seq" : 0, "command" : "get_daa", "data" : { "number" : "15", "name" : "Jon"}}';

$address = '127.0.0.1';
$port = 5008;


$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
socket_connect($sock, $address, $port);
socket_write($sock, $strJson, strlen($strJson));
$data = "";
do{
    $buf = socket_read($sock, 2048);
    if($buf == false){
        break;
    }
    $data .= $buf;
}while(true);
$json = json_decode($data);
for($i = 0; $i <100; $i++){
    echo $json->{$i}->{"url"} . "\t" . $json->{$i}->{"retweet_count_change"} . "\n";
}

socket_close($sock);
?>
