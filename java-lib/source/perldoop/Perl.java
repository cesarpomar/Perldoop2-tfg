package perldoop;

import java.lang.reflect.Array;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

/**
 * Clase para las funciones definidas en Perl
 *
 * @author César
 */
public class Perl {

    /**
     * Imprime un array de valores
     *
     * @param values valores
     * @return 1
     */
    public static int print(Object... values) {
        for (Object value : values) {
            System.out.print(value);
        }
        return 1;
    }

    /* Imprime un array de valores
     *
     * @param values valores
     * @return 1
     */
    public static int say(Object... values) {
        for (Object value : values) {
            System.out.println(value);
        }
        return 1;
    }

    /**
     * Separa una cadena usando regex
     *
     * @param cad Cadena
     * @param regex Separador
     * @return cadena partida
     */
    public static String[] split(String regex, String cad) {
        return cad.split(regex);
    }

    /**
     * Elimina el ultimo caracter de una funcion
     *
     * @param cad Puntero a la cadena
     * @return caracter eliminado
     */
    public static String chop(Ref<String> cad) {
        int pos = cad.get().length() - 1;
        cad.set(cad.get().substring(0, pos));
        return cad.get().charAt(pos) + "";
    }

    /**
     * Elimina el ultimo caracter de una funcion, en este caso ese caracter no
     * se lee y se usa el retorno para actualizar el string
     *
     * @param cad Cadena
     * @return Cadena
     */
    public static String chop(String cad) {
        return cad.substring(0, cad.length() - 1);
    }

    /**
     * Limpia el final de una cadena
     *
     * @param cad Puntero a la cadena
     * @return numero de caracteres eliminados
     */
    public static Integer chomp(Ref<String> cad) {
        int len = cad.get().length();
        cad.set(cad.get().trim());
        return cad.get().length() - len;
    }

    /**
     * Limpia el final de una cadena, en este caso ese caracter no se lee y se
     * usa el retorno para actualizar el string
     *
     * @param cad Cadena
     * @return Cadena
     */
    public static String chomp(String cad) {
        return cad.trim();
    }

    /**
     * Comprueba si un Objeto tiene asignado un valor
     *
     * @param obj Objeto
     * @return True si el objeto es distinto de null, False en otro caso
     */
    public static Boolean defined(Object obj) {
        return obj != null;
    }

    /**
     * Simula la funcion each, realizando las operaciones en cada parametro
     *
     * @param it Coge la siguiente entrada del iterador
     * @param key Actualiza la variable clave
     * @param value Actualiza la variable valor
     * @return true
     */
    public static Boolean each(Object it, Object key, Object value) {
        return true;
    }

    /**
     * Funcion llamada al sistema que ejecuta un comando en el shell
     *
     * @param cmd Comando
     * @return Entero que representa el estado de salida de la ejecucion.
     */
    public static Integer system(String cmd) {
        try {
            Process exec = Runtime.getRuntime().exec(cmd);
            return exec.waitFor();
        } catch (Exception ex) {
            return -1;
        }
    }

    /**
     * Abre un fichero
     *
     * @param file Descriptor del fichero
     * @param mode Finalidad de apertura del fichero
     * @param path Ruta del fichero
     * @return 1 si tuvo existe, 0 en otro caso
     */
    public static Integer open(PerlFile file, String mode, String path) {
        return file.open(path, mode);
    }

    /**
     * Cierra un fichero
     *
     * @param file Descriptor del fichero
     * @return 1 si tuvo existe, 0 en otro caso
     */
    public static Integer close(PerlFile file) {
        return file.close();
    }

    /**
     * Ordena una lista de forma personalizada
     *
     * @param <T> Tipo de la Lista
     * @param list Lista
     * @param comp Comparador para ordenar
     * @return Lista ordenada
     */
    public static <T> List<T> sort(List<T> list, Comparator<T> comp) {
        list = Pd.copy(list);
        Collections.sort(Pd.copy(list), comp);
        return list;
    }

    /**
     * Ordena un array de forma personalizada
     *
     * @param <T> Tipo del Array
     * @param array Array
     * @param comp Comparador para ordenar
     * @return Array ordenado
     */
    public static <T> T[] sort(T[] array, Comparator<T> comp) {
        array = Pd.copy(array);
        Arrays.sort(array, comp);
        return array;
    }

    /**
     * Ordena una lista
     *
     * @param <T> Tipo de la Lista
     * @param list Lista
     * @return Lista ordenada
     */
    public static <T extends Comparable> List<T> sort(List<T> list) {
        list = Pd.copy(list);
        Collections.sort(list);
        return list;
    }

    /**
     * Ordena un array
     *
     * @param <T> Tipo del Array
     * @param array Array
     * @return Array ordenado
     */
    public static <T extends Comparable> T[] sort(T[] array) {
        array = Pd.copy(array);
        Arrays.sort(array);
        return array;
    }

    /**
     * Convierte una cadena a mayusculas
     *
     * @param s cadena
     * @return cadena en mayusculas
     */
    public static String uc(String s) {
        return s.toUpperCase();
    }

    /**
     * Convierte la primera letra en mayusculas
     *
     * @param s cadena
     * @return cadena tranformada
     */
    public static String ucfirst(String s) {
        return s.substring(0, 1).toUpperCase() + s.substring(1);
    }

    /**
     * Convierte una cadena a minusculas
     *
     * @param s cadena
     * @return cadena en minusculas
     */
    public static String lc(String s) {
        return s.toLowerCase();
    }

    /**
     * Convierte la primera letra en minusculas
     *
     * @param s cadena
     * @return cadena tranformada
     */
    public static String lcfirst(String s) {
        return s.substring(0, 1).toLowerCase() + s.substring(1);
    }

    /**
     * Aborta el programa y mustra un mensaje de error
     *
     * @param msg Mensaje de error
     * @return Nunca va a retornar
     */
    public static Integer die(String msg) {
        System.err.println(msg);
        System.exit(-1);
        return 1;
    }

    /**
     * Borra el valor de un hash
     *
     * @param <T> Tipo del valor
     * @param hash Hashmap
     * @param key Clave
     * @return Elemento borrado
     */
    public static <T> T delete(Map<String, T> hash, String key) {
        return hash.remove(key);
    }

    /**
     * Une todo los elementos de una lista separandolos con un separador.
     *
     * @param sep Separador
     * @param list Lista
     * @return Cadena resultante de la union
     */
    public static String join(String sep, List<String> list) {
        StringBuilder sb = new StringBuilder(list.size() * 16);
        for (String e : list) {
            sb.append(e);
            sb.append(sep);
        }
        return sb.substring(0, sb.length() - sep.length());
    }

    /**
     * Une todo los elementos de un array separandolos con un separador.
     *
     * @param sep Separador
     * @param array Array
     * @return Cadena resultante de la union
     */
    public static String join(String sep, String[] array) {
        StringBuilder sb = new StringBuilder(array.length * 16);
        for (String e : array) {
            sb.append(e);
            sb.append(sep);
        }
        return sb.substring(0, sb.length() - sep.length());
    }

    /**
     * Retorna un array con las claves de un hashmap
     *
     * @param hash Hashmap
     * @return Array de claves
     */
    public static String[] keys(Map<String, Object> hash) {
        return hash.keySet().toArray(new String[0]);
    }

    /**
     * Retorna un array con los valores de un hashmap
     *
     * @param hash Hashmap
     * @return Array de valores
     */
    public static <T> T[] values(Map<String, T> hash) {
        Collection<T> values = hash.values();
        T[] array = (T[]) Array.newInstance(values.getClass(), 0);
        return values.toArray(array);
    }

    /**
     * Termina la ejecucion del programa
     *
     * @param status Codigo de salida
     * @return Nunca retorna
     */
    public static Integer exit(Integer status) {
        System.exit(status);
        return 1;
    }

    /**
     * Calcula la longitud de una codena
     *
     * @param string Cadena
     * @return Longitud
     */
    public static Integer length(String string) {
        return string.length();
    }

    /**
     * Crea una subcadena de la cadena actual remplazando un intervalo con otra
     * cadena.
     *
     * @param string Puntero a la cadena original
     * @param init Inicio del corte
     * @param len tamaño del corte
     * @param repl Cadena de remplazo
     * @return Cadena
     */
    public static String substr(Ref<String> string, Integer init, Integer len, String repl) {
        String org = string.get();
        string.set(string.get().substring(0, init) + repl + string.get().substring(init + len));
        return org.substring(init, init + len);
    }

    /**
     * Crea una subcadena de la cadena actual remplazando un intervalo con otra
     * cadena.En este caso la salida no se lee y se usa el retorno para
     * actualizar el string
     *
     * @param string Cadena original
     * @param init Inicio del corte
     * @param len tamaño del corte
     * @param repl Cadena de remplazo
     * @return Cadena
     */
    public static String substr(String string, Integer init, Integer len, String repl) {
        return string.substring(0, init) + repl + string.substring(init + len);
    }

    /**
     * Crea una subcadena de la cadena actual.
     *
     * @param string Cadena original
     * @param init Inicio del corte
     * @param len tamaño del corte
     * @return Cadena
     */
    public static String substr(String string, Integer init, Integer len) {
        return string.substring(init, init + len);
    }

    /**
     * Crea una subcadena de la cadena actual.
     *
     * @param string Cadena original
     * @param init Inicio del corte
     * @return Cadena
     */
    public static String substr(String string, Integer init) {
        return string.substring(init);
    }

    /**
     * Añade un elemento a un array
     *
     * @param <T> Tipo de la coleccion
     * @param array Referencia al Array
     * @param elem Elemento a añadir
     * @return Numero de elementos añadidos
     */
    public static <T> Integer push(Ref<T[]> array, T elem) {
        int len = array.get().length;
        T[] result = (T[]) new Object[len + 1];
        System.arraycopy(array.get(), 0, result, 0, len);
        result[len] = elem;
        array.set(result);
        return 1;
    }

    /**
     * Añade un elemento a un array, en este caso ese elemento no se lee y se
     * usa el retorno para actualizar el array
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param elem Elemento a añadir
     * @return Array actualizado
     */
    public static <T> T[] push(T[] array, T elem) {
        T[] result = (T[]) new Object[array.length + 1];
        System.arraycopy(array, 0, result, 0, array.length);
        result[array.length] = elem;
        return result;
    }

    /**
     * Añade un elemento a una lista
     *
     * @param <T> Tipo de la coleccion
     * @param list Lista
     * @param elem Elemento a añadir
     * @return Numero de elementos añadidos
     */
    public static <T> Integer push(List<T> list, T elem) {
        list.add(elem);
        return 1;
    }

    /**
     * Concatena dos arrays
     *
     * @param <T> Tipo de la coleccion
     * @param array Referencia al Array 1
     * @param elem Array 2
     * @return Numero de elementos añadidos
     */
    public static <T> Integer push(Ref<T[]> array, T[] elem) {
        int len = array.get().length;
        T[] result = (T[]) new Object[len + elem.length];
        System.arraycopy(array.get(), 0, result, 0, len);
        System.arraycopy(elem, 0, result, len, elem.length);
        array.set(result);
        return elem.length;
    }

    /**
     * Concatena dos arrays, en este caso ese elemento no se lee y se usa el
     * retorno para actualizar el array
     *
     * @param <T> Tipo de la coleccion
     * @param array Array 1
     * @param elem Array 2
     * @return Array actualizado
     */
    public static <T> T[] push(T[] array, T[] elem) {
        T[] result = (T[]) new Object[array.length + elem.length];
        System.arraycopy(array, 0, result, 0, array.length);
        System.arraycopy(elem, 0, result, array.length, elem.length);
        return result;
    }

    /**
     * Concatena un array a una lista
     *
     * @param <T> Tipo de la coleccion
     * @param list Lista
     * @param elem Array
     * @return Numero de elementos añadidos
     */
    public static <T> Integer push(List<T> list, T[] elem) {
        Collections.addAll(list, elem);
        return elem.length;
    }

    /**
     * Concatena una lista a un array
     *
     * @param <T> Tipo de la coleccion
     * @param array Referencia al Array
     * @param elem Lista
     * @return Numero de elementos añadidos
     */
    public static <T> Integer push(Ref<T[]> array, List<T> elem) {
        int len = array.get().length;
        T[] result = (T[]) new Object[len + elem.size()];
        System.arraycopy(array.get(), 0, result, 0, len);
        elem.forEach((e) -> {
            int p = len;
            result[p++] = e;
        });
        array.set(result);
        return elem.size();
    }

    /**
     * Concatena una lista a un array, en este caso ese elemento no se lee y se
     * usa el retorno para actualizar el array
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param elem Lista
     * @return Array actualizado
     */
    public static <T> T[] push(T[] array, List<T> elem) {
        T[] result = (T[]) new Object[array.length + elem.size()];
        System.arraycopy(array, 0, result, 0, array.length);
        elem.forEach((e) -> {
            int p = array.length;
            result[p++] = e;
        });
        return result;
    }

    /**
     * Concatena dos listas
     *
     * @param <T> Tipo de la coleccion
     * @param list Lista 1
     * @param elem Lista 2
     * @return Numero de elementos añadidos
     */
    public static <T> Integer push(List<T> list, List<T> elem) {
        list.addAll(elem);
        return elem.size();
    }

    /**
     * Quita el primer elemento de una lista y lo devuelve
     *
     * @param <T> Tipo de la lista
     * @param list Lista
     * @return Caracter eliminado de la primera posicion
     */
    public static <T> T shift(List<T> list) {
        return list.remove(0);
    }

    /**
     * Quita el primer elemento de un array y lo devuelve.
     *
     * @param <T> Tipo del array
     * @param array Puntero al Array
     * @return Caracter eliminado de la primera posicion
     */
    public static <T> T shift(Ref<T[]> array) {
        int len = array.get().length - 1;
        T[] src = array.get();
        T[] copia = (T[]) new Object[len];
        System.arraycopy(src, 1, copia, 0, len);
        array.set(copia);
        return src[0];
    }

    /**
     * Quita el primer elemento de un array y lo devuelve, en este caso ese
     * elemento no se lee y se usa el retorno para actualizar el array
     *
     * @param <T> Tipo del array
     * @param array Array
     * @return Array actualizado
     */
    public static <T> T[] shift(T[] array) {
        T[] copia = (T[]) new Object[array.length - 1];
        System.arraycopy(array, 1, copia, 0, array.length - 1);
        return copia;
    }

    /**
     * Quita el ultimo elemento de una lista y lo devuelve
     *
     * @param <T> Tipo de la lista
     * @param list Lista
     * @return Caracter eliminado de la primera posicion
     */
    public static <T> T pop(List<T> list) {
        return list.remove(list.size() - 1);
    }

    /**
     * Quita el ultimo elemento de un array y lo devuelve.
     *
     * @param <T> Tipo del array
     * @param array Puntero al Array
     * @return Caracter eliminado de la primera posicion
     */
    public static <T> T pop(Ref<T[]> array) {
        int len = array.get().length - 1;
        T[] src = array.get();
        T[] copia = (T[]) new Object[len];
        System.arraycopy(src, 0, copia, 0, len - 1);
        array.set(copia);
        return src[0];
    }

    /**
     * Quita el ultimo elemento de un array y lo devuelve, en este caso ese
     * elemento no se lee y se usa el retorno para actualizar el array
     *
     * @param <T> Tipo del array
     * @param array Array
     * @return Array actualizado
     */
    public static <T> T[] pop(T[] array) {
        T[] copia = (T[]) new Object[array.length - 1];
        System.arraycopy(array, 0, copia, 0, array.length - 1);
        return copia;
    }

    /**
     * Segmenta el array en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @return Segmento eliminado
     */
    public static <T> T[] splice(Ref<T[]> array, Integer init) {
        T[] cut = (T[]) new Object[array.get().length - init];
        T[] dest = (T[]) new Object[init];
        System.arraycopy(array.get(), init, cut, 0, array.get().length - init);
        System.arraycopy(array.get(), 0, dest, 0, init);
        array.set(dest);
        return cut;
    }

    /**
     * Segmenta el array en un intervalo, en este caso ese elemento no se lee y
     * se usa el retorno para actualizar el array
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @return Array actualizado
     */
    public static <T> T[] splice(T[] array, Integer init) {
        T[] dest = (T[]) new Object[init];
        System.arraycopy(array, 0, dest, 0, init);
        return dest;
    }

    /**
     * Segmenta la lista en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param list Lista
     * @param init Inicio
     * @return Segmento eliminado
     */
    public static <T> T[] splice(List<T> list, Integer init) {
        return null;
    }

    /**
     * Segmenta el array en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @param len tamaño del corte
     * @return Segmento eliminado
     */
    public static <T> T[] splice(Ref<T[]> array, Integer init, Integer len) {
        return null;
    }

    /**
     * Segmenta el array en un intervalo, en este caso ese elemento no se lee y
     * se usa el retorno para actualizar el array
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @param len tamaño del corte
     * @return Array actualizado
     */
    public static <T> T[] splice(T[] array, Integer init, Integer len) {
        return null;
    }

    /**
     * Segmenta la lista en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param list Lista
     * @param init Inicio
     * @param len tamaño del corte
     * @return Segmento eliminado
     */
    public static <T> T[] splice(List<T> list, Integer init, Integer len) {
        return null;
    }

    /**
     * Segmenta el array en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @param len tamaño del corte
     * @param repl Segmento de remplazo
     * @return Segmento eliminado
     */
    public static <T> T[] splice(Ref<T[]> array, Integer init, Integer len, T[] repl) {
        return null;
    }

    /**
     * Segmenta el array en un intervalo, en este caso ese elemento no se lee y
     * se usa el retorno para actualizar el array
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @param len tamaño del corte
     * @param repl Segmento de remplazo
     * @return Array actualizado
     */
    public static <T> T[] splice(T[] array, Integer init, Integer len, T[] repl) {
        return null;
    }

    /**
     * Segmenta la lista en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param list Lista
     * @param init Inicio
     * @param len tamaño del corte
     * @param repl Segmento de remplazo
     * @return Segmento eliminado
     */
    public static <T> T[] splice(List<T> list, Integer init, Integer len, T[] repl) {
        return null;
    }

    /**
     * Segmenta el array en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @param len tamaño del corte
     * @param repl Segmento de remplazo
     * @return Segmento eliminado
     */
    public static <T> T[] splice(Ref<T[]> array, Integer init, Integer len, List<T> repl) {
        return null;
    }

    /**
     * Segmenta el array en un intervalo, en este caso ese elemento no se lee y
     * se usa el retorno para actualizar el array
     *
     * @param <T> Tipo de la coleccion
     * @param array Array
     * @param init Inicio
     * @param len tamaño del corte
     * @param repl Segmento de remplazo
     * @return Array actualizado
     */
    public static <T> T[] splice(T[] array, Integer init, Integer len, List<T> repl) {
        return null;
    }

    /**
     * Segmenta la lista en un intervalo
     *
     * @param <T> Tipo de la coleccion
     * @param list Lista
     * @param init Inicio
     * @param len tamaño del corte
     * @param repl Segmento de remplazo
     * @return Segmento eliminado
     */
    public static <T> T[] splice(List<T> list, Integer init, Integer len, List<T> repl) {
        return null;
    }

}
