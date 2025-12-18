# Energy Asset Manager CRUD App

A system for managing energy asset data, built with **FastAPI** and **Microsoft SQL Server** as the backend, and a **Tkinter desktop client** for demonstrating full CRUD (Create, Read, Update, Delete) operations.  
This project showcases integration of enterprise‑grade databases with modern Python APIs, packaged with a simple GUI for interaction.

---

## ✨ Features
- **Backend:** FastAPI with MSSQL for robust CRUD endpoints.
- **Frontend:** Tkinter desktop app for listing, retrieving, creating, updating, and deleting records.
- **Data Model:** Energy product indicators (e.g., crude oil production, stocks, consumption).
- **Architecture:** REST API + GUI client separation.
- **Extensibility:** Can be extended with PySide6, Flet, or web frontends.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+  
- Microsoft SQL Server Express (local or containerized)  
- pip packages: `fastapi`, `uvicorn`, `sqlalchemy`, `pyodbc`, `requests`

```bash
cd backend
uvicorn main:app --reload

cd frontend_tk
python frontend_tk_crud.py
```

### Sample Data :

{
  "TimePeriod": "2002-01-01",
  "EnergyProductName": "Crude Oil",
  "FlowBreakdown": "Production",
  "UnitOfMeasure": "KBBL",
  "ObsValue": 20698.08,
  "AssessmentCode": 3
}
