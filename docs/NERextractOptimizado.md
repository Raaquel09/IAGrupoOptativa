# NERextractOptimizado

Este fichero utiliza el modelo preentrenado de "Jean-Baptiste/roberta-large-ner-english" encontrado en hugging-face y extrae de los acknowledgements todas las Organizaciones (ORG) y personas (PER) de dichos acknowledgements.

## Instalación 

Es necesario instalar el fichero requirements.txt

## Uso

Al ejecutarlo va a promptear al usuario para que le facilite la localizacion de la carpeta en la que se encuentran los archivos TEI_XML calculados anteriormente. Cuando termina su ejecución crea un archivo .json en el que hay un listado con los documentos y las entidades que haya encontrado en los acknowledgements.

## Ejemplo de uso

```bash
python NERextractOptimizado.py
```
 
