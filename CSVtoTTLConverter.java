import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class CSVtoTTLConverter {

    public static void main(String[] args) {
        String csvFile = "movies.csv"; // Path to the CSV file
        String ttlFile = "movies.ttl"; // Path to the TTL output file

        convertCSVtoTTL(csvFile, ttlFile);
    }

    public static void convertCSVtoTTL(String csvFilePath, String ttlFilePath) {
        try (BufferedReader br = new BufferedReader(new FileReader(csvFilePath));
             FileWriter fw = new FileWriter(ttlFilePath)) {
            String line;
            boolean isFirstLine = true;

            while ((line = br.readLine()) != null) {
                if (isFirstLine) {
                    isFirstLine = false;
                    continue; // Skip the header line
                }

                String[] data = line.split(",");

                String title = data[0];
                String year = data[1];
                String director = data[2];
                String genre = data[3];
                String rating = data[4];

                String ttlTriple = generateTTLTriple(title, year, director, genre, rating);
                fw.write(ttlTriple);
            }

            System.out.println("Conversion completed successfully.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String generateTTLTriple(String title, String year, String director, String genre, String rating) {
        StringBuilder ttlTriple = new StringBuilder();

        ttlTriple.append("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n");
        ttlTriple.append("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n");
        ttlTriple.append("@prefix ex: <http://example.com/movies#> .\n\n");

        ttlTriple.append("ex:").append(title.replaceAll("\\s+", ""))
                .append(" rdf:type ex:Movie ;\n")
                .append("    ex:title \"").append(title).append("\" ;\n")
                .append("    ex:year \"").append(year).append("\" ;\n")
                .append("    ex:director \"").append(director).append("\" ;\n")
                .append("    ex:genre \"").append(genre).append("\" ;\n")
                .append("    ex:rating \"").append(rating).append("\" .\n\n");

        return ttlTriple.toString();
    }
}
