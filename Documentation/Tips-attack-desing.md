### 1. Definir el Alcance y Objetivos de la Auditoría

- **Objetivo de la simulación:** Determinar la capacidad de detección y respuesta ante técnicas
 de ataque (por ejemplo, evaluación de controles de seguridad, tiempo de respuesta ante 
 incidentes).
- **Alcance:** Identificar qué segmentos o equipos se auditarán (por ejemplo, endpoints, 
servidores críticos, dispositivos de red) y cuáles quedan excluidos.

---

### 2. Criterios para la Instalación del Agente

- **Clasificación de activos:**  
  - **Críticos vs. No críticos:** Seleccionar aquellos sistemas cuya seguridad es esencial 
  (servidores de correo, controladores de dominio, endpoints de alto riesgo) para evaluar 
  los controles de seguridad.
  - **Tipo de sistema operativo y arquitectura:** Por ejemplo, en entornos mixtos (Windows, 
  Linux, etc.) definir qué versiones son compatibles con el agente y cuáles requieren un 
  enfoque distinto.
  - **Nivel de exposición:** Considerar si el equipo está expuesto a internet o es parte de 
  segmentos internos de alto riesgo.
  - **Permisos y restricciones:** Verificar que se cuenta con los permisos necesarios para 
  instalar agentes en sistemas que puedan tener restricciones operativas o de seguridad.
- **Estrategia de despliegue:**  
  - **Piloto inicial:** Comenzar con un grupo representativo de sistemas (por ejemplo, 
  algunos endpoints y un servidor) para calibrar la ejecución y el comportamiento de las 
  abilities.
  - **Expansión gradual:** Basado en los resultados del piloto, ampliar la instalación a 
  otros segmentos según el nivel de criticidad y exposición.

---

### 3. Selección y Orden de las Abilities

- **Selección de abilities basadas en MITRE ATT&CK:**  
  - **Reconocimiento y Discovery:** Empezar con abilities que permitan identificar información 
  del sistema y la red (por ejemplo, “system network discovery” o “host discovery”).  
  - **Ejecución inicial:** Seleccionar técnicas de ejecución (por ejemplo, comandos a través de
   PowerShell, ejecución de scripts) que simulen la obtención de acceso inicial.  
  - **Escalación de privilegios:** Si la auditoría lo requiere, incluir abilities para simular 
  intentos de elevar privilegios.
  - **Movimiento lateral y persistencia:** Elegir abilities que simulen la propagación en la 
  red y la instalación de mecanismos de persistencia, si es relevante para el escenario del 
  cliente.
  - **Exfiltración (opcional):** En entornos controlados, se puede incluir la simulación de 
  extracción de datos para evaluar la capacidad de respuesta ante movimientos de datos no 
  autorizados.

- **Orden de ejecución sugerido (modelo en fases):**  
  1. **Fase de Reconocimiento:** Ejecución de abilities de descubrimiento del entorno 
  (pueden realizarse en paralelo en varios sistemas). 
  2. **Fase de Acceso Inicial:** Simular la ejecución de comandos o scripts que representen la 
  primera intrusión.  
  3. **Fase de Movimiento Lateral:** Dependiendo del éxito de la fase anterior, probar técnicas
   de lateral movement y escalación de privilegios.  
  4. **Fase de Simulación de Impacto:** (Si procede) Emular actividades que podrían conducir a 
  la exfiltración o a la persistencia en el sistema.
- **Flexibilidad y modularidad:**  
  - La secuencia puede adaptarse en función de los resultados obtenidos en cada fase.  
  - Se pueden definir “playbooks” o flujos de trabajo modulares que se activen según el perfil
   del cliente (por ejemplo, entornos muy protegidos vs. entornos más abiertos).

---

### 4. Documentación del Criterio y Adaptación a Clientes Diversos

- **Matriz de selección:**  
  - Crea una tabla que relacione los tipos de sistemas (según SO, rol y criticidad) con las 
  abilities recomendadas y el orden de ejecución.  
  - Incluye consideraciones sobre restricciones operativas (por ejemplo, equipos que no se 
  pueden interrumpir, sistemas con políticas de alta seguridad).

- **Parámetros de evaluación:**  
  - Define indicadores de éxito para cada fase (por ejemplo, tiempo de respuesta del sistema, 
  detección por parte de soluciones de seguridad, logs generados).
  - Establece criterios de decisión para continuar, detener o modificar el flujo de ataque 
  según la respuesta del entorno.

- **Adaptabilidad del servicio:**  
  - Documenta que el “playbook” de auditoría es adaptable y se puede personalizar según el 
  perfil del cliente.
  - Incluye directrices para actualizar las técnicas (abilities) conforme evolucionen las 
  tácticas de adversarios reales y las capacidades de defensa del cliente.

---

### 5. Recomendaciones Finales

- **Pruebas en entornos controlados:** Antes de la auditoría en producción, valida el flujo de 
ataque en un entorno de laboratorio similar a la infraestructura del cliente.
- **Coordinación y comunicación:** Asegura que el cliente esté informado y de acuerdo con el 
plan de auditoría para evitar malentendidos o interrupciones en operaciones críticas.
- **Seguridad y ética:** Garantiza que todas las acciones se realicen en un marco ético y 
legal, documentando las autorizaciones pertinentes.