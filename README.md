# IAoptativa

# Descripción

Este repositorio está enlazado con Zenodo:
https://zenodo.org/

Zenodo - DOI: https://zenodo.org/doi/10.5281/zenodo.11231689

Este proyecto tiene como objetivo comparar la similitud de contenido entre artículos académicos utilizando modelado de temas y técnicas de agrupación. 
Al emplear estos métodos, el proyecto identifica temas y patrones comunes entre los artículos, permitiendo una comprensión más profunda de sus relaciones de contenido. 
Además, utiliza consultas SparkQL para validar la precisión de la recuperación de información y asegurar la efectividad del análisis.:




# Requisitos

Para que este proyecto funcione hay que instalarse una serie de cosas que explicaremos más adelante como hacerlo.
Necesitamos:

1 Un entorno de python para ejecutar los scripts y comprobar que funciona (también se puede en un entorno virtual como podría ser conda).

2 Las librerías correspondientes a lo que nos pidan los scripts.

3 Instalar Docker.

4 Instalar Grobid (es más fácil hacerlo una vez ya nos hemos instalado Docker).

5 Preparar el cliente de Python para Grobid.

6 Tener los scripts necesarios para que el cliente funcione correctamente.

7 Una vez esta todo preparado se puede ejecutar el proyecto.


# Instrucciones de Instalación

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
pip install numpy
pip install pandas
pip install scikit-learn
pip install sentence-transformers
pip install bertopic
pip install lxml
pip install matplotlib
pip install nltk
pip install gensim
pip install transformers
pip install rdflib
pip install pydot
pip install requests

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
client.process("processFulltextDocument", "C:\\Users\\Admin\\Desktop\\PracticaGrupal", n=20)


(La ruta que se ve en la última línea hay que cambiarla por la ruta del directorio en el que esté el proyecto.)
Estos comandos también están en el fichero codigoCliente.txt que se encuentra en este mismo repositorio.

Y también necesitaremos el fichero config.json (está incluido en el repositorio) en el que especifica las características, entre ellas el puerto al que queremos acceder(8070) cuando no sea el que por defecto(8070).

7 Una vez esta todo preparado se puede ejecutar el proyecto.

- pdftoteixml.py
Este fichero dado unos pdfs saca el xml correspondiente a cada uno de ellos.

- ClusterBERT.py / ClusterBERTCoherence.py / ClusteringLDACoherence.py / ClusteringLDASilhoutte.py
Estos ficheros funcionan para
Al ejecutarlo 
Y se eligen finalmente estos metodos por los siguientes motivos:

- NERextractOptimizado.py
Este fichero funcionan para
Al ejecutarlo 

- rdfs.py
Este fichero crea el grafo RDF teniendo en cuenta las entidades de nuestro proyecto.
Al ejecutarlo crea una carpeta "GrafosRDF" en la que tenemos una imagen .png para poder ver el grafo y un fichero .rdf para usarlo en las consultas de SPARKQL

- datosXML.py
Crea un fichero .rdf por cada pdf que usamos en formato RDF/XML para poder así tener la información suficiente para hacer las consultas en SPARKQL.
Para poder ejecutarlo tenemos que tener la carpeta "ValidationCorpus" que se encuentra en el repositorio de donde coge los ficheros .xml para sacar los .rdf correspondientes.
Y el fichero "Abstract_And_topics.json" para añadir también a los ficheros .rdf los datos de la similitud de cada pdf con cada uno de ellos.

# Instrucciones de Ejecución

## Ejecución en local
1 Abrimos una terminal donde se encuentra el proyecto.

2 Situarnos en la carpeta en la que tengamos el proyecto.

3 python nombreFichero.py 

# Dónde Obtener Ayuda


## Repositorio de Grobid
https://github.com/kermitt2/grobid

## Repositorio del cliente de Python para Grobid
https://github.com/kermitt2/grobid_client_python

## Documentación de Grobid
https://grobid.readthedocs.io/en/latest/
