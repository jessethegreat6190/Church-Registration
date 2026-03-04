$files = @(
    "c:\xampp\htdocs\watchman-to-watchmen\index.html",
    "c:\xampp\htdocs\watchman-to-watchmen\admin.html",
    "c:\xampp\htdocs\watchman-to-watchmen\upload.html"
)

# 1. Fix Firebase scripts to use compat
$oldS = 'firebasejs/9.22.0/firebase-app.js'
$newS = 'firebasejs/9.22.0/firebase-app-compat.js'
$oldAuth = 'firebasejs/9.22.0/firebase-auth.js'
$newAuth = 'firebasejs/9.22.0/firebase-auth-compat.js'
$oldFS = 'firebasejs/9.22.0/firebase-firestore.js'
$newFS = 'firebasejs/9.22.0/firebase-firestore-compat.js'
$oldST = 'firebasejs/9.22.0/firebase-storage.js'
$newST = 'firebasejs/9.22.0/firebase-storage-compat.js'

foreach ($file in $files) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        
        $content = $content.Replace($oldS, $newS)
        $content = $content.Replace($oldAuth, $newAuth)
        $content = $content.Replace($oldFS, $newFS)
        $content = $content.Replace($oldST, $newST)
        
        # 2. Fix placeholders - targeting the pattern specifically
        $content = [regex]::Replace($content, 'placeholder="[^"]*â[^"]*"', 'placeholder="********"')
        
        # 3. Clean up other corrupted emojis in HTML headers
        $content = [regex]::Replace($content, 'ðŸ“¤', '📤')
        $content = [regex]::Replace($content, 'ðŸ‘¨â€ðŸ’¼', '👨‍💼')
        $content = [regex]::Replace($content, 'ðŸ“Š', '📊')
        $content = [regex]::Replace($content, 'â³', '⏳')
        $content = [regex]::Replace($content, 'ðŸ“‹', '📋')
        
        [System.IO.File]::WriteAllText($file, $content, (New-Object System.Text.UTF8Encoding($false)))
    }
}

# 4. Fix auth.js
$authPath = "c:\xampp\htdocs\watchman-to-watchmen\js\auth.js"
if (Test-Path $authPath) {
    $content = Get-Content $authPath -Raw
    $content = [regex]::Replace($content, 'ðŸ‘¤', '👤')
    [System.IO.File]::WriteAllText($authPath, $content, (New-Object System.Text.UTF8Encoding($false)))
}

Write-Output "Successfully updated scripts and fixed encoding"
