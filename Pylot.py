# -*- coding: utf-8 -*-
""" Main file for Pylot.

"""
from typing import List
import sys
import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import PySimpleGUI as sg

import plots as own_plots

STYLE = "darkgrid"
THEME = "DarkAmber"

NUM_OF_FIELDS = 9


def draw_plots(plt_type, cols_per_file, decimal_character, file, legend_text, plt_color,
               plt_line, separator, x_axis_label, x_cols, y_axis_label, y_cols, figure,
               rotation: int = 0, hue=None, do_box: bool = False) -> None:
    """ Function to draw different kind of plots.

    Args:
        plt_type: String with the type of plot to draw.
        cols_per_file: List with the number of columns per file.
        decimal_character: String with the decimal character, typically '.' or ','.
        file: String with the file name.
        legend_text:
        plt_color: (Optional) String with the color of the plot.
        plt_line: (Optional) String with the line style of the plot.
        separator: String .csv file separator.
        x_axis_label: String with the x axis label.
        x_cols: List with the x axis columns.
        y_axis_label: String with the y axis label.
        y_cols: List with the y axis columns.
        hue: (Optional) String with the hue column.
        rotation: Integer indicating the  rotation of the labels in degrees.
        do_box: (Optional) Boolean indicating if the heatmap should be drawn with boxes or not.
        figure: Matplotlib figure object.
    """
    plt.figure(figure.number)

    df = pd.read_csv(file, usecols=cols_per_file, sep=separator, header=None,
                     decimal=decimal_character)[cols_per_file]

    # Plot the data set using Seaborn and set legend labels from user specified ones above
    if plt_type == 'point':
        sns.scatterplot(data=df, x=x_cols, y=y_cols, color=plt_color, s=10,
                        label=f"{legend_text}")
    elif plt_type == "bar":
        df = df.round(1)
        ax = sns.barplot(data=df, x=x_cols, y=y_cols, hue=hue, palette="Blues_d")

        for container in ax.containers:
            ax.bar_label(container)
    elif plt_type == 'heatmap':
        sns.heatmap(df, annot=True, fmt='.3g', cmap="Blues", square=do_box)
    elif plt_type == 'map':
        own_plots.world_map.draw(countries=df[x_cols], values=df[y_cols])
    else:
        sns.lineplot(data=df, x=x_cols, y=y_cols, color=plt_color, linestyle=plt_line,
                     markers=True, dashes=False,
                     label=f"{legend_text}")
        sns.scatterplot(data=df, x=x_cols, y=y_cols, color=plt_color, s=20)

    # Set the x and y axis labels from the user specified ones above
    plt.xlabel(r'{}'.format(x_axis_label))
    plt.ylabel(r'{}'.format(y_axis_label))
    plt.yticks(rotation=rotation, va='center')

    plt.legend(ncol=2, loc=1)


def draw_initial_gui():
    """ Draw the initial GUI.

    This functions draws the first window of the GUI. It contains the field to select the next
    elements:
        The path to the data files.
        The separator character for the data files.
        The decimal character.
        If the output should be saved to a file or not.

    Returns:
        A list of the selected values.
    """
    # Set the theme for PysimpleGUI
    separator = ";"
    decimal_character = ","
    save_to_file = False
    if len(sys.argv) == 1:
        event, inputs_text = sg.Window('Select File(s) you wish to plot.').Layout([
            [sg.Text('Note, select multiple files by holding ctrl')],
            [sg.Input(key='_FILES_'), sg.FilesBrowse()],
            [sg.Text('Options')],
            [sg.Text("_" * 60)],
            [sg.Text("Separator"),
             sg.InputText(";", size=(2, 1), key='separator'),
             sg.Text("Decimal character"),
             sg.InputText(",", size=(2, 1), key='decimal_character'),
             sg.Checkbox('Save to file:', default=False, key='save_to_file')],
            [sg.OK(), sg.Cancel()]]).Read(close=True)
        # Close the window if cancel is pressed
        if event in (sg.WIN_CLOSED, 'Cancel'):
            exit()

        file_names = inputs_text['_FILES_']
        separator = inputs_text['separator']
        save_to_file = inputs_text['save_to_file']
        decimal_character = inputs_text['decimal_character']
    else:
        # Check to see if any files were provided on the command line
        file_names = sys.argv[1]
    return decimal_character, file_names, save_to_file, separator


def draw_main_windows(file_names: List[str]):
    """ Function to draw the main window.

    Args:
        file_names: List of strings with the file names.

    Returns:
        Returns with a list of values from the inputs of the main windows.
    """
    # List the available colours for the plots
    matplotlib_colours = ["dodgerblue", "indianred", "gold", "steelblue", "tomato", "slategray",
                          "plum", "seagreen", "gray", 'chocolate', 'olive', 'darkcyan', 'indigo']
    # List the line-styles you want
    matplotlib_linestyles = ["solid", "dashed", "dashdot", "dotted"]
    headings = ['TYPE', 'COLOUR', 'LINE', 'LEGEND']  # the text of the headings

    # Create the layout of the Window
    layout = [[sg.Text(
        'You can use LaTeX math code for axis labels and legend entries, e.g. $\\mathbf{r}$',
        font=('Courier', 10))],
        [sg.Text('To use regular text in math mode use $\\mathrm{Text}$\n')],
        [sg.Text('_' * 130, size=(100, 1))],  # Add horizontal spacer
        [sg.Text('X-axis label:'),
         sg.InputText(''),
         sg.Text('Y-axis label:'),
         sg.InputText('')],
        [sg.Text('_' * 130, size=(100, 1))],  # Add horizontal spacer
        [sg.Text('Min X:'),
         sg.InputText('', size=(2, 1)),
         sg.Text('Max X:'),
         sg.InputText('', size=(2, 1))],
        [sg.Text('Min Y:'),
         sg.InputText('', size=(2, 1)),
         sg.Text('Max Y:'),
         sg.InputText('', size=(2, 1))
         ],
        [sg.Text('_' * 130, size=(100, 1))],  # Add horizontal spacer
        [sg.Text(' ' * 110)] + [sg.Text(h, size=(9, 1)) for h in headings],
    ]
    for idx, f in enumerate(file_names):
        layout += [
            [sg.Text(f'File: {os.path.basename(os.path.normpath(f))}', size=(10, 1)),
             sg.Text("X"),
             sg.InputText('0', size=(5, 1)),
             sg.Text("Y"),
             sg.InputText('1', size=(5, 1)),
             sg.Text("HUE"),
             sg.InputText('', size=(5, 1)),
             sg.Text("ROT."),
             sg.InputText('0', size=(5, 1)),
             sg.Checkbox('BOX:', default=False, key='save_to_file'),
             sg.InputCombo(values=('point', 'bar', 'line', 'map', 'heatmap'),
                           default_value='line'),
             sg.InputCombo(values=matplotlib_colours, default_value=matplotlib_colours[idx]),
             sg.InputCombo(values=matplotlib_linestyles,
                           default_value=matplotlib_linestyles[0]),
             sg.InputText('Enter Legend Label', size=(20, 1)),
             ]]
    layout += [[sg.Text('_' * 130, size=(100, 1))],
               [sg.Button('Plot'), sg.Button('Cancel')]]
    # Create the Window
    window = sg.Window('Plot v1-01', layout)
    # Read in the events and values
    event, values = window.read()
    values = list(values.values())
    # If cancel is pressed then close the window and exit
    if event in (sg.WIN_CLOSED, 'Cancel'):
        exit()
    window.close()

    return values


def main():
    # set the seaborn dark grid styling
    sns.set_style(STYLE)
    # set the theme for PysimpleGUI
    sg.theme(THEME)

    decimal_character, fnames, save_to_file, separator = draw_initial_gui()
    # count the number of files provided
    fnames = fnames.split(';')
    file_names = fnames

    values = draw_main_windows(file_names)
    # Access the values which were entered and store in lists
    x_axis_label = values[0]
    y_axis_label = values[1]

    min_x = values[2]
    min_y = values[3]
    max_x = values[4]
    max_y = values[5]

    min_x = None if len(min_x) == 0 else int(min_x)
    min_y = None if len(min_y) == 0 else int(min_y)
    max_x = None if len(max_x) == 0 else int(max_x)
    max_y = None if len(max_y) == 0 else int(max_y)

    values = values[6:]

    list_of_data_sets = []
    legend_labels = []
    xcols = []
    ycols = []
    rotations = []
    cols_to_use = []
    plot_type = []
    plot_colour = []
    plot_line = []
    hue_labels = []
    make_boxes = []

    for idx, file in enumerate(file_names):
        # Append the data files to a single list
        list_of_data_sets.append(file)
        value_per_file = values[(idx * NUM_OF_FIELDS): ((idx + 1) * NUM_OF_FIELDS)]
        x_col_index, y_col_index, hue_label, rotation, make_box, type_plot, color_plot, line_style, l_labels = value_per_file

        hue_label = int(hue_label) if len(hue_label) > 0 else None

        x_col_index, y_col_index = int(x_col_index), int(y_col_index)

        xcols.append(x_col_index)
        ycols.append(y_col_index)
        hue_labels.append(hue_label)
        rotations.append(rotation)
        make_boxes.append(make_box)

        if hue_label is not None:
            cols_to_use.append([x_col_index, y_col_index, hue_label])
        else:
            cols_to_use.append([x_col_index, y_col_index])

        plot_type.append(type_plot)  # index 4
        plot_colour.append(color_plot)  # index 5
        plot_line.append(line_style)  # index 6
        legend_labels.append(l_labels)  # index 7

    figures = []
    fig = None
    for file, plt_type, x_cols, y_cols, cols_per_file, legend_label, plt_line, plt_color, hue_l, \
        rot, make_box in zip(list_of_data_sets, plot_type, xcols, ycols, cols_to_use, legend_labels,
                             plot_line, plot_colour, hue_labels, rotations, make_boxes):

        if (plt_type != 'line' and plt_type != 'point') or fig is None:
            fig = plt.figure()
            figures.append(fig)

        draw_plots(plt_type, cols_per_file, decimal_character, file, legend_label, plt_color,
                   plt_line, separator, x_axis_label, x_cols, y_axis_label, y_cols, fig, hue=hue_l)

    # Finally show the plot on screen
    for f_names, fig in zip(file_names, figures):
        folder, f_name = os.path.split(f_names)
        folder = os.path.join(folder, "out")
        os.makedirs(folder, exist_ok=True)

        f_name = os.path.join(folder, f"{f_name.split('.')[0]}.png")
        fig.tight_layout()
        plt.ylim([min_y, max_y])
        plt.xlim([min_x, max_x])

        if save_to_file:
            fig.savefig(f_name)

    plt.show()


if __name__ == '__main__':
    main()
