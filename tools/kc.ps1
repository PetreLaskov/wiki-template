# Windows convenience launcher. Override discovery with an explicit KC_PYTHON path.
param([Parameter(ValueFromRemainingArguments = $true)][string[]]$CompilerArgs)
$ErrorActionPreference = 'Stop'
$compilerPythonCandidates = @()
if ($env:KC_PYTHON) { $compilerPythonCandidates += $env:KC_PYTHON }
if ($env:USERPROFILE) {
    $compilerPythonCandidates += Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
}
foreach ($compilerCommandName in @('python', 'python3')) {
    $compilerCommand = Get-Command $compilerCommandName -ErrorAction SilentlyContinue
    if ($compilerCommand) { $compilerPythonCandidates += $compilerCommand.Source }
}
foreach ($compilerPythonPath in ($compilerPythonCandidates | Select-Object -Unique)) {
    if (-not (Test-Path -LiteralPath $compilerPythonPath -PathType Leaf)) { continue }
    try {
        & $compilerPythonPath -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' 2>$null
        if ($LASTEXITCODE -ne 0) { continue }
    } catch { continue }
    & $compilerPythonPath (Join-Path $PSScriptRoot 'kc.py') @CompilerArgs
    exit $LASTEXITCODE
}
Write-Error 'No runnable Python 3.10+ found. Set KC_PYTHON to an installed Python executable path.'
exit 2
