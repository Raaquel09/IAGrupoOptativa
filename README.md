# IAoptativa

# Descripción

Este repositorio está enlazado con Zenodo:
https://zenodo.org/

Zenodo - DOI: https://zenodo.org/doi/10.5281/zenodo.10783171
 

El proyecto se basa en el manejo de programas escritos en el lenguaje de programación Python y en como se pueden ejecutar en local, con Grobid y Docker.
Tenemos tres tareas a realizar y de cada una de ellas hay dos versiones del script:

1 La que ejecutaremos en nuestro entorno local para comprobar que funciona correctamente(procesa pdfs).

2 Hace lo mismo pero lleva incluido el código correspondiente para que funcione con el cliente de Python para Grobid.
O procesa los xmls que nos da la aplicación de Grobid.

## WordCloud
Crea una nube de palabras basada en la información que obtiene de un pdf/xml.
El resultado es una imagen.png

## NumberOfFigures
Dibuja un gráfico en el que se ve cuantas figuras tiene cada pdf/xml.
El resultado es una imagen.png

## ListOfLinks
Crea una lista de los links que encuentra en un pdf/xml.
El resultado es una lista en un fichero.json


# Requisitos

Para que este proyecto funcione hay que instalarse una serie de cosas que explicaremos más adelante como hacerlo.
Necesitamos:

1 Un entorno de python para ejecutar los scripts y comprobar que funciona (también se puede en un entorno virtual como podría ser conda).

2 Las librerías correspondientes a lo que nos pidan los scripts.

3 Instalar Docker.

4 Instalar Grobid (es más fácil hacerlo una vez ya nos hemos instalado Docker).

5 Preparar el cliente de Python para Grobid.

6 Tener los scripts necesarios para que el cliente funcione correctamente.


Lista de requisitos del sistema o dependencias necesarias para ejecutar el proyecto.


# Instrucciones de Instalación
Pasos detallados sobre cómo instalar el proyecto y configurar las dependencias necesarias.

1 Preparar un entorno para comprobar que los scripts funcionan.
Si queremos hacerlo en Python, habría que entrar en el siguiente enlace e instalarse la versión correspondiente al dispositivo de cada uno.
https://www.python.org/downloads/

Y si queremos que sea en un entorno virtual como conda:

El enlace de instalación
https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
A continuación los comandos para crear el entorno virtual:
conda create -n nombreEntorno python=3(el 3 sería un ejemplo, habría que poner la versión de Python que hayamos instalado antes, esta se puede comprobar con python --version)
conda env list
conda activate nombreEntorno
Y conda deactivate nombreEntorno si queremos cerrarlo una vez hayamos terminado.

2 Las librerías correspondientes a lo que nos pidan los scripts.
En este caso con las siguientes librerías sería suficiente:
pip install PyPDF2
pip install wordcloud
pip install matplotlib
pip install beautifulsoup4



3 Instalar Docker.
Entra en el siguiente enlace e instala la versión correspondiente a tu dispositivo.
https://docs.docker.com/engine/install/

4 Instalar Grobid (es más fácil hacerlo una vez ya nos hemos instalado Docker).
Descarga la imagen de Grobid.
docker pull lfoppiano/grobid:0.7.2 (esto es la versión que quieras tener, si pones lastest se instalará la última)
Lanza el servidor de Grobid con Docker.
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.2 (esto es la versión que quieras tener, si pones lastest se instalará la última)

El primer puerto que vemos arriba es al que nosotros vamos a acceder y el segundo es el que se usa por defecto. 
En este caso el proyecto está preparado para que se acceda al puerto 8070.

Para comprobar que todo ha ido bien accedemos desde internet al puerto correspondiente.
http://localhost:8070/

5 Preparar el cliente de Python para Grobid.
El cliente es recomendable descargarlo en la misma carpeta donde tengas el proyecto para evitar errores.
Antes de poder clonar el reporitorio es  necesario instalarse Git ( https://git-scm.com/download/win ), puedes verificar que se ha hecho correctamente con el comando git --version.

Los comandos a ejecutar son los siguientes:
git clone https://github.com/kermitt2/grobid_client_python
cd grobid_client_python
python3 setup.py install
(Si el comando anterior da fallo porque no estuviesen instaladas todas las herramientas ejecuta "pip install setuptools" y vuelve a ejecutar el otro comando)

Estos comandos también están en el fichero codigoDescargaCliente.txt que se encuentra en este mismo repositorio.

Utilizamos el cliente de Python para Grobid para que nos sea más fácil y el fichero nos genere automáticamente el fichero.xml que tiene que procesar el script de Python.
Tendríamos otra opción si no podemos instalarlo, sería obtener el fichero.xml que luego tiene que procesar el script desde la página de Grobid a la que accedes desde el puerto elegido.
http://localhost:8070/
Una vez dentro seleccionamos TEI, ponemos la opción Process Fulltext Document, elegimos el pdf que queremos usar y le damos a submit.
Cuando termine nos habrá generado un fichero.xml, lo descargamos y ese será el fichero que tendrá que procesar nuestro script.

En este caso vamos a hacer lo segundo, es decir, darle como parametro al script el xml generado por Grobid.

6 Tener los scripts necesarios para que el cliente funcione correctamente.
Para que el script se pueda conectar con el cliente es necesario introducir las siguientes líneas de código en nuestro script de Python:

from grobid_client.grobid_client import GrobidClient

client = GrobidClient(config_path="./config.json")
client.process("processFulltextDocument", "C:\\Users\\Admin\\Desktop\\PracticaIndividual", n=20)


(La ruta que se ve en la última línea hay que cambiarla por la ruta del directorio en el que esté el proyecto.)
Estos comandos también están en el fichero codigoCliente.txt que se encuentra en este mismo repositorio.

Y también necesitaremos el fichero config.json (está incluido en el repositorio) en el que especifica las características, entre ellas el puerto al que queremos acceder(8070) cuando no sea el que por defecto(8070).


# Instrucciones de Ejecución

## Ejecución en local
1 Abrimos una terminal donde se encuentra el proyecto.

2 Situarnos en la carpeta en la que tengamos el proyecto.

3 python nombreFichero.py salida.png ejemplo1.pdf ejemplo2.pdf
En el caso de los links la salida es un fichero.json

### Ejemplos
Para los ejemplos el repositorio incluye 10 pdfs.

#### WordCloud
Recordatorio de lo que hacia el script:
Crea una nube de palabras basada en la información que obtiene de un pdf.
El resultado es una figura.

1 Con un solo pdf: 1.pdf
python keywordCloudTotal.py salidaKeyPdf1.png 1.pdf
Resultado:salidaKeyPdf1.png

2 Con tres pdfs: 2.pdf 3.pdf 4.pdf
python keywordCloudTotal.py salidaKeyPdf234.png 2.pdf 3.pdf 4.pdf
Resultado:salidaKeyPdf234.png

3 Con seis pdfs: 5.pdf 6.pdf 7.pdf 8.pdf 9.pdf 10.pdf
python keywordCloudTotal.py salidaKeyPdf5678910.png 5.pdf 6.pdf 7.pdf 8.pdf 9.pdf 10.pdf
Resultado:salidaKeyPdf5678910.png

Las imagenes de salida están en la carpeta soluciones pdfs.


#### NumberOfFigures
Recordatorio de lo que hacia el script:
Dibuja un gráfico en el que se ve cuantas figuras tiene cada pdf.
El resultado es una figura.

1 Con un solo pdf: 1.pdf
python numberOfFiguresTotal.py 1.pdf
Resultado:salidaFiguresPdf1.png

2 Con tres pdfs: 2.pdf 3.pdf 4.pdf
python numberOfFiguresTotal.py 2.pdf 3.pdf 4.pdf
Resultado:salidaFiguresPdf234.png

3 Con seis pdfs: 5.pdf 6.pdf 7.pdf 8.pdf 9.pdf 10.pdf
python numberOfFiguresTotal.py 5.pdf 6.pdf 7.pdf 8.pdf 9.pdf 10.pdf
Resultado:salidaFiguresPdf5678910.png

Las imagenes de salida están en la carpeta soluciones pdfs.

#### ListOfLinks
Recordatorio de lo que hacia el script:
Crea una lista de los links que encuentra en un pdf.
El resultado es una lista que devuelve por consola en formato json.

1 Con un solo pdf: 1.pdf
python listOfLinksPdf.py 1.pdf
Resultado:salidaLinksPdf1.json

2 Con tres pdfs: 2.pdf 3.pdf 4.pdf
python listOfLinksPdf.py 2.pdf 3.pdf 4.pdf
Resultado:salidaLinksPdf234.json

3 Con seis pdfs: 5.pdf 6.pdf 7.pdf 8.pdf 9.pdf 10.pdf
python listOfLinksPdf.py 5.pdf 6.pdf 7.pdf 8.pdf 9.pdf 10.pdf
Resultado:salidaLinksPdf5678910.json

Los ficheros.json de salida están en la carpeta soluciones pdfs.

## Ejecución con Grobid
En este caso vamos a hacerlo con el cliente de Python para Grobid.

1 Abrimos una terminal donde se encuentra el proyecto.

2 Si no tenemos todavía la imagen de Grobid descargada la descargamos.
docker pull lfoppiano/grobid:0.7.2 (esto es la versión que quieras tener, si pones lastest se instalará la última)

3 Lanza el servidor de Grobid con Docker.
docker run -t --rm -p 8070:8070 lfoppiano/grobid:0.7.2 (esto es la versión que quieras tener, si pones lastest se instalará la última)

4 Accede a Grobid para comprobar que se ha conectado correctamente.
http://localhost:8070/

Como vamos a hacerlo con los xml generados por Grobid:
Le damos a la opción TEI
Ponemos la opción Process Fulltext Document
Elegimos el pdf que queremos usar 
Le damos a submit
Y descargamos el xml

5 Abrimos otra terminal donde se encuentra el proyecto.

6 python nombreFichero.py imagenSalida.png ejemplo1.xml ejemplo2.xml
En el caso de los links la salida es un fichero.json


### Ejemplos
Para los ejemplos el repositorio incluye 10 xmls.

#### WordCloud
Recordatorio de lo que hacia el script:
Crea una nube de palabras basada en la información que obtiene de un pdf.
El resultado es una figura.

1 Con un solo xml: 1.pdf.tei.xml
python keywordCloudTotal.py salidaKeyXml1.png 1.pdf.tei.xml
Resultado:salidaKeyXml1.png

2 Con tres xmls: 2.pdf.tei.xml 3.pdf.tei.xml 4.pdf.tei.xml
python keywordCloudTotal.py salidaKeyXml234.png 2.pdf.tei.xml 3.pdf.tei.xml 4.pdf.tei.xml
Resultado:salidaKeyXml234.png

3 Con seis xmls: 5.pdf.tei.xml 6.pdf.tei.xml 7.pdf.tei.xml 8.pdf.tei.xml 9.pdf.tei.xml 10.pdf.tei.xml
python keywordCloudTotal.py salidaKeyXml5678910.png 5.pdf.tei.xml 6.pdf.tei.xml 7.pdf.tei.xml 8.pdf.tei.xml 9.pdf.tei.xml 10.pdf.tei.xml
Resultado:salidaKeyXml5678910.png

Las imagenes de salida están en la carpeta soluciones xmls.


#### NumberOfFigures
Recordatorio de lo que hacia el script:
Dibuja un gráfico en el que se ve cuantas figuras tiene cada pdf.
El resultado es una figura.

1 Con un solo xml: 1.pdf.tei.xml
python numberOfFiguresTotal.py salidaFiguresXml1.png 1.pdf.tei.xml
Resultado:salidaFiguresXml1.png

2 Con tres xmls: 2.pdf.tei.xml 3.pdf.tei.xml 4.pdf.tei.xml
python numberOfFiguresTotal.py salidaFiguresXml234.png 2.pdf.tei.xml 3.pdf.tei.xml 4.pdf.tei.xml
Resultado:salidaFiguresXml234.png

3 Con seis xmls: 5.pdf.tei.xml 6.pdf.tei.xml 7.pdf.tei.xml 8.pdf.tei.xml 9.pdf.tei.xml 10.pdf.tei.xml
python numberOfFiguresTotal.py salidaFiguresXml5678910.png 5.pdf.tei.xml 6.pdf.tei.xml 7.pdf.tei.xml 8.pdf.tei.xml 9.pdf.tei.xml 10.pdf.tei.xml
Resultado:salidaFiguresXml5678910.png

Las imagenes de salida están en la carpeta soluciones xmls.

#### ListOfLinks
Recordatorio de lo que hacia el script:
Crea una lista de los links que encuentra en un pdf.
El resultado es una lista que devuelve por consola en formato json.

1 Con un solo pdf: 1.pdf.tei.xml
python listOfLinksPdf.py salidaLinksXml1.json 1.pdf.tei.xml
Resultado:salidaLinksXml1.json

2 Con tres pdfs: 2.pdf.tei.xml 3.pdf.tei.xml 4.pdf.tei.xml
python listOfLinksPdf.py salidaLinksXml234.json 2.pdf.tei.xml 3.pdf.tei.xml 4.pdf.tei.xml
Resultado:salidaLinksXml234.json

3 Con seis pdfs: 5.pdf.tei.xml 6.pdf.tei.xml 7.pdf.tei.xml 8.pdf.tei.xml 9.pdf.tei.xml 10.pdf.tei.xml
python listOfLinksPdf.py salidaLinksXml5678910.json 5.pdf.tei.xml 6.pdf.tei.xml 7.pdf.tei.xml 8.pdf.tei.xml 9.pdf.tei.xml 10.pdf.tei.xml
Resultado:salidaLinksXml5678910.json

Los ficheros.json de salida están en la carpeta soluciones xmls.

# Dónde Obtener Ayuda
Información sobre dónde encontrar ayuda en caso de problemas o preguntas sobre el proyecto. Puede incluir enlaces a documentación adicional, foros de discusión, o formas de contacto directo con el equipo de desarrollo.

## Repositorio de Grobid
https://github.com/kermitt2/grobid

## Repositorio del cliente de Python para Grobid
https://github.com/kermitt2/grobid_client_python

## Documentación de Grobid
https://grobid.readthedocs.io/en/latest/
