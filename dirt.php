<?php
$spore = "https://raw.githubusercontent.com/LafeLabs/dirt/refs/heads/main/dirt.php";
$baseurl = explode("dirt.php",$spore)[0];

@copy($baseurl."index.html","index.html");
@copy($baseurl."README.md","README.md");
@copy($baseurl."edit-files.html","edit-files.html");
@copy($baseurl."save-file.php","save-file.php");
@copy($baseurl."save-file-get.php","save-file-get.php");
@copy($baseurl."load-file.php","load-file.php");
@copy($baseurl."list-files.html","list-files.php");

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
<a href = "index.html">index.html</a>
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