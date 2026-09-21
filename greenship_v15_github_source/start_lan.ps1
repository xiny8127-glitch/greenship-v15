$ErrorActionPreference = "Stop"

$python = "C:\Users\m1341\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

Set-Location $projectRoot
$env:PYTHONPATH = Join-Path $projectRoot "vendor"

$ip = Get-NetIPAddress -AddressFamily IPv4 |
    Where-Object {
        $_.IPAddress -notlike "127.*" -and
        $_.IPAddress -notlike "169.254.*" -and
        $_.PrefixOrigin -ne "WellKnown"
    } |
    Select-Object -First 1 -ExpandProperty IPAddress

Write-Host ""
Write-Host "GreenShip V1.5 已启动"
Write-Host "本机打开: http://127.0.0.1:5055"
if ($ip) {
    Write-Host "其他电脑打开: http://$ip`:5055"
} else {
    Write-Host "未能自动识别局域网 IP，请在 Windows 网络设置中查看本机 IPv4 地址。"
}
Write-Host ""

& $python app.py
