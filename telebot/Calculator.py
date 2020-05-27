import math

operators = ['^', 'V', '*', '/', '+', '-']

number_signs = ['.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def SolveEquation(equation: str) -> float:
    equation = equation.replace(' ', '')
    while len(equation) > 0 and equation[0] == '+':
        equation = equation[1:]
    if equation.find("e+") != -1:
        raise Exception('cant calculate big numbers in equation - {}'.format(equation))

    sml_eq = findFirstSimpleEquation(equation)
    sml_eq_result = doOperatorCalculation(substringTuple(equation, sml_eq))
    if sml_eq_result == math.inf:
        return math.inf
    if sml_eq[0] == 0 and sml_eq[1] == len(equation):
        return sml_eq_result

    if equation[sml_eq[0]-1] == '(' and equation[sml_eq[1]] == ')':
        equation = equation[0:sml_eq[0]-1] + str(sml_eq_result) + equation[sml_eq[1]+1:len(equation)]
    else:
        equation = equation[0:sml_eq[0]] + str(sml_eq_result) + equation[sml_eq[1]:len(equation)]

    return SolveEquation(equation)


def findFirstSimpleEquation(equation: str) -> tuple:
    short_eq_indexes = findParentheses(equation)
    if short_eq_indexes:
        shorter_eq = findFirstSimpleEquation(substringTuple(equation, short_eq_indexes))
        if shorter_eq is not None:
            return tuple(index + short_eq_indexes[0] for index in shorter_eq)
        else:
            return None

    for i in range(int(len(operators)/2)):  # needs a rework
        op_index = 0
        op1_index = equation.find(operators[i * 2])
        op2_index = equation.find(operators[i * 2 + 1])
        if op1_index != -1 and (op1_index < op2_index or op2_index == -1):
            op_index = op1_index
            operator = operators[i * 2]
        elif op2_index != -1 and (op2_index < op1_index or op1_index == -1):
            op_index = op2_index
            operator = operators[i * 2 + 1]
        else:
            continue
        op_index = equation.find(operator)
        if op_index == 0:
            op_index = equation.find(operator, op_index + 1)
            if op_index == -1:
                if operator == '+':
                    operator = '-'
                    op_index = equation.find(operator)
                else:
                    operator = '+'
                    op_index = equation.find(operator)
        if op_index > 0:
            numbers_indexes = findNumbers(equation, op_index)
            if numbers_indexes is None:
                return None
            if numbers_indexes[0] == op_index:
                op_index = equation.find(operator, op_index+1)
                if op_index >= 0:
                    numbers_indexes = findNumbers(equation, op_index)
                    return numbers_indexes

            return numbers_indexes

    raise Exception('did not find any operators matching')


def doOperatorCalculation(equation: str) -> str:
    # while len(equation) > 0 and equation[0] == '+':
    #     equation = equation[1:]
    while len(equation) > 0 and (equation[-1] == '+' or equation[-1] == '-'):
        equation = equation[1:]
    try:
        result = None
        for operator in operators:
            op_index = equation.rfind(operator)
            if op_index > 0:
                if operator == '-' or operator == '+' or operator == '*' or operator == '/':
                    result = float(eval(equation))
                    break
                else:
                    segments = equation.split(operator)
                    if operator == 'V':
                        result = float(math.pow(eval(segments[1]), eval("(1/{})".format(segments[0]))))
                    else:
                        result = float(math.pow(eval(segments[0]), eval(segments[1])))
                    break
        if type(result) == float:
            if result < 0:
                return getWholeNumber(result)
            else:
                return "+"+getWholeNumber(result)
    except OverflowError:
        return math.inf
    raise Exception('no supported operator in equation = {}'.format(equation))


def findNumbers(equation, operator_index) -> ():
    left_is_number = False
    left_number_index = operator_index-1
    while left_number_index >= 0 and (equation[left_number_index] == '-' or equation[left_number_index] == '+'):
        left_number_index -= 1
    while left_number_index >= 0 and equation[left_number_index] in number_signs:
        if equation[left_number_index] in number_signs[1:]:
            left_is_number = True
        left_number_index -= 1
    # elif equation[operator_index] != '-':
    #     return None

    while left_number_index >= 0 and (equation[left_number_index] == '-' or equation[left_number_index] == '+'):
        left_number_index -= 1
    left_number_index += 1

    right_is_number = False
    right_number_index = operator_index + 1
    while right_number_index < len(equation) and (equation[right_number_index] == '-' or equation[right_number_index] == '+'):
        right_number_index += 1
    while right_number_index < len(equation) and equation[right_number_index] in number_signs:
        if equation[right_number_index] in number_signs[1:]:
            right_is_number = True
        right_number_index += 1
    if right_number_index == operator_index + 1 or equation[right_number_index-1] == '-'\
            or not right_is_number or (not left_is_number and equation[operator_index] != '-'):
        return None

    return left_number_index, right_number_index
    pass


def findParentheses(equation: str) -> ():
    p_start = equation.find('(')
    p_end = equation.find(')')
    p_start_from_end = equation.rfind('(')
    p_end_from_end = equation.rfind(')')
    if p_end_from_end < p_start or p_start_from_end > p_end_from_end or p_end < p_start:
        return None

    p_start += 1
    p_difference = equation.count('(', p_start, p_end) - \
                   equation.count(')', p_start, p_end)
    while p_difference != 0:
        p_end = equation.find(')', p_end + 1)
        if p_end < 0:
            break
        p_difference = equation.count('(', p_start, p_end) - \
                       equation.count(')', p_start, p_end)
    if p_end < 0:
        return None
    return p_start, p_end

    pass


def substringTuple(equation: str, indexes: tuple):
    return equation[indexes[0]:indexes[1]]


def getWholeNumber(num: float) -> str:
    string = ""

    if math.fabs(num) > 1:
        string = str(num % 1)[1:]
        if string.find('e-') != -1:
            string = ".0"
        while math.fabs(num) > 1:
            string = str(int(num % 10)) + string
            num /= 10
    else:
        if str(num).find('e-'):
            string = "0."
        while math.fabs(num) < 1000000:
            num *= 10
            string += str(int(num % 10))
    if num < 0:
        string = "-" + string
    return string
