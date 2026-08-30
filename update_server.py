import sys, os

path = 'backend/api/server.py'
with open(path, 'r') as f:
    content = f.read()

content = content.replace(
    'from api.routes import stocks, assets',
    'from api.routes import stocks, assets, auth'
)

content = content.replace(
    'app.include_router(assets.router, prefix="/api/assets", tags=["assets"])',
    'app.include_router(assets.router, prefix="/api/assets", tags=["assets"])\napp.include_router(auth.router, prefix="/api/auth", tags=["auth"])'
)

with open(path, 'w') as f:
    f.write(content)

print("server.py updated with auth routes.")
