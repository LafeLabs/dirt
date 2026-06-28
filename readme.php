<!doctype html>
<html lang="en">
<head>
   <meta charset="utf-8">
</head>
<body>    
    <a href="index.html">index.html</a>
<?php
    $files = array(
        "dirt.html" => "html",
        "dirt.css"  => "css",
        "dirt.js"   => "javascript",
        "dirt.py"   => "python",
        "dirt.bat"  => "batch",
        "dirt.php"  => "php",
        "dirt.json" => "json"
    );

    $readme = "# dirt\n\n";
    $readme .= "## human body &harr; p5js &harr; python\n\n";
    $readme .= "## self-replicating code swarm\n\n";
    $readme .= "## [replicator spore](https://raw.githubusercontent.com/LafeLabs/dirt/refs/heads/main/dirt.php)\n\n";
    foreach ($files as $filename => $lang) {
        
        echo "<h2>" . $filename . "</h2>\n";
        echo '<pre id="' . $lang . '">';
        echo htmlspecialchars(file_get_contents($filename));
        echo "</pre>\n";

        $readme .= "## " . $filename . "\n";
        $readme .= "\n```" . $lang . "\n";
        $readme .= file_get_contents($filename);
        $readme .= "\n```\n\n";
    }
    $readme .= "\n## [dirt.md](dirt.md)";

    file_put_contents("README.md", $readme);    
    file_put_contents("dirt.md", $readme);    
    
?>
</body>
</html>
