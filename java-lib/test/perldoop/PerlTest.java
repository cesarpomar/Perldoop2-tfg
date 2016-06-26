package perldoop;

import java.util.Comparator;
import java.util.List;
import java.util.Map;
import org.junit.Test;
import junit.framework.*;
import static org.junit.Assert.*;
import static org.mockito.Matchers.*;
import static org.mockito.Mockito.*;

/**
 * Pruebas de la clase Perl
 *
 * @author César Pomar
 */
public class PerlTest extends TestCase {

    @Test
    public void testPrint() {
        System.out.println("print");
        int expResult = 1;
        int result = Perl.print("");
        assertEquals(expResult, result);
    }

    @Test
    public void testSay() {
        System.out.println("say");
        int expResult = 1;
        int result = Perl.say("");
        assertEquals(expResult, result);
    }

    @Test
    public void testSplit() {
        System.out.println("split");
        String[] expResult = {"1", "2", "3"};
        String[] result = Perl.split(",", "1,2,3");
        assertArrayEquals(expResult, result);
    }

    @Test
    public void testChopRef() {
        System.out.println("chopRef");
        Ref<String> args = new Ref<>("hola");
        String expResult = "a";
        String result = Perl.chop(args);
        assertEquals(expResult, result);
        assertEquals(args.get(), "hol");
    }

    @Test
    public void testChop() {
        System.out.println("chop");
        String expResult = "hol";
        String result = Perl.chop("hola");
        assertEquals(expResult, result);
    }

    @Test
    public void testChompRef() {
        System.out.println("chompRef");
        Ref<String> args = new Ref<>("hola \t");
        Integer expResult = 2;
        Integer result = Perl.chomp(args);
        assertEquals(expResult, result);
        assertEquals(args.get(), "hola");
    }

    @Test
    public void testChomp() {
        System.out.println("chomp");
        String expResult = "hola";
        String result = Perl.chomp("hola \t");
        assertEquals(expResult, result);
    }

    @Test
    public void testDefined() {
        System.out.println("defined");
        //No nulo
        Boolean expResult = true;
        Boolean result = Perl.defined("hola");
        assertEquals(expResult, result);
        //Nulo
        expResult = false;
        result = Perl.defined(null);
        assertEquals(expResult, result);
    }

    @Test
    public void testEach() {
        System.out.println("each");
        Boolean expResult = true;
        Boolean result = Perl.each(null, null, null);
        assertEquals(expResult, result);
    }

    @Test
    public void testSystem() {
        System.out.println("system");
        //No nulo
        Integer expResult = 0;
        Integer result = Perl.system("echo 1");
        assertEquals(expResult, result);
        //Nulo
        expResult = -1;
        result = Perl.system("asf");
        assertEquals(expResult, result);
    }

    @Test
    public void testOpen() {
        System.out.println("open");
        PerlFile file = mock(PerlFile.class);
        Integer expResult = 0;
        when(file.open(any(), any())).thenReturn(expResult);
        Integer result = Perl.open(file, "", "");
        assertEquals(expResult, result);
    }

    @Test
    public void testClose() {
        System.out.println("close");
        PerlFile file = mock(PerlFile.class);
        Integer expResult = 0;
        when(file.close()).thenReturn(expResult);
        Integer result = Perl.close(file);
        assertEquals(expResult, result);
    }

    @Test
    public void testSortArray() {
        System.out.println("sortArray");
        String[] args = {"2", "1", "3"};
        String[] expResult = {"1", "2", "3"};
        String[] result = Perl.sort(args);
        assertArrayEquals(expResult, result);
    }

    @Test
    public void testSortList() {
        System.out.println("sortList");
        List<String> args = Util.list("2", "1", "3");
        List<String> expResult = Util.list("1", "2", "3");
        List<String> result = Perl.sort(args);
        assertArrayEquals(expResult.toArray(), result.toArray());
    }

    @Test
    public void testSortArrayComp() {
        System.out.println("sortArrayComp");
        Comparator<String> cmp = (String o1, String o2) -> o2.compareTo(o1);
        String[] args = {"2", "1", "3"};
        String[] expResult = {"3", "2", "1"};
        String[] result = Perl.sort(args, cmp);
        assertArrayEquals(expResult, result);
    }

    @Test
    public void testSortListComp() {
        System.out.println("sortListComp");
        Comparator<String> cmp = (String o1, String o2) -> o2.compareTo(o1);
        List<String> args = Util.list("2", "1", "3");
        List<String> expResult = Util.list("3", "2", "1");
        List<String> result = Perl.sort(args, cmp);
        assertArrayEquals(expResult.toArray(), result.toArray());
    }

    @Test
    public void testUc() {
        System.out.println("uc");
        String expResult = "HOLA";
        String result = Perl.uc("hola");
        assertEquals(expResult, result);
    }

    @Test
    public void testUcfirst() {
        System.out.println("ucfirst");
        String expResult = "Hola";
        String result = Perl.ucfirst("hola");
        assertEquals(expResult, result);
    }

    @Test
    public void testLc() {
        System.out.println("lc");
        String expResult = "hola";
        String result = Perl.lc("HOLA");
        assertEquals(expResult, result);
    }

    @Test
    public void testLcfirst() {
        System.out.println("lcfirst");
        String expResult = "hOLA";
        String result = Perl.lcfirst("HOLA");
        assertEquals(expResult, result);
    }

    @Test
    public void testDelete() {
        System.out.println("delete");
        Map<String, String> m = new HashPerl<>();
        String key = "key";
        String value = "value";
        m.put(key, value);
        String expResult = value;
        String result = Perl.delete(m, key);
        assertEquals(expResult, result);
        assertFalse(m.containsKey(key));
    }

    @Test
    public void testJoin() {
        System.out.println("join");
        String[] args = {"1", "2", "3"};
        String expResult = "1,2,3";
        String result = Perl.join(",", args);
        assertEquals(expResult, result);
    }

    @Test
    public void testKeys() {
        System.out.println("keys");
        Map<String, String> m = new HashPerl<>();
        m.put("1", "a");
        m.put("2", "b");
        m.put("3", "c");
        String[] result = Perl.keys(m);
        assertEquals(result.length, m.size());
        for (String k : result) {
            assertTrue(m.containsKey(k));
        }
    }

    @Test
    public void testValues() {
        System.out.println("keys");
        Map<String, String> m = new HashPerl<>();
        m.put("1", "a");
        m.put("2", "b");
        m.put("3", "c");
        List<String> result = Perl.values(m);
        assertEquals(result.size(), m.size());
        for (String k : result) {
            assertTrue(m.containsValue(k));
        }
    }

    @Test
    public void testLength() {
        System.out.println("length");
        Integer expResult = 4;
        Integer result = Perl.length("hola");
        assertEquals(expResult, result);
    }

    @Test
    public void testSubstrRefInitLenRepl() {
        System.out.println("substrRefInitLenRepl");
        Ref<String> args = new Ref<>("hola mundo");
        String result = Perl.substr(args, 4, 1, " en el ");
        assertEquals(" ", result);
        assertEquals("hola en el mundo", args.get());
    }

    @Test
    public void testSubstrInitLenRepl() {
        System.out.println("substrInitLenRepl");
        String args = "hola mundo";
        String result = Perl.substr(args, 4, 1, " en el ");
        assertEquals("hola en el mundo", result);
    }

    @Test
    public void testSubstrInitLen() {
        System.out.println("substrInitLen");
        String args = "hola mundo";
        String result = Perl.substr(args, 4, 1);
        assertEquals(" ", result);
    }

    @Test
    public void testSubstrInit() {
        System.out.println("substrInit");
        String args = "hola mundo";
        String result = Perl.substr(args, 4);
        assertEquals(" mundo", result);
    }

    @Test
    public void testSPushRefArrayElem() {
        System.out.println("pushRefArrayElem");
        Ref<Integer[]> args = new Ref(new Integer[]{2, 3, 4});
        Integer[] expResult = {2, 3, 4, 5};
        Integer result = Perl.push(args, 5);
        assertEquals(result, (Integer) 1);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSPushArrayElem() {
        System.out.println("pushArrayElem");
        Integer[] args = {2, 3, 4};
        Integer[] expResult = {2, 3, 4, 5};
        Integer[] result = Perl.push(args, 5);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSPushRefArrayArray() {
        System.out.println("pushRefArrayArray");
        Ref<Integer[]> args = new Ref(new Integer[]{2, 3, 4});
        Integer[] push = {5, 6};
        Integer[] expResult = {2, 3, 4, 5, 6};
        Integer result = Perl.push(args, push);
        assertEquals(result, (Integer) 2);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSPushArrayArray() {
        System.out.println("pushArrayArray");
        Integer[] args = {2, 3, 4};
        Integer[] push = {5, 6};
        Integer[] expResult = {2, 3, 4, 5, 6};
        Integer[] result = Perl.push(args, push);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSPushRefArrayList() {
        System.out.println("pushRefArrayList");
        Ref<Integer[]> args = new Ref(new Integer[]{2, 3, 4});
        List<Integer> push = Util.list(5, 6);
        Integer[] expResult = {2, 3, 4, 5, 6};
        Integer result = Perl.push(args, push);
        assertEquals(result, (Integer) 2);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSPushArrayList() {
        System.out.println("pushArrayList");
        Integer[] args = {2, 3, 4};
        List<Integer> push = Util.list(5, 6);
        Integer[] expResult = {2, 3, 4, 5, 6};
        Integer[] result = Perl.push(args, push);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSPushListElem() {
        System.out.println("pushListElem");
        List<Integer> args = Util.list(2, 3, 4);
        List<Integer> expResult = Util.list(2, 3, 4, 5);
        Integer result = Perl.push(args, 5);
        assertArrayEquals(args.toArray(), expResult.toArray());
        assertEquals(result, (Integer) 1);
    }

    @Test
    public void testSPushListArray() {
        System.out.println("pushListArray");
        List<Integer> args = Util.list(2, 3, 4);
        Integer[] push = {5, 6};
        List<Integer> expResult = Util.list(2, 3, 4, 5, 6);
        Integer result = Perl.push(args, push);
        assertArrayEquals(args.toArray(), expResult.toArray());
        assertEquals(result, (Integer) 2);
    }

    @Test
    public void testSPushListList() {
        System.out.println("pushListList");
        List<Integer> args = Util.list(2, 3, 4);
        List<Integer> push = Util.list(5, 6);
        List<Integer> expResult = Util.list(2, 3, 4, 5, 6);
        Integer result = Perl.push(args, push);
        assertArrayEquals(args.toArray(), expResult.toArray());
        assertEquals(result, (Integer) 2);
    }

    @Test
    public void testSUnshiftRefArrayElem() {
        System.out.println("unshiftRefArrayElem");
        Ref<Integer[]> args = new Ref(new Integer[]{2, 3, 4});
        Integer[] expResult = {1, 2, 3, 4};
        Integer result = Perl.unshift(args, 1);
        assertEquals(result, (Integer) 1);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSUnshiftArrayElem() {
        System.out.println("unshiftArrayElem");
        Integer[] args = {2, 3, 4};
        Integer[] expResult = {1, 2, 3, 4};
        Integer[] result = Perl.unshift(args, 1);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSUnshiftRefArrayArray() {
        System.out.println("unshiftRefArrayArray");
        Ref<Integer[]> args = new Ref(new Integer[]{2, 3, 4});
        Integer[] unshift = {0, 1};
        Integer[] expResult = {0, 1, 2, 3, 4};
        Integer result = Perl.unshift(args, unshift);
        assertEquals(result, (Integer) 2);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSUnshiftArrayArray() {
        System.out.println("unshiftArrayArray");
        Integer[] args = {2, 3, 4};
        Integer[] unshift = {0, 1};
        Integer[] expResult = {0, 1, 2, 3, 4};
        Integer[] result = Perl.unshift(args, unshift);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSUnshiftRefArrayList() {
        System.out.println("unshiftRefArrayList");
        Ref<Integer[]> args = new Ref(new Integer[]{2, 3, 4});
        List<Integer> unshift = Util.list(0, 1);
        Integer[] expResult = {0, 1, 2, 3, 4};
        Integer result = Perl.unshift(args, unshift);
        assertEquals(result, (Integer) 2);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSUnshiftArrayList() {
        System.out.println("unshiftArrayList");
        Integer[] args = {2, 3, 4};
        List<Integer> unshift = Util.list(0, 1);
        Integer[] expResult = {0, 1, 2, 3, 4};
        Integer[] result = Perl.unshift(args, unshift);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSUnshiftListElem() {
        System.out.println("unshiftListElem");
        List<Integer> args = Util.list(2, 3, 4);
        List<Integer> expResult = Util.list(1, 2, 3, 4);
        Integer result = Perl.unshift(args, 1);
        assertArrayEquals(args.toArray(), expResult.toArray());
        assertEquals(result, (Integer) 1);
    }

    @Test
    public void testSUnshiftListArray() {
        System.out.println("unshiftListArray");
        List<Integer> args = Util.list(2, 3, 4);
        Integer[] unshift = {0, 1};
        List<Integer> expResult = Util.list(0, 1, 2, 3, 4);
        Integer result = Perl.unshift(args, unshift);
        assertArrayEquals(args.toArray(), expResult.toArray());
        assertEquals(result, (Integer) 2);
    }

    @Test
    public void testSUnshiftListList() {
        System.out.println("unshiftListList");
        List<Integer> args = Util.list(2, 3, 4);
        List<Integer> unshift = Util.list(0, 1);
        List<Integer> expResult = Util.list(0, 1, 2, 3, 4);
        Integer result = Perl.unshift(args, unshift);
        assertArrayEquals(args.toArray(), expResult.toArray());
        assertEquals(result, (Integer) 2);
    }

    @Test
    public void testShiftList() {
        System.out.println("shiftList");
        List<Integer> args = Util.list(1, 2, 3, 4);
        List<Integer> expResult = Util.list(2, 3, 4);
        Integer result = Perl.shift(args);
        assertEquals(result, (Integer) 1);
        assertArrayEquals(args.toArray(), expResult.toArray());
    }

    @Test
    public void testShiftArray() {
        System.out.println("shiftArray");
        Integer[] args = {1, 2, 3, 4};
        Integer[] expResult = {2, 3, 4};
        args = Perl.shift(args);
        assertArrayEquals(args, expResult);
    }

    @Test
    public void testShiftRefArray() {
        System.out.println("shiftRefArray");
        Ref<Integer[]> args = new Ref(new Integer[]{1, 2, 3, 4});
        Integer[] expResult = {2, 3, 4};
        Integer result = Perl.shift(args);
        assertEquals(result, (Integer) 1);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testPopList() {
        System.out.println("popList");
        List<Integer> args = Util.list(1, 2, 3, 4);
        List<Integer> expResult = Util.list(1, 2, 3);
        Integer result = Perl.pop(args);
        assertEquals(result, (Integer) 4);
        assertArrayEquals(args.toArray(), expResult.toArray());
    }

    @Test
    public void testPopArray() {
        System.out.println("popArray");
        Integer[] args = {1, 2, 3, 4};
        Integer[] expResult = {1, 2, 3};
        args = Perl.pop(args);
        assertArrayEquals(args, expResult);
    }

    @Test
    public void testPopRefArray() {
        System.out.println("popRefArray");
        Ref<Integer[]> args = new Ref(new Integer[]{1, 2, 3, 4});
        Integer[] expResult = {1, 2, 3};
        Integer result = Perl.pop(args);
        assertEquals(result, (Integer) 4);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSpliceArrayInit() {
        System.out.println("spliceArrayInit");
        Integer[] args = {1, 2, 3, 4};
        Integer[] expResult = {1};
        Integer[] result = Perl.splice(args, 1);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSpliceRefArrayInit() {
        System.out.println("spliceRefArrayInit");
        Ref<Integer[]> args = new Ref(new Integer[]{1, 2, 3, 4});
        Integer[] expResult = {1};
        Integer[] expCut = {2, 3, 4};
        Integer[] result = Perl.splice(args, 1);
        assertArrayEquals(result, expCut);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSpliceListInit() {
        System.out.println("spliceListInit");
        List<Integer> args = Util.list(1, 2, 3, 4);
        List<Integer> expResult = Util.list(1);
        List<Integer> expCut = Util.list(2, 3, 4);
        List<Integer> result = Perl.splice(args, 1);
        assertArrayEquals(result.toArray(), expCut.toArray());
        assertArrayEquals(args.toArray(), expResult.toArray());
    }

    @Test
    public void testSpliceArrayInitLen() {
        System.out.println("spliceArrayInitLen");
        Integer[] args = {1, 2, 3, 4};
        Integer[] expResult = {1, 3, 4};
        Integer[] result = Perl.splice(args, 1, 1);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSpliceRefArrayInitLen() {
        System.out.println("spliceRefArrayInitLen");
        Ref<Integer[]> args = new Ref(new Integer[]{1, 2, 3, 4});
        Integer[] expResult = {1, 3, 4};
        Integer[] expCut = {2};
        Integer[] result = Perl.splice(args, 1, 1);
        assertArrayEquals(result, expCut);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSpliceListInitLen() {
        System.out.println("spliceListInitLen");
        List<Integer> args = Util.list(1, 2, 3, 4);
        List<Integer> expResult = Util.list(1, 3, 4);
        List<Integer> expCut = Util.list(2);
        List<Integer> result = Perl.splice(args, 1, 1);
        assertArrayEquals(result.toArray(), expCut.toArray());
        assertArrayEquals(args.toArray(), expResult.toArray());
    }

    @Test
    public void testSpliceArrayInitLenReplArray() {
        System.out.println("spliceArrayInitLenReplArray");
        Integer[] args = {1, 2, 3, 4};
        Integer[] expResult = {1, 5, 6, 3, 4};
        Integer[] repl = {5, 6};
        Integer[] result = Perl.splice(args, 1, 1, repl);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSpliceRefArrayInitLenReplArray() {
        System.out.println("spliceRefArrayInitLenReplArray");
        Ref<Integer[]> args = new Ref(new Integer[]{1, 2, 3, 4});
        Integer[] expResult = {1, 5, 6, 3, 4};
        Integer[] expCut = {2};
        Integer[] repl = {5, 6};
        Integer[] result = Perl.splice(args, 1, 1, repl);
        assertArrayEquals(result, expCut);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSpliceListInitLenReplArray() {
        System.out.println("spliceListInitLenReplArray");
        List<Integer> args = Util.list(1, 2, 3, 4);
        List<Integer> expResult = Util.list(1, 5, 6, 3, 4);
        List<Integer> expCut = Util.list(2);
        Integer[] repl = {5, 6};
        List<Integer> result = Perl.splice(args, 1, 1, repl);
        assertArrayEquals(result.toArray(), expCut.toArray());
        assertArrayEquals(args.toArray(), expResult.toArray());
    }

    @Test
    public void testSpliceArrayInitLenReplList() {
        System.out.println("spliceArrayInitLenReplList");
        Integer[] args = {1, 2, 3, 4};
        Integer[] expResult = {1, 5, 6, 3, 4};
        List<Integer> repl = Util.list(5, 6);
        Integer[] result = Perl.splice(args, 1, 1, repl);
        assertArrayEquals(result, expResult);
    }

    @Test
    public void testSpliceRefArrayInitLenReplList() {
        System.out.println("spliceRefArrayInitLenReplList");
        Ref<Integer[]> args = new Ref(new Integer[]{1, 2, 3, 4});
        Integer[] expResult = {1, 5, 6, 3, 4};
        Integer[] expCut = {2};
        List<Integer> repl = Util.list(5, 6);
        Integer[] result = Perl.splice(args, 1, 1, repl);
        assertArrayEquals(result, expCut);
        assertArrayEquals(args.get(), expResult);
    }

    @Test
    public void testSpliceListInitLenReplList() {
        System.out.println("spliceListInitLenReplList");
        List<Integer> args = Util.list(1, 2, 3, 4);
        List<Integer> expResult = Util.list(1, 5, 6, 3, 4);
        List<Integer> expCut = Util.list(2);
        List<Integer> repl = Util.list(5, 6);
        List<Integer> result = Perl.splice(args, 1, 1, repl);
        assertArrayEquals(result.toArray(), expCut.toArray());
        assertArrayEquals(args.toArray(), expResult.toArray());
    }

}
