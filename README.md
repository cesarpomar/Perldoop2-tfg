# Peldoop 2.0 #

**Perldoop 2.0** es una nueva versión creada desde cero de "[Perldoop](https://github.com/citiususc/perldoop)", una herramienta creada por los investigadores de la Universidad de Santiago de Compostela como parte del proyecto “High Performance Computing for Natural Language Processing-HPCNLP”. Esta herramienta al igual que su predecesora tiene como principal objetivo traducir automáticamente scripts Perl en código java que puede ser ejecutado en un clúster Hadoop aumentado su rendimiento de manera significativa.

Hadoop tiene a disposición del usuario una herramienta para ejecutar aplicaciones escritas en diferentes lenguajes aparte de Java, conocida como Hadoop Streaming. Para poder usar esta esta característica es necesario que la aplicación lea de la entrada estándar <STDIN> y escriba los resultados en la salida estándar <STDOUT>. Incluso cuando Hadoop Streaming es una herramienta muy potente, se detecta una degradación importante del rendimiento cuando comparamos Hadoop Streaming con respecto a Hadoop con códigos java. Solo cuando los códigos requieren un alto grado de computación con una entrada/salida pequeña, el rendimiento de Hadoop Streaming es en algunos casos mejor debido a la opción de usar lenguajes de programación mucho más eficientes.

Por lo tanto, la mejor opción en cuanto a rendimiento es desarrollar las aplicaciones Hadoop usando java. Sin embargo, traducir código Perl a Java puede convertirse en una tarea larga y tediosa, especialmente cuando la aplicación está compuesta por muchas expresiones regulares. Por esta razón, se ha desarrollado Perldoop, con ella puedes automatizar la traducción de código aumentando el rendimiento y la eficiencia tanto coma la productividad.

En general la traducción automática de un código Perl a Java pude ser una tarea muy complicada, debido a las grandes diferencias entre ambos lenguajes. Es importante destacar que el objetivo de esta herramienta no es traducir absolutamente todo código existente en Perl a Java, si no crear una herramienta capaz de traducir un script Perl escrito para Hadoop Streaming, y producir un código java para compatible con Hadoop. 

# Configuración #

En la carpeta perdoop2 se encuentra el fichero perdoop.py que contiene la interfaz por consola de Perldoop, para poder ejecutarlo, es necesario tener instalado el intérprete de Python en su versión 3. 

Para poder usar el traductor de forma cómoda, se conseja añadir esta carpeta al path del terminal, el script perldoop.bat será el script invocado en caso de sistemas operativos Windows y el archivo perldoop en caso de sistemas operativos Linux. Una vez añadida la carpeta al path debería poder invocarse al traductor escribiendo:

`perldoop perl-file [perl-file ...] [opciones]`

En caso de que estos scripts no funcionen asegúrate de que el intérprete Python este añadido al path y la forma en que es invocado, por defecto está configurado python3 en los sistemas Linux y python en la versión Windows, si es necesario edita los scripts cambiando la invocación a la usada en tu sistema. 

