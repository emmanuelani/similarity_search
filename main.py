from fastapi import FastAPI
from io import BytesIO

app = FastAPI(
    title="Visual Search API-1",
    description="This is the API that will be used for bloomzon visual search feature",
)

@app.on_event("startup")
def startup():
    print("Application starting!")

@app.post("/image_match/")
async def predict(file: UploadFile = File(...)):
    # # Check the file type
    if file.content_type not in ["image/jpeg", "image/png"]:
        return {"error": "Invalid file type. Please upload a JPEG or PNG image."}
    try:
        # Read and process the image
        content = await file.read()
        # image = Image.open(io.BytesIO(contents))
        # image = image.convert("RGB")

        image = Image.open(BytesIO(content)).convert("RGB")
        image = transform(image).unsqueeze(0)  # Add batch dimension
        
        # Extract features
        with torch.no_grad():
            input_embedding = resnet50(image).squeeze().numpy()  # Remove extra dimensions
        
        # fetching the embeddings from the database
        async with AsyncSessionLocal() as db:
            prod_embeddings = await db.execute(text("SELECT embeddings FROM products"))
            cosines = []
            for embedding in prod_embeddings:
                # using cosine similarity
                cosine = F.cosine_similarity(
                    input_embeddings.unsqueeze(0), embedding.unsqueeze(0)
                )

                cosine = round(cosine, 2)
                cosines.append(cosine)






        return embedding

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7000, reload=True)
