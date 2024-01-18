import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

public class tourismttl {

    public static void main(String[] args) {
        String csvFile = "tourism_company_data.csv";
        String ttlFile = "tourism_company_data.ttl";
        String namespace = "http://example.com/tourism#";

        try {
            BufferedReader br = new BufferedReader(new FileReader(csvFile));
            BufferedWriter bw = new BufferedWriter(new FileWriter(ttlFile));

            // Write the TTL file header
            bw.write("@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n");
            bw.write("@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n");
            bw.write("@prefix ex: <" + namespace + "> .\n");
            bw.write("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n\n");

            String line;
            boolean isFirstLine = true;

            while ((line = br.readLine()) != null) {
                if (isFirstLine) {
                    isFirstLine = false;
                    continue; // Skip the header line
                }

                String[] data = line.split(",");

                String customerName = data[0];
                String phoneNumber = data[1];
                String place = data[2];
                double rating = Double.parseDouble(data[3]);
                int duration = Integer.parseInt(data[4]);
                int budget = Integer.parseInt(data[5]);
                String guideName = data[6];

                // Write the TTL triples
                bw.write("ex:" + customerName.replaceAll("\\s+", "") + " rdf:type ex:Trip ;\n");
                bw.write("    ex:customerName \"" + customerName + "\" ;\n");
                bw.write("    ex:phoneNumber \"" + phoneNumber + "\" ;\n");
                bw.write("    ex:place \"" + place + "\" ;\n");
                bw.write("    ex:rating " + rating + " ;\n");
                bw.write("    ex:duration " + duration + " ;\n");
                bw.write("    ex:budget " + budget + " ;\n");
                bw.write("    ex:guideName \"" + guideName + "\" .\n\n");
            }

            br.close();
            bw.close();

            System.out.println("Conversion completed successfully.");

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
