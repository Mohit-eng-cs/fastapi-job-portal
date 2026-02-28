from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    company: str
    description: str | None = None
    location: str | None = None
    Min_sal: int  | None = None
    Max_sal:int   | None = None

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    description: str | None = None
    location: str | None = None
    Min_sal: int  | None = None
    Max_sal:int   | None = None


class JobResponse(JobBase):
    id: int
    job_code:str
    title: str 
    company: str
    description: str 
    location: str 
    Min_sal: int
    Max_sal:int

    class Config:
        orm_mode = True


class PaginatedJobsResponse(BaseModel):
    total: int 
    page: int
    limit : int 
    total_pages:int
    data: list[JobResponse]
