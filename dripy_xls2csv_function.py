from google.cloud import storage
import pandas as pd
import tempfile


def convert_xlsx_to_csv(event, context):
  """Reads a XLSX file from Cloud Storage and writes each sheet as a CSV file to the same bucket.

  Args:
    bucket_name: The name of the Cloud Storage bucket containing the XLSX file.
    filename: The name of the XLSX file in the bucket.
  """

  # Get the bucket and filename from the event
  bucket_name = event["bucket"]
  filename = event["name"]

  # Create a storage client
  client = storage.Client()

  # Get the bucket object
  bucket = client.bucket(bucket_name)

  # Download the file as a stream
  blob = bucket.blob(filename)
  data = blob.download_as_string()  # This line stays the same

  # Read the XLSX file into a Pandas DataFrame using a temporary file
  with tempfile.TemporaryFile() as tmpfile:
    tmpfile.write(data)
    tmpfile.seek(0)
    df = pd.read_excel(tmpfile, sheet_name=None)  # Read all sheets into a dictionary

  # Loop through each sheet and write to a separate CSV file in the bucket
  for sheet_name, sheet_data in df.items():
    output_filename = f"{filename}_{sheet_name}.csv"
    output_blob = bucket.blob(output_filename)
    output_blob.upload_from_string(sheet_data.to_csv(index=False), content_type="text/csv")

  print(f"Converted XLSX file '{filename}' to separate CSV files for each sheet in bucket '{bucket_name}'.")


# Replace with your bucket name and filename
#bucket_name = "partarch-notebooks-dripy"
#filename = "your_file.xlsx"

convert_xlsx_to_csv(bucket_name, filename)

