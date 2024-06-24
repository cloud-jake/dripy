from google.cloud import storage
import pandas as pd


def convert_xlsx_to_csv(bucket_name, filename):
  """Reads a XLSX file from Cloud Storage and writes each sheet as a CSV file.

  Args:
    bucket_name: The name of the Cloud Storage bucket containing the XLSX file.
    filename: The name of the XLSX file in the bucket.
  """
  # Create a storage client
  client = storage.Client()

  # Get the bucket and blob objects
  bucket = client.bucket(bucket_name)
  blob = bucket.blob(filename)

  # Download the file content
  data = blob.download_as_string()

  # Read the XLSX file into a Pandas DataFrame
  df = pd.read_excel(data, memory=True)

  # Loop through each sheet and write to a CSV file
  for sheet_name, sheet_data in df.items():
    output_filename = f"{filename}_{sheet_name}.csv"
    sheet_data.to_csv(output_filename, index=False)
    # Upload the CSV file to Cloud Storage (optional)
    csv_blob = bucket.blob(output_filename)
    csv_blob.upload_from_string(sheet_data.to_csv(index=False), content_type="text/csv")

  print(f"Converted XLSX file '{filename}' to separate CSV files for each sheet.")


# Replace with your bucket name and filename
bucket_name = "partarch-notebooks-dripy"
filename = "your_file.xlsx"

convert_xlsx_to_csv(bucket_name, filename)

