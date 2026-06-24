from fastapi import APIRouter
from pydantic import BaseModel

from application.services.phone_service import PhoneService

router = APIRouter()
phone_service = PhoneService()

class TapRequest(BaseModel):
    x: int
    y: int

class SwipeRequest(BaseModel):
    x1: int
    y1: int
    x2: int
    y2: int
    duration: int = 300

class TextRequest(BaseModel):
    text: str


@router.post("/home")
def home():
    return {"result": phone_service.home()}


@router.post("/back")
def back():
    return {"result": phone_service.back()}


@router.post("/power")
def power():
    return {"result": phone_service.power()}


@router.post("/tap")
def tap(req: TapRequest):
    return {"result": phone_service.tap(req.x, req.y)}


@router.post("/swipe")
def swipe(req: SwipeRequest):
    return {"result": phone_service.swipe(req.x1, req.y1, req.x2, req.y2, req.duration)}


@router.post("/text")
def text(req: TextRequest):
    return {"result": phone_service.text(req.text)}