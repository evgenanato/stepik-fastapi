from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from app.models.promocode import PromoCodeModel
from app.schemas.promocode import PromoCodeSchema


from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_db

router = APIRouter()


@router.delete("/{promocode_id}", status_code=status.HTTP_200_OK)
async def delete_promo(
    promocode_id: int,
    db: AsyncSession = Depends(get_async_db),
):
    promo_query = await db.scalars(
        select(PromoCodeModel).where(
            PromoCodeModel.id == promocode_id, PromoCodeModel.is_active == True
        )
    )
    promo = promo_query.first()
    if not promo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Promocode not found or inactive",
        )
    await db.execute(
        update(PromoCodeModel)
        .where(PromoCodeModel.id == promocode_id)
        .values(is_active=False)
    )
    return {"status": "success", "message": "Promocode marked as inactive"}
