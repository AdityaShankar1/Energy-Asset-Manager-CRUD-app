from fastapi import FastAPI, HTTPException
import pyodbc

app = FastAPI()

# Database connection string
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost,1433;"
    "DATABASE=OilIndicators;"
    "UID=sa;"
    "PWD=09012004Adi"
)

def get_connection():
    return pyodbc.connect(conn_str)

@app.get("/records")
def read_records(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT TOP (?) * FROM CrudeOilIndicators", (limit,))
    rows = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    conn.close()
    return result

@app.get("/record/{id}")
def read_record(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM CrudeOilIndicators WHERE AssessmentCode = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Record not found")
    return dict(zip([column[0] for column in cursor.description], row))

@app.post("/record")
def create_record(record: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO CrudeOilIndicators (TimePeriod, EnergyProductName, FlowBreakdown, UnitOfMeasure, ObsValue, AssessmentCode)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        record["TimePeriod"],
        record["EnergyProductName"],
        record["FlowBreakdown"],
        record["UnitOfMeasure"],
        record["ObsValue"],
        record["AssessmentCode"]
    ))
    conn.commit()
    conn.close()
    return {"message": "Record created successfully"}

@app.put("/record/{id}")
def update_record(id: int, record: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE CrudeOilIndicators
        SET TimePeriod=?, EnergyProductName=?, FlowBreakdown=?, UnitOfMeasure=?, ObsValue=?
        WHERE AssessmentCode=?
    """, (
        record["TimePeriod"],
        record["EnergyProductName"],
        record["FlowBreakdown"],
        record["UnitOfMeasure"],
        record["ObsValue"],
        id
    ))
    conn.commit()
    conn.close()
    return {"message": "Record updated successfully"}

@app.delete("/record/{id}")
def delete_record(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM CrudeOilIndicators WHERE AssessmentCode=?", (id,))
    conn.commit()
    conn.close()
    return {"message": "Record deleted successfully"}
