from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SQLite database
DATABASE_URL = "sqlite:///./getyourseat.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Backend working 🚀"}

# ---------------- SIGNUP ----------------
@app.post("/signup")
def signup(user: dict):
    db = SessionLocal()

    existing = db.query(User).filter(User.username == user["username"]).first()
    if existing:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        name=user["name"],
        username=user["username"],
        password=user["password"]
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {"message": "User created successfully"}

# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: dict):
    db = SessionLocal()

    db_user = db.query(User).filter(User.username == user["username"]).first()

    if not db_user:
        db.close()
        raise HTTPException(status_code=400, detail="User not found")

    if db_user.password != user["password"]:
        db.close()
        raise HTTPException(status_code=400, detail="Incorrect password")

    db.close()

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "username": db_user.username
    }