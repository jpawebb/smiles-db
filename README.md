# 🧬 SMILES-DB: Chemical Intellectual Property Registry

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009485.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791.svg)](https://www.postgresql.org/)
[![Apache 2.0 License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](./LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Overview

**SMILES-DB** is a sophisticated database system for registering and managing intellectual property rights in the discovery of novel chemical compounds. Built on the **[Simplified Molecular Input Line Entry System (SMILES)](https://en.wikipedia.org/wiki/Simplified_Molecular_Input_Line_Entry_System)** notation standard, this project provides a robust platform for scientists, researchers, and pharmaceutical companies to document, validate, and track chemical compound discoveries with cryptographic integrity and comprehensive metadata.

The system combines cutting-edge cheminformatics libraries (RDKit) with modern Python frameworks (FastAPI, SQLModel) to deliver a production-ready solution for chemical IP management.

---

## ✨ Key Features

- **🔬 SMILES Validation & Canonicalization**: Automatic validation and standardization of SMILES strings using RDKit
- **⚖️ Molecular Property Calculation**: Automatic computation of molecular weight and other chemical descriptors
- **🔐 IP Registration & Tracking**: Secure registration and timestamped tracking of chemical discoveries
- **📊 Database Indexing**: Optimized database queries with strategic indexing on SMILES strings and molecular properties
- **🌐 RESTful API**: Comprehensive async API for compound registration, retrieval, and management
- **🧪 Comprehensive Testing**: Full test coverage including unit tests and database integration tests
- **📚 Interactive API Documentation**: Built-in Scalar API documentation interface
- **⚙️ Database Migrations**: Alembic-managed schema evolution for production deployments
- **🔄 Async/Await Architecture**: Non-blocking I/O operations for high-performance concurrent requests
- **🏥 Health Checks**: Database connectivity monitoring and health status endpoints

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Application                   │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   API Layer  │  │ Dependencies │  │  Middleware  │  │
│  │   (Routes)   │  │  (Injection) │  │              │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│         │                │                    │          │
│  ┌──────────────────────────────────────────────────┐  │
│  │          Service Layer (Business Logic)          │  │
│  │    DiscoveryService, BaseService                 │  │
│  └──────────────────────────────────────────────────┘  │
│         │                                                │
│  ┌──────────────────────────────────────────────────┐  │
│  │            Schema Layer (Validation)             │  │
│  │  SmilesCreate, DiscoveryCreate, DiscoveryRead    │  │
│  └──────────────────────────────────────────────────┘  │
│         │                                                │
│  ┌───────────────────────���──────────────────────────┐  │
│  │          Database Layer (SQLModel/ORM)           │  │
│  │   Discovery, Publisher, BaseIDModel              │  │
│  └──────────────────────────────────────────────────┘  │
│         │                                                │
└─────────────────────────────────────────────────────────┘
         │
┌─────────────────────────────────────────────────────────┐
│            PostgreSQL Database                          │
│  ┌──────────────────┐  ┌──────────────────┐            │
│  │   publishers     │  │   discoveries    │            │
│  │   - id (UUID)    │  │   - id (UUID)    │            │
│  │   - email        │  │   - name         │            │
│  │   - full_name    │  │   - smiles (UNQ) │◄───────┐   │
│  │   - website      │  │   - mol_weight   │        │   │
│  └──────────────────┘  │   - publisher_id │        │   │
│        ▲               └──────────────────┘        │   │
│        │                                            │   │
│        └────────── Foreign Key ───────────────────┘   │
│                                                        │
└─────────────────────────────────────────────────────────┘
```

### Data Models

#### Publisher
Represents organizations or individuals registering chemical discoveries.

```python
class Publisher(BaseIDModel, table=True):
    email: str
    hashed_password: str
    full_name: str | None
    website: str | None
    discoveries: list["Discovery"]  # Relationship
```

#### Discovery
Represents a registered chemical compound with validated SMILES notation.

```python
class Discovery(BaseIDModel, table=True):
    name: str
    smiles: SmilesStr  # Validated & canonicalized SMILES string
    molecular_weight: float  # Auto-calculated from SMILES
    publisher_id: UUID  # Foreign key to Publisher
    publisher: Publisher  # Relationship
```

---

## 🔧 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | FastAPI | 0.104+ |
| **ORM** | SQLModel | - |
| **Database** | PostgreSQL | 14+ |
| **Async Driver** | asyncpg | - |
| **Cheminformatics** | RDKit | Latest |
| **Validation** | Pydantic | 2.x |
| **Migrations** | Alembic | - |
| **Testing** | pytest, pytest-asyncio | - |
| **Python** | Python | 3.11+ |

---

## 📦 Installation

### Prerequisites

- **Python 3.11** or higher
- **PostgreSQL 14** or higher
- **pip** or **pip-tools** (optional, for dependency management)

### Step 1: Clone Repository

```bash
git clone https://github.com/jpawebb/smiles-db.git
cd smiles-db
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/smiles_db
DATABASE_URL_SYNC=postgresql://user:password@localhost:5432/smiles_db

# Optional
DEBUG=False
LOG_LEVEL=INFO
```

### Step 5: Initialize Database

```bash
# Create database (from PostgreSQL CLI)
createdb smiles_db

# Run migrations
alembic upgrade head
```

---

## 🚀 Running the Application

### Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: `http://localhost:8000`

### Production Deployment

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Health Check

```bash
curl http://localhost:8000/health/db
# Response: {"db": 1}
```

---

## 📚 API Documentation

### Interactive Documentation

- **Scalar API**: http://localhost:8000/scalar
- **Auto-generated Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Register New Chemical Discovery

```http
POST /discoveries
Content-Type: application/json

{
  "name": "Aspirin",
  "smiles": "CC(=O)Oc1ccccc1C(=O)O"
}

# Response: 201 Created
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Aspirin",
  "smiles": "CC(=O)Oc1ccccc1C(=O)O",
  "molecular_weight": 180.157,
  "publisher_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

#### Retrieve Discovery by ID

```http
GET /discoveries/{discovery_id}

# Response: 200 OK
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Aspirin",
  "smiles": "CC(=O)Oc1ccccc1C(=O)O",
  "molecular_weight": 180.157,
  "publisher_id": "550e8400-e29b-41d4-a716-446655440001"
}
```

#### Database Health Check

```http
GET /health/db

# Response: 200 OK
{
  "db": 1
}
```

---

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Test Files Overview

| Test File | Purpose |
|-----------|---------|
| `tests/test_validate_smiles.py` | SMILES validation and canonicalization |
| `tests/test_database_connection.py` | Database connectivity verification |
| `tests/conftest.py` | pytest fixtures and test configuration |

### Test Example: SMILES Validation

```python
def test_validate_smiles():
    # Valid benzene
    assert validate_smiles("c1ccccc1") == "c1ccccc1"
    
    # Non-standard Kekule form
    assert validate_smiles("C1=CC=CC=C1") == "c1ccccc1"
    
    # Invalid SMILES
    with pytest.raises(ValueError):
        validate_smiles("CC(CCCC")  # Incomplete parenthesis
    
    # Type enforcement
    with pytest.raises(TypeError):
        validate_smiles(10.0)  # Must be string
```

---

## 📁 Project Structure

```
smiles-db/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py      # Dependency injection (Publishers, Services)
│   │   ├── router.py            # API route aggregation
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── discoveries.py    # Discovery endpoints
│   │       └── publishers.py     # Publisher endpoints
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLModel ORM models
│   │   └── session.py           # Database session configuration
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── discovery.py         # Discovery Pydantic schemas
│   │   ├── publisher.py         # Publisher Pydantic schemas
│   │   └── smiles.py            # SMILES validation schemas
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py              # Base service class (CRUD operations)
│   │   └── discoveries.py        # Discovery business logic
│   ├── utils.py                 # Utility functions (SMILES validation)
│   ├── config.py                # Configuration management
│   └── main.py                  # FastAPI application entry point
├── migrations/
│   ├── env.py                   # Alembic environment configuration
│   ├── script.py.mako           # Alembic migration template
│   ├── versions/                # Migration scripts
│   └── alembic.ini              # Alembic configuration
├── tests/
│   ├── conftest.py              # pytest configuration & fixtures
│   ├── test_validate_smiles.py  # SMILES validation tests
│   └── test_database_connection.py  # Database integration tests
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create locally)
├── .gitignore                   # Git ignore rules
├── .dockerignore                # Docker ignore rules
├── Dockerfile                   # Docker image definition
├── docker-compose.yml           # Local development environment
├── pyproject.toml               # Project metadata & build config
├── LICENSE                      # Apache 2.0 License
└── README.md                    # This file
```

---

## 🔍 Key Implementation Details

### SMILES Validation

SMILES strings are validated using RDKit's chemical parsing:

```python
def validate_smiles(v: str) -> str:
    """Validate and canonicalize SMILES strings."""
    if not isinstance(v, str):
        raise TypeError(f"SMILES must be a string, not {type(v)}")
    
    mol = Chem.MolFromSmiles(v)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {v}")
    
    # Return canonicalized SMILES
    return Chem.MolToSmiles(mol)
```

### Automatic Molecular Weight Calculation

Molecular weight is automatically calculated from the SMILES string:

```python
@field_validator("molecular_weight")
@classmethod
def calculate_mw(cls, v, info):
    smiles = info.data.get("smiles")
    if smiles:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            return float(Descriptors.MolWt(mol))
    return v
```

### Database Indexing Strategy

- **SMILES Column**: Unique index for O(1) lookups and uniqueness guarantee
- **Molecular Weight**: Index for range queries (e.g., find compounds with MW 100-200)
- **Discovery ID**: Primary key index for fast record retrieval

---

## 🔐 Security Considerations

1. **SMILES Validation**: All SMILES strings are validated server-side
2. **Type Enforcement**: Pydantic enforces strict type checking
3. **Database Integrity**: Foreign key constraints prevent orphaned records
4. **Unique Constraint**: SMILES column is unique to prevent duplicate registrations
5. **Async Operations**: Non-blocking I/O prevents thread exhaustion attacks
6. **Error Handling**: Detailed error messages only in development mode

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Write tests for new functionality
4. Ensure all tests pass: `pytest`
5. Commit changes: `git commit -am 'Add your feature'`
6. Push to the branch: `git push origin feature/your-feature`
7. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for public APIs
- Format code with black: `black app/ tests/`

---

## 📋 Database Migrations

### Create a New Migration

```bash
alembic revision --autogenerate -m "Add new column to discoveries"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
alembic downgrade -1
```

---

## 🐛 Troubleshooting

### Database Connection Errors

```
AsyncConnectionError: Cannot connect to PostgreSQL
```

**Solution**: Verify PostgreSQL is running and credentials in `.env` are correct:

```bash
psql -U user -d smiles_db -c "SELECT 1;"
```

### Invalid SMILES Error

```
ValueError: Invalid SMILES string
```

**Solution**: Ensure SMILES notation follows standard conventions. Test with:

```python
from rdkit import Chem
Chem.MolFromSmiles("your_smiles_string")
```

### Migration Conflicts

**Solution**: Reset migrations (dev only):

```bash
alembic downgrade base
alembic upgrade head
```

---

## 📊 Performance Considerations

- **Async Database Driver**: Uses asyncpg for non-blocking database operations
- **Connection Pooling**: Managed by SQLAlchemy for optimal resource utilization
- **Indexed Queries**: Strategic indexing on frequently queried columns
- **Lazy Loading**: Related objects loaded efficiently via SQLModel relationships
- **Query Optimization**: Use `selectin` loading strategy for preventing N+1 queries

---

## 📄 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](./LICENSE) file for details.

```
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

---

## 📞 Support & Contact

For questions, issues, or suggestions:

- **GitHub Issues**: [jpawebb/smiles-db/issues](https://github.com/jpawebb/smiles-db/issues)
- **API Documentation**: [Scalar Docs](http://localhost:8000/scalar) (when running locally)

---

## 🚀 Roadmap

- [ ] Authentication & authorization (JWT tokens)
- [ ] Advanced search & filtering capabilities
- [ ] Chemical similarity scoring
- [ ] Bulk import/export functionality
- [ ] 3D molecular visualization
- [ ] Machine learning integration for property prediction
- [ ] GraphQL API support
- [ ] Multi-language support

---

## 🙏 Acknowledgments

- [RDKit](https://www.rdkit.org/) - Cheminformatics library
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases in Python
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

**Last Updated**: March 6, 2026 | **Status**: Active Development ✅