from setuptools import setup, find_packages

setup(
    name="wallet_api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "asyncpg",
        "python-dotenv",
    ],
)
