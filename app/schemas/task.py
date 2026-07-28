from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.TODO
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    due_date: datetime | None = None


class TaskUpdateStatus(BaseModel):
    status: TaskStatus


class TaskQuery(BaseModel):
    page: int = Field(default=1, ge=1, description="Số trang (bắt đầu từ 1)")
    page_size: int = Field(
        default=10, ge=1, le=100, description="Số lượng task mỗi trang (tối đa 100)"
    )
    status: TaskStatus | None = Field(
        default=None, description="Lọc theo trạng thái task"
    )
    keyword: str | None = Field(
        default=None, description="Từ khóa tìm kiếm trong tiêu đề hoặc mô tả"
    )
    sort_by: Literal["created_at", "due_date", "title", "status"] = Field(
        default="created_at", description="Trường cần sắp xếp"
    )
    order: Literal["asc", "desc"] = Field(
        default="desc", description="Thứ tự sắp xếp (asc: tăng dần, desc: giảm dần)"
    )
