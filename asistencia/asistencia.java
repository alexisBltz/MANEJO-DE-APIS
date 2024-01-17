import javax.swing.*;
import java.util.*;

public class asistencia {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] lista = { "ALARCON AGUILAR", "ALVARO QUISPE", "ANDRES APAZA", "BARREDA BEJARANO", "BLANCO CAHUANA", "CARDENAS AGUILAR", "CARRIZALES VERA", "CAYLLAHUA SOLIS", "CAYO MAMANI", "CCOMPI LACUAÑA", "CCONISLLA FERNANDEZ", "CCONISLLA HANAMPA", "CHECASACA DIAZ", "CHUCO TACO", "CHUTA LLANQUI", "CONDORI HUARACA", "CUYO KANA", "DÁVILA LAZO", "FLORES CONDE", "GUTIERREZ CARBAJAL", "HUARACA TICLLAHUANACO", "HUAYNILLO COAQUIRA", "HUERTA ACOSTA", "LAZARTE CASTILLO", "LEADBE YUCRA", "LLAMOCCA CHOQUE", "LUPO NUÑONCCA", "MACHACA APAZA", "MAMANI HUAHUACHAMPI", "MANGO LUJAN", "MONTES CHACONDORI", "NINA QUICA", "ORDOÑEZ VALENCIA", "PACOMPIA COARI", "PACURI GOMEZ", "PADILLA CAMPANO", "PERALTA HUANACO", "QUISPE CRUZ", "QUISPE HACHA", "RAFAEL RAMOS", "ROSAS COAQUIRA", "TICONA CASTILLO", "USCAMAYTA QUISPE", "VALERIANO PUMA", "VALERIANO RIVEROS"};


        while (true) {
            System.out.println("Ingrese los nombres de los alumnos (ingrese 'fin' para terminar):");
            List<String> alumnos = new ArrayList<>();
            //AÑADE AL ARRAYLIST LOS NOMBRES

            String nombre;
            while (true) {
                nombre = sc.nextLine().toUpperCase();
                if (nombre.equalsIgnoreCase("fin")) {
                    break;
                }
                alumnos.add(nombre);
            }
            //-------
            List<String> surnames = new ArrayList<>();
            for(int i=0; i<alumnos.size(); i++) {
                surnames.add(obtenerApellido(alumnos.get(i)));
            }

            System.out.println("Asistencia:");
            System.out.println("");
            int i=0;
            for (String nombreLista : lista) {
                //System.out.print("PRUEBA::");
                //System.out.println(nombreLista);
                //System.out.println(surnames);
                if (!surnames.contains(nombreLista)) {
                    System.out.println("F");
                    continue;
                }
                //System.out.println("hola");
                int duracionTotal = calcularDuracionTotal(alumnos, nombreLista)*60;
                if (duracionTotal >= 360) {
                    //System.out.println("------------------------------------------");
                    System.out.println("A");
                } else {
                    System.out.println("F");
                    i++;
                }
            }
        }
    }

    private static int calcularDuracionTotal(List<String> alumnos, String nombre) {
        for (String alumno : alumnos) {
            if (alumno.contains(nombre)) {
                String[] partes = alumno.split("\\s+|\\t+");
                if (partes.length >= 3) {
                    return Integer.parseInt(partes[2]); // Cambiado el índice
                }
            }
        }
        return 0;
    }

    private static String obtenerApellido(String nombre) {
        // Obtiene el apellido desde la cadena de entrada
        String[] partes = nombre.split("\\s+");
        //System.out.println(partes[0]);
        //System.out.println(partes[1]);

        if (partes.length >= 2) {
            return partes[0] +" " +partes[1];
        }
        return "";
    }
}