from fastapi import FastAPI
from database import engine
from models import Base
from routes import router as user_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# # Initialize the FastAPI app
# app = FastAPI()

# Include the task router with the specified prefix and tags
EUREKA_SERVER = "http://localhost:8761/eureka/"
SERVICE_NAME = "USER-SERVICE"
PORT = 8001

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register this service with Eureka on startup
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name=SERVICE_NAME,
        instance_port=PORT,
        instance_host="127.0.0.1"
    )
    print(f"Registered {SERVICE_NAME} with Eureka at port {PORT}")
    yield
    # Stop/Unregister from Eureka on shutdown
    await eureka_client.stop_async()
    print(f"Unregistered {SERVICE_NAME} from Eureka")

app = FastAPI(title="User Service", lifespan=lifespan)
app.include_router(user_router, prefix="/user", tags=["users"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Service"}