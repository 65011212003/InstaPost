from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class PostCreate(BaseModel):
    image_url: str
    caption: str

class Comment(BaseModel):
    id: int
    post_id: int
    content: str
    created_at: datetime

class Post(PostCreate):
    id: int
    created_at: datetime
    likes: int = 0
    comments: List[Comment] = []

# In-memory list to store posts
posts = []

@app.get("/api/posts")
def read_posts() -> List[Post]:
    return posts

@app.post("/api/posts")
def create_post(post: PostCreate) -> Post:
    new_post = Post(
        id=len(posts) + 1,
        image_url=post.image_url,
        caption=post.caption,
        created_at=datetime.now(),
        likes=0,
        comments=[]
    )
    posts.append(new_post)
    return new_post

@app.post("/api/posts/{post_id}/like")
def like_post(post_id: int) -> Post:
    post = next((p for p in posts if p.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    post.likes += 1
    return post

class CommentCreate(BaseModel):
    content: str

@app.post("/api/posts/{post_id}/comment")
def add_comment(post_id: int, comment: CommentCreate) -> Post:
    post = next((p for p in posts if p.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    new_comment = Comment(
        id=len(post.comments) + 1,
        post_id=post_id,
        content=comment.content,
        created_at=datetime.now()
    )
    post.comments.append(new_comment)
    return post

@app.on_event("startup")
async def startup_event():
    # Add sample posts
    posts.append(Post(
        id=1,
        image_url="https://buffer.com/cdn-cgi/image/w=1000,fit=contain,q=90,f=auto/library/content/images/size/w1200/2023/10/free-images.jpg",
        caption="Sample post 1",
        created_at=datetime.now(),
        likes=0,
        comments=[]
    ))
    posts.append(Post(
        id=2,
        image_url="https://buffer.com/cdn-cgi/image/w=1000,fit=contain,q=90,f=auto/library/content/images/size/w1200/2023/10/free-images.jpg",
        caption="Sample post 2",
        created_at=datetime.now(),
        likes=0,
        comments=[]
    ))