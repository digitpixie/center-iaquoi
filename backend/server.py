import os
import asyncio
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Outils Interactifs Platform", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(MONGO_URL)
db = client.outils_interactifs

# Collections
users_collection = db.users
tools_collection = db.tools
pet_states_collection = db.pet_states

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class ToolCreate(BaseModel):
    title: str
    description: str
    category: str
    html_content: str
    preview_image: Optional[str] = None

class Tool(BaseModel):
    id: str
    title: str
    description: str
    category: str
    html_content: str
    preview_image: Optional[str] = None
    user_id: str
    created_at: datetime
    updated_at: datetime

class PetStateCreate(BaseModel):
    name: str = "PIXEL-IA"
    level: int = 1
    happiness: int = 80
    knowledge: int = 60
    energy: int = 75
    hunger: int = 70
    stage: str = "baby"
    modules_completed: int = 0
    mood: str = "happy"

class PetState(BaseModel):
    id: str
    user_id: str
    name: str
    level: int
    happiness: int
    knowledge: int
    energy: int
    hunger: int
    stage: str
    modules_completed: int
    mood: str
    created_at: datetime
    updated_at: datetime

class SkoolModuleCreate(BaseModel):
    title: str
    description: str
    skool_module_id: str
    completion_code: str
    reward_points: int = 30
    required_for_evolution: bool = True

class SkoolModule(BaseModel):
    id: str
    title: str
    description: str
    skool_module_id: str
    completion_code: str
    reward_points: int
    required_for_evolution: bool
    created_at: datetime
    updated_at: datetime

class SkoolProgressCreate(BaseModel):
    module_id: str
    completion_code: str
    notes: Optional[str] = None

class SkoolProgress(BaseModel):
    id: str
    user_id: str
    module_id: str
    module_title: str
    completion_code: str
    completed_at: datetime
    notes: Optional[str] = None
    pet_evolution_triggered: bool = False

# Helper functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = await users_collection.find_one({"id": user_id})
    if user is None:
        raise credentials_exception
    return user

# API Routes
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc)}

@app.post("/api/auth/register", response_model=Token)
async def register(user: UserCreate):
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid.uuid4())
    hashed_password = get_password_hash(user.password)
    
    user_doc = {
        "id": user_id,
        "email": user.email,
        "name": user.name,
        "hashed_password": hashed_password,
        "created_at": datetime.now(timezone.utc)
    }
    
    await users_collection.insert_one(user_doc)
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/auth/login", response_model=Token)
async def login(user: UserLogin):
    db_user = await users_collection.find_one({"email": user.email})
    if not db_user or not verify_password(user.password, db_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["id"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=User)
async def get_current_user_info(current_user = Depends(get_current_user)):
    return User(
        id=current_user["id"],
        email=current_user["email"],
        name=current_user["name"],
        created_at=current_user["created_at"]
    )

@app.get("/api/tools", response_model=List[Tool])
async def get_tools(current_user = Depends(get_current_user)):
    tools = []
    cursor = tools_collection.find({"user_id": current_user["id"]}).sort("created_at", -1)
    async for tool in cursor:
        tools.append(Tool(
            id=tool["id"],
            title=tool["title"],
            description=tool["description"],
            category=tool["category"],
            html_content=tool["html_content"],
            preview_image=tool.get("preview_image"),
            user_id=tool["user_id"],
            created_at=tool["created_at"],
            updated_at=tool["updated_at"]
        ))
    return tools

@app.post("/api/tools", response_model=Tool)
async def create_tool(tool: ToolCreate, current_user = Depends(get_current_user)):
    tool_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    
    tool_doc = {
        "id": tool_id,
        "title": tool.title,
        "description": tool.description,
        "category": tool.category,
        "html_content": tool.html_content,
        "preview_image": tool.preview_image,
        "user_id": current_user["id"],
        "created_at": now,
        "updated_at": now
    }
    
    await tools_collection.insert_one(tool_doc)
    
    return Tool(**tool_doc)

@app.get("/api/tools/{tool_id}", response_model=Tool)
async def get_tool(tool_id: str, current_user = Depends(get_current_user)):
    tool = await tools_collection.find_one({
        "id": tool_id,
        "user_id": current_user["id"]
    })
    
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool not found"
        )
    
    return Tool(**tool)

@app.put("/api/tools/{tool_id}", response_model=Tool)
async def update_tool(tool_id: str, tool_update: ToolCreate, current_user = Depends(get_current_user)):
    existing_tool = await tools_collection.find_one({
        "id": tool_id,
        "user_id": current_user["id"]
    })
    
    if not existing_tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool not found"
        )
    
    update_doc = {
        "title": tool_update.title,
        "description": tool_update.description,
        "category": tool_update.category,
        "html_content": tool_update.html_content,
        "preview_image": tool_update.preview_image,
        "updated_at": datetime.now(timezone.utc)
    }
    
    await tools_collection.update_one(
        {"id": tool_id, "user_id": current_user["id"]},
        {"$set": update_doc}
    )
    
    updated_tool = await tools_collection.find_one({
        "id": tool_id,
        "user_id": current_user["id"]
    })
    
    return Tool(**updated_tool)

@app.delete("/api/tools/{tool_id}")
async def delete_tool(tool_id: str, current_user = Depends(get_current_user)):
    result = await tools_collection.delete_one({
        "id": tool_id,
        "user_id": current_user["id"]
    })
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool not found"
        )
    
    return {"message": "Tool deleted successfully"}

@app.get("/api/categories")
async def get_categories(current_user = Depends(get_current_user)):
    pipeline = [
        {"$match": {"user_id": current_user["id"]}},
        {"$group": {"_id": "$category", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    
    categories = []
    async for category in tools_collection.aggregate(pipeline):
        categories.append({
            "name": category["_id"],
            "count": category["count"]
        })
    
    return categories

@app.get("/api/pet-state", response_model=PetState)
async def get_pet_state(current_user = Depends(get_current_user)):
    """Get the user's pet state, create default if none exists"""
    pet_state = await pet_states_collection.find_one({"user_id": current_user["id"]})
    
    if not pet_state:
        # Create default pet state for new user
        pet_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)
        
        default_pet = {
            "id": pet_id,
            "user_id": current_user["id"],
            "name": "PIXEL-IA",
            "level": 1,
            "happiness": 80,
            "knowledge": 60,
            "energy": 75,
            "hunger": 70,
            "stage": "baby",
            "modules_completed": 0,
            "mood": "happy",
            "created_at": now,
            "updated_at": now
        }
        
        await pet_states_collection.insert_one(default_pet)
        return PetState(**default_pet)
    
    return PetState(**pet_state)

@app.post("/api/pet-state", response_model=PetState)
async def save_pet_state(pet_data: PetStateCreate, current_user = Depends(get_current_user)):
    """Save or update the user's pet state"""
    now = datetime.now(timezone.utc)
    existing_pet = await pet_states_collection.find_one({"user_id": current_user["id"]})
    
    if existing_pet:
        # Update existing pet state
        update_doc = {
            "name": pet_data.name,
            "level": pet_data.level,
            "happiness": pet_data.happiness,
            "knowledge": pet_data.knowledge,
            "energy": pet_data.energy,
            "hunger": pet_data.hunger,
            "stage": pet_data.stage,
            "modules_completed": pet_data.modules_completed,
            "mood": pet_data.mood,
            "updated_at": now
        }
        
        await pet_states_collection.update_one(
            {"user_id": current_user["id"]},
            {"$set": update_doc}
        )
        
        updated_pet = await pet_states_collection.find_one({"user_id": current_user["id"]})
        return PetState(**updated_pet)
    else:
        # Create new pet state
        pet_id = str(uuid.uuid4())
        
        pet_doc = {
            "id": pet_id,
            "user_id": current_user["id"],
            "name": pet_data.name,
            "level": pet_data.level,
            "happiness": pet_data.happiness,
            "knowledge": pet_data.knowledge,
            "energy": pet_data.energy,
            "hunger": pet_data.hunger,
            "stage": pet_data.stage,
            "modules_completed": pet_data.modules_completed,
            "mood": pet_data.mood,
            "created_at": now,
            "updated_at": now
        }
        
        await pet_states_collection.insert_one(pet_doc)
        return PetState(**pet_doc)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)