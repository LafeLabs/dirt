<?php
$spore = "https://raw.githubusercontent.com/LafeLabs/dirt/refs/heads/main/dirt.php";
$baseurl = explode("dirt.php",$spore)[0];
$fileExtensions = ["html", "css", "js", "py", "bat", "md", "php", "json"];
foreach ($fileExtensions as $extension) {
    @copy($baseurl."dirt.".$extension,"dirt.".$extension);
}
if (!is_dir("data")) {
    mkdir("data");
}
if (!is_dir("plots")) {
    mkdir("plots");
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