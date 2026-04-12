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
    "\.validation-reports"
)

$readmes = Get-ChildItem -Path . -Filter "README.md" -Recurse | Where-Object {
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

foreach ($file in $readmes) {
    $content = Get-Content $file.FullName -Raw

    # Ja tem type: definido? Pula
    if ($content -match "(?m)^type:") { continue }

    # Tem frontmatter?
    if ($content -match "^---\r?\n") {
        # Insere type: readme apos o primeiro ---
        $newContent = $content -replace "^(---\r?\n)", "`$1type: readme`n"
    } else {
        # Cria frontmatter
        $today = Get-Date -Format "yyyy-MM-dd"
        $newContent = "---`ntype: readme`nstatus: draft`nupdated: $today`n---`n`n$content"
    }

    Set-Content -Path $file.FullName -Value $newContent -NoNewline
    Write-Host "Updated: $($file.FullName)"
}

Write-Host "`nDone. Processed $($readmes.Count) README files."
