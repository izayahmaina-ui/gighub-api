# GigHub API
# Admission Number: C027-01-2020/2024
# Last digit: 0 -> 5 + 0 = 5 gigs
# xxxx = 2020 (even) -> Categories: ["Development", "Design", "Writing"]
# First two digits of xxxx = "20" -> Currency: USD

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

app = FastAPI(
    title="GigHub API-C027-01-2020/2024",
    description="An API for GigHub, a Nairobi-based freelancing platform connecting freelancers with clients.",
    version="1.0.0"
)

ALLOWED_CATEGORIES = ["Development", "Design", "Writing"]
ALLOWED_STATUSES = ["Open", "In Progress", "Closed"]
CURRENCY = "USD"

# In-memory "database"
gigs_db = [
    {
        "id": 1,
        "title": "Build a React Dashboard",
        "description": "Build a responsive React dashboard for a fintech startup, including charts and a mobile-friendly layout.",
        "category": "Development",
        "budget": 1500.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Design a Mobile App UI",
        "description": "Design a clean, modern UI for a fitness tracking mobile app, including wireframes and a style guide.",
        "category": "Design",
        "budget": 900.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Brian Otieno"
    },
    {
        "id": 3,
        "title": "Write SEO Blog Articles",
        "description": "Write five SEO-optimized blog articles about personal finance for a Kenyan fintech blog.",
        "category": "Writing",
        "budget": 350.0,
        "currency": "USD",
        "status": "In Progress",
        "client_name": "Grace Wanjiru"
    },
    {
        "id": 4,
        "title": "Develop a REST API for Inventory",
        "description": "Develop a REST API using FastAPI to manage inventory for a small e-commerce business.",
        "category": "Development",
        "budget": 2000.0,
        "currency": "USD",
        "status": "Open",
        "client_name": "Kevin Mwangi"
    },
    {
        "id": 5,
        "title": "Design a Company Logo",
        "description": "Design a modern, minimalist logo and brand identity kit for a new consulting startup.",
        "category": "Design",
        "budget": 400.0,
        "currency": "USD",
        "status": "Closed",
        "client_name": "Amina Hassan"
    },
]


# Pydantic model for creating a new gig
class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: str
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)

    @field_validator("category")
    @classmethod
    def validate_category(cls, value):
        if value not in ALLOWED_CATEGORIES:
            raise ValueError(f"category must be one of {ALLOWED_CATEGORIES}")
        return value


# Pydantic model for updating a gig
class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value is not None and value not in ALLOWED_STATUSES:
            raise ValueError(f"status must be one of {ALLOWED_STATUSES}")
        return value


# GET /gigs - list all gigs, with optional filtering
@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):
    """
    Retrieve all gigs, optionally filtered by category and/or budget range.
    """
    results = gigs_db

    if category is not None:
        results = [g for g in results if g["category"].lower() == category.lower()]

    if min_budget is not None:
        results = [g for g in results if g["budget"] >= min_budget]

    if max_budget is not None:
        results = [g for g in results if g["budget"] <= max_budget]

    return results


# GET /gigs/search - search gigs by title
@app.get("/gigs/search")
def search_gigs(q: str):
    """
    Search for gigs whose title contains the query string.
    """
    return [g for g in gigs_db if q.lower() in g["title"].lower()]


# GET /gigs/{gig_id} - retrieve a single gig
@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    """
    Retrieve a single gig by its ID.
    """
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")


# POST /gigs - create a new gig
@app.post("/gigs")
def create_gig(gig: GigCreate):
    """
    Create a new gig posting. Status defaults to "Open" and currency is fixed to USD.
    """
    new_id = max([g["id"] for g in gigs_db]) + 1 if gigs_db else 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": CURRENCY,
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }


# PUT /gigs/{gig_id} - update a gig's budget or status
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget and/or status.
    """
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:

            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")


# DELETE /gigs/{gig_id} - delete a gig
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig by its ID.
    """
    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

