from sentence_transformers import SentenceTransformer
from model import model_path
# Step 1: Load the SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 2: Serialize (save) the model
model.save(model_path)

