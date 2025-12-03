
# User Management System – FastAPI + PostgreSQL + ETL Pipeline

This project demonstrates a complete Data Engineering workflow implementing:

- REST API using **FastAPI**
- Relational database using **PostgreSQL (Docker)**
- SQL scripts for schema + sample data
- ETL pipeline using **Python + Pandas**
- Postman collection for API testing
- Clean folder structure and documentation

---

# 🚀 **1. Features Overview**

## **A. Backend API (FastAPI)**
Implements CRUD operations for:

- **Users**
- **Employment Info**
- **Bank Details**

### **API Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create user + nested employment + bank info |
| GET | `/users` | Get all users (supports filters) |
| GET | `/users/{id}` | Get 1 user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user (cascade) |
| POST | `/users/{id}/employment` | Add extra employment record |
| POST | `/users/{id}/bank` | Add extra bank record |

Swagger UI:  
👉 **http://127.0.0.1:8000/docs**

---

# 🗄️ **2. Database (PostgreSQL)**

Three tables are used:

```
users
employment_info
user_bank_info
```

SQL folder contains:

- `01_create_tables.sql`
- `02_insert_sample_data.sql`

These scripts can be executed in pgAdmin or psql.

---

# 🔄 **3. ETL Pipeline**

Python script:  
📄 `etl/group_users.py`

### **ETL Responsibilities:**

✔ Connect to PostgreSQL  
✔ Read all 3 tables  
✔ Join and group users by:

- bank_name  
- company_name  
- pincode  

✔ Generate CSVs with:

- `group_key`
- `user_count`
- `user_ids`

✔ Save outputs in:

```
etl/output/
```

Example output files:

```
group_by_bank_<timestamp>.csv
group_by_company_<timestamp>.csv
group_by_pincode_<timestamp>.csv
```

---

# 🧪 **4. Postman API Collection**

Postman collection is stored in:

```
postman/api_collection.json
```

Contains all API tests for:

- Create  
- Get  
- Filters  
- Update  
- Delete  
- Add bank & employment entries  

---

# 📁 **5. Project Structure**

```
service_app/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── database.py
│   └── __init__.py
│
├── etl/
│   ├── group_users.py
│   └── output/
│
├── sql/
│   ├── 01_create_tables.sql
│   └── 02_insert_sample_data.sql
│
├── postman/
│   └── api_collection.json
│
├── .env
└── README.md
```

---

# 🔧 **6. Environment Variables (.env)**

Your `.env` file must contain:

```
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=user_management
```

FastAPI + ETL script both read from these.

---

# ▶️ **7. How to Run the Backend**

```
cd service_app
.env\Scripts\Activate.ps1
python -m uvicorn main:app --reload --port 8000
```

Swagger:  
👉 http://127.0.0.1:8000/docs

---

# ▶️ **8. How to Run ETL Script**

```
cd service_app
.env\Scripts\Activate.ps1
cd etl
python group_users.py
```

Outputs generated in:

```
etl/output/
```

---

# 📦 **9. Technologies Used**

- FastAPI  
- PostgreSQL (Docker)  
- SQLAlchemy  
- Pandas  
- Python-dotenv  
- Postman  
- Uvicorn  
- VS Code  
- GitHub Desktop  

---

# 📝 **10. Summary**

This project shows skills in:

- REST API development  
- Relational DB design  
- Writing SQL  
- ETL development using Python & Pandas  
- Using Docker  
- API testing with Postman  
- Logging, query filters, cascade delete  
- Organizing a production-style project  

---

# ✅ **Project Ready for Submission**

This codebase is clean, modular, tested and well-documented — suitable for Data Engineering assessment and TL evaluation.
