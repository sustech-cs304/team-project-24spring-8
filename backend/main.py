from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./test.db"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 创建会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

# 定义用户模型
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)

# 定义其他模型（例如Item模型）
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 添加测试数据
def add_test_data(db: Session):
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

# 创建 FastAPI 应用
app = FastAPI()

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic 模型
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

@app.on_event("startup")
def startup_event():
    # 启动时添加测试数据
    db = SessionLocal()
    add_test_data(db)
    db.close()

@app.get("/hello")
def read_hello():
    return {"message": "Hello from FastAPI"}

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

@app.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}
