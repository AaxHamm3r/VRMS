# ============================================
# Vehicle Rental Management System (VRMS)
# Part 2 - GUI + Database Interaction
# ============================================

# AI DISCLOSURE:
# Tool used: ChatGPT (GPT-5.3)
# AI-generated parts: GUI structure, database connection code,
# insert vehicle function, and rental agreement retrieval logic.
# All code was reviewed, tested, and modified by the student.

import tkinter as tk
from idlelib.debugger_r import frametable
from tkinter import messagebox
import mysql.connector

# -------------------------------
# DATABASE CONNECTION
# -------------------------------
def connect_db(username, password, database, host):
    Connection = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )

    if Connection.is_connected():
        print("Connected to Database: " + Connection.database.title())
        return Connection;
    else:
        print("Failed to connect to Database: " + database)
        return None


# -------------------------------
# INSERT VEHICLE FUNCTION
# -------------------------------
def insert_vehicle():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Get values
        license_plate = entry_license.get()
        make = entry_make.get()
        model = entry_model.get()
        year = entry_year.get()
        color = entry_color.get()
        rate = entry_rate.get()
        mileage = entry_mileage.get()
        type_id = entry_type.get()
        branch_id = entry_branch.get()

        # Validation
        if not license_plate or not make or not model:
            messagebox.showerror("Error", "Required fields missing")
            return

        if not year.isdigit():
            messagebox.showerror("Error", "Year must be a number")
            return

        query = """
        INSERT INTO Vehicle
        (LicensePlate, Make, Model, Year, Color, DailyRate, CurrentMileage, VehicleTypeID, BranchID)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (license_plate, make, model, int(year), color,
                  float(rate), int(mileage), int(type_id), int(branch_id))

        cursor.execute(query, values)
        conn.commit()

        messagebox.showinfo("Success", "Vehicle inserted successfully")

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# -------------------------------
# DISPLAY RENTAL AGREEMENTS
# -------------------------------
def get_agreements():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        customer_id = entry_customer.get()

        if not customer_id.isdigit():
            messagebox.showerror("Error", "Enter valid Customer ID")
            return

        query = """
        SELECT AgreementID, VehicleID, Status, ScheduledPickup, ScheduledReturn
        FROM RentalAgreement
        WHERE CustomerID = %s
        """

        cursor.execute(query, (customer_id,))
        results = cursor.fetchall()

        text_output.delete("1.0", tk.END)

        if not results:
            text_output.insert(tk.END, "No agreements found.\n")
        else:
            for row in results:
                text_output.insert(tk.END, str(row) + "\n")

        conn.close()

    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def login(loginWindow):
    username = loginWindow.usernameEntry.get()
    password = loginWindow.passwordEntry.get()

    Connection = connect_db(username, password, "driveeasyrentals", "LocalHost")
    if Connection.is_connected():
        showWindow(VRMSWindow(Connection))


currentWindow = None
def showWindow(windowFunction):
    global currentWindow

    if currentWindow is not None:
        currentWindow.destroy()

    currentWindow = windowFunction
    currentWindow.pack(expand="true")

def loginWindow():
    loginWindow = tk.Frame(root)

    loginWindow.loginLabel = tk.Label(loginWindow, text="Login")
    loginWindow.loginLabel.pack()

    loginWindow.usernameLabel = tk.Label(loginWindow, text="Username")
    loginWindow.usernameLabel.pack()
    loginWindow.usernameEntry = tk.Entry(loginWindow)
    loginWindow.usernameEntry.pack()

    loginWindow.passwordLabel = tk.Label(loginWindow, text="Password")
    loginWindow.passwordLabel.pack()
    loginWindow.passwordEntry = tk.Entry(loginWindow, show="*")
    loginWindow.passwordEntry.pack()

    loginWindow.loginButton = tk.Button(loginWindow, text="Login", command=lambda: login(loginWindow))
    loginWindow.loginButton.pack()

    return loginWindow

def VRMSWindow(Connection):

    if not Connection.is_connected:
        return None

    vrmsWindow = tk.Frame(root)

    vrmsWindow.label = tk.Label(text="label")
    vrmsWindow.label.pack()

    vrmsWindow.entry_license = tk.Entry(vrmsWindow)
    vrmsWindow.entry_license.grid(row=1, column=1)
    vrmsWindow.plateWindow = tk.Label(vrmsWindow, text="License Plate").grid(row=1, column=0)

    vrmsWindow.entry_make = tk.Entry(vrmsWindow)
    vrmsWindow.entry_make.grid(row=2, column=1)
    vrmsWindow.makeLabel = tk.Label(vrmsWindow, text="Make").grid(row=2, column=0)

    vrmsWindow.entry_model = tk.Entry(vrmsWindow)
    vrmsWindow.entry_model.grid(row=3, column=1)
    vrmsWindow.modelLabel = tk.Label(vrmsWindow, text="Model").grid(row=3, column=0)

    vrmsWindow.entry_year = tk.Entry(vrmsWindow)
    vrmsWindow.entry_year.grid(row=4, column=1)
    vrmsWindow.yearLabel = tk.Label(vrmsWindow, text="Year").grid(row=4, column=0)

    vrmsWindow.entry_color = tk.Entry(vrmsWindow)
    vrmsWindow.entry_color.grid(row=5, column=1)
    vrmsWindow.colorLabel = tk.Label(vrmsWindow, text="Color").grid(row=5, column=0)

    vrmsWindow.entry_rate = tk.Entry(vrmsWindow)
    vrmsWindow.entry_rate.grid(row=6, column=1)
    vrmsWindow.dailyRateLabel = tk.Label(vrmsWindow, text="Daily Rate").grid(row=6, column=0)

    vrmsWindow.entry_mileage = tk.Entry(vrmsWindow)
    vrmsWindow.entry_mileage.grid(row=7, column=1)
    vrmsWindow.milageLabel = tk.Label(vrmsWindow, text="Mileage").grid(row=7, column=0)

    vrmsWindow.entry_type = tk.Entry(vrmsWindow)
    vrmsWindow.entry_type.grid(row=8, column=1)
    vrmsWindow.idLabel = tk.Label(vrmsWindow, text="Vehicle Type ID").grid(row=8, column=0)

    vrmsWindow.entry_branch = tk.Entry(vrmsWindow)
    vrmsWindow.entry_branch.grid(row=9, column=1)
    vrmsWindow.bIdLabel = tk.Label(vrmsWindow, text="Branch ID").grid(row=9, column=0)

    #
    vrmsWindow.insertButton = tk.Button(vrmsWindow, text="Insert Vehicle", command=insert_vehicle).grid(row=10, column=1)

    # -------- RENTAL AGREEMENTS --------
    vrmsWindow.cIdLabel = tk.Label(vrmsWindow, text="Customer ID").grid(row=11, column=0)

    vrmsWindow.entry_customer = tk.Entry(vrmsWindow)
    vrmsWindow.entry_customer.grid(row=11, column=1)

    vrmsWindow.agreementsButton = tk.Button(vrmsWindow, text="Show Agreements", command=get_agreements).grid(row=12, column=1)

    vrmsWindow.text_output = tk.Text(vrmsWindow, height=10, width=50)
    vrmsWindow.text_output.grid(row=13, column=0, columnspan=2)

    return vrmsWindow




# -------------------------------
# GUI SETUP
# -------------------------------
root = tk.Tk()
root.title("VRMS System")


# ------- LOGIN ---------
showWindow(loginWindow())
root.mainloop()

# -------- VEHICLE INPUT --------
tk.Label(root, text="Insert Vehicle").grid(row=0, column=0)

entry_license = tk.Entry(root)
entry_license.grid(row=1, column=1)
tk.Label(root, text="License Plate").grid(row=1, column=0)

entry_make = tk.Entry(root)
entry_make.grid(row=2, column=1)
tk.Label(root, text="Make").grid(row=2, column=0)

entry_model = tk.Entry(root)
entry_model.grid(row=3, column=1)
tk.Label(root, text="Model").grid(row=3, column=0)

entry_year = tk.Entry(root)
entry_year.grid(row=4, column=1)
tk.Label(root, text="Year").grid(row=4, column=0)

entry_color = tk.Entry(root)
entry_color.grid(row=5, column=1)
tk.Label(root, text="Color").grid(row=5, column=0)

entry_rate = tk.Entry(root)
entry_rate.grid(row=6, column=1)
tk.Label(root, text="Daily Rate").grid(row=6, column=0)

entry_mileage = tk.Entry(root)
entry_mileage.grid(row=7, column=1)
tk.Label(root, text="Mileage").grid(row=7, column=0)

entry_type = tk.Entry(root)
entry_type.grid(row=8, column=1)
tk.Label(root, text="Vehicle Type ID").grid(row=8, column=0)

entry_branch = tk.Entry(root)
entry_branch.grid(row=9, column=1)
tk.Label(root, text="Branch ID").grid(row=9, column=0)

tk.Button(root, text="Insert Vehicle", command=insert_vehicle).grid(row=10, column=1)

# -------- RENTAL AGREEMENTS --------
tk.Label(root, text="Customer ID").grid(row=11, column=0)

entry_customer = tk.Entry(root)
entry_customer.grid(row=11, column=1)

tk.Button(root, text="Show Agreements", command=get_agreements).grid(row=12, column=1)

text_output = tk.Text(root, height=10, width=50)
text_output.grid(row=13, column=0, columnspan=2)

root.mainloop()

vrmsWindow = tk.Frame(root)

tk.Label(vrmsWindow, text="Insert Vehicle").grid(row=0, column=0)




