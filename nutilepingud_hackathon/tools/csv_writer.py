import csv


# Specify the CSV file path
csv_file_path = 'output.csv'


def write_to_csv(data, filename):
    if not data:
        print("Data is empty. Nothing to write.")
        return

    # Determine field names dynamically from the keys of the first dictionary in the data
    field_names = list(data[0].keys())

    with open(filename, 'w', newline='') as csvfile:
        # Define the CSV field names based on the keys in your dictionary

        # Create a CSV writer object
        csv_writer = csv.DictWriter(csvfile, fieldnames=field_names)

        # Write the header row
        csv_writer.writeheader()

        # Write the data rows
        csv_writer.writerows(data)