# **FastAPI Based Image search API 🔎💻**

This project was an improvement on a previous project on comparing images from a user input with images in a database. 
The improvement was focused on making the whole process faster and more efficient. 
This was done by extracting the embeddings of product images using ResNet50 and storing it in a vector database. .

### _To use this API, copy and run this code in your terminal_
```python
git clone https://github.com/emmanuelani/similarity_search

docker build -t my-app .
```

The above code will build a docker image which you can now run on your system.

The app takes in an image, processes it and pass it to the model which then predcits the image category.
