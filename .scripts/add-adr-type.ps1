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

$adrs = Get-ChildItem -Path . -Filter "ADR-*.md" -Recurse | Where-Object {
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

foreach ($file in $adrs) {
    $content = Get-Content $file.FullName -Raw

    # Ja tem type: definido? Pula
    if ($content -match "(?m)^type:") { continue }

    # Tem frontmatter?
    if ($content -match "^---\r?\n") {
        # Insere type: adr apos o primeiro ---
        $newContent = $content -replace "^(---\r?\n)", "`$1type: adr`n"
    } else {
        # Cria frontmatter
        $today = Get-Date -Format "yyyy-MM-dd"
        $newContent = "---`ntype: adr`nstatus: draft`nupdated: $today`n---`n`n$content"
    }

    Set-Content -Path $file.FullName -Value $newContent -NoNewline
    Write-Host "Updated: $($file.FullName)"
}

Write-Host "`nDone. Processed $($adrs.Count) ADR files."
