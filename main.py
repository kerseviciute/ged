from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.ttk import *

window = Tk()

#
# Window setup
#
window.title('Generalized Eigenvalue Decomposition')

window.resizable(False, False)

window_width = 1200
window_height = 800

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


def open_file():
    file = askopenfile(mode = 'r', filetypes = [('Pickle', '*.pkl')], initialdir = '.', title = 'Select EEG data')

    if file is not None:
        file_label.config(text = file.name)


button_open_file = Button(window, text = 'Open', command = lambda: open_file())
button_open_file.grid(row = 0, column = 0)

file_label = Label(window, text = '/Users/ieva/Master/ged/mne_raw.pkl')
file_label.grid(row = 0, column = 1, columnspan = 5)

frequency_range_label = Label(window, text = 'Frequency range from')
frequency_range_label.grid(row = 1, column = 0)

frequency_from_entry = Entry(window, width = 5)
frequency_from_entry.insert(0, '4')
frequency_from_entry.grid(row = 1, column = 1)

frequency_range_label_2 = Label(window, text = ' to ')
frequency_range_label_2.grid(row = 1, column = 2)

frequency_to_entry = Entry(window, width = 5)
frequency_to_entry.insert(0, '8')
frequency_to_entry.grid(row = 1, column = 3)

eigenvalue_id_label = Label(window, text = 'Eigenvalue ID')
eigenvalue_id_label.grid(row = 2, column = 0)

eigenvalue_id_entry = Entry(window, width = 5)
eigenvalue_id_entry.insert(0, '254')
eigenvalue_id_entry.grid(row = 2, column = 1)

timestep_label = Label(window, text = 'Time step (s)')
timestep_label.grid(row = 3, column = 0)

timestep_entry = Entry(window, width = 5)
timestep_entry.insert(0, '0.5')
timestep_entry.grid(row = 3, column = 1)


def run():
    print(f'Preprocessing file {file_label["text"]}')
    print(f'Preprocess to select frequencies from {frequency_from_entry.get()} Hz to {frequency_to_entry.get()} Hz')
    print(f'Selecting eigenvalue with id {eigenvalue_id_entry.get()}')
    print(f'Time step {timestep_entry.get()} seconds')


def stop():
    print('Oops not implemented yet, cant stop')


run_button = Button(window, width = 5, text = 'Run', command = run)
run_button.grid(row = 4, column = 4)

stop_button = Button(window, width = 5, text = 'Stop', command = stop)
stop_button.grid(row = 4, column = 5)

window.mainloop()
