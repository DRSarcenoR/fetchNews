# Luego de crear este Dockerfile, desde el directorio donde se encuentra
# ejecutar el siguiente comando:

# docker build -t <nombre de la imagen> .
# donde -t es equivalente a --tag

# Luego se crea el contenedor usando el siguiente comando comando dependiendo del sistema operativo
# Linux/macOS: docker run --rm -v $(pwd):/data compilador-latex
# Windows(PowerShell): docker run --rm -v ${PWD}:/data compilador-l+atex
# Windows(CMD): docker run --rm -v %cd%:/data compilador-latex


# Otra forma es la siguiente: docker run --rm -v "%cd%:/data" <nombre de la imagen (presentacion)> pdflatex main.tex




# Se puede abrir docker desde la terminal
# Windows (PowerShell): start-process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
# Sin abrir la interfaz gráfica: docker ps 
# este ultimo mostrara los contenedores en ejecucion


# Para cerrar un contenedor
# docker stop <nombre/ID del contenedor>
# docker stop $(docker ps -q)

# DISCLAIMER: Un Dockerfile es opcional cuando se utilizan imágenes preconstruidas de 
#             Docker Hub. Sin embargo, es necesario para personalizarlas o ampliarlas.
#             https://www.hostinger.es/tutoriales/como-crear-contenedor-docker#Como_crear_un_contenedor_Docker



# Utiliza una imagen base de LaTeX
FROM blang/latex:ctanfull

# Actualiza el repositorio e instala paquetes adicionales si es necesario
RUN apt-get update && \
    apt-get install -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /data

CMD ["pdflatex", "main.tex"]
