variables_dict = {}
operators = ('+', '-', '*', '/')


def smart_calculator(operation):
    if operation == '/exit':
        return 'Bye!'
    else:
        line_to_numbers = prepare_expression(operation)

        if line_to_numbers == []:
            pass

        else:
            if '=' in operation:
                handle_variables(operation)

            elif line_to_numbers[0][0] == '/':
                user_command = operation
                print(handle_command(user_command))

            else:
                try:
                    calc_result = reverse_polish_notation(line_to_numbers)
                except:
                    print('Invalid expression')
                else:
                    print(calc_result)
        return smart_calculator(input())


def handle_command(user_command):
    if user_command == "/help":
        return """This is an instraction.\nThe program with new operations"""
    else:
        return 'Unknown command'


def count(user_list):
    if len(user_list) == 1:
        if user_list[0].isalpha():
            try:
                variables_dict[user_list[0]]
            except:
                return 'Unknown variable'
            else:
                return variables_dict[user_list[0]]
        else:
            return int(user_list[0])
    else:
        for item in user_list:
            if item.isalpha():
                user_list[user_list.index(item)] = variables_dict[item]

        user_sum = int(user_list[0])
        symbol = ''
        for item in user_list[1:]:
            if '+' in item:
                symbol = '+'
            elif '-' in item:
                number_of_minus = item.count('-')
                if number_of_minus % 2 == 0:
                    symbol = '+'
                else:
                    symbol = '-'
            elif item == '/':
                symbol = '/'
            elif item == '*':
                symbol = '*'
            elif '-' not in item and '*' not in item and '+' not in item and '/' not in item:
                item = int(item)
                if symbol == '+':
                    user_sum += item
                elif symbol == '/':
                    user_sum //= item
                elif symbol == '*':
                    user_sum *= item
                elif symbol == '-':
                    user_sum -= item
            else:
                return 'Invalid expression'
        return str(user_sum)


def handle_variables(math_string):
    math_string = math_string.replace(' ', '')
    equal_sign = math_string.index('=')
    variable = math_string[0:equal_sign]
    if not variable.isalpha():
        print('Invalid identifier')
    var_value = math_string[equal_sign+1:]
    if not var_value.isdigit():
        if not var_value.isalpha():
            print('Invalid assignment')
        else:
            try:
                variables_dict[var_value]
            except:
                print('Unknown variable')
            else:
                var_value = variables_dict[var_value]
    variables_dict[variable] = var_value


def prepare_expression(expression):
    if ' ' not in expression:
        expression = list(expression)
        prev_item = ' '
        new_expression = []
        for item in expression:
            if item.isdigit() and prev_item.isdigit():
                place_of_item = expression.index(item)
                new_item = str(prev_item) + str(item)
                new_expression[place_of_item - 1] = new_item
            else:
                new_expression.append(item)

            prev_item = new_expression[-1]
        return new_expression
    elif ' ' in expression:
        expression = [a for a in expression.split(' ')]
        if expression[0] == '':
            del expression[0]
            return expression
        else:
            return expression


def reverse_polish_notation(line_of_expression):

    # dealing with parentheses slipped with numbers
    for item in line_of_expression:
        if item[0] == '(' and len(item) > 1:
            index_of_item = line_of_expression.index(item)
            del line_of_expression[index_of_item]
            line_of_expression.insert(index_of_item, item[1:])
            line_of_expression.insert(index_of_item, item[0])

        if item[-1] == ')' and len(item) > 1:
            index_of_item = line_of_expression.index(item)
            del line_of_expression[index_of_item]
            line_of_expression.insert(index_of_item, item[-1])
            line_of_expression.insert(index_of_item, item[0:-1])

    result = []
    stack_line = []
    while len(line_of_expression) > 0:
        item = line_of_expression[0]
        if item.isdigit() or item.isalpha():
            result.append(item)
        elif item == '(':
            stack_line.append(item)
        elif item == ')':
            while stack_line[-1] != '(':
                result.append(stack_line.pop())
            stack_line.pop()
        elif len(stack_line) == 0 or '(' == stack_line[-1]:
            stack_line.append(item)
        elif (item == '*' or item == '/') and ('+' in stack_line[-1] or '-' in stack_line[-1]):
            stack_line.append(item)
        elif ('+' in item or '-' in item or item == '/') and (stack_line[-1] != '*' or stack_line[-1] != '/'):
            while len(stack_line) > 0 and stack_line[-1] != '(':
                result.append(stack_line.pop())
            stack_line.append(item)
        del line_of_expression[0]

    while len(stack_line) > 0:
        result.append(stack_line.pop())

    if '(' in result or ')' in result:
        return 'Invalid expression'
        # smart_calculator(input())

    try:
        calc_result = calculate_rpn_result(result)
    except:
        return 'Unknown variable'
        # smart_calculator(input())
    else:
        return calc_result


def calculate_rpn_result(rpn_result):
    if len(rpn_result) == 2:
        return rpn_result[1] + rpn_result[0]
    elif len(rpn_result) == 1:
        if rpn_result[0].isalpha():
            return variables_dict[rpn_result[0]]
        else:
            return rpn_result[0]
    else:
        calc_stack = []
        while len(rpn_result) > 0:
            item = rpn_result[0]
            if item.isdigit():
                calc_stack.append(item)
                del rpn_result[0]
            if item.isalpha():
                calc_stack.append(variables_dict[item])
                del rpn_result[0]
            if item[0] in operators:
                first_pop = calc_stack.pop()
                second_pop = calc_stack.pop()
                result_counted = count([second_pop, item, first_pop])
                calc_stack.append(result_counted)
                del rpn_result[0]
        return calc_stack.pop()


print(smart_calculator(input()))
