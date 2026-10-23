$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
$archive = Join-Path $projectRoot 'deadlineator-source.zip'
$outputDir = Join-Path $projectRoot '.ci-runner-output'

if (-not (Test-Path -LiteralPath $pythonExe)) { throw "Python 3.12 was not found: $pythonExe" }
if (-not (Test-Path -LiteralPath $archive)) { throw "Source archive was not found: $archive" }
if (-not (Test-Path -LiteralPath $outputDir)) { New-Item -ItemType Directory -Path $outputDir | Out-Null }
Expand-Archive -LiteralPath $archive -DestinationPath $projectRoot -Force

$id = [Guid]::NewGuid().ToString('N')
$stdoutPath = Join-Path $outputDir "$id.stdout"
$stderrPath = Join-Path $outputDir "$id.stderr"
$process = Start-Process -FilePath $pythonExe -ArgumentList @('-m', 'unittest', 'discover', '-s', 'tests', '-v') -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath -Wait -PassThru -NoNewWindow
if (Test-Path -LiteralPath $stdoutPath) { Get-Content -LiteralPath $stdoutPath | ForEach-Object { Write-Output $_ } }
if (Test-Path -LiteralPath $stderrPath) { Get-Content -LiteralPath $stderrPath | ForEach-Object { Write-Output $_ } }
if ($process.ExitCode -ne 0) { throw "Unit tests failed with exit code $($process.ExitCode)." }
Write-Output 'Unit tests passed.'