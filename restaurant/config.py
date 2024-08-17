class Config:
    SQLALCHEMY_DATABASE_URI= 'mysql+pymysql://root:xyz1234@localhost/restaurant'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'  # Change this!
