### 1. Definición de objetivos
- **Objetivo:** Determinar la capacidad de detección y respuesta ante técnicas
 de ataque de forma automatizada. 

### 2. Criterios de instalación del agente
- **Clasificación de activos:**
    - **Activos críticos VS Activos no críticos:** La primera tarea es seleccionar aquellos 
    activos los cuales son criticos desde el punto de vista del Blue Team.
- **Estrategia de despliegue:**
    - **Equipo fuera de la infraestructura:** Este es el primer tipo de agente que se instala. 
    Su función es simular el comportamiento de un atacante desde el principio (cuando todavia 
    no esta dentro de la infraestructura)

    - **Equipo dentro de la infraestructura con limitación de privilegios:** Lo ideal, es que 
    los sistemas de seguridad bloquen y paren al primer tipo de agente que se instala. Sin 
    embargo, es necesario definir un segundo tipo de agente que intenta simular el 
    comportamiento de un atacante una vez ya esta dentro de la infraestructura. 

    - **Equipo dentro de la infraestructura con privilegios elevados:** Al igual que en el 
    caso anterior, lo ideal es que los sistemas hayan bloqueado al anterior tipo de agente. Sin
    embargo, es necesario definir un último tipo de agente que simule el comportamiento de un 
    atacante una vez que tiene un usuario con privilegios de forma que se pueda testear si los
    sistemas de seguridad estan preparados para actuar incluso cuando las ordenes estan 
    ejecutadas por un usuario administrador.
- **Forma de persistir la conexión del agente:**
    - **Windows:** Como es de esperar, Windows Defender bloquea la ejecución del script que se
    encarga de descargar el agente y ejecutarlo. Para solucionar este problema se ha optado
    por usar el hash. El hash de este script es único para el, por lo que nos aseguramos de que
    un atacante no pueda intentar utilizar un agente similar para intentar entrar. 
    La idea es crear una politica en Windows Defender o en una GPO en la que se especifica que
    si el hash del script que se esta ejecutando es X, entonces Windows Defender debe pasarlo.
    Permitir la ejecución del script:
    *Get-FileHash <file> -Algorithm SHA256* 
    *Add-MpPreference -AttackSurfaceReductionOnlyExclusions <"HASH_DEL_ARCHIVO">*
    Permitir la ejecución el ejecutable .exe:

    Creación de servicio para autoarranque del agente:
    *sc.exe create SandcatService binPath= "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -ExecutionPolicy Bypass -File C:\Users\Public\caldera-agent.ps1" start= auto*
    *Get-Service SandcatService*
    *Start-Service SandcatService*



### 3. Selección y ordén de las abilities
Consultar la tabla

### 4. Flujo de trabajo por parte del SOC


Apoyarme en recursos graficos
Matriz de mitre, diagramas, etc...
Explicar el flujo para alguien que no conoce Caldera.
Diagrama de red
Daigrama de donde se instalan los agentes
