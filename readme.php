    <!doctype html>
    <html lang="en">
    <head>
       <meta charset="utf-8">
    </head>
    <body>    
        <a href="index.html">index.html</a>
    
        <?php
        // 1. Define the files and their markdown language types
        $files = array(
            "dirt.html" => "html",
            "dirt.css"  => "css",
            "dirt.js"   => "javascript",
            "dirt.py"   => "python",
            "dirt.bat"  => "batch",
            "dirt.php"  => "php",
            "dirt.json" => "json"
        );
    
        // 2. Start the README string
        $readme = "# README.md\n\n";
    
        // 3. Loop through each file
        foreach ($files as $filename => $lang) {
            
            // --- Part A: HTML Browser Output ---
            echo "<h2>" . $filename . "</h2>\n";
            echo '<pre id="' . $lang . '">';
            echo htmlspecialchars(file_get_contents($filename));
            echo "</pre>\n";
    
            // --- Part B: README Generator Output ---
            $readme .= "# " . $filename . "\n";
            $readme .= "\n```" . $lang . "\n";
            $readme .= file_get_contents($filename);
            $readme .= "\n```\n\n";
        }
    
        // 4. Save the finished README file
        file_put_contents("README.md", $readme);
        ?>
    
    </body>
    </html>
