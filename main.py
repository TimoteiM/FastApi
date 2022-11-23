from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from flask import jsonify

app = FastAPI()

class Post(BaseModel):
    title : str
    content : str
    published: bool = True
    rating: Optional[float] = None

my_posts = []

@app.get("/")
def root():
    return {"message" : "Welcome to my page!"}

@app.get("/posts")
def get_posts():
    return {'data': my_posts}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def get_indexPost(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
            i = len(my_posts)
        else:
            return (-1)

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.dict()
    id = randrange(0, 5)
    post_dict['id'] = id
    my_posts.append(post_dict)
    return {'new_post': post_dict}

@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail" : post}

@app.get("/posts/{id}")
def get_one_post(id : int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail" : post}

@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    index = get_indexPost(id)
    my_posts.pop(index)
    if index == -1:
        raise HTTPException(status_code= status.HTTP_304_NOT_MODIFIED,
                            detail=f"post with id: {id} was not found")
    return {"message" : "post was succesfully deleted"}





print(my_posts)