import os

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DEFAULT_SCHEMA = "cargo_auction"


def _secret_or_env(key: str, default: str | None = None) -> str:
    if key in st.secrets:
        return str(st.secrets[key])
    value = os.getenv(key, default)
    if value is None:
        raise RuntimeError(
            f"Missing required setting '{key}'. Add it to .streamlit/secrets.toml or set it as an env var."
        )
    return value


def get_db_schema() -> str:
    return _secret_or_env("DB_SCHEMA", DEFAULT_SCHEMA)


def get_db_config() -> dict[str, str]:
    return {
        "host": _secret_or_env("DB_HOST"),
        "port": _secret_or_env("DB_PORT", "5432"),
        "dbname": _secret_or_env("DB_NAME", "postgres"),
        "user": _secret_or_env("DB_USER", "postgres"),
        "password": _secret_or_env("DB_PASSWORD"),
        "options": f"-c search_path={get_db_schema()},public",
    }


@st.cache_resource
def get_engine():
    config = get_db_config()
    dsn = (
        f"postgresql+psycopg2://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['dbname']}"
    )
    return create_engine(dsn, connect_args={"options": config["options"]}, future=True)


@st.cache_resource
def get_session_factory():
    return sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, future=True)
