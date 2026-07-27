from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_buyer, get_current_user
from src.db_depends import get_async_db
from src.models.products import Product as ProductModel
from src.models.reviews import Review as ReviewModel
from src.models.users import User as UserModel
from src.schemas.schemas import (
    Review as ReviewSchema,
    ReviewCreate,
)

router = APIRouter(prefix="/reviews", tags=["reviews"])

from sqlalchemy.sql import func


async def update_product_rating(db: AsyncSession, product_id: int):
    result = await db.execute(
        select(func.avg(ReviewModel.grade)).where(
            ReviewModel.product_id == product_id, ReviewModel.is_active == True
        )
    )
    avg_rating = result.scalar() or 0.0
    product = await db.get(ProductModel, product_id)
    product.rating = avg_rating
    await db.commit()


@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    all_reviews = reviews.all()
    return all_reviews


@router.get("/{product_id}/reviews", response_model=list[ReviewSchema])
async def get_reviews_about_product(
    product_id: int, db: AsyncSession = Depends(get_async_db)
):
    product_is_active = await db.scalars(
        select(ProductModel).where(
            ProductModel.is_active == True, ProductModel.id == product_id
        )
    )
    product = product_is_active.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )
    reviews_is_active = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.is_active == True, ReviewModel.product_id == product_id
        )
    )
    reviews = reviews_is_active.all()
    return reviews


@router.post("/", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def add_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_buyer),
):
    product_is_active = await db.scalars(
        select(ProductModel).where(
            ProductModel.is_active == True, ProductModel.id == review.product_id
        )
    )
    product = product_is_active.first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or inactive",
        )
    db_review = ReviewModel(**review.model_dump(), user_id=current_user.id)
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    await update_product_rating(db, product.id)
    return db_review


@router.delete("/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user=Depends(get_current_user),
):
    review_is_active = await db.scalars(
        select(ReviewModel).where(
            ReviewModel.is_active == True, ReviewModel.id == review_id
        )
    )
    review = review_is_active.first()
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or inactive",
        )

    if (
        current_user.role != "admin"
        and current_user.role != "buyer"
        and current_user.id != review.user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not author or admin",
        )
    await db.execute(
        update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False)
    )
    await db.commit()
    await db.refresh(review)
    await update_product_rating(db, review.product_id)
    return {"message": "Review deleted"}
