import math


def sin_t(angle_radians, n = 20):
    angle_degrees = (angle_radians + math.pi) % (2 * math.pi) - math.pi
    total = 0
    term = angle_degrees
    for i in range(n):
        total += term
        term *= -angle_degrees * angle_degrees / ((2 * i + 2) * (2 * i + 3))
    return total

def cos_t(x, terms = 20):
    return sin_t(x + math.pi / 2, terms)

functions = {
    "sqrt": math.sqrt,
    "abs": abs,
    "sin": sin_t,
    "cos": cos_t,
}

consts = {
    "pi": math.pi,
    "e": math.e
}

def evaluate(expression):
    tokens = []
    position = 0
    while position < len(expression):
        char = expression[position]
        if char.isspace():
            position += 1
        elif char.isdigit() or char == ".":
            end = position
            while end < len(expression) and (expression[end].isdigit() or expression[end] == "."):
                end += 1
            tokens.append(float(expression[position:end]))
            position = end
        elif char.isalpha():
            end = position
            while end < len(expression) and expression[end].isalnum():
                end += 1
            tokens.append(expression[position:end])
            position = end
        elif char == "*" and position + 1 < len(expression) and expression[position + 1] == "*":
            tokens.append("**")
            position += 2
        else:
            tokens.append(char)
            position += 1
    cursor = [0]

    def peek():
        return tokens[cursor[0]] if cursor[0] < len(tokens) else None
    
    def take():
        token = tokens[cursor[0]]
        cursor[0] += 1
        return token

    def parse_atom():
        token = take()
        if isinstance(token, float):
            return token
        if token == "(":
            value = parse_xor()
            take()
            return value
        if peek() == "(":
            take()
            argument = parse_xor()
            take()
            return functions[token](argument)
        try:
            return consts[token]
        except KeyError:
            return f"\nОшибка: Неизвестный символ: {token}"

    def parse_unary():
        if peek() in ("-", "+"):
            sign = take()
            return -parse_unary() if sign == "-" else parse_unary()
        return parse_power()

    def parse_power():
        base = parse_atom()
        if peek() == "**":
            take()
            return base ** parse_power()
        return base
    

    def parse_xor():
        value = parse_sum()
        while peek() == "^":
            take()
            right = parse_sum()
            value = int(value) ^ int(right)
        return value

    
    def parse_product():
        value = parse_unary()
        while peek() in ("*", "/"):
            oper = take()
            right = parse_unary()
            try:
                value = value * right if oper == "*" else value / right
            except ZeroDivisionError:
                return "\nОшибка: Деление на ноль"
            except TypeError:
                return "\nОшибка: Некоректное написание выражения"
        return value
    
    def parse_sum():
        value = parse_product()
        while peek() in ("+", "-"):
            oper = take()
            right = parse_product()
            try:
                value = value + right if oper == "+" else value - right
            except TypeError:
                return "\nОшибка: Некоректное написание выражения"
        return value

    return parse_xor()


while True:
    a = input("Введите выражение: ")
    if a == "":
        break
    print(f"Результат {a}: {evaluate(a)}")