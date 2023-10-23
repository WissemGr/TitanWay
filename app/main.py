from fastapi import FastAPI
# from routes import  service # Import the routers for both services

app = FastAPI()

# app.include_router(service.router, prefix="/tracking")  # Add the service routes

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
