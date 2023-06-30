import tkinter as tk
from tkinter import messagebox

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class CafeBillingApplication:
    def __init__(self):
        self.menu = []
        self.order = {}
        self.checkboxes = []
        self.quantities = []

    def add_menu_item(self, name, price):
        item = MenuItem(name, price)
        self.menu.append(item)
        messagebox.showinfo("Success", f"Added {name} to the menu.")
        self.refresh_menu()
        menu_window.destroy()

    def edit_menu_item(self, name, price):
        for item in self.menu:
            if item.name == name:
                item.price = price
                messagebox.showinfo("Success", f"Updated {name} price to {price}.")
                self.refresh_menu()
                return
        messagebox.showerror("Error", f"{name} not found in the menu.")

    def delete_menu_item(self, name):
        for item in self.menu:
            if item.name == name:
                self.menu.remove(item)
                messagebox.showinfo("Success", f"Deleted {name} from the menu.")
                self.refresh_menu()
                return
        messagebox.showerror("Error", f"{name} not found in the menu.")

    def display_menu(self):
        global menu_window
        menu_window = tk.Toplevel()
        menu_window.title("Menu")

        frame_menu = tk.Frame(menu_window)
        frame_menu.pack(padx=10, pady=10)

        label_menu = tk.Label(frame_menu, text="Menu")
        label_menu.pack()

        for item in self.menu:
            frame_item = tk.Frame(frame_menu)
            frame_item.pack()

            label_item = tk.Label(frame_item, text=item.name)
            label_item.pack(side=tk.LEFT)

            entry_price = tk.Entry(frame_item)
            entry_price.insert(tk.END, str(item.price))
            entry_price.pack(side=tk.LEFT)

            btn_edit = tk.Button(frame_item, text="Edit", command=lambda item_name=item.name: self.edit_menu_item(item_name, entry_price.get()))
            btn_edit.pack(side=tk.LEFT)

            btn_delete = tk.Button(frame_item, text="Delete", command=lambda item_name=item.name: self.delete_menu_item(item_name))
            btn_delete.pack(side=tk.LEFT)

        def add_item():
            name = entry_new_name.get()
            price = float(entry_new_price.get())
            self.add_menu_item(name, price)

        label_new_name = tk.Label(frame_menu, text="New Item Name:")
        label_new_name.pack(pady=5)
        entry_new_name = tk.Entry(frame_menu)
        entry_new_name.pack()

        label_new_price = tk.Label(frame_menu, text="New Item Price (Rs.):")
        label_new_price.pack(pady=5)
        entry_new_price = tk.Entry(frame_menu)
        entry_new_price.pack()

        btn_add = tk.Button(frame_menu, text="Add Item", command=add_item)
        btn_add.pack(pady=5)

        self.refresh_menu()

    def submit_order(self):
        order_window = tk.Toplevel()
        order_window.title("Order")

        frame_order = tk.Frame(order_window)
        frame_order.pack(padx=10, pady=10)

        label_menu = tk.Label(frame_order, text="Menu")
        label_menu.pack()

        for i, item in enumerate(self.menu):
            frame_item = tk.Frame(frame_order)
            frame_item.pack()

            checkbox_var = tk.IntVar()
            checkbox = tk.Checkbutton(frame_item, text=item.name, variable=checkbox_var)
            checkbox.pack(side=tk.LEFT)
            self.checkboxes.append(checkbox_var)

            quantity_var = tk.IntVar()
            quantity_var.set(1)
            quantity_entry = tk.Entry(frame_item, textvariable=quantity_var, width=5)
            quantity_entry.pack(side=tk.LEFT)
            self.quantities.append(quantity_var)

            btn_increase = tk.Button(frame_item, text="+", command=lambda idx=i: self.increase_quantity(idx))
            btn_increase.pack(side=tk.LEFT)

            btn_decrease = tk.Button(frame_item, text="-", command=lambda idx=i: self.decrease_quantity(idx))
            btn_decrease.pack(side=tk.LEFT)

        btn_submit_order = tk.Button(order_window, text="Submit Order", command=self.calculate_bill)
        btn_submit_order.pack(pady=10)

    def increase_quantity(self, index):
        current_quantity = self.quantities[index].get()
        self.quantities[index].set(current_quantity + 1)

    def decrease_quantity(self, index):
        current_quantity = self.quantities[index].get()
        if current_quantity > 1:
            self.quantities[index].set(current_quantity - 1)

    def calculate_bill(self):
        total = 0
        ordered_items = ""
        for i, item in enumerate(self.menu):
            if self.checkboxes[i].get() == 1:
                quantity = self.quantities[i].get()
                total += item.price * quantity
                ordered_items += f"{item.name} (Qty: {quantity})\n"
        total_with_tax = total + (total * 0.002 * len(self.menu))
        messagebox.showinfo("Bill", f"Total bill: Rs. {total_with_tax:.2f} (Including 0.2% tax)\n\nOrdered Items:\n{ordered_items}")

    def refresh_menu(self):
        menu_text.delete(1.0, tk.END)
        for item in self.menu:
            menu_text.insert(tk.END, f"{item.name}: Rs. {item.price:.2f}\n")


# Create the CafeBillingApplication instance
cafe = CafeBillingApplication()

# Create the main window
window = tk.Tk()
window.title("Cafe Billing Application")

# Create and arrange the widgets for managing the menu
frame_menu_management = tk.Frame(window)
frame_menu_management.pack(padx=10, pady=10)

btn_display_menu = tk.Button(frame_menu_management, text="Menu", command=cafe.display_menu)
btn_display_menu.pack(pady=5)

menu_text = tk.Text(frame_menu_management, width=30, height=10)
menu_text.pack()

# Create and arrange the widgets for ordering and calculating the bill
frame_order = tk.Frame(window)
frame_order.pack(padx=10, pady=10)

btn_order = tk.Button(frame_order, text="Order", command=cafe.submit_order)
btn_order.pack(pady=5)

# Start the GUI event loop
window.mainloop()
