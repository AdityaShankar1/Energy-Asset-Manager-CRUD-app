import tkinter as tk
from tkinter import ttk, messagebox
import requests

API = "http://127.0.0.1:8000"

def list_records():
    try:
        r = requests.get(f"{API}/records", params={"limit": 5}, timeout=5)
        r.raise_for_status()
        data = r.json()
        text.delete("1.0", tk.END)
        for row in data:
            text.insert(tk.END, f"{row}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def get_record():
    rid = entry_id.get().strip()
    if not rid:
        messagebox.showwarning("Input", "Enter AssessmentCode ID")
        return
    try:
        r = requests.get(f"{API}/record/{rid}", timeout=5)
        if r.status_code == 404:
            messagebox.showinfo("Not found", "Record not found")
            return
        r.raise_for_status()
        text.delete("1.0", tk.END)
        text.insert(tk.END, f"{r.json()}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def create_record():
    record = {
        "TimePeriod": entry_time.get(),
        "EnergyProductName": entry_product.get(),
        "FlowBreakdown": entry_flow.get(),
        "UnitOfMeasure": entry_unit.get(),
        "ObsValue": float(entry_value.get()),
        "AssessmentCode": int(entry_id.get())
    }
    try:
        r = requests.post(f"{API}/record", json=record, timeout=5)
        r.raise_for_status()
        messagebox.showinfo("Success", r.json()["message"])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def update_record():
    rid = entry_id.get().strip()
    if not rid:
        messagebox.showwarning("Input", "Enter AssessmentCode ID")
        return
    record = {
        "TimePeriod": entry_time.get(),
        "EnergyProductName": entry_product.get(),
        "FlowBreakdown": entry_flow.get(),
        "UnitOfMeasure": entry_unit.get(),
        "ObsValue": float(entry_value.get())
    }
    try:
        r = requests.put(f"{API}/record/{rid}", json=record, timeout=5)
        r.raise_for_status()
        messagebox.showinfo("Success", r.json()["message"])
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_record():
    rid = entry_id.get().strip()
    if not rid:
        messagebox.showwarning("Input", "Enter AssessmentCode ID")
        return
    try:
        r = requests.delete(f"{API}/record/{rid}", timeout=5)
        r.raise_for_status()
        messagebox.showinfo("Success", r.json()["message"])
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("OilIndicators CRUD (Tkinter)")
frm = ttk.Frame(root, padding=10)
frm.pack(fill="both", expand=True)

# Input fields
ttk.Label(frm, text="AssessmentCode ID").grid(row=0, column=0, sticky="w")
entry_id = ttk.Entry(frm, width=20)
entry_id.grid(row=0, column=1, sticky="w")

ttk.Label(frm, text="TimePeriod (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
entry_time = ttk.Entry(frm, width=20)
entry_time.grid(row=1, column=1, sticky="w")

ttk.Label(frm, text="EnergyProductName").grid(row=2, column=0, sticky="w")
entry_product = ttk.Entry(frm, width=20)
entry_product.grid(row=2, column=1, sticky="w")

ttk.Label(frm, text="FlowBreakdown").grid(row=3, column=0, sticky="w")
entry_flow = ttk.Entry(frm, width=20)
entry_flow.grid(row=3, column=1, sticky="w")

ttk.Label(frm, text="UnitOfMeasure").grid(row=4, column=0, sticky="w")
entry_unit = ttk.Entry(frm, width=20)
entry_unit.grid(row=4, column=1, sticky="w")

ttk.Label(frm, text="ObsValue").grid(row=5, column=0, sticky="w")
entry_value = ttk.Entry(frm, width=20)
entry_value.grid(row=5, column=1, sticky="w")

# Buttons
btn_get = ttk.Button(frm, text="Get Record", command=get_record)
btn_get.grid(row=0, column=2, padx=5)

btn_list = ttk.Button(frm, text="List 5 Records", command=list_records)
btn_list.grid(row=0, column=3, padx=5)

btn_create = ttk.Button(frm, text="Create Record", command=create_record)
btn_create.grid(row=6, column=0, pady=10)

btn_update = ttk.Button(frm, text="Update Record", command=update_record)
btn_update.grid(row=6, column=1, pady=10)

btn_delete = ttk.Button(frm, text="Delete Record", command=delete_record)
btn_delete.grid(row=6, column=2, pady=10)

# Output area
text = tk.Text(frm, height=20, width=100)
text.grid(row=7, column=0, columnspan=4, pady=10)

root.mainloop()