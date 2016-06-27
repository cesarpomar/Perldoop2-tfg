@echo off
rm *.java
echo. 2>log.txt
for %%f in (*.pl) do perldoop %%f >>log.txt && javac -cp ".;../java-lib/dist/Perldoop.jar" *.java 2>>log.txt && rm *.class