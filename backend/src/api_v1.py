from fastapi import APIRouter

from src.modules.auth.router import router as auth_router
from src.modules.auto_bids.router import router as auto_bids_router
from src.modules.bids.router import router as bids_router
from src.modules.companies.router import router as companies_router
from src.modules.dashboard.router import router as dashboard_router
from src.modules.documents.router import router as documents_router
from src.modules.scoring.router import router as scoring_router
from src.modules.tenders.router import router as tenders_router

router = APIRouter(prefix="/api/v1")
router.include_router(auth_router)
router.include_router(tenders_router)
router.include_router(bids_router)
router.include_router(companies_router)
router.include_router(auto_bids_router)
router.include_router(scoring_router)
router.include_router(documents_router)
router.include_router(dashboard_router)
