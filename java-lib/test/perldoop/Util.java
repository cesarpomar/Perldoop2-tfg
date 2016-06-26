package perldoop;

import java.util.List;

/**
 * Clase de utilidades para pruebas
 *
 * @author César Pomar
 */
public class Util {

    /**
     * Crea una lista
     * @param <T> Tipo
     * @param values Valores
     * @return Lista
     */
    public static <T> List<T> list(T... values) {
        PerlList<T> l = new PerlList<>(values.length);
        for (T v : values) {
            l.add(v);
        }
        return l;
    }

}
