package perldoop.util;

/**
 * Generacion de cadenas
 *
 * @author César
 */
public class Sequence {

    private final static char[] upper = {'A','B','C','D'};
    private final static char[] down = {'a','b','c','d'};
    private final static char[] number = {};

    private char[] rtype;
    private char[] buffer;
    private int bufferPos;
    private int index;

    public static Sequence[] getSequence(String begin, String end) {
        char[] seq = end.toCharArray();
        Sequence[] res = new Sequence[seq.length];
        for (int i = 0,j=res.length-1; i < res.length; i++,j--) {
            res[i] = new Sequence(seq, j, begin);
        }
        return res;
    }

    private Sequence(char[] buffer, int bufferPos, String begin) {
        char c = begin.charAt(begin.length()-1);
        int desp=buffer.length-begin.length();
        if (c >= 'A' && c <= 'Z') {
            rtype = upper;
        } else if (c >= 'a' && c <= 'z') {
            rtype = down;
        } else {
            rtype = number;
        }
        this.buffer = buffer;
        this.bufferPos = bufferPos;
        if (desp>bufferPos) {
            index = -1;
            buffer[bufferPos] = 0;
        } else {
            for (int i = 0; i < rtype.length; i++) {
                if (rtype[i] == begin.charAt(bufferPos-desp)) {
                    index = i;
                    buffer[bufferPos] = begin.charAt(bufferPos-desp);
                    break;
                }
            }
        }
    }

    public boolean next() {
        boolean flag = false;
        index++;
        if (index == rtype.length) {
            index = 0;
            flag = true;
        }
        buffer[bufferPos] = rtype[index];
        return flag;
    }

    public String getString() {
        return new String(buffer);
    }

}
