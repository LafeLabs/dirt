<?php

$dirtJSONurl = "https://raw.githubusercontent.com/LafeLabs/dirt/refs/heads/main/dirt.json";
$json_raw = file_get_contents($dirtJSONurl);
$dirtJSON = json_decode($json_raw);

mkdir("data");
mkdir("plots");

$baseurl = explode("dirt.json",$dirtJSONurl)[0];

foreach($file_set as $value){
    copy($baseurl.$value,$value);
}

?>
<a href = "dirt.html">dirt.html</a>
<style>
body{
    font-size:3em;
    font-family:arial;
}
a{
    font-size:3em;
    color:blue;
}
</style>
