#Import Libraries
#When calling tkinter use tk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

#Rooms Information
rooms = {
    101: {"type": "Single Room", "price": 1500, "available": True},
    102: {"type": "Single Room", "price": 1500, "available": True},
    201: {"type": "Double Room", "price": 2500, "available": True},
    202: {"type": "Double Room", "price": 2500, "available": True},
    301: {"type": "Deluxe Room", "price": 4000, "available": True},
    302: {"type": "Deluxe Room", "price": 4000, "available": True}
}

#Bookings are saved here (room number -> guest details)
bookings = {}


#Show the rooms in the table
def refresh_table():
    # Remove old rows first
    for row in table.get_children():
        table.delete(row)

    # Add every room again with its latest status
    for number, info in rooms.items():
        if info["available"]:
            status = "Available"
            guest = ""
        else:
            status = "Booked"
            guest = bookings[number]["guest"]
        table.insert("", "end", iid=str(number),
                     values=(number, info["type"], "₱" + str(info["price"]), status, guest))


#Check if a name is valid (letters, spaces, - ' . only)
def is_valid_name(name):
    has_letter = False
    for ch in name:
        if ch.isalpha():
            has_letter = True
        elif ch not in " -'.":
            return False  # found a number or symbol
    return has_letter  # must have at least one letter


#ADD a booking
def add_booking():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Room Selected", "Please click a room in the table first.")
        return

    number = int(selected[0])

    if not rooms[number]["available"]:
        messagebox.showwarning("Room Not Available",
                               "Room " + str(number) + " is already booked.\nPlease choose another room.")
        return

    # Ask for the guest name
    # (it keeps asking until the name is valid or the user presses Cancel)
    while True:
        guest = simpledialog.askstring("Add Booking", "Guest name:")
        if guest is None:
            return  # user pressed Cancel, so stop quietly
        guest = guest.strip()  # remove extra spaces
        if guest == "":
            messagebox.showwarning("Missing Name", "Please enter the guest's name.")
        elif not is_valid_name(guest):
            messagebox.showwarning("Invalid Name", "The name should only contain letters, not numbers or symbols.")
        else:
            break  # name is good, continue

    # Ask for the number of nights
    while True:
        nights = simpledialog.askinteger("Add Booking", "Number of nights:")
        if nights is None:
            return  # user pressed Cancel
        if nights < 1 or nights > 30:
            messagebox.showwarning("Invalid Nights", "Please enter a number of nights from 1 to 30.")
        else:
            break  # nights is good, continue

    total = rooms[number]["price"] * nights

    # Save the booking
    rooms[number]["available"] = False
    bookings[number] = {
        "guest": guest,
        "nights": nights,
        "total": total,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    refresh_table()
    messagebox.showinfo("Booking Successful",
                        "Guest: " + guest +
                        "\nRoom: " + str(number) +
                        "\nNights: " + str(nights) +
                        "\nTotal: ₱" + str(total))


#CANCEL a booking
def cancel_booking():
    selected = table.selection()
    if not selected:
        messagebox.showwarning("No Room Selected", "Please click a booked room in the table first.")
        return

    number = int(selected[0])

    if rooms[number]["available"]:
        messagebox.showinfo("Nothing to Cancel", "Room " + str(number) + " has no booking.")
        return

    guest = bookings[number]["guest"]
    sure = messagebox.askyesno("Cancel Booking",
                               "Cancel the booking of " + guest + " for room " + str(number) + "?")
    if sure:
        rooms[number]["available"] = True
        del bookings[number]
        refresh_table()
        messagebox.showinfo("Cancelled", "The booking was cancelled.")


#Initialize GUI
root = tk.Tk()
root.title("Hotel Reservation System")
root.geometry("700x420")

# Title
title = tk.Label(root, text="Hotel Reservation System", font=("Arial", 18, "bold"))
title.pack(pady=10)

tip = tk.Label(root, text="Click a room, then press a button below.")
tip.pack()

# Table of rooms
columns = ("Room", "Type", "Price", "Status", "Guest")
table = ttk.Treeview(root, columns=columns, show="headings", height=8)
for col in columns:
    table.heading(col, text=col)
    table.column(col, width=120, anchor="center")
table.pack(padx=15, pady=10, fill="x")

# Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Booking", width=15, bg="#4CAF50", fg="white",
          command=add_booking).grid(row=0, column=0, padx=8)
tk.Button(button_frame, text="Cancel Booking", width=15, bg="#f44336", fg="white",
          command=cancel_booking).grid(row=0, column=1, padx=8)
tk.Button(button_frame, text="Exit", width=15,
          command=root.destroy).grid(row=0, column=2, padx=8)

refresh_table()
root.mainloop()