from fastapi import FastAPI, HTTPException, Depends, status, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, joinedload
from pydantic import BaseModel
from jose import jwt, JWTError
from typing import List, Optional
from datetime import datetime, timedelta
import os
import shutil

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
    money = Column(Integer, default=0)
    avatar_path = Column(String, default="avatars/default_avatar.png")
    events = relationship("Event", back_populates="owner")
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    tickets = relationship("Ticket", back_populates="owner")
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
    haven_read = Column(Boolean, default=False)


class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    event_time = Column(DateTime)
    description = Column(String)
    duration_hours = Column(Integer)
    duration_minutes = Column(Integer)
    price = Column(Integer, default=0)
    tickets_sold = Column(Integer, default=0)  # 已售出票数
    max_tickets = Column(Integer)  # 最大票数限制
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="events")
    tickets = relationship("Ticket", back_populates="event")
    comments = relationship("Comment", back_populates="event")  # 添加反向关系


class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    IDcard = Column(String)
    phonenumber = Column(String, index=True)
    number = Column(Integer)
    event_id = Column(Integer, ForeignKey('events.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    event = relationship("Event", back_populates="tickets")  # 添加关系属性
    owner = relationship("User", back_populates="tickets")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    event = relationship("Event", back_populates="comments")
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="comments")

class PostComment(Base):
    __tablename__ = 'post_comments'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="comments")
    owner_id = Column(Integer, ForeignKey('users.id'))
    owner = relationship("User", back_populates="post_comments")

Post.comments = relationship("PostComment", back_populates="post", cascade="all, delete-orphan")
User.post_comments = relationship("PostComment", back_populates="owner", cascade="all, delete-orphan")


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
    money: int


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    avatar_path: str
    money: int


class UserLogin(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    full_name: str
    email: str


class PostCreate(BaseModel):
    title: str
    content: str


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: Optional[int]


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
    haven_read: bool

    class Config:
        orm_mode = True
        from_attributes = True


class TicketRead(BaseModel):
    id: int
    name: str
    IDcard: str
    phonenumber: str
    number: int
    event_id: int
    event_name: str
    event_time: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class EventCreate(BaseModel):
    name: str
    event_time: datetime
    description: str
    duration_hours: int  # 新增字段
    duration_minutes: int
    price: int
    tickets_sold: int
    max_tickets: int


class EventRead(BaseModel):
    id: int
    name: str
    event_time: datetime
    description: str
    duration_hours: int  # 新增字段
    duration_minutes: int
    price: int
    owner_id: int
    tickets_sold: int
    max_tickets: int

    class Config:
        orm_mode = True


class TicketCreate(BaseModel):
    name: str
    IDcard: int
    phonenumber: int
    number: int


class CommentCreate(BaseModel):
    content: str


class CommentRead(BaseModel):
    id: int
    content: str
    owner_id: int
    event_id: int

class PostCommentCreate(BaseModel):
    content: str

class PostCommentRead(BaseModel):
    id: int
    content: str
    owner_id: int
    post_id: int


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


UPLOAD_DIRECTORY = "avatars"
@app.on_event("startup")
def startup_event():
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    db = SessionLocal()
    # Adding users
    test_users = [
        {"username": "user1", "email": "user1@example.com", "full_name": "User One",
         "hashed_password": "1", "avatar_path": "avatars/1_avatar.jpg", "money": 200},
        {"username": "user2", "email": "user2@example.com", "full_name": "User Two",
         "hashed_password": "2", "avatar_path": "avatars/2_avatar.jpg", "money": 200},
        {"username": "user3", "email": "user3@example.com", "full_name": "User Three",
         "hashed_password": "3", "avatar_path": "avatars/3_avatar.jpg", "money": 200}
    ]
    for user_data in test_users:
        user = db.query(User).filter(User.username == user_data['username']).first()
        if not user:
            db_user = User(**user_data)
            db.add(db_user)
    db.commit()

    # Assuming user1 exists, let's add some posts for user1
    user1 = db.query(User).filter(User.username == "user1").first()
    user2 = db.query(User).filter(User.username == "user2").first()
    user3 = db.query(User).filter(User.username == "user3").first()
    if user1:
        test_posts = [
            {"title": "探讨最近的机器学习讲座", "content": "非常有见地的讲座，有很多启发性的内容。",
             "owner_id": user1.id},
            {"title": "人工智能与未来社会的讲座回顾", "content": "详细回顾了AI的发展历史及其对未来社会的影响。",
             "owner_id": user1.id},
            {"title": "原末鸣初？反鸣复原！", "content": "鸣潮:如果原神4.7有炸的话，可能稍微有点麻烦呢。幻塔:会输吗？鸣潮:会赢的。鸣潮:在开战之前，我事先声明一下，原神，你才是挑战者!原神:你只不过是生在没有我的时代的凡夫罢了。幻塔:怎么样？鸣潮:原神超——强的，这些年积蓄的力量，买来的风向，自己的技术力，已经毫无保留地展现出来，没能让原神大人使出全力，我很抱歉。绝对的强者，由此而生的孤独，教会你爱的是…原神:令人愉悦，鸣潮，我大概一生都不会忘记你吧。一刻都没有为鸣潮的死亡哀悼，立即奔赴战场的是——蓝色星源，王者荣耀世界(新建文件夹)，无限大(新建文件夹)!原神:希望你能让我尽兴，可不要让我失望。", "owner_id": user1.id}
        ]
        for post_data in test_posts:
            post = db.query(Post).filter(Post.title == post_data['title']).first()
            if not post:
                db_post = Post(**post_data)
                db.add(db_post)
        db.commit()

        # Adding comments for posts
        test_post_comments = [
            {"content": "非常有见地的讲座，有很多启发性的内容。", "owner_id": user1.id, "post_id": 1},
            {"content": "详细回顾了AI的发展历史及其对未来社会的影响。", "owner_id": user2.id, "post_id": 1},
            {"content": "探讨了大数据技术面临的主要挑战及其解决方案。", "owner_id": user1.id, "post_id": 2},
            {"content": "讲座内容非常丰富，涵盖了很多前沿的技术话题。", "owner_id": user3.id, "post_id": 1},
            {"content": "AI技术的发展速度令人惊叹，未来会有更多的应用场景。", "owner_id": user3.id, "post_id": 2}
        ]
        for post_comment_data in test_post_comments:
            post_comment = db.query(PostComment).filter(PostComment.content == post_comment_data['content']).first()
            if not post_comment:
                db_post_comment = PostComment(**post_comment_data)
                db.add(db_post_comment)
        db.commit()

        test_comments = [
            {"content": "非常有见地的讲座，有很多启发性的内容。", "owner_id": user1.id, "event_id": 1},
            {"content": "详细回顾了AI的发展历史及其对未来社会的影响。", "owner_id": user1.id, "event_id": 1},
            {"content": "探讨了大数据技术面临的主要挑战及其解决方案。", "owner_id": user1.id, "event_id": 2}
        ]
        for comment_data in test_comments:
            comment = db.query(Comment).filter(Comment.content == comment_data['content']).first()
            if not comment:
                db_comment = Comment(**comment_data)
                db.add(db_comment)
        db.commit()

        # Adding notifications for user1
        notificationsList = [
            {"message": "你有一个新的讨论回复", "created_at": "2023-04-01T12:00:00Z", "sender": "系统通知",
             "owner_id": user1.id, "haven_read": False},
            {"message": "活动报名开始了", "created_at": "2023-04-02T12:00:00Z", "sender": "系统通知",
             "owner_id": user1.id, "haven_read": False},
            {"message": "新的评论在你的帖子上", "created_at": "2023-04-03T12:00:00Z", "sender": "系统通知",
             "owner_id": user1.id, "haven_read": False}
        ]
        for notification_data in notificationsList:
            notification = db.query(Notification).filter(Notification.message == notification_data['message']).first()
            if not notification:
                db_notification = Notification(**notification_data)
                db.add(db_notification)
        db.commit()

        test_events = [
            {"name": "南科音乐节", "event_time": datetime(2023, 6, 9, 10, 0),
             "description": "享受音乐狂欢",
             "duration_hours": 2, "duration_minutes": 30, "price": 20, "owner_id": user1.id, "max_tickets": 10, "tickets_sold": 9},
            {"name": "科技博览会", "event_time": datetime(2023, 6, 13, 14, 0),
             "description": "近距离接触世界最前沿的科技成果。",
             "duration_hours": 3, "duration_minutes": 20, "price":30, "owner_id": user1.id, "max_tickets": 5, "tickets_sold": 0},
            {"name": "南科足球赛", "event_time": datetime(2023, 6, 8, 8, 0),
             "description": "强强对决，谁与争锋。",
             "duration_hours": 2, "duration_minutes": 10, "price":25, "owner_id": user1.id, "max_tickets": 15, "tickets_sold": 2}
        ]
        print("events_init")
        for event_data in test_events:
            existing_event = db.query(Event).filter(Event.name == event_data['name']).first()
            if existing_event:
                # 如果存在同名事件，则更新已存在事件的属性
                for key, value in event_data.items():
                    setattr(existing_event, key, value)
            else:
                # 如果不存在同名事件，则创建新事件并添加到数据库中
                db_event = Event(**event_data)
                db.add(db_event)

        db.commit()
    if user2:
        test_posts_user2 = [
            {"title": "南科大上空直升机遭受肘击", "content": "man, what can i say", "owner_id": user2.id},
            {"title": "好想玩原神，好像玩原神！", "content": "你说的对，但是《原神》是由米哈游自主研发的一款全新开放世界冒险游戏。\n游戏发生在一个被称作「提瓦特」的幻想世界，在这里，被神选中的人将被授予「神之眼」，导引元素之力。你将扮演一位名为「旅行者」的神秘角色，在自由的旅行中邂逅性格各异、能力独特的同伴们，和他们一起击败强敌，找回失散的亲人——同时，逐步发掘「原神」的真相。..........................................\n这里是七种元素交汇的幻想世界“提瓦特”。在遥远的过去，人们藉由对神灵的信仰，获赐了驱动元素的力量，得以在荒野中筑起家园。五百年前，古国的覆灭却使得天地变异……如今，席卷大陆的灾难已经停息，和平却仍未如期光临。作为故事的主人公，你从世界之外漂流而来，降临大地。你将在这广阔的世界中，自由旅行、结识同伴、寻找掌控尘世元素的七神，直到与分离的血亲重聚 。", "owner_id": user2.id},
            {"title": "致仁书院的科研成果", "content": "总结了致仁书院在科研方面取得的主要成就。", "owner_id": user2.id}
        ]
        for post_data in test_posts_user2:
            post = db.query(Post).filter(Post.title == post_data['title']).first()
            if not post:
                db_post = Post(**post_data)
                db.add(db_post)
        db.commit()
        test_post_comments_user2 = [
            {"content": "man, what can i say", "owner_id": user3.id, "post_id": 4},
            {"content": "这篇文章太棒了，详细介绍了《原神》的背景故事和游戏特色。", "owner_id": user2.id, "post_id": 5},
            {"content": "原神的世界设定非常吸引人，尤其是七种元素的设定。", "owner_id": user3.id, "post_id": 5},
            {"content": "致仁书院的科研成果令人印象深刻，期待更多详细的介绍。", "owner_id": user1.id, "post_id": 6},
            {"content": "科研成就展示了致仁书院在学术领域的实力。", "owner_id": user2.id, "post_id": 6},
            {"content": "希望能看到更多关于致仁书院科研项目的具体内容。", "owner_id": user3.id, "post_id": 6},
            {"content": "原神的开放世界探险真是令人期待，角色设计也非常精美。", "owner_id": user1.id, "post_id": 5},
            {"content": "非常精彩的游戏介绍，让我迫不及待想要体验《原神》。", "owner_id": user2.id, "post_id": 5},
            {"content": "man, what can i say", "owner_id": user2.id, "post_id": 4}
        ]
        for post_comment_data in test_post_comments_user2:
            post_comment = db.query(PostComment).filter(PostComment.content == post_comment_data['content']).first()
            if not post_comment:
                db_post_comment = PostComment(**post_comment_data)
                db.add(db_post_comment)
        db.commit()

    if user3:
        test_posts_user3 = [
            {"title": "王大兴老师好帅，收个微信", "content": "如题", "owner_id": user3.id},
            {"title": "致仁书院的创新课程设计", "content": "介绍了致仁书院在课程设计方面的创新举措。", "owner_id": user3.id},
            {"title": "大沙河游泳", "content": "有没有人周末来大沙河一起游泳？很早之前就想游了，一直没找到同伴。", "owner_id": user3.id},
        ]
        for post_data in test_posts_user3:
            post = db.query(Post).filter(Post.title == post_data['title']).first()
            if not post:
                db_post = Post(**post_data)
                db.add(db_post)
        test_post_comments_user3 = [
            {"content": "如题", "owner_id": user3.id, "post_id": 7},
            {"content": "创新课程设计能够激发学生的创造力和学习兴趣。", "owner_id": user1.id, "post_id": 8},
            {"content": "致仁书院的课程设计确实非常有新意，值得学习。", "owner_id": user3.id, "post_id": 8},
            {"content": "大沙河游泳活动听起来很有趣，期待一起参加。", "owner_id": user3.id, "post_id": 9},
            {"content": "周末正好有空，可以一起去大沙河游泳。", "owner_id": user2.id, "post_id": 9},
            {"content": "王大兴老师确实很帅，能不能加个微信？", "owner_id": user2.id, "post_id": 7},
            {"content": "课程设计的创新举措非常重要，能够提升教学质量。", "owner_id": user2.id, "post_id": 8},
            {"content": "致仁书院的课程设计理念非常先进，期待更多介绍。", "owner_id": user3.id, "post_id": 8},
            {"content": "有没有其他人也想去大沙河游泳的？一起来吧！", "owner_id": user1.id, "post_id": 9}
        ]
        for post_comment_data in test_post_comments_user3:
            post_comment = db.query(PostComment).filter(PostComment.content == post_comment_data['content']).first()
            if not post_comment:
                db_post_comment = PostComment(**post_comment_data)
                db.add(db_post_comment)
        db.commit()

    db.close()


@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, full_name=user.full_name,
                   hashed_password=user.hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(db_user.avatar_path)
    return db_user


@app.put("/users/{user_id}/profile", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.full_name = user.full_name
    db_user.email = user.email
    db.commit()
    db.refresh(db_user)
    return db_user



app.mount("/avatars", StaticFiles(directory=UPLOAD_DIRECTORY), name="avatars")
@app.post("/upload-avatar/{user_id}", response_model=UserRead)
async def upload_avatar(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    print("upload_avatar")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    file_location = f"{UPLOAD_DIRECTORY}/{user_id}_{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    user.avatar_path = f"avatars/{user_id}_{file.filename}"  # 更新用户头像路径
    db.commit()
    db.refresh(user)
    return user


@app.post("/events/", response_model=EventRead)
def create_event(event: EventCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_event = Event(
        name=event.name,
        event_time=event.event_time,
        description=event.description,
        duration_hours=event.duration_hours,
        duration_minutes=event.duration_minutes,
        price=event.price,
        tickets_sold=event.tickets_sold,
        max_tickets=event.max_tickets,
        owner_id=user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event



@app.get("/events/", response_model=List[EventRead])
def read_events(skip: int = 0, limit: int = 10, search: str = None, db: Session = Depends(get_db)):
    print("read_events")
    query = db.query(Event)
    if search:
        query = query.filter(Event.name.contains(search))
    events = query.offset(skip).limit(limit).all()

    for event in events:
        print(
            f"Event ID: {event.id}, Duration: {event.duration_hours} hours and {event.duration_minutes} minutes")  # 调试语句

    return events


@app.get("/events/{event_id}", response_model=EventRead)
def read_event(event_id: int, db: Session = Depends(get_db)):
    print("read_event")
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event


@app.put("/events/{event_id}", response_model=EventRead)
def update_event(event_id: int, event: EventCreate, db: Session = Depends(get_db),
                 user_id: int = Depends(get_current_user_id)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")

    db_event.name = event.name
    db_event.event_time = event.event_time
    db_event.description = event.description
    db_event.duration_hours = event.duration_hours
    db_event.duration_minutes = event.duration_minutes
    db_event.price = event.price
    db_event.tickets_sold = event.tickets_sold
    db_event.max_tickets = event.max_tickets

    db.commit()
    db.refresh(db_event)
    return db_event


@app.delete("/events/{event_id}", response_model=dict)
def delete_event(event_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    print("delete_event")
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.owner_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted"}


@app.post("/tickets/{event_id}", response_model=dict)
def create_ticket(event_id: int, ticket: TicketCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    # 确认事件ID是否有效
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    # 检查是否还有剩余票数
    if event.tickets_sold >= event.max_tickets:
        raise HTTPException(status_code=400, detail="Tickets are sold out for this event")

    # 获取当前用户信息
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 计算购票总金额
    total_cost = event.price * ticket.number

    # 检查用户余额是否足够支付购票费用
    if user.money < total_cost:
        raise HTTPException(status_code=400, detail="资金无法支付票价")

    # 创建票务记录的逻辑
    new_ticket = Ticket(event_id=event_id, owner_id=user_id, number=ticket.number, name=ticket.name,
                        IDcard=ticket.IDcard, phonenumber=ticket.phonenumber)
    db.add(new_ticket)

    # 更新已售出票数和用户余额
    event.tickets_sold += ticket.number
    user.money -= total_cost

    db.commit()
    db.refresh(new_ticket)

    return {"message": "Ticket created successfully"}



@app.get("/events/{event_id}/event_name")
def get_event_details(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    event_name = event.name
    print(f'event_name: {event_name}')
    return {
        "event_name": event_name,
    }


@app.get("/events/{event_id}/tickets_left")
def get_tickets_left(event_id: int, db: Session = Depends(get_db)):
    print(event_id)
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    tickets_left = event.max_tickets - event.tickets_sold
    return {"tickets_left": tickets_left}


@app.get("/users/{user_id}/tickets", response_model=List[TicketRead])
def read_user_tickets(user_id: int, db: Session = Depends(get_db), current_user_id: int = Depends(get_current_user_id)):
    # Check if the user ID matches the current logged-in user
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Operation not permitted")

    tickets = db.query(Ticket).filter(Ticket.owner_id == user_id).options(joinedload(Ticket.event)).all()
    result = []
    for ticket in tickets:
        result.append(TicketRead(
            id=ticket.id,
            name=ticket.name,
            IDcard=ticket.IDcard,
            phonenumber=ticket.phonenumber,
            number=ticket.number,
            event_id=ticket.event_id,
            event_name=ticket.event.name,
            event_time=ticket.event.event_time,
        ))
    return result



@app.put("/users/{user_id}/password", response_model=UserRead)
def update_password(user_id: int, password_update: PasswordUpdate, db: Session = Depends(get_db),
                    current_user_id: int = Depends(get_current_user_id)):
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

@app.post("/comments/{event_id}", response_model=CommentRead)
def create_comment(event_id: int,comment: CommentCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_comment = Comment( content=comment.content, owner_id=user_id,event_id=event_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
@app.get("/comments/{event_id}", response_model=List[CommentRead])
def read_comments(event_id: int,db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.event_id == event_id).all()
    return comments

# @app.get("/comments/{comment_id}", response_model=CommentRead)
# def read_comment(comment_id: int, db: Session = Depends(get_db)):
#     print(f"Fetching comment with ID: {comment_id}")  # Log the ID being requested
#     db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
#     if db_comment:
#         print(f"Comment found: {db_comment.content}")  # Log details of the found post
#     else:
#         print("Comment not found")  # Log if the post is not found
#         raise HTTPException(status_code=404, detail="Comment not found")
#     return db_comment

@app.post("/post_comments/{post_id}", response_model=PostCommentRead)
def create_post_comment(post_id: int, comment: PostCommentCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    db_comment = PostComment(content=comment.content, owner_id=user_id, post_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@app.get("/post_comments/{post_id}", response_model=List[PostCommentRead])
def read_post_comments(post_id: int, db: Session = Depends(get_db)):
    comments = db.query(PostComment).filter(PostComment.post_id == post_id).all()
    return comments


@app.post("/notifications/", response_model=NotificationRead)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db),
                        user_id: int = Depends(get_current_user_id)):
    print(
        f"Creating notification for user_id: {user_id}, message: {notification.message}, sender: {notification.sender}")
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
    notifications = db.query(Notification).filter(Notification.owner_id == user_id).order_by(Notification.created_at.desc()).all()
    print(f"Fetched {len(notifications)} notifications")
    return NotificationsResponse(
        count=len(notifications),
        notifications=[NotificationRead.from_orm(notification) for notification in notifications]
    )


@app.get("/notifications/{notification_id}", response_model=NotificationRead)
def read_notification(notification_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    print(f"Fetching notification with ID: {notification_id} for user_id: {user_id}")
    db_notification = db.query(Notification).filter(Notification.id == notification_id,
                                                    Notification.owner_id == user_id).first()
    if db_notification is None:
        print(f"Notification with ID: {notification_id} not found")
        raise HTTPException(status_code=404, detail="Notification not found")
    print(f"Notification with ID: {notification_id} found")
    return NotificationRead.from_orm(db_notification)

@app.put("/notifications/mark_all_read")
def mark_all_notifications_read(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    print(f"Marking all notifications as read for user_id: {user_id}")
    db.query(Notification).filter(Notification.owner_id == user_id).update({"haven_read": True})
    db.commit()
    print(f"All notifications marked as read for user_id: {user_id}")
    return {"detail": "All notifications marked as read"}
