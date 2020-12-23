# Predicción de horas de llegada de buses
### CC5214 Proyecto de Ciencia de Datos

## Descripción
Transapp es una aplicación que te permite consultar el tiempo de espera de los buses de transantiago y ver dónde vienen en el mapa.
También te permite reportar cualquier problema que encuentres en el bus o paradero y ver lo que otros usuarios han reportado.

La métrica utilizada hoy en día para estimar horario de llegada es ofrecida como un servicio de www.sonda.com y les entrega un intervalo de tiempo en vez de una hora estimada. Esto dificulta la comparación entre buses.

#### Objetivo
Desarrollar una nueva métrica para estimar el tiempo de llegada de los buses a los paraderos o puntos específicos de la ruta.


## Instalación



#### Requisitos

- cython==0.29.13
- matplotlib==3.3.1
- numpy==1.19.2
- pandas==1.1.2
- pytorch==1.7.0
- scipy==1.5.2
- seaborn==0.11.0


## Modo de uso

Para lograr crear un modelo de predicción de tiempos de espera se debe proceder como sigue:

1. Ejecutar archivo **visualizacion.ipynb (opcional)**: este archivo permite obtener una primera mirada a los datos con respecto a su contenido, además de información estadística básica.
2. Ejecutar archivo **comparacion.ipynb**: este archivo utiliza el módulo de limpieza para preparar la base de datos y posteriormente crear nuevas columnas útiles para la predicción. En este paso se realiza la filtración por expedición y pareamiento de puntos, además de la creación de la columna objetivo diferencia de tiempo.
Es importante notar que en el contexto del curso, este notebook recibe la base de datos previamente filtrada con los servicios de interés y ese paso *no* está incluido en el código.
3. Ejecutar archivo **codificacion_servicios.ipynb**: en este paso se realiza la codificación de los servicios para poder utilizarlos como feature en la regresión. Correr sólo en caso de utilizar otros servicios distintos a los considerados relevantes durante este proyecto.
4. Ejecutar notebooks **regersion_lineal_polinomial.ipynb** y **random_forest.ipynb**: en este último paso se entrenan, validan y testean los modelos, obteniendo errores MAE, MRS  y R2 por intervalo de tiempo.
5. En la carpeta **redes neuronales** se encuentran notebooks donde se implementan arquitecturas con distintas variaciones, además están disponibles los checkpoints de las distintas pruebas.

##### Observaciones
1. La descripción detallada de la base de datos se encuentra en el archivo **descripcion.txt**

 