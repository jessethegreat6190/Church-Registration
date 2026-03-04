$files = @(
    "c:\xampp\htdocs\watchman-to-watchmen\index.html",
    "c:\xampp\htdocs\watchman-to-watchmen\admin.html",
    "c:\xampp\htdocs\watchman-to-watchmen\upload.html"
)

# 1. Switch to compat scripts (required for the global 'firebase' object used in auth.js)
$oldScripts = @(
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js"',
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth.js"',
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore.js"',
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-storage.js"'
)

$newScripts = @(
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"',
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"',
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore-compat.js"',
    'src="https://www.gstatic.com/firebasejs/9.22.0/firebase-storage-compat.js"'
)

# 2. Fix corrupted characters (placeholder dots)
$corrupted = 'placeholder="â€¢â€¢â€¢â€¢â€¢â€¢â€¢â€¢"'
$fixed = 'placeholder="********"'

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        
        # Replace scripts
        for ($i=0; $i -lt $oldScripts.Count; $i++) {
            $content = $content.Replace($oldScripts[$i], $newScripts[$i])
        }
        
        # Fix placeholder
        $content = $content.Replace($corrupted, $fixed)
        
        # Save as UTF-8 without BOM to avoid encoding issues in browser
        [System.IO.File]::WriteAllText($file, $content, (New-Object System.Text.UTF8Encoding($false)))
    }
}

# 3. Fix corrupted characters in auth.js as well
$authPath = "c:\xampp\htdocs\watchman-to-watchmen\js\auth.js"
if (Test-Path $authPath) {
    $content = Get-Content $authPath -Raw
    $content = $content.Replace('ðŸ‘¤', '👤')
    [System.IO.File]::WriteAllText($authPath, $content, (New-Object System.Text.UTF8Encoding($false)))
}

Write-Output "Successfully fixed scripts and encoding"
