import uuid
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.membership import Membership
from app.models.group import Group


from app.db.base import BareBaseModel
from app.utils.enums import UserRole


class User(BareBaseModel):
    uuid = Column(
        UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4, index=True
    )
    full_name = Column(String, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone_number = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String, default=UserRole.USER.value)
    last_login = Column(DateTime)

    owned_groups = relationship(
        "Group", back_populates="owner", cascade="all, delete-orphan"
    )

    memberships = relationship(
        "Membership", back_populates="user", cascade="all, delete-orphan"
    )

    groups = relationship(
        "Group",
        secondary="memberships",
        back_populates="members",
        overlaps="group,user,memberships",
        lazy="selectin",
    )

    @property
    def uuid_str(self):
        return str(self.uuid)
