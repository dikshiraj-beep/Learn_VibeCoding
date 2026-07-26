from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    Text,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.schema import CreateSchema

from db import get_db_schema, get_engine

Base = declarative_base()
SCHEMA = get_db_schema()


class Profile(Base):
    __tablename__ = "profiles"
    __table_args__ = {"schema": SCHEMA}

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(Text, nullable=False)
    email = Column(Text, nullable=False)
    role = Column(Text, nullable=False, server_default=text("'customer'"))
    company_name = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class Port(Base):
    __tablename__ = "ports"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    country = Column(Text)


class Vessel(Base):
    __tablename__ = "vessels"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    status = Column(Text, nullable=False, server_default=text("'active'"))


class VesselSchedule(Base):
    __tablename__ = "vessel_schedule"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey(f"{SCHEMA}.vessels.id"), nullable=False)
    port_id = Column(Integer, ForeignKey(f"{SCHEMA}.ports.id"), nullable=False)
    sequence = Column(Integer, nullable=False)
    eta = Column(DateTime, nullable=False)


class CargoAuction(Base):
    __tablename__ = "cargo_auctions"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True)
    vessel_id = Column(Integer, ForeignKey(f"{SCHEMA}.vessels.id"), nullable=False)
    load_port_id = Column(Integer, ForeignKey(f"{SCHEMA}.ports.id"), nullable=False)
    discharge_port_id = Column(Integer, ForeignKey(f"{SCHEMA}.ports.id"), nullable=False)
    capacity_available = Column(Numeric, nullable=False)
    capacity_unit = Column(Text, nullable=False, server_default=text("'MT'"))
    base_rate = Column(Numeric, nullable=False)
    currency = Column(Text, nullable=False, server_default=text("'USD'"))
    auction_close_at = Column(DateTime, nullable=False)
    status = Column(Text, nullable=False, server_default=text("'open'"))
    winning_bid_id = Column(Integer)
    created_by = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.profiles.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())


class Bid(Base):
    __tablename__ = "bids"
    __table_args__ = {"schema": SCHEMA}

    id = Column(Integer, primary_key=True)
    auction_id = Column(Integer, ForeignKey(f"{SCHEMA}.cargo_auctions.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey(f"{SCHEMA}.profiles.id"), nullable=False)
    cargo_description = Column(Text, nullable=False)
    cargo_weight = Column(Numeric, nullable=False)
    bid_rate = Column(Numeric, nullable=False)
    bid_time = Column(DateTime, nullable=False, server_default=func.now())
    status = Column(Text, nullable=False, server_default=text("'pending'"))


def init_db() -> None:
    engine = get_engine()
    with engine.begin() as connection:
        connection.execute(CreateSchema(SCHEMA, if_not_exists=True))
        Base.metadata.create_all(connection)
