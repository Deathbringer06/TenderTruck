from sqlalchemy import func, select, true
from sqlalchemy.orm import Session

from src.modules.auth.models import User
from src.modules.bids.models import Bid
from src.modules.companies.models import Company
from src.modules.dashboard.schemas import CarrierWins, DashboardStats
from src.modules.tenders.models import Tender, TenderStatus


def get_dashboard_stats(session: Session) -> DashboardStats:
    carrier_wins = (
        select(Bid.carrier_id.label("carrier_id"), func.count(Bid.id).label("wins"))
        .where(Bid.is_winner.is_(True))
        .group_by(Bid.carrier_id)
        .order_by(func.count(Bid.id).desc(), Bid.carrier_id)
        .limit(5)
        .subquery()
    )
    wins = (
        select(
            carrier_wins.c.carrier_id,
            carrier_wins.c.wins,
            func.coalesce(
                select(Company.name)
                .where(Company.owner_id == carrier_wins.c.carrier_id)
                .limit(1)
                .scalar_subquery(),
                User.email,
            ).label("name"),
        )
        .join(User, User.id == carrier_wins.c.carrier_id)
        .order_by(carrier_wins.c.wins.desc(), carrier_wins.c.carrier_id)
        .subquery()
    )
    bid_counts = (
        select(Bid.tender_id, func.count(Bid.id).label("bid_count"))
        .group_by(Bid.tender_id)
        .subquery()
    )
    metrics = select(
        select(
            func.coalesce(
                func.sum(Tender.start_price - Tender.current_price).filter(
                    Tender.status == TenderStatus.CLOSED
                ),
                0,
            )
        ).scalar_subquery().label("total_saved"),
        select(func.count(Tender.id))
        .where(Tender.status == TenderStatus.ACTIVE)
        .scalar_subquery()
        .label("active_tenders"),
        select(func.coalesce(func.avg(func.coalesce(bid_counts.c.bid_count, 0)), 0))
        .select_from(Tender)
        .outerjoin(bid_counts, bid_counts.c.tender_id == Tender.id)
        .scalar_subquery()
        .label("avg_bids_per_tender"),
    ).subquery()

    rows = session.execute(
        select(
            metrics.c.total_saved,
            metrics.c.active_tenders,
            metrics.c.avg_bids_per_tender,
            wins.c.carrier_id,
            wins.c.name,
            wins.c.wins,
        ).select_from(metrics.outerjoin(wins, true()))
    ).all()
    first = rows[0]
    return DashboardStats(
        total_saved=first.total_saved,
        active_tenders=first.active_tenders,
        avg_bids_per_tender=float(first.avg_bids_per_tender),
        top_carriers=[
            CarrierWins(carrier_id=row.carrier_id, name=row.name, wins=row.wins)
            for row in rows
            if row.carrier_id is not None
        ],
    )
