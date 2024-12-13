import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import tkinter as tk


class PolynomialArithmeticApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Polynomial Arithmetic in GF(2^m)")
        self.root.geometry("900x600") 
        self.root.resizable(True, True)

        # Set up ttkbootstrap style
        self.style = ttk.Style("cosmo")

        # Create custom styles with smaller fonts
        self.style.configure('Custom.TRadiobutton', font=('Helvetica', 12))
        self.style.configure('Custom.TLabel', font=('Helvetica', 12))
        self.style.configure('Custom.TEntry', font=('Helvetica', 12))
        self.style.configure('Custom.TButton', font=('Helvetica', 12))
        self.style.configure('Custom.TLabelframe.Label', font=('Helvetica', 12, 'bold'))

        # Define a custom style for disabled Entry widgets
        self.style.configure('Custom.TEntry',
                             fieldbackground='white',
                             foreground='black')

        self.style.map('Custom.TEntry',
                       fieldbackground=[('disabled', 'lightgray')],
                       foreground=[('disabled', 'gray')])              

        # Initialize irreducible polynomials up to degree 8
        self.irreducible_polynomials = {
            2: 0b111,          # x^2 + x + 1
            3: 0b1011,         # x^3 + x + 1
            4: 0b10011,        # x^4 + x + 1
            5: 0b100101,       # x^5 + x^2 + 1
            6: 0b1000011,      # x^6 + x + 1
            7: 0b10000011,     # x^7 + x + 1
            8: 0b100011011,    # x^8 + x^4 + x^3 + x + 1
        }

        self.create_widgets()
        self.root.bind('<Return>', self.compute)  # Bind Enter key to compute method

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding=30)
        main_frame.pack(fill='both', expand=True)

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)

        options_frame = ttk.Frame(main_frame)
        options_frame.grid(row=0, column=0, pady=10, sticky='w')

        options_frame.columnconfigure(0, weight=0)
        options_frame.columnconfigure(1, weight=0)

        degree_frame = ttk.Labelframe(options_frame, text="Select Degree m\n", padding=0, style='Custom.TLabelframe')
        degree_frame.grid(row=0, column=0, padx=10, sticky='w')

        self.degree_var = tk.IntVar()
        degrees = sorted(self.irreducible_polynomials.keys())
        self.degree_var.set(degrees[0])
        degree_menu = ttk.Combobox(degree_frame, textvariable=self.degree_var, values=degrees, width=10, font=('Helvetica', 12))
        degree_menu.pack(padx=10, pady=10)

        format_frame = ttk.Labelframe(options_frame, text="Output Format", padding=0, style='Custom.TLabelframe')
        format_frame.grid(row=0, column=1, padx=10, sticky='w')

        self.format_var = tk.StringVar()
        self.format_var.set("Binary")

        formats = ["Binary", "Hexadecimal"]
        for fmt in formats:
            ttk.Radiobutton(
                format_frame, text=fmt, variable=self.format_var, value=fmt, bootstyle="toolbutton",
                style='Custom.TRadiobutton'
            ).pack(anchor='w', padx=10, pady=5)

        degree_frame.update_idletasks()
        format_frame.update_idletasks()
        max_width = max(degree_frame.winfo_width(), format_frame.winfo_width())
        degree_frame.config(width=max_width)
        format_frame.config(width=max_width)

        instruction_label = ttk.Label(
            main_frame,
            text="Enter polynomials based on the selected format.\nFor Binary: e.g., 1011\nFor Hex: e.g., 0x1b or 1b",
            font=('Helvetica', 12, 'bold')
        )
        instruction_label.grid(row=1, column=0, pady=10, sticky='w')

        input_frame = ttk.Labelframe(main_frame, text="Polynomial Inputs", padding=20, style='Custom.TLabelframe')
        input_frame.grid(row=2, column=0, pady=10, sticky='ew')
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Polynomial A:", style='Custom.TLabel').grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.poly_a_entry = ttk.Entry(input_frame, width=50, font=('Helvetica', 12), style='Custom.TEntry')
        self.poly_a_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        
        ttk.Label(input_frame, text="Polynomial B:", style='Custom.TLabel').grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.poly_b_entry = ttk.Entry(input_frame, width=50, font=('Helvetica', 12), style='Custom.TEntry')
        self.poly_b_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        
        operation_frame = ttk.Labelframe(main_frame, text="Select Operation", padding=20, style='Custom.TLabelframe')
        operation_frame.grid(row=3, column=0, pady=10, sticky='ew')

        self.operation_var = tk.StringVar()
        self.operation_var.set("Addition")

        operations = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo Reduction", "Inverse"]
        for op in operations:
            rb = ttk.Radiobutton(
                operation_frame, text=op, variable=self.operation_var, value=op,
                command=self.toggle_poly_b_entry, bootstyle="primary toolbutton",
                style='Custom.TRadiobutton'
            )
            rb.pack(anchor='w', padx=10, pady=5)

        compute_button = ttk.Button(
            main_frame, text="Compute", command=self.compute_action, bootstyle="success",
            padding=10, width=15, style='Custom.TButton'
        )
        compute_button.grid(row=4, column=0, pady=20)

        result_frame = ttk.Labelframe(main_frame, text="Result", padding=20, style='Custom.TLabelframe')
        result_frame.grid(row=5, column=0, pady=10, sticky='nsew')

        self.result_text = tk.Text(result_frame, font=('Helvetica', 12), wrap='word', height=15)
        self.result_text.pack(fill='both', expand=True, padx=10, pady=10)

        self.toggle_poly_b_entry()

    def toggle_poly_b_entry(self):
        operation = self.operation_var.get()
        if operation in ["Inverse", "Modulo Reduction"]:
            self.poly_b_entry.delete(0, tk.END)
            self.poly_b_entry.config(state='disabled')
        else:
            self.poly_b_entry.config(state='normal')

    def parse_polynomial(self, poly_str):
        input_format = self.format_var.get()
        poly_str = poly_str.strip().lower()

        if not poly_str:
            Messagebox.show_error("Empty polynomial input.", title="Invalid Input")
            return None

        try:
            if input_format == "Binary":
                return int(poly_str, 2)
            else:
                if not poly_str.startswith("0x"):
                    poly_str = "0x" + poly_str
                return int(poly_str, 16)
        except ValueError:
            Messagebox.show_error("Invalid polynomial format for the selected input type.", title="Invalid Input")
            return None

    def format_polynomial(self, poly_int):
        fmt = self.format_var.get()
        if fmt == "Binary":
            return bin(poly_int)[2:]
        else:
            return hex(poly_int)[2:]

    def polynomial_to_string(self, poly):
        if poly == 0:
            return '0'
        terms = []
        degree = poly.bit_length() - 1
        for i in reversed(range(degree + 1)):
            if poly & (1 << i):
                if i == 0:
                    terms.append('1')
                elif i == 1:
                    terms.append('x')
                else:
                    terms.append(f'x^{i}')
        return ' + '.join(terms)

    def compute(self, event=None):
        self.compute_action()

    def compute_action(self):
        m = self.degree_var.get()
        poly_mod = self.irreducible_polynomials[m]

        a_str = self.poly_a_entry.get().strip()
        b_str = self.poly_b_entry.get().strip()

        if not a_str:
            Messagebox.show_error("Polynomial A is required.", title="Input Error")
            return

        a = self.parse_polynomial(a_str)
        if a is None:
            return

        operation = self.operation_var.get()

        if operation not in ["Inverse", "Modulo Reduction"]:
            if not b_str:
                Messagebox.show_error("Polynomial B is required for this operation.", title="Input Error")
                return
            b = self.parse_polynomial(b_str)
            if b is None:
                return
        else:
            b = None

        if operation in ["Addition", "Subtraction"]:
            # In GF(2^m), addition = subtraction = XOR
            result = self.gf2n_poly_add(a, b)
            self.display_result(result)
        elif operation == "Multiplication":
            result = self.polynomial_multiply(a, b, poly_mod, m)
            self.display_result(result)
        elif operation == "Division":
            if b == 0:
                Messagebox.show_error("Division by zero is undefined.", title="Math Error")
                return
            # Division in GF(2^m) = a * inverse(b) mod poly
            try:
                inverse_b = self.polynomial_inverse(b, poly_mod, m)
                quotient = self.polynomial_multiply(a, inverse_b, poly_mod, m)
                # In a field, remainder is always 0 when dividing by a nonzero element
                self.display_division_result(quotient, 0)
            except ValueError as e:
                Messagebox.show_error(str(e), title="Math Error")
        elif operation == "Modulo Reduction":
            result = self.polynomial_mod(a, poly_mod)
            self.display_result(result, prefix="Modulo Reduction Result")
        elif operation == "Inverse":
            try:
                inverse = self.polynomial_inverse(a, poly_mod, m)
                result = self.polynomial_mod(inverse, poly_mod)
                self.display_result(result, prefix="Inverse")
            except Exception as e:
                Messagebox.show_error(str(e), title="Math Error")
        else:
            Messagebox.show_error("Invalid operation selected.", title="Operation Error")

    def display_result(self, result, prefix="Result"):
        result_str = self.format_polynomial(result)
        poly_str = self.polynomial_to_string(result)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, f"{prefix} ({self.format_var.get()}): {result_str}\nPolynomial: {poly_str}")

    def display_division_result(self, quotient, remainder):
        # Quotient and remainder after division in a field
        quotient_str = self.format_polynomial(quotient)
        remainder_str = self.format_polynomial(remainder)
        quotient_poly_str = self.polynomial_to_string(quotient)
        remainder_poly_str = self.polynomial_to_string(remainder)
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(
            tk.END,
            f"Quotient ({self.format_var.get()}): {quotient_str}\n"
            f"Quotient Polynomial: {quotient_poly_str}\n"
            f"Remainder ({self.format_var.get()}): {remainder_str}\n"
            f"Remainder Polynomial: {remainder_poly_str}"
        )

    def polynomial_multiply(self, a, b, mod_poly, m):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & (1 << m):
                a ^= mod_poly
        return result & ((1 << m) - 1)

    def polynomial_mod(self, poly, mod_poly):
        poly_degree = poly.bit_length() - 1
        mod_degree = mod_poly.bit_length() - 1

        while poly_degree >= mod_degree:
            shift = poly_degree - mod_degree
            poly ^= mod_poly << shift
            poly_degree = poly.bit_length() - 1

        return poly

    # Helper functions for Extended Euclidean Algorithm
    def gf2n_poly_add(self, a, b):
        return a ^ b

    def gf2n_poly_mul(self, a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            a <<= 1
            b >>= 1
        return result

    def gf2n_poly_divmod(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Polynomial division by zero.")
        quotient = 0
        remainder = a
        deg_b = b.bit_length() - 1
        while remainder.bit_length() >= b.bit_length():
            shift = remainder.bit_length() - b.bit_length()
            quotient ^= (1 << shift)
            remainder ^= b << shift
        return quotient, remainder

    def gf2n_extended_gcd(self, a, b):
        x0, x1 = 1, 0
        y0, y1 = 0, 1
        while b != 0:
            q, r = self.gf2n_poly_divmod(a, b)
            a, b = b, r
            x0, x1 = x1, self.gf2n_poly_add(x0, self.gf2n_poly_mul(q, x1))
            y0, y1 = y1, self.gf2n_poly_add(y0, self.gf2n_poly_mul(q, y1))
        return a, x0, y0  # gcd, x, y

    def gf2n_modinv(self, a, modulus):
        gcd, x, _ = self.gf2n_extended_gcd(a, modulus)
        if gcd != 1:
            raise ValueError("No inverse exists for the given polynomial modulo modulus over GF(2^n)")
        # Reduce x modulo the modulus polynomial
        inverse = self.polynomial_mod(x, modulus)
        return inverse

    def polynomial_inverse(self, a, mod_poly, m):
        return self.gf2n_modinv(a, mod_poly)


if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = PolynomialArithmeticApp(root)
    root.mainloop()
