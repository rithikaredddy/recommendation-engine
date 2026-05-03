# Movie Recommendation Engine 🎬

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-blue?style=for-the-badge&logo=react)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=nextdotjs)
![MongoDB](https://img.shields.io/badge/MongoDB-7-green?style=for-the-badge&logo=mongodb)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3-orange?style=for-the-badge&logo=scikitlearn)

> A full-stack movie recommendation system combining **Content-Based Filtering** and **Collaborative Filtering** — served via a FastAPI backend with a Next.js frontend and JWT authentication.

---

## How It Works

| Method | Algorithm | When Used |
|---|---|---|
| Content-Based | TF-IDF + Cosine Similarity | "More like this movie" |
| Collaborative | SVD Matrix Factorization | "Users like you also liked" |
| Hybrid | Weighted blend of both | Default recommendations |

---

## Features

- JWT Authentication (Register / Login)
- Search movies with instant results
- Content-based recommendations (genre, cast, keywords)
- Collaborative filtering (user behavior patterns)
- Rate movies (1–5 stars) — improves future recs
- User profile with watch history & rated movies
- Trending movies dashboard
- Fully responsive UI

---

## Tech Stack

| Layer | Technology |
|---|---|
| ML / Recommendation | Python, Scikit-learn, Pandas, NumPy, Surprise (SVD) |
| Backend API | FastAPI, Motor (async MongoDB), JWT |
| Frontend | Next.js 14, React 18, Tailwind CSS |
| Database | MongoDB |
| Dataset | MovieLens 100K (ml-100k) |
| Deployment | Vercel (frontend) + Render (backend) |

---

## Project Structure

```
recommendation-engine/
├── backend/                   # FastAPI Python backend
│   ├── main.py                # FastAPI app entry point
│   ├── routes/
│   │   ├── auth.py            # Register / Login
│   │   ├── movies.py          # Search, detail, trending
│   │   └── recommendations.py # Content + collaborative recs
│   ├── models/
│   │   ├── user.py            # User Pydantic model
│   │   └── movie.py           # Movie Pydantic model
│   ├── middleware/
│   │   └── auth.py            # JWT verification
│   ├── recommender/
│   │   ├── content_based.py   # TF-IDF + Cosine Similarity
│   │   ├── collaborative.py   # SVD Matrix Factorization
│   │   └── hybrid.py          # Blended recommender
│   ├── seed/
│   │   └── seed_movies.py     # Load MovieLens dataset → MongoDB
│   └── requirements.txt
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/               # Next.js 14 App Router
│   │   │   ├── page.jsx       # Home / trending
│   │   │   ├── login/page.jsx
│   │   │   ├── register/page.jsx
│   │   │   ├── movie/[id]/page.jsx
│   │   │   └── profile/page.jsx
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── MovieCard.jsx
│   │   │   ├── MovieGrid.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── StarRating.jsx
│   │   │   └── RecommendationSection.jsx
│   │   └── context/
│   │       └── AuthContext.jsx
│   ├── package.json
│   └── next.config.js
├── ml/
│   ├── notebooks/
│   │   └── EDA_and_Model.ipynb  # Full EDA + model training notebook
│   └── data/                    # MovieLens dataset goes here
├── .env.example
├── .gitignore
├── docker-compose.yml
├── GITHUB_STRATEGY.md
└── README.md
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- MongoDB running locally or MongoDB Atlas URI

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/recommendation-engine
cd recommendation-engine
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
# Edit .env with your MONGO_URI and JWT_SECRET
python seed/seed_movies.py   # Load MovieLens data into MongoDB
uvicorn main:app --reload --port 8000
# API running at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### 3. Frontend setup
```bash
cd frontend
npm install
npm run dev
# UI running at http://localhost:3000
```

---

## API Endpoints

```
POST   /auth/register                     Register new user
POST   /auth/login                        Login + get JWT

GET    /movies/trending                   Top trending movies
GET    /movies/search?q=inception         Search movies
GET    /movies/{movie_id}                 Movie detail
POST   /movies/{movie_id}/rate            Rate a movie { rating: 4 }

GET    /recommendations/content/{movie_id}    Content-based recs
GET    /recommendations/collaborative         Collaborative recs for user
GET    /recommendations/hybrid                Hybrid recs for user
```

---

## Resume Bullet Points

- Built a **full-stack movie recommendation system** combining Content-Based Filtering (TF-IDF + Cosine Similarity) and Collaborative Filtering (SVD Matrix Factorization) using the MovieLens 100K dataset
- Designed a **FastAPI** backend with async MongoDB (Motor), JWT authentication, and a hybrid recommender engine blending content and collaborative signals
- Trained and evaluated multiple recommendation models (cosine similarity, SVD, hybrid) with precision@K metrics; deployed best model as a REST API
- Built a **Next.js 14** frontend with real-time search, 1–5 star rating system, personalized recommendation sections, and user watch history

---

## Live Demo

🔗 https://recommendation-engine-lyart.vercel.app/

---

## Dataset

This project uses the [MovieLens 100K dataset](https://grouplens.org/datasets/movielens/100k/) — 100,000 ratings from 943 users on 1,682 movies.

---

## Future Improvements

- [ ] Deep learning recommender (Neural Collaborative Filtering)
- [ ] Real-time rec updates on new ratings
- [ ] A/B test content-based vs collaborative
- [ ] Add TV shows dataset
- [ ] Redis caching for recommendation results
