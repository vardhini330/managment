import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from auth import login
from database import init_db
from inventory import add_product, update_product, delete_product, get_all_products, sell_product, clear_all_data
from reports import get_low_stock, get_sales_summary

def login_screen():
    def attempt_login():
        if login(username_entry.get(), password_entry.get()):
            win.destroy()
            main_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    win = tk.Tk()
    win.title("Login - Inventory System")
    win.geometry("350x200")
    win.resizable(False, False)

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text="Username:").grid(row=0, column=0, sticky="w")
    username_entry = ttk.Entry(frame, width=30)
    username_entry.grid(row=0, column=1, pady=5)

    ttk.Label(frame, text="Password:").grid(row=1, column=0, sticky="w")
    password_entry = ttk.Entry(frame, show='*', width=30)
    password_entry.grid(row=1, column=1, pady=5)

    ttk.Button(frame, text="Login", command=attempt_login).grid(row=2, columnspan=2, pady=15)

    win.mainloop()

def main_screen():
    win = tk.Tk()
    win.title("Inventory Management System")
    win.geometry("800x600")
    win.configure(bg="#f5f5f5")

    def refresh_products():
        for widget in product_frame.winfo_children():
            widget.destroy()
        products = get_all_products()
        if products:
            for prod in products:
                ttk.Label(product_frame, text=f"ID: {prod[0]} | {prod[1]} | Qty: {prod[2]} | Price: ₹{prod[3]:.2f}",
                          padding=5).pack(anchor="w")
        else:
            ttk.Label(product_frame, text="No products found.", padding=5).pack()
    def add():
        add_window = tk.Toplevel()  
        add_window.title("Add Product")

        tk.Label(add_window, text="Product Name:").grid(row=0, column=0, pady=5, padx=5)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(add_window, text="Quantity:").grid(row=1, column=0, pady=5, padx=5)
        qty_entry = tk.Entry(add_window)
        qty_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(add_window, text="Price:").grid(row=2, column=0, pady=5, padx=5)
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=2, column=1, pady=5, padx=5)

        def submit():
            try:
                name = name_entry.get()
                qty = int(qty_entry.get())
                price = float(price_entry.get())
                if name:
                    add_product(name, qty, price)  # now this calls your real function
                    messagebox.showinfo("Success", "Product added successfully!")
                    refresh_products()
                    add_window.destroy()
                else:
                    messagebox.showerror("Error", "Product name cannot be empty.")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid quantity and price.")

        tk.Button(add_window, text="Add", command=submit).grid(row=3, column=0, columnspan=2, pady=10)

    def edit():
        edit_window = tk.Toplevel()
        edit_window.title("Edit Product")

        tk.Label(edit_window, text="Product ID:").grid(row=0, column=0, pady=5, padx=5)
        id_entry = tk.Entry(edit_window)
        id_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(edit_window, text="New Quantity:").grid(row=1, column=0, pady=5, padx=5)
        qty_entry = tk.Entry(edit_window)
        qty_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(edit_window, text="New Price:").grid(row=2, column=0, pady=5, padx=5)
        price_entry = tk.Entry(edit_window)
        price_entry.grid(row=2, column=1, pady=5, padx=5)

        def submit_edit():
            try:
                prod_id = int(id_entry.get())
                qty = int(qty_entry.get())
                price = float(price_entry.get())
                update_product(prod_id, qty, price)
                messagebox.showinfo("Success", "Product updated successfully.")
                refresh_products()
                edit_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values.")

        tk.Button(edit_window, text="Update", command=submit_edit).grid(row=3, column=0, columnspan=2, pady=10)

    def delete():
        prod_id = simpledialog.askinteger("Product ID", "Enter product ID to delete:")
        if prod_id:
            delete_product(prod_id)
            refresh_products()

    def low_stock():
        low = get_low_stock()
        if low:
            msg = "\n".join([f"{item[1]} (Qty: {item[2]})" for item in low])
        else:
            msg = "All items have sufficient stock."
        messagebox.showinfo("Low Stock Alert", msg)

    def sales_report():
        summary = get_sales_summary()
        if summary:
            msg = "\n".join([f"{name}: Sold {qty} | Revenue ₹{total:.2f}" for name, qty, total in summary])
        else:
            msg = "No sales yet."
        messagebox.showinfo("Sales Summary", msg)

    def sell():
        sell_window = tk.Toplevel()
        sell_window.title("Sell Product")

        tk.Label(sell_window, text="Product ID:").grid(row=0, column=0, pady=5, padx=5)
        id_entry = tk.Entry(sell_window)
        id_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(sell_window, text="Quantity:").grid(row=1, column=0, pady=5, padx=5)
        qty_entry = tk.Entry(sell_window)
        qty_entry.grid(row=1, column=1, pady=5, padx=5)

        def submit_sell():
            try:
                prod_id = int(id_entry.get())
                qty = int(qty_entry.get())
                if prod_id and qty:
                    success = sell_product(prod_id, qty)
                    if success:
                        messagebox.showinfo("Sale", "Sale recorded successfully.")
                    else:
                        messagebox.showerror("Error", "Not enough stock or invalid product.")
                    refresh_products()
                    sell_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid values.")

        tk.Button(sell_window, text="Sell", command=submit_sell).grid(row=2, column=0, columnspan=2, pady=10)


    def reset_database():
        confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to clear all inventory and sales data?")
        if confirm:
            clear_all_data()
            refresh_products()
            messagebox.showinfo("Done", "Database has been cleared.")

    # --- Top Button Section ---
    control_frame = ttk.LabelFrame(win, text="Controls", padding=10)
    control_frame.pack(fill=tk.X, padx=20, pady=10)

    for i, (label, func) in enumerate([
        ("Add Product", add),
        ("Edit Product", edit),
        ("Delete Product", delete),
        ("Sell Product", sell),
        ("Low Stock Alert", low_stock),
        ("Sales Summary", sales_report),
        ("Reset DB", reset_database)
    ]):
        ttk.Button(control_frame, text=label, command=func).grid(row=0, column=i, padx=5)

    # --- Product Display Section ---
    product_display_frame = ttk.LabelFrame(win, text="Product List", padding=10)
    product_display_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    canvas = tk.Canvas(product_display_frame)
    scrollbar = ttk.Scrollbar(product_display_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    product_frame = scrollable_frame
    refresh_products()

    win.mainloop()

if __name__ == "__main__":
    init_db()
    login_screen()
