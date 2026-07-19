from pydantic import BaseModel, Field

class JobBase(BaseModel):
    title: str
    company: str
    description: str | None = None
    location: str | None = None
    skills_required: str | None = None
    Min_sal: int | None = Field(None, alias="min_sal")
    Max_sal: int | None = Field(None, alias="max_sal")

    model_config = {
        "populate_by_name": True,
    }

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    description: str | None = None
    location: str | None = None
    skills_required: str | None = None
    Min_sal: int | None = Field(None, alias="min_sal")
    Max_sal: int | None = Field(None, alias="max_sal")

    model_config = {
        "populate_by_name": True,
    }


class JobResponse(JobBase):
    id: int
    job_code: str

    model_config = {
        "from_attributes": True,
    }


class PaginatedJobsResponse(BaseModel):
    total: int 
    page: int
    limit : int 
    total_pages:int
    data: list[JobResponse]
