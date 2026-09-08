param([string]$PipeName = '')
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

function Read-Controller([string]$Path) {
    $pipe = [System.IO.Pipes.NamedPipeClientStream]::new('.', $script:SelectedPipe,
        [System.IO.Pipes.PipeDirection]::InOut, [System.IO.Pipes.PipeOptions]::Asynchronous)
    $output = [System.IO.MemoryStream]::new()
    try {
        $pipe.Connect(3000)
        $request = [System.Text.Encoding]::ASCII.GetBytes(
            "GET $Path HTTP/1.0`r`nHost: localhost`r`nConnection: close`r`n`r`n")
        $write = $pipe.WriteAsync($request, 0, $request.Length)
        if (!$write.Wait(3000)) { throw 'Controller write timed out' }
        $clock = [System.Diagnostics.Stopwatch]::StartNew()
        $buffer = New-Object byte[] 65536
        while ($true) {
            $remaining = 10000 - [int]$clock.ElapsedMilliseconds
            if ($remaining -le 0) { throw 'Controller read timed out' }
            $read = $pipe.ReadAsync($buffer, 0, $buffer.Length)
            if (!$read.Wait($remaining)) { throw 'Controller read timed out' }
            if ($read.Result -eq 0) { break }
            if ($output.Length + $read.Result -gt 16777216) { throw 'Controller response too large' }
            $output.Write($buffer, 0, $read.Result)
        }
        $parts = [System.Text.Encoding]::UTF8.GetString($output.ToArray()) -split "`r`n`r`n", 2
        if ($parts.Length -ne 2 -or $parts[0] -notmatch '^HTTP/1\.[01] 200 ') {
            throw 'Controller GET failed; raw response withheld'
        }
        if ($parts[0] -match '(?im)^Transfer-Encoding:') {
            throw 'Unsupported response encoding; raw response withheld'
        }
        return ($parts[1] | ConvertFrom-Json)
    } finally {
        $pipe.Dispose()
        $output.Dispose()
    }
}

try {
    $pipes = @([System.IO.Directory]::GetFiles('\\.\pipe\') |
        Where-Object { $_ -like '*MihomoParty*mihomo-*' } |
        ForEach-Object { $_.Substring(9) })
    if ($PipeName) {
        if ($PipeName -notin $pipes) { throw 'Requested controller pipe not found' }
        $script:SelectedPipe = $PipeName
    } elseif ($pipes.Count -eq 1) {
        $script:SelectedPipe = $pipes[0]
    } else { throw 'Expected exactly one controller pipe; specify -PipeName after local inspection' }

    $config = Read-Controller '/configs'
    $connections = Read-Controller '/connections'
    $safeConfig = [ordered]@{}
    foreach ($key in @('tun', 'interface-name', 'port', 'socks-port', 'mixed-port',
        'redir-port', 'tproxy-port', 'ipv6', 'bind-address', 'allow-lan', 'mode')) {
        if ($config.PSObject.Properties.Name -contains $key) { $safeConfig[$key] = $config.$key }
    }
    $warnings = @()
    $physical = $null
    $name = $config.'interface-name'
    if ($name) {
        $adapters = @(Get-NetAdapter -Name $name | Where-Object { $_.Name -eq $name })
        if ($adapters.Count -eq 1 -and $adapters[0].HardwareInterface -eq $true) {
            $adapter = $adapters[0]
            $ip = Get-NetIPInterface -InterfaceIndex $adapter.ifIndex -AddressFamily IPv4 -PolicyStore ActiveStore
            $physical = [ordered]@{
                name = $adapter.Name; index = $adapter.ifIndex
                status = [string]$adapter.Status; forwarding = [string]$ip.Forwarding
            }
        } else { $warnings += 'Bound interface is not a uniquely identified physical adapter' }
    } else { $warnings += 'No explicit interface-name; determine actual egress before repair' }
    $now = [DateTimeOffset]::UtcNow
    $own = @($connections.connections | Where-Object { $_.metadata.process -ieq 'mihomo.exe' })
    $recentOwn = @($own | Where-Object { [DateTimeOffset]::Parse($_.start) -gt $now.AddMinutes(-2) })
    $cores = @(Get-Process -Name mihomo -ErrorAction SilentlyContinue | ForEach-Object {
        [ordered]@{ pid = $_.Id; startedAt = $_.StartTime.ToUniversalTime().ToString('o'); cpuSeconds = $_.CPU }
    })
    [ordered]@{
        schemaVersion = 1; observedAt = $now.ToString('o'); config = $safeConfig
        physicalInterface = $physical; cores = $cores
        connectionSummary = [ordered]@{
            total = @($connections.connections).Count; coreSelfConnections = $own.Count
            coreSelfConnectionsLastTwoMinutes = $recentOwn.Count
        }
        warnings = $warnings
    } | ConvertTo-Json -Depth 30
} catch {
    # Exception objects can contain raw controller/configuration content.
    [Console]::Error.WriteLine('Inspection failed. No changes made; inspect dependencies and controller access locally.')
    exit 1
}
