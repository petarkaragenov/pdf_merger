import os
import PySimpleGUI as sg
from pdf_functions import merge_pdfs

listbox_selected = []


DEFAULT_FILENAME = "merged.pdf"
DEFAULT_FILEPATH = "C:/Users/petar/Documents/PDFs"


def move_up(values, cur_values, idx):
    prev_el = cur_values[idx-1]
    new_vals = []

    for i, val in enumerate(cur_values):
        print(val)
        if val == prev_el:
            new_vals.append(values['-FILES-'][0])
        elif i == idx:
            new_vals.append(prev_el)
        else:
            new_vals.append(val)
    
    return new_vals

def move_down(values, cur_values, idx):
    next_el = cur_values[idx+1]
    new_vals = []

    for i, val in enumerate(cur_values):
        if i == idx:
            new_vals.append(next_el)
        elif val == next_el:
            new_vals.append(values['-FILES-'][0])
        else:
            new_vals.append(val)
    
    return new_vals

def remove_file(cur_values, idx):
    cur_values.pop(idx)
    return cur_values

def clear_inputs(window):
    window['-IN-'].update('')
    window['-FILES-'].update([])
    window['-FILENAME-'].update('')
    window['-FILEPATH-'].update('')


left_col = [
    [sg.Text('Choose Files:')],
    [sg.Text("Choose Path:")], 
    [sg.Text("Choose Name:")]
]

right_col = [
    [
        sg.In(key='-IN-', size=(30, 1), enable_events=True), 
        sg.FilesBrowse(file_types=(('PDF Files', '*.pdf'),), files_delimiter=";", initial_folder="C:/Users/petar/Documents/PDFs")
    ],
    [sg.In(key="-FILEPATH-", size=(30, 1)),sg.FolderBrowse()],
    [sg.In(key="-FILENAME-", size=(30, 1))]

]

layout = [
    [sg.Column(left_col), sg.Column(right_col)],
    [sg.Listbox(values=[], size=(50, 8), expand_x=True, enable_events=True, key="-FILES-")],
    [sg.B("Merge", expand_x=True), sg.B("Up", expand_x=True), sg.B("Down", expand_x=True), sg.B("Remove", expand_x=True), sg.B("Clear", expand_x=True)]
]


window = sg.Window("PDF Merger", layout)


while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    if event == '-IN-':
        vals = values['Browse'].split(';')
        window['-FILES-'].update(values=[*window['-FILES-'].get_list_values(), *vals])

    elif event == '-FILES-':
        listbox_selected = []

    elif event in ("Up", "Down", "Remove"):
        if len(listbox_selected) > 0:
            values['-FILES-'] = listbox_selected
            print(values)
        if values['-FILES-'] == [] or len(window['-FILES-'].get_list_values()) < 2:
            pass
        else:
            cur_values = window['-FILES-'].get_list_values()
            sel_val_idx = cur_values.index(values['-FILES-'][0])
            sel_val = values['-FILES-']

            if event == "Up":
                if sel_val_idx == 0:
                    pass
                else:
                    vals = move_up(values, cur_values, sel_val_idx)
                    listbox_selected = sel_val
            elif event == 'Down':
                if sel_val_idx == len(cur_values)-1:
                    pass
                else:
                    vals = move_down(values, cur_values, sel_val_idx)
                    listbox_selected = sel_val
            elif event == "Remove":
                vals = remove_file(cur_values, sel_val_idx)
            
            window['-FILES-'].update(values=vals)

    elif event == "Merge":
        if len(window['-FILES-'].get_list_values()) >= 2:
            cur_values = window['-FILES-'].get_list_values()

            if values['-FILENAME-'] == '':
                filename = DEFAULT_FILENAME
            else:
                filename = values['-FILENAME-'] + ".pdf"

            if values['-FILEPATH-'] == '':
                filepath = DEFAULT_FILEPATH
            else:
                filepath = values['-FILEPATH-']

            output = os.path.join(filepath, filename)
            print(output)
            
            merge_pdfs(cur_values, output=output)
            clear_inputs(window)

    elif event == "Clear":
        clear_inputs(window)
        

window.close()