import os
DATABASE_URL=os.getenv('DATABASE_URL','mysql+pymysql://cenan:cenan_demo_2026@localhost:17739/stratified_association')
REDIS_URL=os.getenv('REDIS_URL','redis://localhost:6379/0')
JWT_SECRET=os.getenv('JWT_SECRET','cenan-local-demo-change-for-deployment')
