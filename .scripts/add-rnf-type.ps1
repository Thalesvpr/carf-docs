$excludePatterns = @(
    "SRC-CODE",
    "node_modules",
    "\.vitepress",
    "dist",
    "\\docs\\",
    "\.vscode",
    "\.idea",
    "logs",
    "\.claude",
    "\.temp_reports",
    "\.validation-reports"
)

$files = Get-ChildItem -Path . -Filter "RNF-*.md" -Recurse | Where-Object {
    $path = $_.FullName
    $exclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($path -match $pattern) {
            $exclude = $true
            break
        }
    }
    -not $exclude
}

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match "(?m)^type:") { continue }
    if ($content -match "^---\r?\n") {
        $newContent = $content -replace "^(---\r?\n)", "`$1type: rnf`n"
    } else {
        $today = Get-Date -Format "yyyy-MM-dd"
        $newContent = "---`ntype: rnf`nstatus: draft`nupdated: $today`n---`n`n$content"
    }
    Set-Content -Path $file.FullName -Value $newContent -NoNewline
    Write-Host "Updated: $($file.FullName)"
}

Write-Host "`nDone. Processed $($files.Count) RNF files."
