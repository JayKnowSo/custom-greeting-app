# The main.py file is the entry point of the FastAPI application.
# It sets up the application, including database initialization, middleware, and routes.
# The app is created with a lifespan function that initializes the database
# tables when the app starts.
# The app includes the API routes from the greetings module and adds middleware for
# security headers. It also sets up custom exception handlers for rate limit errors.


from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.infrastructure.functions import engine
from app.api import routes as greetings
from app.error_handling import add_exception_handlers
from app.security.limiter import limiter
from app.security.headers import SecurityHeadersMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# The FastAPI app is created with the defined lifespan function,
# and the limiter is attached to the app state.
# Custom exception handlers are added to handle rate limit exceeded errors,
# and the API routes are included in the app. Finally, security headers middleware is added.

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
add_exception_handlers(app)
app.include_router(greetings.router)
app.add_middleware(SecurityHeadersMiddleware)


# The root endpoint is defined to return a simple message indicating that the API is running.
# This can be used as a quick check to verify that the application is up and running.

@app.get("/")
def root():
    return {"message": "API is running"}

# A health check endpoint is added to allow monitoring tools
# to check the health of the application.
# This endpoint can be used by load balancers or monitoring services to ensure that the application is responsive and healthy.
# The /health endpoint returns a JSON response with a status of
# "healthy" to indicate that the application is functioning properly.
@app.get("/health")
def health():
    return {"status": "healthy"}
