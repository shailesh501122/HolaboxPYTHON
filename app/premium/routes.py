from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.config.database import get_db
from app.users.models import User
from app.premium.models import Subscription
from app.common.helpers import get_current_user

router = APIRouter(prefix="/premium", tags=["Premium"])


class PlanUpgrade(BaseModel):
    plan_type: str
    payment_method: str
    

class SubscriptionResponse(BaseModel):
    id: int
    plan_type: str
    is_active: bool
    start_date: datetime
    end_date: datetime | None
    
    class Config:
        from_attributes = True


@router.get("/plans")
def get_available_plans():
    return {
        "plans": [
            {
                "name": "free",
                "storage": "20 GB",
                "price": 0,
                "features": ["Basic file storage", "Public sharing"]
            },
            {
                "name": "premium",
                "storage": "1 TB",
                "price": 9.99,
                "features": ["1TB storage", "Password protected shares", "Priority support"]
            },
            {
                "name": "ultra",
                "storage": "2 TB",
                "price": 19.99,
                "features": ["2TB storage", "All premium features", "Advanced analytics"]
            }
        ]
    }


@router.post("/upgrade", response_model=SubscriptionResponse)
def upgrade_plan(
    upgrade_data: PlanUpgrade,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    valid_plans = ["premium", "ultra"]
    
    if upgrade_data.plan_type not in valid_plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan type"
        )
    
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        subscription = Subscription(user_id=current_user.id)
        db.add(subscription)
    
    subscription.plan_type = upgrade_data.plan_type
    subscription.payment_method = upgrade_data.payment_method
    subscription.transaction_id = f"TXN_{datetime.utcnow().timestamp()}"
    subscription.is_active = True
    subscription.start_date = datetime.utcnow()
    subscription.end_date = datetime.utcnow() + timedelta(days=30)
    
    if upgrade_data.plan_type == "premium":
        subscription.amount_paid = 9.99
    elif upgrade_data.plan_type == "ultra":
        subscription.amount_paid = 19.99
    
    current_user.plan_type = upgrade_data.plan_type
    
    db.commit()
    db.refresh(subscription)
    
    return subscription


@router.get("/subscription", response_model=SubscriptionResponse)
def get_current_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No subscription found"
        )
    
    return subscription
