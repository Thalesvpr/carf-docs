$excludePatterns = @(
    "SRC-CODE",
    "node_modules",
    "\.vitepress",
    "dist",
    "CARF\\docs\\",
    "\.vscode",
    "\.idea",
    "logs",
    "\.claude",
    "\.temp_reports",
    "\.validation-reports",
    "\.template"
)

$files = Get-ChildItem -Path . -Filter "*.md" -Recurse | Where-Object {
    $path = $_.FullName
    $name = $_.Name

    # Exclui READMEs
    if ($name -eq "README.md") { return $false }

    # Exclui patterns
    $exclude = $false
    foreach ($pattern in $excludePatterns) {
        if ($path -match $pattern) {
            $exclude = $true
            break
        }
    }
    -not $exclude
}

$updated = 0
foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw
    if ($content -match "(?m)^type:") { continue }
    if ($content -match "^---\r?\n") {
        $newContent = $content -replace "^(---\r?\n)", "`$1type: leaf`n"
    } else {
        $today = Get-Date -Format "yyyy-MM-dd"
        $newContent = "---`ntype: leaf`nstatus: draft`nupdated: $today`n---`n`n$content"
    }
    Set-Content -Path $file.FullName -Value $newContent -NoNewline
    Write-Host "Updated: $($file.FullName)"
    $updated++
}

Write-Host "`nDone. Updated $updated leaf files (of $($files.Count) checked)."
