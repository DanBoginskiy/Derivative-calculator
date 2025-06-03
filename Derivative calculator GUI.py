import tkinter as tk
import re
 


# ============================================================================
# Global Variables
# ============================================================================

tokens = []  # Список для збереження введених символів
text_field = None  # Поле для відображення виразу/результату
window = None  # Головне вікно програми (додано)


# ============================================================================
# Button Functions (Logic)
# ============================================================================

def update_text_field(value=None):
    """Оновлює текстове поле."""
    global text_field
    if value is not None:
        text_field.config(text=str(value))
    else:
        text_field.config(text="".join(tokens))

def add():
    tokens.append('+')
    update_text_field()

def sub():
    tokens.append('-')
    update_text_field()

def mult():
    tokens.append('*')
    update_text_field()

def div():
    tokens.append('/')
    update_text_field()

def exp():
    tokens.append('^')
    update_text_field()

def num_9():
    tokens.append('9')
    update_text_field()

def num_8():
    tokens.append('8')
    update_text_field()

def num_7():
    tokens.append('7')
    update_text_field()

def num_6():
    tokens.append('6')
    update_text_field()

def num_5():
    tokens.append('5')
    update_text_field()

def num_4():
    tokens.append('4')
    update_text_field()

def num_3():
    tokens.append('3')
    update_text_field()

def num_2():
    tokens.append('2')
    update_text_field()

def num_1():
    tokens.append('1')
    update_text_field()

def num_0():
    tokens.append('0')
    update_text_field()  

def dot():
    tokens.append('.')
    update_text_field()

def left_parhentheses():
    tokens.append('(')
    update_text_field()

def right_parhentheses():
    tokens.append(')')
    update_text_field()

def delete():
    if tokens:
        tokens.pop()
        update_text_field()

def sqrt_func():
    tokens.append('sqrt(')
    update_text_field()

def sin_func():
    tokens.append('sin(')
    update_text_field()

def cos_func():
    tokens.append('cos(')
    update_text_field()

def tan_func():
    tokens.append('tan(')
    update_text_field()

def cot_func():
    tokens.append('сot(') 
    update_text_field()

def log_func():
    tokens.append('log(') 
    update_text_field()

def coma_func():
    tokens.append(',')
    update_text_field()

def e_const():
    tokens.append('e')
    update_text_field()

def pi_const():
    tokens.append('pi')
    update_text_field()

def derivative_func():
    tokens.append('d/dx(') 
    update_text_field()

def clear_all():
    tokens.clear()
    update_text_field()

def x():
    tokens.append('x') 
    update_text_field()

def clear_all():
    global tokens
    tokens = []
    update_text_field()

def eq():
    """Обчислює вираз або похідну, залежно від вводу."""
    global tokens
    line = "".join(tokens)
    print(f"Введений вираз: {line}")
    print(f"is_fraction(tokens): {is_fraction(tokens)}")
    print(f"is_multiplication(tokens): {is_multiplication(tokens)}")
    print(f"is_power(tokens): {is_power(tokens)}")

    if line.count('(') != line.count(')'):
        tokens = ['Error: Parentheses don`t match']
        update_text_field()
        return

    tokens = change(tokens)
    line = "".join(tokens)
    print(f"Вираз для обчислення: {line}")

    try:
        if line.startswith("d/dx("):
            equation_string = line[5:-1].strip()
            print(f"Рядок всередині d/dx: '{equation_string}'")
            tokenized_equation = tokenize(equation_string)
            print(f"Токени всередині d/dx: {tokenized_equation}")

            if is_fraction(tokenized_equation):
                slash_index = [i for i, token in enumerate(tokenized_equation) if token == '/' and sum(1 for t in tokenized_equation[:i] if t == '(') == sum(1 for t in tokenized_equation[:i] if t == ')')][0]
                u_tokens = tokenized_equation[:slash_index]
                v_tokens = tokenized_equation[slash_index + 1:]
                print("Виявлено ділення на верхньому рівні")
                print(f"Токени чисельника: {u_tokens}")
                print(f"Токени знаменника: {v_tokens}")
                u_prime = part_derivative(u_tokens)
                v_prime = part_derivative(v_tokens)
                result_tokens = ['(', '(', *u_prime, ')', '*', '(', *v_tokens, ')', '-', '(', *u_tokens, ')', '*', '(', *v_prime, ')', ')', '/', '(', '(', *v_tokens, ')', '^', '2', ')']
                tokens = ["d/dx = "] + result_tokens
                update_text_field("".join(tokens))
                print(f"Похідна: {''.join(result_tokens)}")
                return
            elif is_multiplication(tokenized_equation):
                star_index = [i for i, token in enumerate(tokenized_equation) if token == '*' and sum(1 for t in tokenized_equation[:i] if t == '(') == sum(1 for t in tokenized_equation[:i] if t == ')')][0]
                u_tokens = tokenized_equation[:star_index]
                v_tokens = tokenized_equation[star_index + 1:]
                print("Виявлено множення на верхньому рівні")
                print(f"Токени першого множника: {u_tokens}")
                print(f"Токени другого множника: {v_tokens}")
                u_prime = part_derivative(u_tokens)
                v_prime = part_derivative(v_tokens)
                result_tokens = ['(', *u_prime, ')', '*', '(', *v_tokens, ')', '+', '(', *u_tokens, ')', '*', '(', *v_prime, ')']
                tokens = ["d/dx = "] + result_tokens
                update_text_field("".join(tokens))
                print(f"Похідна: {''.join(result_tokens)}")
                return
            elif is_power(tokenized_equation):
                hat_index = [i for i, token in enumerate(tokenized_equation) if token == '^' and sum(1 for t in tokenized_equation[:i] if t == '(') == sum(1 for t in tokenized_equation[:i] if t == ')')][0]
                base_tokens = tokenized_equation[:hat_index]
                exponent_tokens = tokenized_equation[hat_index + 1:]
                print("Виявлено степінь на верхньому рівні")
                print(f"Основа: {base_tokens}")
                print(f"Показник: {exponent_tokens}")
                base_prime = part_derivative(base_tokens)
                result_tokens = ['(', *exponent_tokens, ')', '*', '(', *base_tokens, ')', '^', '(', *exponent_tokens, '-', '1', ')', '*', '(', *base_prime, ')']
                tokens = ["d/dx = "] + result_tokens
                update_text_field("".join(tokens))
                print(f"Похідна: {''.join(result_tokens)}")
                return
            else:
                print("Ділення, множення або степінь на верхньому рівні не виявлено, обчислюємо похідну всього виразу")
                input_tokens = tokenize(equation_string)
                derivative_tokens = part_derivative(input_tokens)
                tokens = ["d/dx = "] + derivative_tokens
                update_text_field("".join(tokens))
                print(f"Похідна: {''.join(derivative_tokens)}")
                return

        else:
            answer = eval(line)
            update_text_field(answer)
            print(f"Результат: {answer}")

    except (SyntaxError, NameError, TypeError, ZeroDivisionError, Exception) as e:
        tokens = [f'Error: {e}']
        update_text_field()
        print(f"Помилка обчислення: {e}")


def show_instructions():
    instructions_window = tk.Toplevel(window)
    instructions_window.title("Інструкції")
    instructions_text = tk.Text(instructions_window, width=40, height=15)
    instructions_text.insert(tk.END, "Інструкції з використання калькулятора:\n")
    instructions_text.insert(tk.END, "- Вводьте числа та оператори за допомогою кнопок.\n")
    instructions_text.insert(tk.END, "- Для введення десяткової коми використовуйте кнопку '.'\n")
    instructions_text.insert(tk.END, "- Тригонометричні функції (sin, cos, tan, cot) приймають аргумент у дужках.\n")
    instructions_text.insert(tk.END, "- Логарифми (log) приймають аргумент у дужках.\n")
    instructions_text.insert(tk.END, "- Для введення основи логарифма використовуйте синтаксис 'log(число, основа)'.\n")
    instructions_text.insert(tk.END, "- Кнопка 'del' видаляє останній введений символ.\n")
    instructions_text.insert(tk.END, "- Кнопка 'd/dx'  відображає символ похідної. Обчислення піднесення до степеня двох функцій не реалізовано.\n")
    instructions_text.config(state=tk.DISABLED)
    instructions_text.pack(padx=10, pady=10)


# ============================================================================
# Calculation Functions (Logic)
# ============================================================================


def is_fraction(tokens):
    slash_index = -1
    open_parentheses = 0
    for i, token in enumerate(tokens):
        if token == '(':
            open_parentheses += 1
        elif token == ')':
            open_parentheses -= 1
        elif token == '/' and open_parentheses == 0:
            slash_index = i
            break
    return slash_index > 0 and slash_index < len(tokens) - 1

def is_multiplication(tokens):
    star_indices = [i for i, token in enumerate(tokens) if token == '*' and sum(1 for t in tokens[:i] if t == '(') == sum(1 for t in tokens[:i] if t == ')')]
    return len(star_indices) == 1 and star_indices[0] > 0 and star_indices[0] < len(tokens) - 1

def is_power(tokens):
    hat_index = -1
    open_parentheses = 0
    for i, token in enumerate(tokens):
        if token == '(':
            open_parentheses += 1
        elif token == ')':
            open_parentheses -= 1
        elif token == '**' and open_parentheses == 0:
            hat_index = i
            break
    return hat_index > 0 and hat_index < len(tokens) - 1

def change(t):
    """
    Перетворює токени для eval().
    Замінює математичні функції та константи на їхні відповідники з модуля math
    та змінює оператор піднесення до степеня.
    """
    new_tokens = []
    for token in t:
        if token == 'log(':
            new_tokens.append('math.log(')
        elif token == 'e':
            new_tokens.append(str(math.e))
        elif token == 'pi':
            new_tokens.append(str(math.pi))
        elif token == 'sqrt(':
            new_tokens.append('math.sqrt(')
        elif token == '^':
            new_tokens.append('**')
        elif token == 'sin(':
            new_tokens.append('math.sin(')
        elif token == 'cos(':
            new_tokens.append('math.cos(')
        elif token == 'tan(':
            new_tokens.append('math.tan(')
        elif token == 'cot(':
            new_tokens.append('1/math.tan(')
        else:
            new_tokens.append(token)
    return new_tokens

def part_derivative(tokens):
    derivative_tokens = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
            derivative_tokens.append('0')
        elif token == 'x':
            if i + 1 < len(tokens) and tokens[i + 1] == '**' and i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())):
                power = float(tokens[i + 2])
                derivative_tokens.extend([str(power), '*', 'x'])
                if power > 2:
                    derivative_tokens.extend(['**', str(power - 1)])
                elif power == 2:
                    pass
                else:
                    pass
                i += 2
            else:
                derivative_tokens.append('1')
        elif token == '*':
            i += 1
        elif token == '^':
            i += 1
        elif token == 'sqrt':
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['1', '/', '(', '2', '*', 'sqrt(', 'x', ')', ')'])
                i += 3
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else:
                derivative_tokens.append('0')
        elif token == 'cos':
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['-sin', '(', 'x', ')'])
                i += 3
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == '*' and i + 4 < len(tokens) and tokens[i + 4] == 'x' and i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = float(tokens[i + 2])
                derivative_tokens.extend(['-', str(a), '*', 'sin', '(', str(a), '*', 'x', ')'])
                i += 5
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else:
                derivative_tokens.append('0')
        elif token == 'sin':
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['cos', '(', 'x', ')'])
                i += 3
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == '*' and i + 4 < len(tokens) and tokens[i + 4] == 'x' and i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = float(tokens[i + 2])
                derivative_tokens.extend([str(a), '*', 'cos', '(', str(a), '*', 'x', ')'])
                i += 5
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else:
                derivative_tokens.append('0')
        elif token == 'tan':
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['1', '/', '(', 'cos', '(', 'x', ')', '^', '2', ')'])
                i += 3
            elif i + 2 < len(tokens) and (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit()) and i + 3 < len(tokens) and tokens[i + 3] == '*' and i + 4 < len(tokens) and tokens[i + 4] == 'x' and i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = float(tokens[i + 2])
                derivative_tokens.extend([str(a), '/', '(', 'cos', '(', str(a), '*', 'x', ')', '^', '2', ')'])
                i += 5
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else:
                derivative_tokens.append('0')
        elif token == 'ctg':
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['-1', '/', '(', 'sin', '(', 'x', ')', '^', '2', ')'])
                i += 3
            elif i + 2 < len(tokens) and (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit()) and i + 3 < len(tokens) and tokens[i + 3] == '*' and i + 4 < len(tokens) and tokens[i + 4] == 'x' and i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = float(tokens[i + 2])
                derivative_tokens.extend(['-', str(a), '/', '(', 'sin', '(', str(a), '*', 'x', ')', '^', '2', ')'])
                i += 5
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else:
                derivative_tokens.append('0')
        elif token == 'ln':
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['1', '/', 'x'])
                i += 3
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == '*' and i + 4 < len(tokens) and tokens[i + 4] == 'x' and i + 5 < len(tokens) and tokens[i + 5] == ')':
                derivative_tokens.extend(['1', '/', 'x'])
                i += 5
            elif i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else:
                derivative_tokens.append('0')
        elif token == 'e':
            if i + 1 < len(tokens) and tokens[i + 1] == '^' and i + 2 < len(tokens) and tokens[i + 2] == 'x' and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['e', '^', '(', 'x', ')'])
                i += 3
            elif i + 1 < len(tokens) and tokens[i + 1] == '^' and i + 2 < len(tokens) and (tokens[i + 2].isdigit() or (tokens[i + 2][0] == '-' and tokens[i + 2][1:].isdigit())) and i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            elif i + 1 < len(tokens) and tokens[i + 1] == '^' and i + 2 < len(tokens) and '(' in tokens[i+2:]:
                # Обробка складнішого показника, що містить 'x'
                exponent_tokens = []
                balance = 0
                start_index = i + 2
                for j in range(start_index, len(tokens)):
                    exponent_tokens.append(tokens[j])
                    if tokens[j] == '(':
                        balance += 1
                    elif tokens[j] == ')':
                        balance -= 1
                        if balance == 0:
                            break
                if exponent_tokens:
                    exponent_prime = part_derivative(exponent_tokens[:-1]) 
                    derivative_tokens.extend(['(', 'e', '^', '(', *exponent_tokens, ')', ')', '*', '(', *exponent_prime, ')'])
                    i += (len(exponent_tokens) + 1) 
                else:
                    derivative_tokens.extend(['e', '^', '(', 'x', ')'])
                    i += 1
            else:
                derivative_tokens.append('e') 
        else:
            derivative_tokens.append(token)
        i += 1
    return derivative_tokens


def tokenize(expression):
    return re.findall(r'(\b\w+\b|[\+\-\/\^\(\),]|(?:\d+\.\d*)|\d+|\*\*|\*)', expression)


# ============================================================================
# UI
# ============================================================================

def create_calculator_window():
    """Створює та відображає вікно калькулятора з усіма кнопками та текстовим полем."""
    global window, text_field
    #Window
    window = tk.Tk()
    window.geometry("650x650")
    window.title('calculator')
    #Text field
    text_field = tk.Label(window, text="", bg='white', width=60, height=5, font=('Arial', 16), anchor='e', relief='sunken', borderwidth=2)
    text_field.grid(row=0, column=0, columnspan=6, padx=5, pady=10, sticky='ew')

    button_width = 7
    button_height = 2
    button_padx = 5
    button_pady = 5
    button_font = ('Arial', 12)

    # Row 1
    button_sqrt = tk.Button(window, text='√', command=sqrt_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_sqrt.grid(row=1, column=0, padx=5, pady=5)
    button_left_par = tk.Button(window, text='(', command=left_parhentheses, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_left_par.grid(row=1, column=1, padx=5, pady=5)
    button_right_par = tk.Button(window, text=')', command=right_parhentheses, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_right_par.grid(row=1, column=2, padx=5, pady=5)
    button_exp = tk.Button(window, text='^', command=exp, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_exp.grid(row=1, column=3, padx=5, pady=5)
    button_del = tk.Button(window, text='del', command=delete, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font, bg='lightcoral')
    button_del.grid(row=1, column=4, padx=5, pady=5)
    button_c = tk.Button(window, text='C', command=clear_all, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font, bg='lightcoral')
    button_c.grid(row=1, column=5, padx=5, pady=5)

    # Row 2
    button_sin = tk.Button(window, text='sin', command=sin_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_sin.grid(row=2, column=0, padx=5, pady=5)
    button_cos = tk.Button(window, text='cos', command=cos_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_cos.grid(row=2, column=1, padx=5, pady=5)
    button_tan = tk.Button(window, text='tan', command=tan_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_tan.grid(row=2, column=2, padx=5, pady=5)
    button_cot = tk.Button(window, text='cot', command=cot_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_cot.grid(row=2, column=3, padx=5, pady=5)
    button_log = tk.Button(window, text='log', command=log_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_log.grid(row=2, column=4, padx=5, pady=5)
    button_ln = tk.Button(window, text=',', command=coma_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_ln.grid(row=2, column=5, padx=5, pady=5)

    # Row 3
    button_7 = tk.Button(window, text='7', command=num_7, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_7.grid(row=3, column=0, padx=5, pady=5)
    button_8 = tk.Button(window, text='8', command=num_8, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_8.grid(row=3, column=1, padx=5, pady=5)
    button_9 = tk.Button(window, text='9', command=num_9, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_9.grid(row=3, column=2, padx=5, pady=5)
    button_div = tk.Button(window, text='/', command=div, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_div.grid(row=3, column=3, padx=5, pady=5)
    button_e = tk.Button(window, text='e', command=e_const, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_e.grid(row=3, column=4, padx=5, pady=5)
    button_pi = tk.Button(window, text='π', command=pi_const, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_pi.grid(row=3, column=5, padx=5, pady=5)

    # Row 4
    button_4 = tk.Button(window, text='4', command=num_4, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_4.grid(row=4, column=0, padx=5, pady=5)
    button_5 = tk.Button(window, text='5', command=num_5, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_5.grid(row=4, column=1, padx=5, pady=5)
    button_6 = tk.Button(window, text='6', command=num_6, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_6.grid(row=4, column=2, padx=5, pady=5)
    button_mult = tk.Button(window, text='*', command=mult, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_mult.grid(row=4, column=3, padx=5, pady=5)
    button_x = tk.Button(window, text='x',command=x, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_x.grid(row=4, column=4, padx=5, pady=5)
    button_derivative = tk.Button(window, text='d/dx', command=derivative_func, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_derivative.grid(row=4, column=5, padx=5, pady=5)

    # Row 5
    button_1 = tk.Button(window, text='1', command=num_1, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_1.grid(row=5, column=0, padx=5, pady=5)
    button_2 = tk.Button(window, text='2', command=num_2, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_2.grid(row=5, column=1, padx=5, pady=5)
    button_3 = tk.Button(window, text='3', command=num_3, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_3.grid(row=5, column=2, padx=5, pady=5)
    button_sub = tk.Button(window, text='-', command=sub, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_sub.grid(row=5, column=3, padx=5, pady=5)
    button_eq = tk.Button(window, text='=', command=eq, width=button_width * 2 + 1, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_eq.grid(row=5, column=4, columnspan=2, padx=5, pady=5, sticky='ew')

    # Row 6
    button_0 = tk.Button(window, text='0', command=num_0, width=button_width * 2 + 1, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_0.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
    button_dot = tk.Button(window, text='.', command=dot, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_dot.grid(row=6, column=2, padx=5, pady=5)
    button_add = tk.Button(window, text='+', command=add, width=button_width, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_add.grid(row=6, column=3, padx=5, pady=5)
    button_instructions = tk.Button(window, text='Інструкції', command=show_instructions, width=button_width * 2 + 1, height=button_height, padx=button_padx, pady=button_pady, font=button_font)
    button_instructions.grid(row=6, column=4, columnspan=2, padx=5, pady=5, sticky='ew')

    for i in range(7):
        window.columnconfigure(i, weight=1)
    for i in range(7):
        window.rowconfigure(i, weight=1)

    window.mainloop()

if __name__ =='__main__':
    create_calculator_window()
    print(tokens)

