import re

# --- Input Validation Functions ---

def eq_input():
    """
    Prompts the user to enter an equation and validates its correctness
    using regular expressions and basic mathematical notation rules.
    Returns a valid equation string in lowercase.
    """
    # Regular expression for allowed tokens in the equation.
    # ^(?: ... )+$ - means that the entire string must consist of one or more allowed tokens.
    allowed_tokens = re.compile(r'^(?:'
                                r'[0-9]+(?:\.[0-9]*)?|'      # Numbers (integers or decimals, e.g., 2, 3.14)
                                r'[+\-*/^()\{\}]|'          # Operator and parenthesis symbols (+, -, *, /, ^, (, ), {, })
                                r'x|'                       # Variable 'x'
                                r'(?:sin|cos|tan|cth|ln|sqrt)\(|' # Trigonometric and other functions followed by an opening parenthesis
                                r'log\{[0-9]*\}\(|'         # 'log' with optional base in {} followed by an opening parenthesis (e.g., log{2}(x), log{}(x))
                                r'e'                        # Constant 'e' (Euler's number)
                                r')+$')

    while True:
        line = input("Enter equation: ") # Prompt for user input
        line = line.strip()              # Remove leading/trailing whitespace
        line = line.lower()              # Convert the input string to lowercase for easier comparison

        if not line:
            print("Error: Please enter a non-empty equation.")
            continue # Repeat the loop if the string is empty

        # Check for disallowed symbols at the beginning or end of the equation
        # For example: "+x", "x+" or "()"
        if re.search(r'^[+*/^)]|[+\-*/^( ]$', line) is not None:
            print("Error: Invalid equation. Please check leading/trailing symbols.")
            continue

        # Check for double operators (e.g., "x++y", "x**y")
        if re.search(r'[+\-*/^][+\-*/^]', line) is not None:
            print("Error: Invalid equation. Double operators are not allowed.")
            continue

        # Check for matching counts of opening and closing parentheses
        if line.count('(') != line.count(')'):
            print("Error: Invalid equation. Mismatched parentheses.")
            continue
        
        # Final check for full matching of the entire equation against allowed tokens
        if allowed_tokens.fullmatch(line):
            return line # Return the valid equation
        else:
            print("Error: Invalid equation. Contains disallowed symbols or incorrect format.")

# --- Function for (Symbolic) Partial Derivative ---

def part_derivative(tokens):
    """
    Calculates the symbolic partial derivative of a given equation with respect to 'x'.
    This function operates on a tokenized equation and implements basic differentiation rules.
    Its capabilities are limited, as noted in the main part of the program.

    Arguments:
        tokens (list): A list of strings representing the equation's tokens.
                       For example, for "2*x^3" this would be ['2', '*', 'x', '^', '3'].

    Returns:
        list: A list of tokens representing the derivative function.
    """
    derivative_tokens = [] # List to store the tokens of the derivative
    i = 0 # Index for iterating through the tokens

    while i < len(tokens):
        token = tokens[i]

        # Rule: derivative of a constant = 0
        if token.isdigit():
            derivative_tokens.append('0')
        
        # Rule: derivative of x^n (where n is a number)
        elif token == 'x':
            # Check if the next tokens are "^" and a digit (for x^n)
            if i + 1 < len(tokens) and tokens[i + 1] == '^' and \
               i + 2 < len(tokens) and tokens[i + 2].isdigit():
                power = int(tokens[i + 2]) # Get the exponent
                derivative_tokens.extend([str(power), '*', 'x']) # Add n * x
                if power > 2: # If power > 2, add x^(n-1)
                    derivative_tokens.extend(['^', str(power - 1)])
                elif power == 2: # If power is 2, it's just 2*x
                    # Already added '2', '*', 'x', so just proceed
                    pass
                # Move forward by 2 tokens (skip '^' and 'n')
                i += 2
            else: # If it's just 'x' (i.e., x^1), derivative = 1
                derivative_tokens.append('1')
        
        # Rule: derivative of c*f(x) (where c is a constant)
        # This handles cases like 2*x, 3*sin(x), etc.
        elif token == '*' and i > 0 and tokens[i - 1].isdigit():
            constant = int(tokens[i - 1]) # Get the constant before '*'
            if i + 1 < len(tokens) and tokens[i + 1] == 'x':
                # Case c*x^n
                if i + 2 < len(tokens) and tokens[i + 2] == '^' and \
                   i + 3 < len(tokens) and tokens[i + 3].isdigit():
                    power = int(tokens[i + 3])
                    # Replace the previous constant with c * n
                    derivative_tokens[-1] = str(constant * power)
                    derivative_tokens.extend(['*', 'x'])
                    if power > 2:
                        derivative_tokens.extend(['^', str(power - 1)])
                    i += 3 # Skip '^' and 'n'
                else: # Case c*x, derivative = c
                    derivative_tokens[-1] = str(constant) # Replace previous constant with itself
                    i += 1 # Skip 'x'
            else: # If "*" is not followed by "x" after a constant, it's not x^n or x, so keep it as is
                derivative_tokens.append(token)
        
        # Rule: ignore the '^' token, as it's handled with 'x' or 'e'
        elif token == '^':
            # This token is already processed in the preceding 'x' or 'e' blocks,
            # so just skip it.
            pass # No operation, just increment i at the end of the loop

        # Rule: derivative of sqrt(x)
        elif token == 'sqrt':
            # Check for sqrt(x)
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and \
               i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['1', '/', '(', '2', '*', 'sqrt(', 'x', ')', ')'])
                i += 3 # Skip "(", "x", ")"
            # Check for sqrt(number) - derivative is 0
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3 # Skip "(", "number", ")"
            else: # Other sqrt() cases are treated as constants
                derivative_tokens.append('0')
        
        # Rule: derivative of sin(x) and sin(k*x)
        elif token == 'sin':
            # Check for sin(x) -> cos(x)
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and \
               i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['cos','(','x',')'])
                i += 3
            # Check for sin(k*x) -> k*cos(k*x)
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == '*' and \
                 i + 4 < len(tokens) and tokens[i + 4] == 'x' and \
                 i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = int(tokens[i+2])
                derivative_tokens.extend([f'{a}','*','cos','(',f'{a}','*','x',')'])
                i += 5
            # Check for sin(number) -> 0
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else: # Other sin() cases are treated as constants
                derivative_tokens.append('0')
        
        # Rule: derivative of cos(x) and cos(k*x)
        elif token == 'cos':
            # Check for cos(x) -> -sin(x)
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and \
               i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['-','sin','(','x',')'])
                i += 3
            # Check for cos(k*x) -> -k*sin(k*x)
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == '*' and \
                 i + 4 < len(tokens) and tokens[i + 4] == 'x' and \
                 i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = int(tokens[i+2])
                derivative_tokens.extend(['-',f'{a}','*','sin','(',f'{a}','*','x',')'])
                i += 5
            # Check for cos(number) -> 0
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else: # Other cos() cases are treated as constants
                derivative_tokens.append('0')
        
        # Rule: derivative of tan(x) and tan(k*x)
        elif token == 'tan':
            # Check for tan(x) -> 1/cos^2(x)
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and \
               i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['1','/','(','cos','(','x',')','^','2',')'])
                i += 3
            # Check for tan(k*x) -> k/cos^2(k*x)
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == '*' and \
                 i + 4 < len(tokens) and tokens[i + 4] == 'x' and \
                 i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = int(tokens[i+2])
                derivative_tokens.extend([f'{a}','/','(','cos','(',f'{a}','*','x',')','^','2',')'])
                i += 5
            # Check for tan(number) -> 0
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else: # Other tan() cases are treated as constants
                derivative_tokens.append('0')
        
        # Rule: derivative of ctg(x) and ctg(k*x)
        elif token == 'ctg':
            # Check for ctg(x) -> -1/sin^2(x)
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and \
               i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['-','1','/','(','sin','(','x',')','^','2',')'])
                i += 3
            # Check for ctg(k*x) -> -k/sin^2(k*x)
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == '*' and \
                 i + 4 < len(tokens) and tokens[i + 4] == 'x' and \
                 i + 5 < len(tokens) and tokens[i + 5] == ')':
                a = int(tokens[i+2])
                derivative_tokens.extend(['-',f'{a}','/','(','sin','(',f'{a}','*','x',')','^','2',')'])
                i += 5
            # Check for ctg(number) -> 0
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else: # Other ctg() cases are treated as constants
                derivative_tokens.append('0')
        
        # Rule: derivative of ln(x) and ln(k*x)
        elif token == 'ln':
            # Check for ln(x) -> 1/x
            if i + 2 < len(tokens) and tokens[i + 2] == 'x' and \
               i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['1', '/', '(', 'x', ')'])
                i += 3
            # Check for ln(k*x) -> 1/x
            # (d/dx(ln(ax)) = (1/(ax)) * a = 1/x)
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == '*' and \
                 i + 4 < len(tokens) and tokens[i + 4] == 'x' and \
                 i + 5 < len(tokens) and tokens[i + 5] == ')':
                derivative_tokens.extend(['1', '/', '(', 'x', ')'])
                i += 5
            # Check for ln(number) -> 0
            elif i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.append('0')
                i += 3
            else: # Other ln() cases are treated as constants
                derivative_tokens.append('0')
        
        # Rule: derivative of log{base}(x) and log(x) (base 10)
        elif token == 'log':
            # Check for log{base}(k*x)
            if i + 1 < len(tokens) and tokens[i + 1] == '{' and \
               i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
               i + 3 < len(tokens) and tokens[i + 3] == '}' and \
               i + 4 < len(tokens) and tokens[i + 4] == '(' and \
               i + 5 < len(tokens) and tokens[i + 5].isdigit() and \
               i + 6 < len(tokens) and tokens[i + 6] == '*' and \
               i + 7 < len(tokens) and tokens[i + 7] == 'x' and \
               i + 8 < len(tokens) and tokens[i + 8] == ')':
                base = tokens[i + 2]
                derivative_tokens.extend(['1','/','(','x','*','ln','(',f'{base}',')',')'])
                i += 8
            # Check for log{base}(x)
            elif i + 1 < len(tokens) and tokens[i + 1] == '{' and \
                 i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == '}' and \
                 i + 4 < len(tokens) and tokens[i + 4] == '(' and \
                 i + 5 < len(tokens) and tokens[i + 5] == 'x' and \
                 i + 6 < len(tokens) and tokens[i + 6] == ')':
                base = tokens[i + 2]
                derivative_tokens.extend(['1','/','(','x','*','ln','(',f'{base}',')',')'])
                i += 6
            # Check for log{}(k*x) - base 10
            elif i + 1 < len(tokens) and tokens[i + 1] == '{' and \
                 i + 2 < len(tokens) and tokens[i + 2] == '}' and \
                 i + 3 < len(tokens) and tokens[i + 3] == '(' and \
                 i + 4 < len(tokens) and tokens[i + 4].isdigit() and \
                 i + 5 < len(tokens) and tokens[i + 5] == '*' and \
                 i + 6 < len(tokens) and tokens[i + 6] == 'x' and \
                 i + 7 < len(tokens) and tokens[i + 7] == ')':
                derivative_tokens.extend(['1','/','(','x','*','ln','(','10',')',')'])
                i += 7
            # Check for log{}(x) - base 10
            elif i + 1 < len(tokens) and tokens[i + 1] == '{' and \
                 i + 2 < len(tokens) and tokens[i + 2] == '}' and \
                 i + 3 < len(tokens) and tokens[i + 3] == '(' and \
                 i + 4 < len(tokens) and tokens[i + 4] == 'x' and \
                 i + 5 < len(tokens) and tokens[i + 5] == ')':
                derivative_tokens.extend(['1','/','(','x','*','ln','(','10',')',')'])
                i += 5
            # Check for log(k*x) (without base in {}) - base 10
            elif i + 1 < len(tokens) and tokens[i + 1] == '(' and \
                 i + 2 < len(tokens) and tokens[i + 2].isdigit() and \
                 i + 3 < len(tokens) and tokens[i + 3] == '*' and \
                 i + 4 < len(tokens) and tokens[i + 4] == 'x' and \
                 i + 5 < len(tokens) and tokens[i + 5] == ')':
                derivative_tokens.extend(['1','/','(','x','*','ln','(','10',')',')'])
                i += 5
            # Check for log(x) (without base in {}) - base 10
            elif i + 1 < len(tokens) and tokens[i + 1] == '(' and \
                 i + 2 < len(tokens) and tokens[i + 2] == 'x' and \
                 i + 3 < len(tokens) and tokens[i + 3] == ')':
                derivative_tokens.extend(['1','/','(','x','*','ln','(','10',')',')'])
                i += 3
            # Other log() cases are treated as constants
            else:
                derivative_tokens.append('0')
        
        # Rule: derivative of e^x and e^(k*x)
        elif token == 'e':
            # Check for e^x -> e^x
            if i + 1 < len(tokens) and tokens[i + 1] == '^' and \
               i + 2 < len(tokens) and tokens[i + 2] == 'x':
                derivative_tokens.extend(['e','^','x'])
                i += 2
            # Check for e^(k*x) -> k*e^(k*x)
            elif i + 1 < len(tokens) and tokens[i + 1] == '^' and \
                 i + 2 < len(tokens) and tokens[i + 2] == '(' and \
                 i + 3 < len(tokens) and tokens[i + 3].isdigit() and \
                 i + 4 < len(tokens) and tokens[i + 4] == '*' and \
                 i + 5 < len(tokens) and tokens[i + 5] == 'x' and \
                 i + 6 < len(tokens) and tokens[i + 6] == ')':
                coef = int(tokens[i+3])
                derivative_tokens.extend([f'{coef}','*','e','^','(',f'{coef}','*','x',')'])
                i += 6
            # Other 'e' cases are treated as constants (e.g., just 'e')
            else:
                derivative_tokens.append('0')
        
        else:
            # If the token is not a recognized function, 'x', or a number,
            # it's added to the derivative without changes (e.g., operators)
            derivative_tokens.append(token)
        
        i += 1 # Move to the next token
    return derivative_tokens

# --- Tokenization Function ---

def tokenize(eq_components):
    """
    Splits the input string (or list of strings) into individual tokens:
    numbers, operators, variables, and function names.

    Arguments:
        eq_components (str or list): The equation as a string or a list of equation parts.

    Returns:
        list: A list of tokens.
    """
    all_tokens = []
    # Determine if the input is a list or a single string
    if isinstance(eq_components, list):
        for component in eq_components:
            # Finds all sequences of digits (with or without a decimal part),
            # or single operator/parenthesis symbols,
            # or sequences of letters/underscores (for function/variable names)
            tokens = re.findall(r'\d+\.?\d*|[+\-*/^(){}]|[a-zA-Z_]\w*', component)
            all_tokens.extend(tokens)
    elif isinstance(eq_components, str):
        tokens = re.findall(r'\d+\.?\d*|[+\-*/^(){}]|[a-zA-Z_]\w*', eq_components)
        all_tokens.extend(tokens)
    return all_tokens

# --- Main Program Execution ---

if __name__ == "__main__":
    # Display information about allowed symbols and functions to the user
    print(r'''
Allowed Symbols and Functions:
Numbers: Use integers and decimal numbers (e.g., 2, 3.14, -5).
Variable: The variable is denoted by the letter x.
Operators: The following basic mathematical operators are allowed:
+ (addition)
- (subtraction)
* (multiplication)
/ (division)
^ (exponentiation)
Parentheses: Use round parentheses () to group expressions and define the order of operations,
and curly braces {} to put the base of the logarithm.
Functions: The following functions are supported (the function argument must always be in round parentheses):
sin(x) (sine)
cos(x) (cosine)
tan(x) (tangent)
cth(x) (cotangent)
ln(x) (natural logarithm)
log(x) (base-10 logarithm if no base specified, or log{base}(x))
sqrt(x) (square root)
e (Euler's number, the base of the natural logarithm)
          
Limitations (IMPORTANT):
The calculator only supports differentiation with respect to the variable x.
The calculation of the derivative of products (e.g., x*sin(x)) may be incorrect.
The calculation of the derivative of quotients (e.g., sin(x)/x) may be incorrect.
The calculation of the derivative of composite functions (e.g., sin(x^2), ln(cos(x))) may be incorrect,
except for simple cases such as cos(k*x) or e^(k*x) (where k is a number).
Trigonometric functions are only handled for simple arguments x or a numerical constant.
Logarithms are only handled for simple arguments x or a numerical constant.
Exponentiation is only handled for cases x^n (where n is a number) or e^x and e^(k*x) (where k is a number).

Examples of Correct Input:
x^2
2*x + 3
sin(x)
e^x
e^(2*x)
log{}(x)
ln(5*x)
''')

    # Main program loop
    while True:
        choice = input('Enter 1 for work or 2 to quit: ')
        if choice == '1':
            equation = eq_input()      # Get a valid equation from the user
            tokens = tokenize(equation)  # Tokenize the equation
            answer = part_derivative(tokens) # Calculate the derivative
            print(f'Equation tokens: {tokens}')
            print(f'd/dx = {"".join(answer)}') # Print the result
        elif choice == '2':
            print("Exiting program.")
            break # Exit the loop, terminating the program
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue # Repeat the loop if the choice is invalid