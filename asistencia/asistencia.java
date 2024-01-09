import java.util.*;

public class asistencia {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] lista = { "ALARCON AGUILAR", "ALVARO QUISPE", "ANDRES APAZA", "BARREDA BEJARANO", "BLANCO CAHUANA", "CARDENAS AGUILAR", "CARRIZALES VERA", "CAYLLAHUA SOLIS", "CAYO MAMANI", "CCOMPI LACUAÑA", "CCONISLLA FERNANDEZ", "CCONISLLA HANAMPA", "CHECASACA DIAZ", "CHUCO TACO", "CHUTA LLANQUI", "CONDORI HUARACA", "CUYO KANA", "DÁVILA LAZO", "FLORES CONDE", "GUTIERREZ CARBAJAL", "HUARACA TICLLAHUANACO", "HUAYNILLO COAQUIRA", "HUERTA ACOSTA", "LAZARTE CASTILLO", "LEADBE YUCRA", "LLAMOCCA CHOQUE", "LUPO NUÑONCCA", "MACHACA APAZA", "MAMANI HUAHUACHAMPI", "MANGO LUJAN", "MONTES CHACONDORI", "NINA QUICA", "ORDOÑEZ VALENCIA", "PACOMPIA COARI", "PACURI GOMEZ", "PADILLA CAMPANO", "PERALTA HUANACO", "QUISPE CRUZ", "QUISPE HACHA", "RAFAEL RAMOS", "ROSAS COAQUIRA", "TICONA CASTILLO", "USCAMAYTA QUISPE", "VALERIANO PUMA", "VALERIANO RIVEROS"};
        while(true){
            System.out.println("Ingrese los apellidos de los alumnos (ingrese 'fin' para terminar):");
            List<String> alumnos = new ArrayList<>();

            String apellido;
            while (true) {
                apellido = sc.nextLine().toUpperCase();
                if (apellido.equalsIgnoreCase("fin")) {
                    break;
                }
                alumnos.add(apellido);
            }
            System.out.println(alumnos);
            System.out.println("Apellidos no encontrados en la lista:");
            System.out.println("");
            System.out.println(" ");
            for (String apellidoLista : lista) {

                if (!alumnos.contains(apellidoLista)) {
                    //System.out.println(apellidoLista);
                    System.out.println("F");
                    continue;
                }
                System.out.println("A");
            }
        }
    }
}