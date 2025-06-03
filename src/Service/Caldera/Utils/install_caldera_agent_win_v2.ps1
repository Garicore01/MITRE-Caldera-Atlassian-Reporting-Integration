# --- CONFIGURACIÓN ---
$agentUrl = "http://<YOUR_CALDERA_IP>/file/download"
$agentFilename = "caldera-agent.exe"
$installPath = <PATH_TO_INSTALL_CALDERA_AGENT>
$nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
$nssmZip = "$env:TEMP\nssm.zip"
$nssmPath = <PATH_FOR_NSSM>
$serviceName = <NAME_FOR_THE_SERVICE>
# -- SET THE GROUP TO WHICH THE AGENT WILL BE ASSIGNED. (CLIENT NAME) --
$agentArgs = "-server http://<YOUR_CALDERA_IP>:<PORT> -group red"

# -- IT IS NECESSARY TO DOWNLOAD NSSM TO WRAP THE AGENT INTO A SERVICE --
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12


Write-Host "`n==== 🛠️ Iniciando instalación del agente Caldera ====" -ForegroundColor Cyan


# --- 1. CREATE AGENT FOLDER ---

try {
	New-Item -Path $installPath -ItemType Directory -Force -ErrorAction Stop | Out-Null
   	Write-Host "✅ Carpeta del agente creada en $installPath"
} catch {
    exit 1
}


# --- 2. DOWNLOAD THE AGENT---

try {
    Invoke-WebRequest -Uri "$agentUrl" `
      -Headers @{platform="windows"; file="sandcat.go"} `
      -OutFile "$installPath\$agentFilename"	
	Write-Host "✅ Agente descargado como $agentFilename"

} catch {
	Write-Error "❌ Error al descargar el agente: $_"
    exit 1

}


# --- 3. CREATE THE FIREWALL RULE ---

try {
	New-NetFirewallRule -DisplayName "CalderaAgent Allow Outbound" `
	       	-Direction Outbound `
		-Program "$installPath\$agentFilename" `
		-Action Allow -Profile Any -ErrorAction SilentlyContinue
	Write-Host "✅ Regla de firewall creada"

} catch {
	Write-Warning "⚠️ No se pudo crear la regla de firewall (puede requerir privilegios elevados)"
}


# --- 4. DOWNLOAD NSSM ---
# NSSM (Non-Sucking Service Manager) is a service helper that allows us 
# to run any executable as a Windows service. In this case, we will use it to run the 
# Caldera agent as a service because we need to run it in the background and configure it 
# to start automatically when the system starts or when the service fails.
try {
	Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip -UseBasicParsing
	Expand-Archive -Path $nssmZip -DestinationPath $nssmPath -Force
	Write-Host "✅ NSSM descargado y extraído"
} catch {
	Write-Error "❌ Error al descargar o extraer NSSM: $_"
	exit 1
}


# --- 5. FIND NSSM.EXE ---

try {
	$nssmExe = Get-ChildItem -Path "$nssmPath\nssm-*" -Recurse -Filter nssm.exe |
	Where-Object { $_.FullName -like "*win64*" } |           
	Select-Object -First 1 -ExpandProperty FullName
	if (-not (Test-Path $nssmExe)) {
	 throw "No se encontró nssm.exe en $nssmPath"
	}
	Write-Host "✅ NSSM localizado en: $nssmExe"
} catch {
    Write-Error "❌ Error al localizar nssm.exe: $_"
    exit 1
}


# --- 6. CREATE THE SERVICE WITH NSSM ---

try {
    & $nssmExe install $serviceName "$installPath\$agentFilename" $agentArgs
    Write-Host "✅ Servicio '$serviceName' creado con NSSM"
} catch {
    Write-Error "❌ Error al crear el servicio con NSSM: $_"
    exit 1
}


# --- 7. AUTO LAUNCH CONFIGURATION ---
try {
    sc.exe config $serviceName start= auto | Out-Null
    Write-Host "✅ Servicio configurado para inicio automático"
} catch {
    Write-Warning "⚠️ No se pudo configurar el inicio automático: $_"
}


# --- 8. RECUPERATION CONFIGURATION (RELOAD IF FAIL) ---
try {
    sc.exe failure $serviceName reset= 0 actions= restart/5000 | Out-Null
    Write-Host "✅ Servicio configurado para reinicio en fallo"
} catch {
    Write-Warning "⚠️ No se pudo configurar la recuperación del servicio: $_"
}


# --- 9. START SERVICE ---
try {
    Start-Service -Name $serviceName -ErrorAction Stop
    Write-Host "`n🚀 Servicio $serviceName iniciado correctamente." -ForegroundColor Green
} catch {
    Write-Error "❌ Error al iniciar el servicio: $_"
    Write-Warning "Es posible que el ejecutable haya sido bloqueado por Windows Defender."
}
