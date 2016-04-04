
package perldoop;

/**
 * Clase para definir los metodos relacionados con expresiones regulares
 * @author César
 */
public class Regex {
    
    /**
     * Compreuba si una cadena cumple una expresion regular
     * @param cad Cadena
     * @param regex Expresion regular
     * @return True si coincide, False en otro caso
     */
    public static Boolean match(String cad,String regex){
        regex=regex.replaceAll("\"", "\\\"");
        cad=cad.replaceAll("\"", "\\\"");
        StringBuilder sb=new StringBuilder(100);
        sb.append("perl -e ");
        sb.append('"');
        sb.append("print(\'").append(cad).append("\' =~ ").append(regex).append(");");
        sb.append('"');       
        return !Pd.cmd(sb.toString()).isEmpty();
    }
    
        /**
     * Realiza una substitucion mediante una expresion regular
     * @param cad Cadena
     * @param regex Expresion regular
     * @return Scadena
     */
    public static String s(String cad,String regex){
        regex=regex.replaceAll("\"", "\\\"");
        StringBuilder sb=new StringBuilder(100);
        sb.append("perl -e ");
        sb.append('"');
        sb.append("$x='").append(cad).append("';\n");
        sb.append("$x =~ ").append(regex).append(";\n");
        sb.append("print $x;");
        sb.append('"');
        return Pd.cmd(sb.toString());
    }
    
        /**
     * Realiza una transliteracion mediante una expresion regular
     * @param cad Cadena
     * @param regex Expresion regular
     * @return True si coincide, False en otro caso
     */
    public static String tr(String cad,String regex){
        regex=regex.replaceAll("\"", "\\\"");
        StringBuilder sb=new StringBuilder(100);
        sb.append("perl -e ");
        sb.append('"');
        sb.append("$x='").append(cad).append("';\n");
        sb.append("$x =~ ").append(regex).append(";\n");
        sb.append("print $x;");
        sb.append('"');
        return Pd.cmd(sb.toString());
    }
    
}
