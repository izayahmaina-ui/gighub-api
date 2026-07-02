# GigHub API

**Admission Number:** C027-01-2020/2024

GigHub is a REST API built with FastAPI for a Nairobi-based freelancing platform that connects clients with freelance developers, designers, and writers. Clients can post gigs, and both clients and freelancers can browse, search, update, and delete listings.

The dataset contains five gigs across three categories: Development, Design, and Writing, with budgets in USD.

To run the API, install dependencies with `pip install fastapi uvicorn`, then start the server with `uvicorn main:app --reload`. Visit `http://127.0.0.1:8000/docs` to view the interactive Swagger documentation.
