from app.models import ATBase


class Result(ATBase):
    start_timestamp: str
    end_timestamp: str
    video_path: str


class ResultCreate(Result):
    ...


class ResultUpdate(Result):
    ...


class ResultResponse(ATBase):
    id: int
    start_timestamp: str
    end_timestamp: str
