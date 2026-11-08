param(
    [switch]$GenerateAudio,
    [switch]$UseAudio,
    [ValidateRange(0, 100)][int]$Speed = 45
)

$ErrorActionPreference = 'Stop'
if ($GenerateAudio) { $UseAudio = $true }
$audioDirectory = Join-Path $PSScriptRoot 'audio'
$sourceRecord = Join-Path $audioDirectory 'speech-source.json'
$gap = 0.75
$hold = 10.0
$clips = @()

function Get-DialogueHash($Turns) {
    $speech = @($Turns | ForEach-Object {
        [ordered]@{ speaker = $_.speaker; text = ($_.text -replace '\r?\n', '') }
    })
    $json = ConvertTo-Json -InputObject $speech -Depth 3 -Compress
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        return [System.BitConverter]::ToString($sha.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($json))).Replace('-', '').ToLowerInvariant()
    } finally {
        $sha.Dispose()
    }
}

function Read-PcmWave($Path) {
    $reader = [System.IO.BinaryReader]::new([System.IO.File]::OpenRead($Path))
    try {
        if ([System.Text.Encoding]::ASCII.GetString($reader.ReadBytes(4)) -ne 'RIFF') { throw "Invalid RIFF: $Path" }
        $null = $reader.ReadUInt32()
        if ([System.Text.Encoding]::ASCII.GetString($reader.ReadBytes(4)) -ne 'WAVE') { throw "Invalid WAVE: $Path" }
        $byteRate = 0
        $data = $null
        while ($reader.BaseStream.Position + 8 -le $reader.BaseStream.Length) {
            $id = [System.Text.Encoding]::ASCII.GetString($reader.ReadBytes(4))
            $size = $reader.ReadUInt32()
            $next = $reader.BaseStream.Position + $size + ($size % 2)
            if ($next -gt $reader.BaseStream.Length) { throw "Truncated WAV: $Path" }
            if ($id -eq 'fmt ') {
                if ($size -lt 16) { throw "Invalid WAV format: $Path" }
                $format = $reader.ReadUInt16()
                $channels = $reader.ReadUInt16()
                $rate = $reader.ReadUInt32()
                $byteRate = $reader.ReadUInt32()
                $alignment = $reader.ReadUInt16()
                $bits = $reader.ReadUInt16()
                if ($format -ne 1 -or $channels -ne 1 -or $rate -ne 48000 -or $bits -ne 16 -or $alignment -ne 2 -or $byteRate -ne 96000) {
                    throw "Expected 48 kHz, mono, 16-bit PCM: $Path"
                }
            } elseif ($id -eq 'data') {
                $data = $reader.ReadBytes($size)
            }
            $reader.BaseStream.Position = $next
        }
        if ($byteRate -eq 0 -or -not $data -or $data.Length % 2) { throw "Empty or invalid PCM: $Path" }
        $peak = 0
        for ($i = 0; $i + 1 -lt $data.Length; $i += 1000) {
            $peak = [math]::Max($peak, [math]::Abs([int][System.BitConverter]::ToInt16($data, $i)))
        }
        if ($peak -eq 0) { throw "Silent dialogue: $Path" }
        return @{ Data = $data; Duration = $data.Length / [double]$byteRate }
    } finally {
        $reader.Dispose()
    }
}

if ($GenerateAudio) {
    Add-Type -Path 'C:\Program Files\CeVIO\CeVIO AI\CeVIO.Talk.RemoteService2.dll'
    if (-not [CeVIO.Talk.RemoteService2.ServiceControl2]::IsHostStarted) { throw 'Start CeVIO AI before generating audio.' }
    $sasara = [regex]::Unescape('\u3055\u3068\u3046\u3055\u3055\u3089')
    $takahashi = [regex]::Unescape('\u30bf\u30ab\u30cf\u30b7')
    $available = [CeVIO.Talk.RemoteService2.TalkerAgent2]::AvailableCasts
    if ($available -notcontains $sasara -or $available -notcontains $takahashi) { throw 'Both licensed voices must be available.' }
    $talkers = @{}
    $talkers[[regex]::Unescape('\u3055\u3055\u3089')] = [CeVIO.Talk.RemoteService2.Talker2]::new($sasara)
    $talkers[[regex]::Unescape('\u9ad8\u6a4b')] = [CeVIO.Talk.RemoteService2.Talker2]::new($takahashi)
    foreach ($talker in $talkers.Values) { $talker.Speed = $Speed }
    $null = New-Item -ItemType Directory -Path $audioDirectory -Force
}
$source = Join-Path $PSScriptRoot 'security_video_script.txt'
$text = Get-Content -LiteralPath $source -Raw -Encoding UTF8
$sections = [regex]::Matches($text, '(?ms)^\u3010([1-6])\u3000([^\r\n]+)\u3011\r?\n(.*?)(?=^\u3010|\z)')
$budgets = @(35, 70, 75, 80, 65, 35)
$turns = @()
$start = 0.0
foreach ($section in $sections) {
    $index = [int]$section.Groups[1].Value - 1
    $dialogue = [regex]::Matches($section.Groups[3].Value, '(?ms)^(\u3055\u3055\u3089|\u9ad8\u6a4b)\uff1a\r?\n(.*?)(?=\r?\n\r?\n)')
    if ($dialogue.Count -eq 0) { throw "No dialogue in section $($index + 1)" }
    $weights = @($dialogue | ForEach-Object { ([regex]::Replace($_.Groups[2].Value, '\s', '')).Length + 12 })
    $totalWeight = ($weights | Measure-Object -Sum).Sum
    for ($i = 0; $i -lt $dialogue.Count; $i++) {
        $duration = $budgets[$index] * $weights[$i] / $totalWeight
        $speaker = $dialogue[$i].Groups[1].Value
        $spoken = $dialogue[$i].Groups[2].Value.Trim()
        $turn = [ordered]@{
            scene = $index
            speaker = $speaker
            text = $spoken
            start = $start
            duration = $duration
        }
        $turns += $turn
        $start += $duration
    }
}
if ($sections.Count -ne 6 -or $turns.Count -eq 0) {
    throw "Unexpected script structure: $($sections.Count) sections, $($turns.Count) turns. Review parsing and timing."
}
$dialogueHash = Get-DialogueHash $turns
$missing = @(1..$turns.Count | Where-Object {
    -not (Test-Path -LiteralPath (Join-Path $audioDirectory ('turn-{0:D3}.wav' -f $_)) -PathType Leaf)
})
$audioState = if ($missing.Count -eq 0) { 'unverified' } else { 'missing' }
if (-not $GenerateAudio -and (Test-Path -LiteralPath $sourceRecord -PathType Leaf)) {
    $record = ConvertFrom-Json (Get-Content -LiteralPath $sourceRecord -Raw -Encoding UTF8)
    if ($record.version -ne 1 -or $record.dialogueHash -notmatch '^[0-9a-f]{64}$') { throw 'Invalid audio source record. Regenerate audio.' }
    if ($record.dialogueHash -ne $dialogueHash) { $audioState = 'outdated' }
    elseif ($missing.Count -eq 0) { $audioState = 'current' }
}
if ($UseAudio -and -not $GenerateAudio -and $audioState -ne 'current') {
    throw "Audio state is '$audioState'. Generate audio for the current dialogue, or run without arguments for a silent preview."
}
if ($GenerateAudio -and (Test-Path -LiteralPath $sourceRecord)) {
    Remove-Item -LiteralPath $sourceRecord
}
if ($UseAudio) {
    $start = 0.0
    for ($i = 0; $i -lt $turns.Count; $i++) {
        $turn = $turns[$i]
        $audioName = 'turn-{0:D3}.wav' -f ($i + 1)
        $audioPath = Join-Path $audioDirectory $audioName
        if ($GenerateAudio) {
            $speech = $turn.text -replace '\r?\n', ''
            if (-not $talkers[$turn.speaker].OutputWaveToFile($speech, $audioPath)) { throw "Voice export failed: $audioName" }
            Write-Output "Generated $audioName ($($turn.speaker))"
        }
        $clip = Read-PcmWave $audioPath
        $clips += $clip
        $turn.start = $start
        $turn.duration = $clip.Duration + $gap
        $turn.audioDuration = $clip.Duration
        $turn.audio = "audio/$audioName"
        $start += $turn.duration
    }
}
$json = ConvertTo-Json -InputObject $turns -Depth 4
$audioJson = 'null'
if ($UseAudio) {
    $total = $start + $hold
    if ($total -lt 300 -or $total -gt 420) {
        throw "Narrated video is $([math]::Round($total, 2)) seconds, outside the 5-7 minute target. Regenerate with an adjusted -Speed."
    }
    $pause = [byte[]]::new([int](96000 * $gap))
    $closing = [byte[]]::new([int](96000 * $hold))
    $size = ($clips | ForEach-Object { $_.Data.Length } | Measure-Object -Sum).Sum + $pause.Length * $clips.Count + $closing.Length
    $wavePath = Join-Path $audioDirectory 'security-narration.wav'
    $temporary = "$wavePath.tmp"
    $writer = [System.IO.BinaryWriter]::new([System.IO.File]::Create($temporary))
    try {
        $writer.Write([System.Text.Encoding]::ASCII.GetBytes('RIFF'))
        $writer.Write([uint32]($size + 36))
        $writer.Write([System.Text.Encoding]::ASCII.GetBytes('WAVEfmt '))
        $writer.Write([uint32]16)
        $writer.Write([uint16]1)
        $writer.Write([uint16]1)
        $writer.Write([uint32]48000)
        $writer.Write([uint32]96000)
        $writer.Write([uint16]2)
        $writer.Write([uint16]16)
        $writer.Write([System.Text.Encoding]::ASCII.GetBytes('data'))
        $writer.Write([uint32]$size)
        foreach ($clip in $clips) { $writer.Write([byte[]]$clip.Data); $writer.Write($pause) }
        $writer.Write($closing)
    } finally {
        $writer.Dispose()
    }
    Move-Item -LiteralPath $temporary -Destination $wavePath -Force
    $audioJson = ConvertTo-Json -InputObject ([ordered]@{ src = 'audio/security-narration.wav'; duration = $total; gap = $gap; hold = $hold }) -Compress
}
if ($GenerateAudio) {
    $recordJson = ConvertTo-Json -InputObject ([ordered]@{ version = 1; dialogueHash = $dialogueHash }) -Compress
    [System.IO.File]::WriteAllText("$sourceRecord.tmp", "$recordJson`n", [System.Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath "$sourceRecord.tmp" -Destination $sourceRecord -Force
    $audioState = 'current'
}
$output = Join-Path $PSScriptRoot 'security_preview_data.js'
[System.IO.File]::WriteAllText($output, "window.securityPreviewTurns = $json;`nwindow.securityPreviewAudio = $audioJson;`nwindow.securityPreviewAudioStatus = `"$audioState`";`n", [System.Text.UTF8Encoding]::new($false))
Write-Output "Generated $($turns.Count) turns; dialogue timeline: $([math]::Round($start)) seconds."
Write-Output "Dialogue/audio status: $audioState"
