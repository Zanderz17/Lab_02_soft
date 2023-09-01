import csv

with open('spotify2.csv', 'r', newline='') as input_file, open('modified_canciones.csv', 'w', newline='') as output_file:
    csv_reader = csv.reader(input_file)
    csv_writer = csv.writer(output_file)

    for row in csv_reader:
        # Modificar el formato del arreglo en la columna "artists"
        row[2] = row[2].replace('[', '{').replace(']', '}')

        # Escribir la fila modificada en el nuevo archivo CSV
        csv_writer.writerow(row)