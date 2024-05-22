# ClusterBERTCoherence

Este script genera una matriz de similaridad comparando los abstracts de los documentos TEI_XML y además hace topic similarity de los abstracts preprocesados para eliminar las "stopwords" y poder elegir en que temas
iría cada uno de los documentos. No sólo eso sino que también dice con que porcentaje pertenece a dicho topic. Nota, cuando dice que pertenece un 0% a un topic significa que el abstract no se parecía demasiado a los
otros o que simplemnte era demasiado corto para poder hacer la comparación.

#Instalación

Como el resto de scripts, no hace falta ninguna instalación extra, bastaría con lo instalado por requirements.txt

#Uso

Para utilizar este script, tiene que ejecutar el 'ClusterBERTCoherence.py' y seguir los prompts que se van mostrando, facilitando, de este modo la carpeta en la que se encuentran los TEI_XML, el sitio donde le gustaría
que se guardase el png generado con el resultado del clustering y por último escribir el nombre (con la extension) del archivo que contendrá la matriz de similaridad.

```bash
python .\ClusterBERTCoherence.py
```
