/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package perldoop;

import java.util.HashMap;
import java.util.Map;

/**
 * Clase para imitar los hash de perl, donde al añadir un valor se devuelve el
 * mismo.
 * @author César
 */
public class HashPerl<K, V> extends HashMap<K, V>{

    /**
     * Crea un hash con un tamaño y un factor de crecimiento
     * @param initialCapacity Tamaño inicial
     * @param loadFactor Factor de crecimiento
     */
    public HashPerl(int initialCapacity, float loadFactor) {
        super(initialCapacity, loadFactor);
    }

    /**
     * Crea un hash con un tamaño determinado
     * @param initialCapacity
     */
    public HashPerl(int initialCapacity) {
        super(initialCapacity);
    }

    /**
     * Crea un hash por defecto
     */
    public HashPerl() {
        super();
    }

    /**
     * Crea un hash a partir de otro hash
     * @param m hash
     */
    public HashPerl(Map<? extends K, ? extends V> m) {
        super(m);
    }

    /**
     * Guarda un elemento asociandolo a una clave
     * @param key Clave
     * @param value Valor
     * @return Valor añadido
     */
    @Override
    public V put(K key, V value) {
        super.put(key, value);
        return  value;
    }
    
    
}
