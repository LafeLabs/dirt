<?php
$dirtspore = file_get_contents("dirtspore.py");

$dirt = explode("#spore-break", $dirtspore)[2];

$dirt_array = explode("\n", $dirt);

$raw_dirt = "";
foreach ($dirt_array as $line) {
    if (strlen($line) > 0) {
        $raw_dirt .= substr($line, 1) . "\n";
    }
}

$json_text = explode("</dirt.json>", explode("<dirt.json>", $raw_dirt)[1])[0];

$json_data = json_decode($json_text, true);

$file_names = $json_data['files'];

foreach ($file_names as $file_name) {
    $file_text = explode("</" . $file_name . ">", explode("<" . $file_name . ">", $raw_dirt)[1])[0];
    file_put_contents($file_name, $file_text);
}
?>
