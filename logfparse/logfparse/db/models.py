from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.sql import func

from .database import Base

# TODO: if database is not postgresql then change INET(MACADDR for client_identifier is not working) to TEXT


class DateTimeMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class DHCPRequestData(Base, DateTimeMixin):

    __tablename__ = "dhcp_request_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # NOTE: client_identifier is unique for duplication problem, if will be not unique then remove unique.
    # if this streaming data contunally getting same clients then it will be a problem.
    # We need to remove unique constraint and maybe will be able to parse the in stream logs "time" rows. For catching to their own time.
    client_identifier = Column(String(20), name="client_id", nullable=True, unique=True)
    request_ip_address = Column(INET, index=True, name="request_ip", nullable=True)
    vendor_class_identifier = Column(String(30), name="vendor_class_id", nullable=True)
    hostname = Column(String(30), name="host_name", nullable=True)

    def __str__(self):
        return (
            f"Client: {self.client_identifier}, Request IP: {self.request_ip_address}"
        )


class ParseTask(Base, DateTimeMixin):

    __tablename__ = "parse_tasks"

    # TODO: use alembic for migration
    # TODO: relationship with dhcp_request_data table, like a dhcp_request_data table  in task_id information.
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    task_name = Column(String, nullable=False)
    is_running = Column(Boolean, default=False, nullable=False)
    # interval = Column(Integer, nullable=False)
    run_command = Column(String(255), nullable=False)
    command_run_time = Column(Integer, nullable=False)
    log_file_path = Column(String(255), nullable=False)
    parse_template_path = Column(String(255), nullable=False)
    # last_result = Column(String, nullable=True)

    def __str__(self):
        return f"Task: {self.task_name}, Status: {'Running' if self.is_running else 'Stopped'}"
