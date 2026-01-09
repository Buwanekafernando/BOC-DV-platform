from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    role = Column(String, default="user")  # user, admin
    created_at = Column(DateTime, default=datetime.utcnow)

    datasets = relationship("Dataset", back_populates="owner")
    reports = relationship("Report", back_populates="owner")

class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(String, primary_key=True, index=True)  # UUID
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    row_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="datasets")

class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, index=True)  # UUID
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="reports")

class DashboardShare(Base):
    __tablename__ = "dashboard_shares"

    id = Column(Integer, primary_key=True, index=True)
    dashboard_id = Column(String, ForeignKey("dashboards.id"), nullable=False)
    shared_with_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    permission = Column(String, default="view")  # view, edit
    created_at = Column(DateTime, default=datetime.utcnow)

    dashboard = relationship("Dashboard")
    shared_user = relationship("User")
