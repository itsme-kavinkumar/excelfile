from fastapi import APIRouter
from src.endpoints import employee,student,exportexcel,login,program

router=APIRouter()
router.include_router(employee.router)
router.include_router(student.router)
router.include_router(exportexcel.router)
router.include_router(login.router)
router.include_router(program.router)