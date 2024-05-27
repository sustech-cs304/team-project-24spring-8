from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from jose import jwt, JWTError
from typing import List
from datetime import datetime, timedelta

DATABASE_URL = "sqlite:///./test.db"
SECRET_KEY = "YOUR_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    posts = relationship("Post", back_populates="owner")
    notifications = relationship("Notification", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="posts")

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    created_at = Column(String)  # Ensure this line exists
    sender = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="notifications")

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class UserCreate(BaseModel):
    username: str
    email: str
    full_name: str
    hashed_password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    full_name: str

class UserLogin(BaseModel):
    username: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str

class PostRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int

class PasswordUpdate(BaseModel):
    password: str

# 定义 Pydantic 模型
class NotificationCreate(BaseModel):
    message: str
    sender: str

class NotificationRead(BaseModel):
    id: int
    message: str
    created_at: str
    sender: str
    owner_id: int

    class Config:
        orm_mode = True

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid user ID")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")



@app.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if user:
        print(f"Stored username: {user.username}")
        print(f"Stored password: {user.hashed_password}")
    
    if not user or user.hashed_password != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id}


@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    # Adding users
    test_users = [
        {"username": "user1", "email": "user1@example.com", "full_name": "User One", "hashed_password": "hashedpassword1"},
        {"username": "user2", "email": "user2@example.com", "full_name": "User Two", "hashed_password": "hashedpassword2"},
        {"username": "user3", "email": "user3@example.com", "full_name": "User Three", "hashed_password": "hashedpassword3"}
    ]
    for user_data in test_users:
        user = db.query(User).filter(User.username == user_data['username']).first()
        if not user:
            db_user = User(**user_data)
            db.add(db_user)
    db.commit()
    
    # Assuming user1 exists, let's add some posts for user1
    user1 = db.query(User).filter(User.username == "user1").first()
    if user1:
        test_posts = [
            {"title": "探讨最近的机器学习讲座", "content": "非常有见地的讲座，有很多启发性的内容。", "owner_id": user1.id},
            {"title": "人工智能与未来社会的讲座回顾", "content": "详细回顾了AI的发展历史及其对未来社会的影响。", "owner_id": user1.id},
            {"title": "大数据技术的前景和挑战", "content": "探讨了大数据技术面临的主要挑战及其解决方案。", "owner_id": user1.id}
        ]
        for post_data in test_posts:
            post = db.query(Post).filter(Post.title == post_data['title']).first()
            if not post:
                db_post = Post(**post_data)
                db.add(db_post)
        db.commit()
        # 给user1填充Notification 表
        notificationsList = [
            {"message": "你有一个新的讨论回复", "created_at": "2023-04-01T12:00:00Z", "sender": "系统通知", "owner_id": user1.id},
            {"message": "活动报名开始了", "created_at": "2023-04-02T12:00:00Z", "sender": "系统通知", "owner_id": user1.id},
            {"message": "新的评论在你的帖子上", "created_at": "2023-04-03T12:00:00Z", "sender": "user2", "owner_id": user1.id}
        ]
        for notification_data in notificationsList:
            notification = db.query(Notification).filter(Notification.message == notification_data['message']).first()
            if not notification:
                db_notification = Notification(**notification_data)
                db.add(db_notification)
        db.commit()
    db.close()

@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, full_name=user.full_name, hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user.username
    db_user.email = user.email
    db_user.full_name = user.full_name
    db_user.hashed_password = user.hashed_password
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/users/{user_id}/password", response_model=UserRead)
def update_password(user_id: int, password_update: PasswordUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    
    print(type(user_id))
    print(type(current_user_id))
    print(user_id != current_user_id)
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.hashed_password = password_update.password
    print(db_user.hashed_password)
    print(password_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

@app.post("/posts/", response_model=PostRead)
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_post = Post(title=post.title, content=post.content, owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[PostRead])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(Post).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostRead)
def read_post(post_id: int, db: Session = Depends(get_db)):
    print(f"Fetching post with ID: {post_id}")  # Log the ID being requested
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        print(f"Post found: {db_post.title}")  # Log details of the found post
    else:
        print("Post not found")  # Log if the post is not found
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@app.post("/notifications/", response_model=NotificationRead)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    print(f"Creating notification for user_id: {user_id}, message: {notification.message}, sender: {notification.sender}")
    db_notification = Notification(
        message=notification.message,
        sender=notification.sender,
        owner_id=user_id,
        created_at=datetime.utcnow().isoformat()
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    print(f"Notification created with ID: {db_notification.id}")
    return db_notification

class NotificationsResponse(BaseModel):
    count: int
    notifications: List[NotificationRead]

@app.get("/notifications/", response_model=NotificationsResponse)  # 修改这里使用新的响应模型
def read_notifications(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    print(f"Fetching notifications for user_id: {user_id}")
    notifications = db.query(Notification).filter(Notification.owner_id == user_id).all()
    print(f"Fetched {len(notifications)} notifications")
    return NotificationsResponse(
        count=len(notifications),
        notifications=[NotificationRead.from_orm(notification) for notification in notifications]
    )

@app.get("/notifications/{notification_id}", response_model=NotificationRead)
def read_notification(notification_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    print(f"Fetching notification with ID: {notification_id} for user_id: {user_id}")
    db_notification = db.query(Notification).filter(Notification.id == notification_id, Notification.owner_id == user_id).first()
    if db_notification is None:
        print(f"Notification with ID: {notification_id} not found")
        raise HTTPException(status_code=404, detail="Notification not found")
    print(f"Notification with ID: {notification_id} found")
    return NotificationRead.from_orm(db_notification)
