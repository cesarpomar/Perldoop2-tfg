@echo off
echo. 2>log.txt
cmd /C @echo off & for %%f in (*.pl) do perldoop %%f >> log.txt &^
cmd /C @echo off & javac -cp ".;../java-lib/dist/Perldoop.jar" *.java >> log.txt &^
rm *.class