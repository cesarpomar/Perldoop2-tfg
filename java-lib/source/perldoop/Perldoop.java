/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package perldoop;

import java.io.IOException;

/**
 *
 * @author César
 */
public class Perldoop {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {

    }
    private class Text{

        private Text(String valueOf) {
            throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
        }
        public String get(){
            return null;
        }
    }
    
        private class Context{
        public void write(Text pd_key,Text pd_key2){
           
        }
    }
    

    public void reduce(Text pd_key, Iterable<Text> pd_value, Context pd_context) throws IOException, InterruptedException{
        String value = null;
        Integer count = 0;
        String oldkey = null;
        oldkey = pd_key.get();
        for(Text pd_i : pd_value){
            value = pd_i.get();
            count = (int)(count + Double.parseDouble(value));
        }
        pd_context.write(new Text(oldkey), new Text(String.valueOf(count)));
    }

}
