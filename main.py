import PySimpleGUI as sg
import pyttsx3 as tts

global_values = []
deleted = True


def click_reset():
    global deleted
    global_values.clear()
    deleted = True


def update_out_operator(element):
    global_values.append(element)


def update_out_operator_check(element):
    if len(global_values) < 1 and element != '-':
        sg.popup_error("Operators are not allowed as first input.")
        return 0
    elif len(global_values) > 0 and global_values[-1] in ('+', '-', '/', '*'):
        sg.popup_error("Only one operator allowed.")
        return 0
    else:
        return 1


def update_out_digit(element):
    global deleted
    if len(global_values) >= 14:
        sg.popup_error("Expression entered is too long.")
    elif not deleted and global_values[-1] not in ('+', '-', '/', '*'):
        sg.popup_error("Cannot modify the result without deleting first.")
    elif not len(global_values) and element == '0':
        sg.popup_error("Cannot start expression with 0.")
    else:
        global_values.append(element)
        deleted = True


def compute_expr():
    global deleted
    expr = ''.join(global_values)
    res = eval(expr)
    res = str(round(res, 2))
    if len(res) > 14:
        sg.popup_no_border("The result is too large and will be truncated.")
    deleted = False
    global_values.clear()
    auxList = list(str(res)[:14])
    global_values.extend(auxList)


def compute_expr_check():
    if len(global_values) < 1:
        sg.popup_error("No input detected.")
        return 0
    elif len(global_values) > 0 and global_values[-1] in ('+', '-', '/', '*'):
        sg.popup_error("Expression cannot end with an operator.")
        return 0
    elif len(global_values) > 0 and not any(item in global_values for item in ('+', '-', '/', '*')):
        sg.popup_error("Expression is missing an operator.")
        return 0
    else:
        return 1


def erase_elem():
    global deleted
    try:
        global_values.pop()
        if len(global_values) > 0:
            if global_values[-1] == '.' or global_values[-1] == '-':
                global_values.pop()
                if global_values[-1] == '0':
                    global_values.pop()
        deleted = True
    except IndexError:
        sg.popup_error("Expression is already empty.")


def text_to_speech(text):
    engine = tts.init()
    engine.say(text)
    engine.runAndWait()


def gui():
    sg.theme('DarkAmber')

    btnDigit = {'size': (5, 1), 'font': ('Franklin Gothic Book',
                                         20), 'button_color': ("#f2f2f2", "black")}
    btnOperator = {'size': (5, 1), 'font': ('Franklin Gothic Book',
                                            20), 'button_color': ("#f2f2f2", "grey")}
    btnReset = {'size': (5, 1), 'font': ('Franklin Gothic Book',
                                         20), 'button_color': ("#f2f2f2", "#6e1010")}

    layout = [
        [sg.Text("", size=(16, 1), font=('Franklin Gothic Book',
                                         31), key='_OUT_', justification='right',
                 background_color="#8f8f8f", text_color="#f2f2f2")],
        [sg.Button('C', **btnReset, key='_reset_'),
         sg.Push(),
         sg.Button('Erase', **btnOperator)],
        [sg.Button('7', **btnDigit), sg.Button('8', **btnDigit),
         sg.Button('9', **btnDigit), sg.Button('/', **btnOperator)],
        [sg.Button('4', **btnDigit), sg.Button('5', **btnDigit),
         sg.Button('6', **btnDigit), sg.Button('*', **btnOperator)],
        [sg.Button('1', **btnDigit), sg.Button('2', **btnDigit),
         sg.Button('3', **btnDigit), sg.Button('-', **btnOperator)],
        [sg.Button('0', **btnDigit), sg.Button('PLAY', **btnReset, key='_voice_'),
         sg.Button('=', **btnOperator), sg.Button('+', **btnOperator)]
    ]

    window = sg.Window('Calculator',
                       layout)

    while True:
        event, values = window.read()

        print(event, values)

        if event == sg.WINDOW_CLOSED:
            break

        if event == '_voice_':
            text_to_speech(''.join(global_values))

        if event in ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            update_out_digit(event)
            window['_OUT_'].update(''.join(global_values))

        if event in ('+', '-', '/', '*'):
            if update_out_operator_check(event):
                update_out_operator(event)
                window['_OUT_'].update(''.join(global_values))

        if event == '_reset_':
            click_reset()
            window['_OUT_'].update('')

        if event == '=':
            if compute_expr_check():
                compute_expr()
                window['_OUT_'].update(''.join(global_values)[:14])

        if event == 'Erase':
            erase_elem()
            window['_OUT_'].update(''.join(global_values)[:14])

    window.close()


if __name__ == '__main__':
    gui()
