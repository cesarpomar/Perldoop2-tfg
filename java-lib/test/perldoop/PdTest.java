package perldoop;

import org.junit.Test;
import junit.framework.*;
import static org.junit.Assert.*;

/**
 * Pruebas de la clase Pd
 *
 * @author César Pomar
 */
public class PdTest extends TestCase {

    @Test
    public void testRangeInteger() {
        System.out.println("rangeInteger");
        Integer[] expResult;
        Integer[] result;
        //Comportamiento normal
        expResult = new Integer[]{1, 2, 3, 4, 5, 6, 7, 8, 9};
        result = Pd.range(1, 9);
        assertArrayEquals(expResult, result);
        //Negativos
        expResult = new Integer[]{-5, -4, -3, -2, -1, 0};
        result = Pd.range(-5, 0);
        assertArrayEquals(expResult, result);
        //Vacio
        expResult = new Integer[]{};
        result = Pd.range(4, 2);
        assertArrayEquals(expResult, result);
    }

    @Test
    public void testRangeString() {
        System.out.println("rangeString");
        String[] expResult;
        String[] result;
        //Comportamiento normal
        expResult = new String[]{"a", "b", "c", "d", "e", "f", "g", "h", "i"};
        result = Pd.range("a", "i");
        assertArrayEquals(expResult, result);
        //mayusculas
        expResult = new String[]{"A", "B", "C", "D", "E", "F", "G", "H", "I"};
        result = Pd.range("A", "I");
        assertArrayEquals(expResult, result);
        //Numeros
        expResult = new String[]{"1", "2", "3", "4", "5", "6", "7", "8", "9"};
        result = Pd.range("1", "9");
        assertArrayEquals(expResult, result);
        //Vacio
        expResult = new String[]{};
        result = Pd.range("z", "a");
        assertArrayEquals(expResult, result);
    }

}
