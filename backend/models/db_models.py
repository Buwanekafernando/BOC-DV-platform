from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    datasets = relationship("Dataset", back_populates="owner")

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    user_id = Column(UNIQUEIDENTIFIER, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    data_schema = Column(String, nullable=True)  # NVARCHAR(MAX) for JSON
    uploaded_at = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="datasets")

class Report(Base):
    __tablename__ = "reports"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    dashboard_id = Column(UNIQUEIDENTIFIER, ForeignKey("dashboards.id"), nullable=False)
    report_type = Column(String, nullable=False)  # pdf, png, etc.
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class DashboardShare(Base):
    __tablename__ = "dashboard_shares"

    id = Column(UNIQUEIDENTIFIER, primary_key=True, server_default=func.newid())
    dashboard_id = Column(UNIQUEIDENTIFIER, ForeignKey("dashboards.id"), nullable=False)
    shared_with_user_id = Column(UNIQUEIDENTIFIER, ForeignKey("users.id"), nullable=False)
    permission = Column(String, default="view")  # view, edit
    shared_at = Column(DateTime, server_default=func.now())

    dashboard = relationship("Dashboard")
    shared_user = relationship("User")
