# Dockerización del Cliente MITRE Caldera

Este documento explica cómo dockerizar el cliente de MITRE Caldera para facilitar su despliegue y ejecución.

## Requisitos previos

- Docker instalado en tu máquina
- Acceso al código fuente del cliente MITRE Caldera

## Archivos incluidos

- `Dockerfile`: Configuración para crear la imagen Docker
- `requirements.txt`: Dependencias de Python necesarias para el proyecto
- `.env`: Archivo para variables de entorno (debes crearlo tú mismo)

## Instrucciones de uso

### 1. Preparar el archivo .env

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```
caldera_server=http://your-caldera-server:8888
api_key=your-caldera-api-key
atlassian_url=https://your-confluence.atlassian.net/wiki/api/v2/pages
atlassian_token=your-atlassian-token
atlassian_email=your-email@example.com
confluence_space_id=your-space-id
confluence_father_id=your-parent-page-id
gitlab_token=your-gitlab-token
gitlab_url=https://your-gitlab-url/api/v4/projects/your-project-id/repository/archive.zip
```

### 2. Construir la imagen Docker

```bash
docker build -t mitre-caldera-client .
```

### 3. Ejecutar el contenedor

```bash
docker run --env-file .env mitre-caldera-client
```

Para ejecutar un script específico:

```bash
docker run --env-file .env mitre-caldera-client python Scripts/test.py
```

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| caldera_server | URL del servidor Caldera |
| api_key | Clave API para autenticarse con Caldera |
| atlassian_url | URL de la API de Confluence |
| atlassian_token | Token de autenticación para Confluence |
| atlassian_email | Email asociado con la cuenta de Confluence |
| atlassian_space_id | ID del espacio en Confluence |
| atlassian_father_id | ID de la página padre en Confluence |
| gitlab_token | Token de autenticación para GitLab |
| gitlab_url | URL para descargar el archivo ZIP del repositorio |

## Consejos para el desarrollo

- Para montar tu código local en el contenedor durante el desarrollo:

```bash
docker run -v $(pwd)/Scripts:/app/Scripts --env-file .env mitre-caldera-client
```

- Para entrar al contenedor con una shell:

```bash
docker run -it --env-file .env mitre-caldera-client /bin/bash
```

## Solución de problemas

- Si encuentras errores de permisos, asegúrate de que los directorios `Scripts/Service/builds` y `Scripts/repository` existan en tu código local.
- Verifica que las variables de entorno sean correctas para tu entorno.
- Para depurar, puedes añadir `print` statements y ejecutar el contenedor con el flag `-it`. 