import tkinter as tk
from tkinter import ttk, messagebox

def calculate():
    try:
        ratio_chaos_per_divine = float(entry_ratio.get())
        divines_invested = float(entry_invested.get())
        base_chaos_value = divines_invested * ratio_chaos_per_divine

        results = []
        for i in range(1):
            items_per_chaos = float(item_inputs[i]["items_per_chaos"].get())
            current_ratio = float(item_inputs[i]["current_ratio"].get())

            buy_value = base_chaos_value * items_per_chaos
            sell_value = buy_value / current_ratio
            profit_ratio = sell_value / (base_chaos_value / ratio_chaos_per_divine)

            results.append((buy_value, sell_value, profit_ratio))

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, f"Total Profit: {profit_ratio:.1f}\n\n")
        for i, (buy, sell, profit) in enumerate(results, start=1):
            result_text.insert(
                tk.END,
                f"Item {i}:\n"
                f"  Buy Value (items): {buy:.2f}\n"
                f"  Sell Value (divines): {sell:.2f}\n"
                f"  Profit Ratio: {profit:.3f}\n"
                f"{'-'*30}\n"
            )

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")


root = tk.Tk()
root.title("POE2 Arbitrage Calculator")
root.geometry("500x600")
root.resizable(False, False)

# --- Global inputs ---
tk.Label(root, text="1 Divine =").pack(pady=2)
entry_ratio = tk.Entry(root)
entry_ratio.pack()

tk.Label(root, text="Total Divine Orbs Invested:").pack(pady=2)
entry_invested = tk.Entry(root)
entry_invested.pack()

ttk.Separator(root, orient="horizontal").pack(fill="x", pady=5)

item_inputs = []
for i in range(1):
    frame = tk.LabelFrame(root, text=f"Item {i+1}", padx=10, pady=5)
    frame.pack(fill="x", padx=10, pady=5)

    tk.Label(frame, text="Items per chaos orb:").grid(row=1, column=0, sticky="w")
    items_per_chaos = tk.Entry(frame, width=10)
    items_per_chaos.grid(row=1, column=1)

    tk.Label(frame, text="Current ratio (1 Divine = ? of this item):").grid(row=2, column=0, sticky="w")
    current_ratio = tk.Entry(frame, width=10)
    current_ratio.grid(row=2, column=1)

    item_inputs.append({
        "items_per_chaos": items_per_chaos,
        "current_ratio": current_ratio
    })

# --- Calculate Button ---
tk.Button(root, text="Calculate", command=calculate).pack(pady=10)

# --- Results Box ---
result_text = tk.Text(root, height=15, width=60)
result_text.pack(padx=10, pady=5)

root.mainloop()