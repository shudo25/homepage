param(
    [Parameter(Mandatory = $true)][string]$FrameArchive,
    [string]$FfmpegPath = 'ffmpeg'
)

$ErrorActionPreference = 'Stop'
$encoder = (Get-Command $FfmpegPath -ErrorAction Stop).Source
$archive = (Resolve-Path -LiteralPath $FrameArchive).Path
$raw = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'security_preview_data.js') -Raw -Encoding UTF8
$match = [regex]::Match($raw, '(?s)^window\.securityPreviewTurns = (.*?);\s*window\.securityPreviewAudio = (.*?);\s*(?:window\.securityPreviewAudioStatus = "(current|outdated|missing|unverified)";\s*)?$')
if (-not $match.Success) { throw 'Invalid preview data. Run build_preview_data.ps1 -UseAudio.' }
$turns = ConvertFrom-Json $match.Groups[1].Value
$audio = ConvertFrom-Json $match.Groups[2].Value
if ($match.Groups[3].Success -and $match.Groups[3].Value -ne 'current') { throw 'Audio does not match the dialogue. Regenerate audio or use a silent preview.' }
if ($turns.Count -eq 0 -or -not $audio -or $audio.duration -lt 300 -or $audio.duration -gt 420) {
    throw 'Expected narrated turns and a 5-7 minute timeline.'
}
$entries = @(& tar -tf $archive)
if ($LASTEXITCODE -ne 0) { throw 'Cannot read frame archive.' }
if ($entries -notcontains 'frames.json' -or @($entries | Where-Object { $_ -ne 'frames.json' -and $_ -notmatch '^frame-\d{3}\.png$' }).Count) {
    throw 'Expected an animated frame archive. Export images again from the current preview.'
}
$manifestText = @(& tar -xOf $archive frames.json)
if ($LASTEXITCODE -ne 0) { throw 'Cannot read frame manifest.' }
$manifest = ConvertFrom-Json ($manifestText -join "`n")
$narration = Join-Path $PSScriptRoot $audio.src.Replace('/', '\')
if ($manifest.version -ne 1 -or $manifest.fps -ne 15 -or [math]::Abs($manifest.duration - $audio.duration) -gt 0.0001) {
    throw 'Frame manifest does not match the narrated timeline.'
}
if ($manifest.dataHash -ne (Get-FileHash -LiteralPath (Join-Path $PSScriptRoot 'security_preview_data.js')).Hash.ToLowerInvariant() -or
    $manifest.audioHash -ne (Get-FileHash -LiteralPath $narration).Hash.ToLowerInvariant()) {
    throw 'Audio or subtitle data changed after frame export. Export images again.'
}
if (-not $manifest.segments -or $manifest.segments.Count -gt [math]::Ceiling($audio.duration * 15)) {
    throw 'Invalid frame segment count.'
}
$sum = 0.0
foreach ($segment in $manifest.segments) {
    if ($segment.file -notmatch '^frame-\d{3}\.png$' -or -not ($segment.duration -is [double] -or $segment.duration -is [decimal] -or $segment.duration -is [int] -or $segment.duration -is [long]) -or
        [double]::IsNaN($segment.duration) -or [double]::IsInfinity($segment.duration) -or $segment.duration -le 0) {
        throw 'Invalid frame segment.'
    }
    $sum += $segment.duration
}
if ([math]::Abs($sum - $audio.duration) -gt 0.0001) { throw 'Frame durations do not cover the audio timeline.' }
$names = @($manifest.segments | ForEach-Object { $_.file } | Sort-Object -Unique)
if ($entries.Count -ne $names.Count + 1 -or (Compare-Object (@($names) + @('frames.json')) $entries)) {
    throw 'Frame archive entries do not match the manifest.'
}
$work = Join-Path ([System.IO.Path]::GetTempPath()) ('security-video-' + [guid]::NewGuid().ToString('N'))
$null = New-Item -ItemType Directory -Path $work
$temporary = Join-Path $work 'security-preview-animated.mp4'
try {
    & tar -xf $archive -C $work
    if ($LASTEXITCODE -ne 0) { throw 'Cannot extract frame archive.' }
    foreach ($name in $names) {
        $file = Get-Item -LiteralPath (Join-Path $work $name)
        if ($file.Length -eq 0 -or $file.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            throw "Invalid frame: $name"
        }
    }
    $list = @('ffconcat version 1.0')
    foreach ($segment in $manifest.segments) {
        $list += "file '$($segment.file)'"
        $list += 'option framerate 48000'
        $list += 'duration ' + ([double]$segment.duration).ToString('0.########', [System.Globalization.CultureInfo]::InvariantCulture)
    }
    $list += "file '$($manifest.segments[-1].file)'"
    $list += 'option framerate 48000'
    $concat = Join-Path $work 'frames.txt'
    [System.IO.File]::WriteAllLines($concat, $list, [System.Text.UTF8Encoding]::new($false))
    $total = ([double]$audio.duration).ToString('0.########', [System.Globalization.CultureInfo]::InvariantCulture)
    & $encoder -hide_banner -loglevel warning -nostdin -y -f concat -safe 0 -i $concat -i $narration -map 0:v:0 -map 1:a:0 -vf fps=15 -c:v libx264 -threads 4 -preset fast -crf 22 -pix_fmt yuv420p -c:a aac -b:a 160k -t $total -movflags +faststart $temporary
    if ($LASTEXITCODE -ne 0) { throw 'MP4 encoding failed.' }
    & $encoder -hide_banner -loglevel error -nostdin -i $temporary -map 0:v:0 -map 0:a:0 -f null -
    if ($LASTEXITCODE -ne 0) { throw 'Encoded MP4 did not fully decode.' }
    $output = Join-Path $PSScriptRoot 'security-preview-animated.mp4'
    Move-Item -LiteralPath $temporary -Destination $output -Force
    Write-Output "Saved $output ($total seconds, H.264/AAC, 1600x900, 15 fps)."
} finally {
    Remove-Item -LiteralPath $work -Recurse -Force
}
