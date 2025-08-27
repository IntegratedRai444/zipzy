param(
	[string]$TreeFile = 'TREE-STRUCTURE-GENERATED.txt',
	[bool]$DryRun = $true
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $TreeFile)) {
	Write-Error "Tree file not found: $TreeFile"
	exit 1
}

$root = Get-Location
$regex = [regex]'(?i)[A-Za-z0-9_\-\/\.]+\.[A-Za-z0-9]+'
$listed = New-Object System.Collections.Generic.HashSet[string]

Get-Content -Path $TreeFile -ReadCount 2000 | ForEach-Object {
	foreach ($line in $_) {
		foreach ($m in $regex.Matches($line)) {
			$p = $m.Value.Trim()
			$p = $p -replace '^[\.\\/]+',''
			$p = $p -replace '\\','/'
			if (-not [string]::IsNullOrWhiteSpace($p)) {
				[void]$listed.Add($p)
			}
		}
	}
}

# Build actual file list relative to root
$actual = Get-ChildItem -Recurse -File |
	ForEach-Object { $_.FullName.Replace(($root.Path + '\\'),'') } |
	ForEach-Object { $_ -replace '\\','/' }

# Compute extras (on disk but not listed)
$extras = New-Object System.Collections.Generic.List[string]
foreach ($a in $actual) { if (-not ($listed.Contains($a))) { [void]$extras.Add($a) } }

$deleted = 0

if ($DryRun) {
	Write-Output ("Dry run: would delete {0} files not present in tree list" -f $extras.Count)
	$extras | Sort-Object | Select-Object -First 200 | ForEach-Object { Write-Output $_ }
	if ($extras.Count -gt 200) { Write-Output ("...and {0} more" -f ($extras.Count - 200)) }
} else {
	foreach ($rel in $extras) {
		$full = Join-Path -Path $root -ChildPath $rel
		try {
			Remove-Item -LiteralPath $full -Force -ErrorAction SilentlyContinue
			$deleted++
		} catch {}
	}
	Write-Output ("Deleted: {0} files" -f $deleted)
}


