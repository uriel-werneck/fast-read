import tkinter as tk
from tkinter.ttk import Combobox
from tkinter import filedialog
from pypdf import PdfReader

# Functions
def take_focus(e):
    """This function will take the focus from selected widgets"""
    screen.focus()


def config_objects(objects: list, state: str) -> None:
    """This function will change the state of a list of objects"""
    for obj in objects:
        obj.config(state=state)


def open_file_dialog():
    """This function will open 'file dialog' so the user can select a pdf file"""
    global page_options

    screen.focus()
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("PDF files", "*.pdf")])

    if file_path:
        reader = PdfReader(file_path)

        max_page = reader.get_num_pages()
        page_options = list(range(1, max_page + 1))
        page_combobox.current(0)

        entry_text.set(file_path)

        try:
            centralized_word.set(f'{reader._info['/Title']}\n({reader._info['/Author']})')
        except:
            centralized_word.set('(Undefined)')

        page_combobox.config(values=page_options, state='normal')
        config_objects([read_button, color_combobox, speed_combobox, size_combobox], state='normal')


def page_to_text(reader: object, page: int) -> str:
    """ This function will convert a pdf page to a string"""
    current_page = reader.pages[page]
    string = current_page.extract_text()
    return string


def start_reading():
    """This function will read the selected page"""
    global is_reading
    screen.focus()

    if not is_reading:
        is_reading = True

        read_or_stop_string.set('STOP')

        word_label.config(fg=color_combobox.get(), font=('inter', size_combobox.get(), 'bold')) # choose color and text size
        speed = int(60 / int(speed_combobox.get()) * 1000) # choose speed
        page = int(page_combobox.get()) - 1 # choose page

        try:
            reader = PdfReader(entry_text.get().strip())
            page_string = page_to_text(reader, page)
            all_words = page_string.split()

            max_page = reader.get_num_pages()
            page_options = list(range(1, max_page + 1))

            page_combobox.config(values=page_options, state='normal')
            config_objects([color_combobox, speed_combobox, size_combobox], 'normal')

            #print(page_string)
            #print(all_words)

            for word in all_words:
                centralized_word.set(word)
                screen.after(speed, screen.update())

                if not is_reading:
                    break

        except FileNotFoundError:
            centralized_word.set('<File not found>')
            page_combobox.current(0)
            config_objects([page_combobox, speed_combobox, color_combobox, size_combobox], 'disabled')

        except IndexError:
            centralized_word.set('<Page not found>')
            page_combobox.current(0)
            config_objects([page_combobox, speed_combobox, color_combobox, size_combobox], 'disabled')
        
        is_reading = False
        read_or_stop_string.set('READ')

    else:
        is_reading = False


# Debounce Variable
is_reading = False

# Screen Configuration
screen = tk.Tk()
screen.configure(background='gray')
#img = tk.PhotoImage(file='images/book icon.png') # find the image in the folder
#screen.iconphoto(False, img) # define the screen icon
screen.geometry('640x480')
screen.title('Fast Read')

# Option Menus
page_options = [1]
color_options = ['Black', 'Red', 'Blue', 'Green', 'Gold']
size_options = [20, 30, 40, 50]
speed_options = [200, 250, 300, 350, 400]

# StringVariables
centralized_word = tk.StringVar(value='Bem Vindo!')
read_or_stop_string = tk.StringVar(value='READ')
entry_text = tk.StringVar()

# Canvas
main_canvas = tk.Canvas(screen, bg='gray', highlightthickness=0)
main_canvas.place(relwidth=1, relheight=1)

# Frames
main_frame = tk.Frame(screen)
main_frame.place(relx=0.5, rely=0.4259, relwidth=0.9375, relheight=0.771, anchor='center')

lower_frame = tk.Frame(screen, bg='gray')
lower_frame.place(relx=0.5, rely=1, relwidth=1, relheight=0.1875, anchor='s')

book_entry_frame = tk.Frame(lower_frame, width=640, bg='gray')
book_entry_frame.place(rely=0.2, relwidth=1, relheight=0.24, anchor='w')

page_text_frame = tk.Frame(lower_frame, width=87, height=20, bg='gray')
page_text_frame.place(relx=0.03, rely=0.5, anchor='w')

speed_frame = tk.Frame(lower_frame, width=87, height=20, bg='gray')
speed_frame.place(relx=0.03, rely=0.8, anchor='w')

color_frame = tk.Frame(lower_frame, width=87, height=20, bg='gray')
color_frame.place(relx=0.97, rely=0.5, anchor='e')

size_frame = tk.Frame(lower_frame, width=87, height=20, bg='gray')
size_frame.place(relx=0.97, rely=0.8, anchor='e')

search_button_frame = tk.Frame(book_entry_frame, bg='gray',)
search_button_frame.place(relx=0.936, rely=0.5, relwidth=0.11, relheight=1, anchor='center')

# Labels
word_label = tk.Label(main_frame, font=('inter', 30, 'bold'), textvariable=centralized_word)
word_label.place(relx=0.5, rely=0.5, anchor='center')

page_label = tk.Label(page_text_frame, font=('inter', 12), text='Page:', bg='gray', fg='white')
page_label.grid(row=0, column=0)

path_label = tk.Label(book_entry_frame, font=('inter', 12), text='File URL:', bg='gray', fg='white', anchor='e')
path_label.place(relx=0.06, rely=0.5, relwidth=0.12, anchor='center')

speed_label = tk.Label(speed_frame, font=('inter', 12), text='Speed:', bg='gray', fg='white')
speed_label.grid(row=0, column=0)

wpm_label = tk.Label(speed_frame, font=('inter', 9, 'bold'), text='(WPM)', bg='gray', fg='white')
wpm_label.grid(row=0, column=2)

color_label = tk.Label(color_frame, font=('inter', 12), text='Color:', bg='gray', fg='white')
color_label.grid(row=0, column=0)

size_label = tk.Label(size_frame, font=('inter', 12), text='Size:', bg='gray', fg='white')
size_label.grid(row=0, column=0)

# ComboBoxes
page_combobox = Combobox(page_text_frame, values=page_options, width=4, state='disabled')
page_combobox.current(0)
page_combobox.grid(row=0, column=1, padx=9)

speed_combobox = Combobox(speed_frame, values=speed_options, width=4, state='disabled')
speed_combobox.current(1)
speed_combobox.grid(row=0, column=1)

color_combobox = Combobox(color_frame, values=color_options, width=5, state='disabled')
color_combobox.current(0)
color_combobox.grid(row=0, column=1)

size_combobox = Combobox(size_frame, values=size_options, width=5, state='disabled')
size_combobox.current(1)
size_combobox.grid(row=0, column=1)

# Entries
book_entry = tk.Entry(book_entry_frame, textvariable=entry_text)
book_entry.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.75, anchor='center')

# Buttons
read_button = tk.Button(lower_frame, textvariable=read_or_stop_string, command=lambda: start_reading())
read_button.place(relx=0.5, rely=0.65, relwidth=0.12, relheight=0.5, anchor='center')

search_button = tk.Button(search_button_frame, text='Search', width=8, command=open_file_dialog)
search_button.place(rely=0.5, anchor='w')

# Binding
main_canvas.bind('<Button-1>', take_focus)
main_frame.bind('<Button-1>', take_focus)
lower_frame.bind('<Button-1>', take_focus)

# Mainloop
tk.mainloop()
