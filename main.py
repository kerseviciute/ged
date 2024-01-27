from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.ttk import *
import matplotlib.colors

import numpy as np
import pandas as pd


def scale_number(unscaled, to_min, to_max, from_min, from_max):
    return (to_max - to_min) * (unscaled - from_min) / (from_max - from_min) + to_min


def scale_list(l, to_min, to_max):
    return [scale_number(i, to_min, to_max, min(l), max(l)) for i in l]


class Ball:
    def __init__(self, posx, posy, size):
        self.ball = canvas.create_oval(posx - size, posy - size, posx + size, posy + size, fill = 'black')

    def update_color(self, color):
        canvas.itemconfig(self.ball, fill = color, outline = color)


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


def open_file_eeg():
    file = askopenfile(mode = 'r', filetypes = [('Pickle', '*.pkl')], initialdir = '.', title = 'Select EEG data')

    if file is not None:
        file_label.config(text = file.name)


def open_file_events():
    file = askopenfile(mode = 'r', filetypes = [('Pickle', '*.pkl')], initialdir = '.', title = 'Select events data')

    if file is not None:
        events_file_label.config(text = file.name)


button_open_file = Button(window, text = 'Open EEG', command = lambda: open_file_eeg())
button_open_file.grid(row = 0, column = 0)

file_label = Label(window, text = '/Users/ieva/Master/ged/mne_raw.pkl')
file_label.grid(row = 0, column = 1, columnspan = 5)

button_open_file_events = Button(window, text = 'Open events', command = lambda: open_file_events())
button_open_file_events.grid(row = 1, column = 0)

events_file_label = Label(window, text = '/Users/ieva/Master/ged/events.pkl')
events_file_label.grid(row = 1, column = 1, columnspan = 5)

frequency_range_label = Label(window, text = 'Frequency range from')
frequency_range_label.grid(row = 2, column = 0)

frequency_from_entry = Entry(window, width = 5)
frequency_from_entry.insert(0, '4')
frequency_from_entry.grid(row = 2, column = 1)

frequency_range_label_2 = Label(window, text = ' to ')
frequency_range_label_2.grid(row = 2, column = 2)

frequency_to_entry = Entry(window, width = 5)
frequency_to_entry.insert(0, '8')
frequency_to_entry.grid(row = 2, column = 3)

eigenvalue_id_label = Label(window, text = 'Eigenvalue ID')
eigenvalue_id_label.grid(row = 3, column = 0)

eigenvalue_id_entry = Entry(window, width = 5)
eigenvalue_id_entry.insert(0, '254')
eigenvalue_id_entry.grid(row = 3, column = 1)

timestep_label = Label(window, text = 'Time step (s)')
timestep_label.grid(row = 4, column = 0)

timestep_entry = Entry(window, width = 5)
timestep_entry.insert(0, '0.5')
timestep_entry.grid(row = 4, column = 1)


def run():
    print(f'Preprocessing file {file_label["text"]}')
    print(f'Events file {events_file_label["text"]}')
    print(f'Preprocess to select frequencies from {frequency_from_entry.get()} Hz to {frequency_to_entry.get()} Hz')
    print(f'Selecting eigenvalue with id {eigenvalue_id_entry.get()}')
    print(f'Time step {timestep_entry.get()} seconds')

    global mne_data
    print('Reading the data')
    mne_data = pd.read_pickle(file_label["text"])
    print('Filtering the data')
    mne_data.filter(l_freq = float(frequency_from_entry.get()), h_freq = float(frequency_to_entry.get()))

    montage = mne_data.get_montage().get_positions()['ch_pos']
    montage_coordinates = np.array(list(montage.values()))

    coordinates_x = scale_list(montage_coordinates[:, 0], window_width * 0.05, window_width - window_width * 0.05)
    coordinates_y = scale_list(montage_coordinates[:, 1], 600 * 0.05, 600 - 600 * 0.05)

    global electrodes
    electrodes = []
    for x, y in zip(coordinates_x, coordinates_y):
        electrode = Ball(x, y, 5)
        electrodes.append(electrode)

    global event_counter
    event_counter = 1

    global events
    events = pd.read_pickle(events_file_label["text"])


# the color palette for colouring the eeg points
cmap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["red", "orange", "green"])


def update_electrode_color():
    global electrodes
    global event_counter
    global mne_data

    event_counter = event_counter + 1
    print(event_counter)
    event = events.iloc[event_counter]

    event_data = mne_data.copy().crop(tmin = event['Start'] + 0.5, tmax = event['End'] - 0.5)
    cov_matrix = np.cov(event_data.get_data())
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    eigenvector = eigenvectors[:, int(eigenvalue_id_entry.get())]
    eigenvector = scale_list(eigenvector, 0, 1)

    status_label.config(text = f'Event: {event["Event"]}')

    for i, electrode in enumerate(electrodes):
        rgba = cmap(eigenvector[i])
        color = matplotlib.colors.rgb2hex(rgba)
        electrode.update_color(color)


def stop():
    print('Oops not implemented yet, cant stop')


run_button = Button(window, width = 5, text = 'Run', command = run)
run_button.grid(row = 5, column = 4)

stop_button = Button(window, width = 5, text = 'Stop', command = stop)
stop_button.grid(row = 5, column = 5)

next_button = Button(window, width = 5, text = 'Next', command = update_electrode_color)
next_button.grid(row = 5, column = 6)

canvas = Canvas(window, width = window_width, height = 600, background = 'white')
canvas.grid(row = 6, column = 0, columnspan = 10)

status_label = Label(window)
status_label.grid(row = 7, column = 0, columnspan = 10)

window.mainloop()
