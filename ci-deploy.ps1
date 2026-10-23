$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
Set-Location -LiteralPath $projectRoot

$archive = Join-Path $projectRoot 'deadlineator-source.zip'
$releaseParent = Join-Path $projectRoot 'deploy\releases'
if (-not (Test-Path -LiteralPath $archive)) {
    throw "Source archive was not found: $archive"
}

Expand-Archive -LiteralPath $archive -DestinationPath $projectRoot -Force

$releaseName = 'release-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff')
$releasePath = Join-Path $releaseParent $releaseName
New-Item -ItemType Directory -Path $releasePath -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $releasePath 'data'), (Join-Path $releasePath 'scripts') -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot 'src') -Destination $releasePath -Recurse
Copy-Item -LiteralPath (Join-Path $projectRoot 'data\demo_tasks.json') -Destination (Join-Path $releasePath 'data') -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'scripts\seed_demo_data.py') -Destination (Join-Path $releasePath 'scripts') -Force
Copy-Item -LiteralPath (Join-Path $projectRoot 'README.md') -Destination $releasePath -Force

$requiredFiles = @(
    (Join-Path $releasePath 'src\server.py'),
    (Join-Path $releasePath 'src\static\index.html'),
    (Join-Path $releasePath 'data\demo_tasks.json'),
    (Join-Path $releasePath 'scripts\seed_demo_data.py')
)
foreach ($file in $requiredFiles) {
    if (-not (Test-Path -LiteralPath $file)) {
        throw "Release is incomplete; missing $file"
    }
}

Write-Output "Local release prepared: $releasePath"
