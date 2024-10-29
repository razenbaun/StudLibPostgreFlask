import os


class Config:
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://my_user:446977@localhost/lib"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
