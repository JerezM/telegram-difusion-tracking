# telegram-difusion-tracking
## Info:
La idea del programa es generar una difusion a todos los miembros de un grupo de manera automatizada y trackear a su vez si ya se contactaron con dicho miembro del grupo o no.
Para lograr esto se tuvieron que tener algunas consideraciones, por ejemplo para que telegram no detecte como spam o actividad sospechosa este programa, se tuvo que segmentar
los msg que se mandan, asi que el programa lo que va a hacer es mandar mensajes de a tandas de 30 mensajes, y cada mensaje va a tener una pausa de 1min entre cada uno, como para
simular un poco mas de realizmo y reducir las posibilidades de ban. 

### Considerando esto, el programa va a tener 2 flujos de ejecucion:
A) Cuando ejecutas el programa por primera vez que te va a preguntar los Grupos a los que queres mandar el mensaje, y te va a generar el archivo CSV con el nombre que vos elijas.
 Una cuestion a considear de esto es que si el/los grupos que elijas tiene mas de 30 miembros en total, entonces la primera iteracion no va a llegar a mandarle el mensaje a todos
 los miembros, por eso va a ser necesaria una segunda(o mas) iteraciones a futuro para poder mandar el msg deseado a todos los miembros.
 
IMPORTARTE: No correr el programa mas de una vez por dia, porque si lo ejecutan 2 veces, entonces van a mandar muchos mensajes con la cuenta de rama y puede llevar a que los baneen.

B) Cuando ya corriste el programa una vez y tenes un CSV creado pero que no se termino de mandar el mensaje a todos los miembros, podes elejir si queres continuar mandando los msg
pendientes y el programa va a retomar desde donde se dejo la ultima vez. En caso de que el archivo CSV seleccionado ya este completado o vos elijas discontinuar la ejecucion, 
entonces se va a reiniciar el programa y va a ejecutar lo mencionado en el paso A.

## Modo de uso:
1) Crear un archivo .txt situado en la carpeta donde este el ejecutable con el nombre "message-file.txt"
2) Escribir el mensaje que queres enviar a los miembros adentro del .txt y guardarlo
3) Ejecutar el programa

4) Al iniciar te va a preguntar que pongas el nombre del CSV que queres checkear el estado(esto es para el caso en que haya un csv creado y toda tenga mensajes pendientes)
4.1) Si el archivo existe y tiene mensajes pendientes entonces retoma la ejecucion y vuelve a mandar 30mensajes a los miembros que siguen
4.2) En caso de que el archivo no exista o exista pero ya no tiene mensajes pendientes, sigue con el paso 5)

5)Te va a preguntar los grupos que queres seleccionar para mandar el mensaje guardado en message-file.txt

6)Una vez seleccionado los grupos, se va a empezar a mandar el mensaje a los distintos miembros, y luego de eso va a terminar el programa.

## OBS:
En el csv se va a guardar el nombre del grupo, la info para identificar al user y el status en relacion a los mensaje enviado(SENDED/NOT SENT/PENDING).
En NOT SENT se aplica para los casos en que hubo algun error al mandar el mensaje y no se acepto el hacerlo, en caso de que pase se podria contartar manualmente porque capaz es un tema
de telegram que flasho(ya si paso con muchos user me avisan porque seguro se depreco algo de la API de telegram o capaz hay algo que esta off y necesita un minifix)