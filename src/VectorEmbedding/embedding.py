# %pip install llama-index-embeddings-huggingface
# %pip install llama-index-embeddings-instructor
# !pip install llama-index

import warnings

# Suppress specific FutureWarnings
warnings.filterwarnings("ignore", category=FutureWarning, module="huggingface_hub")

from llama_index.embeddings.huggingface import HuggingFaceEmbedding


# Assuming the HuggingFaceEmbedding class and methods are correctly defined and imported

# Initialize the embedding model with the desired Hugging Face model
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# List of product descriptions
product_descriptions = [
    "Under colors of Benetton Men White Boxer Trunks",
    "Turtle Men Check Red Shirt",
    "United Colors of Benetton Men White Check Shirt",
    "United Colors of Benetton Men Check White Shirts",
    "Wrangler Men Broad Blue Shirt"
]

# Iterate over each product description
for i, product_desc in enumerate(product_descriptions, start=1):
    # Get embeddings for the current product description
    embeddings = embed_model.get_text_embedding(product_desc)
    
    # Format the embeddings to a specific format, e.g., printing the first 5 elements
    formatted_embeddings = '[' + ', '.join(f"{emb:.16f}" for emb in embeddings[:5]) + ']'
    
    # Prepare and print the output in the specified format
    output = f"{i},{product_desc},{formatted_embeddings}"
    print(output)
