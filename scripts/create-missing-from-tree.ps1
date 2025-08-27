param(
	[string]$TreeFile = 'TREE-STRUCTURE-GENERATED.txt'
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $TreeFile)) {
	Write-Error "Tree file not found: $TreeFile"
	exit 1
}

$root = Get-Location
$regex = [regex]'(?i)[A-Za-z0-9_\-\/\.]+\.[A-Za-z0-9]+'
$set = New-Object System.Collections.Generic.HashSet[string]

# Collect unique file paths from the tree structure
Get-Content -Path $TreeFile -ReadCount 1000 | ForEach-Object {
	foreach ($line in $_) {
		foreach ($m in $regex.Matches($line)) {
			$p = $m.Value.Trim()
			# Normalize: strip leading ./ or .\ and collapse backslashes
			$p = $p -replace '^[\.\\/]+',''
			$p = $p -replace '\\','/'
			if (-not [string]::IsNullOrWhiteSpace($p)) {
				[void]$set.Add($p)
			}
		}
	}
}

$created = 0
$skipped = 0

foreach ($rel in $set) {
	$full = Join-Path -Path $root -ChildPath $rel
	$dir = Split-Path -Path $full -Parent
	if ($dir -and -not [string]::IsNullOrWhiteSpace($dir)) {
		New-Item -ItemType Directory -Path $dir -Force | Out-Null
	}
	if (Test-Path -LiteralPath $full) {
		$skipped++
		continue
	}
	try {
		New-Item -ItemType File -Path $full -Force | Out-Null
		$created++
	} catch {
		# ignore errors and continue
	}
}

# Build current actual list
$actual = Get-ChildItem -Recurse -File |
	ForEach-Object { $_.FullName.Replace(($root.Path + '\\'),'') } |
	ForEach-Object { $_ -replace '\\','/' }

$missing = New-Object System.Collections.Generic.List[string]
foreach ($rel in $set) { if (-not ($actual -contains $rel)) { [void]$missing.Add($rel) } }

$extra = New-Object System.Collections.Generic.List[string]
foreach ($a in $actual) { if (-not ($set.Contains($a))) { [void]$extra.Add($a) } }

Write-Output ("Created: {0}  Skipped(existing): {1}" -f $created, $skipped)
Write-Output '--- Still Missing (in TXT but not on disk) ---'
$missing | Sort-Object -Unique | Out-String | Write-Output
Write-Output '--- Extra (on disk but not in TXT) ---'
$extra | Sort-Object -Unique | Out-String | Write-Output


