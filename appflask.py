from flask import Flask, render_template, request, redirect, url_for, session
import sys
import os
import openai

app = Flask(__name__)
app.secret_key = "secret_key"  

# Set your OpenAI API 
openai.api_key = "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"

# Irreducible polynomials up to degree 8
IRREDUCIBLE_POLYNOMIALS = {
    2: 0b111,          # x^2 + x + 1
    3: 0b1011,         # x^3 + x + 1
    4: 0b10011,        # x^4 + x + 1
    5: 0b100101,       # x^5 + x^2 + 1
    6: 0b1000011,      # x^6 + x + 1
    7: 0b10000011,     # x^7 + x + 1
    8: 0b100011011,    # x^8 + x^4 + x^3 + x + 1
}

def gf2_poly_add(a, b):
    return a ^ b

def gf2_poly_mul(a, b):
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        b >>= 1
    return result

def gf2_poly_divmod(a, b):
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

def gf2_extended_gcd(a, b):
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    while b != 0:
        q, r = gf2_poly_divmod(a, b)
        a, b = b, r
        x0, x1 = x1, gf2_poly_add(x0, gf2_poly_mul(q, x1))
        y0, y1 = y1, gf2_poly_add(y0, gf2_poly_mul(q, y1))
    return a, x0, y0  # gcd, x, y

def gf2_poly_mod(a, modulus):
    _, remainder = gf2_poly_divmod(a, modulus)
    return remainder

def polynomial_inverse(a, mod_poly, m):
    if a == 0:
        raise ValueError("Zero has no multiplicative inverse.")
    gcd, x, _ = gf2_extended_gcd(a, mod_poly)
    if gcd != 1:
        raise ValueError("No multiplicative inverse exists for the given polynomial modulo the modulus polynomial.")
    inverse = gf2_poly_mod(x, mod_poly)
    return inverse

def parse_polynomial(poly_str, input_format):
    poly_str = poly_str.strip().lower()
    if not poly_str:
        raise ValueError("Empty polynomial input.")
    try:
        if input_format == "Binary":
            return int(poly_str, 2)
        else:
            if not poly_str.startswith("0x"):
                poly_str = "0x" + poly_str
            return int(poly_str, 16)
    except ValueError:
        raise ValueError("Invalid polynomial format for the selected input type.")

def format_polynomial(poly_int, fmt):
    if fmt == "Binary":
        return bin(poly_int)[2:]
    else:
        return hex(poly_int)[2:]

def polynomial_to_string(poly):
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

def polynomial_multiply(a, b, mod_poly, m):
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & (1 << m):
            a ^= mod_poly
    return result & ((1 << m) - 1)

def polynomial_mod(poly, mod_poly):
    poly_degree = poly.bit_length() - 1
    mod_degree = mod_poly.bit_length() - 1
    while poly_degree >= mod_degree:
        shift = poly_degree - mod_degree
        poly ^= mod_poly << shift
        poly_degree = poly.bit_length() - 1
    return poly

@app.route("/")
def welcome():
    return render_template("welcome.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    degrees = sorted(IRREDUCIBLE_POLYNOMIALS.keys())
    formats = ["Binary", "Hexadecimal"]
    operations = ["Addition", "Subtraction", "Multiplication", "Division", "Modulo Reduction", "Inverse"]

    result = None
    error = None
    explanation = session.pop('explanation', None)
    selected_degree = degrees[0]
    selected_format = formats[0]
    selected_operation = operations[0]
    poly_a = ""
    poly_b = ""

    if request.method == "POST":
        try:
            selected_degree = int(request.form.get("degree", degrees[0]))
            selected_format = request.form.get("format", formats[0])
            selected_operation = request.form.get("operation", operations[0])
            poly_a = request.form.get("poly_a", "").strip()
            poly_b = request.form.get("poly_b", "").strip()

            m = selected_degree
            poly_mod = IRREDUCIBLE_POLYNOMIALS[m]

            if not poly_a:
                raise ValueError("Polynomial A is required.")
            a = parse_polynomial(poly_a, selected_format)

            if selected_operation not in ["Inverse", "Modulo Reduction"]:
                if not poly_b:
                    raise ValueError("Polynomial B is required for this operation.")
                b = parse_polynomial(poly_b, selected_format)
            else:
                b = None

            if selected_operation in ["Addition", "Subtraction"]:
                res_int = gf2_poly_add(a, b)
                res_str = format_polynomial(res_int, selected_format)
                poly_str = polynomial_to_string(res_int)
                result = {
                    "title": "Result",
                    "res_str": res_str,
                    "poly_str": poly_str,
                    "format": selected_format
                }

            elif selected_operation == "Multiplication":
                res_int = polynomial_multiply(a, b, poly_mod, m)
                res_str = format_polynomial(res_int, selected_format)
                poly_str = polynomial_to_string(res_int)
                result = {
                    "title": "Result",
                    "res_str": res_str,
                    "poly_str": poly_str,
                    "format": selected_format
                }

            elif selected_operation == "Division":
                if b == 0:
                    raise ValueError("Division by zero is undefined.")
                inverse_b = polynomial_inverse(b, poly_mod, m)
                quotient = polynomial_multiply(a, inverse_b, poly_mod, m)
                remainder = 0
                q_str = format_polynomial(quotient, selected_format)
                q_poly_str = polynomial_to_string(quotient)
                r_str = format_polynomial(remainder, selected_format)
                r_poly_str = polynomial_to_string(remainder)
                result = {
                    "title": "Division Result",
                    "quotient_str": q_str,
                    "quotient_poly_str": q_poly_str,
                    "remainder_str": r_str,
                    "remainder_poly_str": r_poly_str,
                    "format": selected_format
                }

            elif selected_operation == "Modulo Reduction":
                res_int = polynomial_mod(a, poly_mod)
                res_str = format_polynomial(res_int, selected_format)
                poly_str = polynomial_to_string(res_int)
                result = {
                    "title": "Modulo Reduction Result",
                    "res_str": res_str,
                    "poly_str": poly_str,
                    "format": selected_format
                }

            elif selected_operation == "Inverse":
                inv = polynomial_inverse(a, poly_mod, m)
                inv_mod = polynomial_mod(inv, poly_mod)
                res_str = format_polynomial(inv_mod, selected_format)
                poly_str = polynomial_to_string(inv_mod)
                result = {
                    "title": "Inverse",
                    "res_str": res_str,
                    "poly_str": poly_str,
                    "format": selected_format
                }

            else:
                raise ValueError("Invalid operation selected.")

            if result:
                session['last_operation'] = {
                    'degree': selected_degree,
                    'format': selected_format,
                    'operation': selected_operation,
                    'poly_a': poly_a,
                    'poly_b': poly_b,
                    'result': result
                }

        except Exception as e:
            error = str(e)

    return render_template(
        "index.html", 
        degrees=degrees,
        formats=formats,
        operations=operations,
        selected_degree=selected_degree,
        selected_format=selected_format,
        selected_operation=selected_operation,
        poly_a=poly_a,
        poly_b=poly_b,
        result=result,
        error=error,
        explanation=explanation
    )

@app.route("/explain", methods=["POST"])
def explain():
    operation_details = session.get('last_operation', None)
    if not operation_details:
        return "No operation to explain.", 400

    prompt = f"""
Explain step-by-step the polynomial arithmetic operation performed.

Operation: {operation_details['operation']}
Degree m: {operation_details['degree']}
Format: {operation_details['format']}
Polynomial A: {operation_details['poly_a']}
Polynomial B: {operation_details['poly_b']}
Result: {operation_details['result']}

Details:
- The operation is done in GF(2^m).
- Show how the polynomials are represented.
- Show all intermediate steps of the computation.
- Provide a clear, human-readable explanation.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.7
    )

    explanation = response.choices[0].message.content.strip()
    session['explanation'] = explanation
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
