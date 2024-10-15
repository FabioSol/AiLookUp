"""import pandas as pd
from datasets import load_dataset

# Load the dataset
ds = load_dataset("booksouls/goodreads-book-descriptions")

# Convert the dataset to a pandas DataFrame
df = ds['train'].to_pandas().head(100)

# Save the DataFrame as a CSV file
df.to_csv('goodreads_book_descriptions.csv', index=False)
print(df)"""


import pandas as pd
df = pd.read_csv('goodreads_book_descriptions.csv')
from db.controller import FileController
import os

f = FileController.new(os.path.join('goodreads_book_descriptions.csv'),['title','description'])
f.save()