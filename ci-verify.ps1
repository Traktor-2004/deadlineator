param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('build', 'test')]
    [string]$Mode
)

$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python312\python.exe'
$archive = Join-Path $projectRoot 'deadlineator-source.zip'
$outputDir = Join-Path $projectRoot '.ci-runner-output'

Write-Output "Mode: $Mode"
Write-Output "Working directory: $projectRoot"
Write-Output "Python executable: $pythonExe"

if (-not (Test-Path -LiteralPath $pythonExe)) {
    throw "Python 3.12 was not found: $pythonExe"
}
if (-not (Test-Path -LiteralPath $archive)) {
    throw "Source archive was not found: $archive"
}

if (-not (Test-Path -LiteralPath $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}
Write-Output 'Python and source archive found.'

Write-Output 'Extracting source archive...'
Expand-Archive -LiteralPath $archive -DestinationPath $projectRoot -Force
Write-Output 'Source archive extracted.'

function Invoke-CapturedPython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments,
        [Parameter(Mandatory = $true)]
        [string]$Description
    )

    $logPath = Join-Path $outputDir (([Guid]::NewGuid().ToString('N')) + '.log')
    Write-Output "Running: $Description"
    $commandOutput = & $pythonExe @Arguments 2>&1
    $pythonExitCode = $LASTEXITCODE
    $commandOutput | Tee-Object -FilePath $logPath

    if ($pythonExitCode -ne 0) {
        throw "$Description failed with exit code $pythonExitCode. Output: $logPath"
    }
}

if ($Mode -eq 'build') {
    Invoke-CapturedPython -Arguments @('--version') -Description 'Python version check'
    Invoke-CapturedPython -Arguments @('-m', 'compileall', '-q', 'src', 'tests', 'scripts') -Description 'Python compilation'
    Write-Output 'Compilation passed.'
} else {
    Invoke-CapturedPython -Arguments @('-m', 'unittest', 'discover', '-s', 'tests', '-v') -Description 'Unit tests'
    Write-Output 'Unit tests passed.'
}
