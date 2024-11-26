from datetime import datetime

# from netaddr import AddrFormatError, IPNetwork
from ipaddress import IPv4Address
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DHCPRequestDataCreate(BaseModel):

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    client_identifier: str
    request_ip_address: IPv4Address
    vendor_class_identifier: str
    hostname: Optional[str] = None


class DHCPRequestDataRead(DHCPRequestDataCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


class DHCPRequestDataUpdate(BaseModel):

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    client_identifier: Optional[str] = None
    request_ip_address: Optional[IPv4Address] = None
    vendor_class_identifier: Optional[str] = None
    hostname: Optional[str] = None


class ParseTaskCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_name: str
    is_running: bool = False
    run_command: str
    command_run_time: int
    log_file_path: str
    parse_template_path: str
    # last_result: Optional[str] = None


class ParseTaskRead(ParseTaskCreate):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


# NOTE: Query Filter will be added later
# class ParseTaskReadFilter(Filter):
#     task_name: Optional[str] = None
#     task_name__ilike: Optional[str] = None
#     is_running: Optional[bool] = None
#     is_running__eq: Optional[bool] = None
#     run_command: Optional[str] = None
#     command_run_time: Optional[int] = None
#     log_file_path: Optional[str] = None
#     parse_template_path: Optional[str] = None
#
#     order_by: list[str] = []
#     search: Optional[str] = None
#
#     class Constants(Filter.Constants):
#         model = ParseTaskRead
#         order_by = ["-created_at"]
#         search_fields = ["task_name"]


class ParseTaskUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    task_name: Optional[str] = None
    is_running: Optional[bool] = None
    run_command: Optional[str] = None
    command_run_time: Optional[int] = None
    log_file_path: Optional[str] = None
    parse_template_path: Optional[str] = None
    # last_result: Optional[str] = None
