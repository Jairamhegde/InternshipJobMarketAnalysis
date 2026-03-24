# Internship Job Market Analysis

An end-to-end data analysis project that scrapes real internship job postings, stores them in a normalized SQLite database, and analyzes market demand for roles and skills using SQL and Python. The insights are presented through an interactive Streamlit dashboard.

---

## Problem Statement

Students often struggle to understand:
- which internship roles are most in demand
- which technical skills are consistently required
- how skills overlap across different job roles

This project aims to answer these questions using **real-world job data** instead of assumptions.

---

## Tech Stack

- **Python** – Web scraping, data processing
- **BeautifulSoup & Requests** – Data extraction
- **SQLite** – Relational data storage
- **SQL** – Data analysis and aggregation
- **Pandas** – Query result handling
- **Streamlit** – Interactive dashboard
- **Plotly** – Data visualization

---

## Database Design

The database follows **normalization principles** to avoid redundancy.

### Tables

#### `jobs`
- job title
- company
- location
- salary
- hiring status

#### `skills`
- unique list of technical skills

#### `job_skills`
- mapping table (many-to-many relationship between jobs and skills)

This design allows:
- accurate skill demand analysis
- reuse of skills across multiple jobs
- clean analytical queries

---

## Data Pipeline

1. Scrape internship postings from Internshala
2. Clean and validate extracted data
3. Insert data into SQLite with:
   - duplicate protection (UNIQUE constraints)
   - backfilling missing fields using UPDATE queries
4. Run analytical SQL queries
5. Visualize insights in Streamlit

---

##Live demo
https://internshipjobmarketanalysis.streamlit.app/

## Key Analyses Performed

- Top demanded internship skills
- Most common internship roles
- Skills common across top hiring roles
- Role and skill demand distribution

All insights are **derived dynamically from the database**, not hard-coded.

---

## Dashboard Highlights

The Streamlit dashboard provides:
- Market overview of skills and roles
- Identification of universally required skills
- Automatically updating insights when data changes

---

## Key Insights (Example)

- Backend and Full Stack roles dominate internship hiring.
- Python, SQL, and JavaScript are consistently in high demand.
- Several skills appear across multiple top roles, indicating stack-based hiring.

---

## Challenges Faced

- Handling duplicate job postings across multiple runs
- Managing missing company data already stored in the database
- Designing SQL queries involving multiple joins, grouping, and intersections
- Converting static insights into dynamic, data-driven explanations

---

## Future Improvements

- Add time-based trend analysis
- Include salary normalization and comparisons
- Add filters (role, skill, location) to the dashboard
- Migrate from SQLite to PostgreSQL for larger datasets

---

##  How to Run the Project

```bash
pip install -r requirements.txt
python db/init_db.py
python main.py
streamlit run dashboard/app.py