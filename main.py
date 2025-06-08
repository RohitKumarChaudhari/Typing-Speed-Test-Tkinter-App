import random
from tkinter import *

APP_BACKGROUND ='#EFE4D2'
DIALOG_BOX_BACKGROUND = APP_BACKGROUND

TITLE_COLOR = '#254D70'
TEXT_COLOR = '#131D4F'
DIALOG_BOX_TEXT_COLOR ='#2C2C2C'
LABEL_COLOR = '#954C2E'

WORD_HIGHLIGHT_COLOR ='#9FC87E'
CORRECT_WORD_HIGHLIGHT_COLOR = 'BLUE'

CORRECT_COLOR = '#F2F2F2'
WRONG_COLOR = '#E55050'

FONT = ('Helvetica', 20 )
LETTER_FONT = ('Sarif', 14)
TITLE_FONT = ('Sarif', 50, 'italic')

TOTAL_GIVEN_TIME = 10

TEXTBOX_AND_USERBOX_COLOR = "White"
USERBOX_DISABLE_COLOR ='#FFDCDC'


typing_words = [
    # Common
    "the", "and", "you", "have", "this", "from", "they", "with", "not", "what",

    # Medium / trickier spelling
    "through", "because", "another", "however", "business", "language",
    "between", "example", "different", "important", "sentence",

    # Programming-related
    "function", "variable", "object", "boolean", "integer", "return",
    "import", "package", "class", "parameter", "camelCase", "snake_case",

    # Long words / spelling practice
    "imagination", "possibility", "communication", "responsibility",
    "organization", "implementation", "misunderstanding", "synchronization",

    # Keyboard exercise
    "quick", "brown", "fox", "jumps", "over", "lazy", "dog",
    "typing", "keyboard", "practice", "accuracy", "consistency",
    "shift", "control", "backspace", "capslock", "tab", "enter",

    # Punctuation-heavy / code simulation
    "def", "main()", "print('Hello')", "if x == 10:", "try:",
    "except:", "for i in range(5):", "while True:", "elif condition:",

    # Real-world and useful
    "email", "address", "schedule", "meeting", "project", "report",
    "deadline", "feedback", "presentation", "download", "upload",

    # Mixed style
    "Python3", "JavaScript", "HTML_CSS", "Tkinter", "Django", "FlaskApp"
]


class Ui:
    def __init__(self, typing_text:list):

        self.typing_word = typing_text
        self.i = 0
        self.word_to_highlight = 1.0
        self.word_start_of_highlight = 1.0
        self.total_typed_word = 0
        self.total_wrong_typed_word = 0
        self.first_time = True
        self.cpm = 0
        self.wpm = 0

        self.text = " ".join(random.sample(self.typing_word, 50))

        self.timer = TOTAL_GIVEN_TIME

        self.total_wrong_typed_word_list = []
        self.total_attempted_word_list = []

        # root Setup
        self.root = Tk()

        self.root.title('Typing Speed Test')
        self.root.config(bg=APP_BACKGROUND, padx=20,)
        self.root.maxsize(width=750, height=400)
        self.root.minsize(width=750, height=400)

        # Dialog window
        self.dlg = None
        self.txt_file = self.resource_path("./assets/text files/score.txt")

        try:
            with open(self.txt_file, 'r') as file:
                self.highscore_text = file.readline()
        except FileNotFoundError:
            self.highscore_text = 'High Score: 0'

        # App Name
        self.title =Label(text='Typing Speed Test',bg=APP_BACKGROUND,width=18,font=TITLE_FONT, fg=TITLE_COLOR,
                          pady=20)
        self.title.grid(row=0, column=1)

        # container
        self.container = Frame(self.root, background=APP_BACKGROUND)
        self.container.grid(row=1, column=1, pady=5)

        # High Score label
        self.highscore_label = Label(self.container,width=len(self.highscore_text),
                                     text= self.highscore_text, foreground=LABEL_COLOR,
                                     background=APP_BACKGROUND, font=LETTER_FONT,
                                     )
        self.highscore_label.grid(row=0, column=0)

        # CPM label
        self.cpm_label = Label(self.container,width=16, text=f"Corrected CPM: {self.cpm}", foreground=LABEL_COLOR,
                               background=APP_BACKGROUND, font=LETTER_FONT,)
        self.cpm_label.grid(row=0, column=1)

        # WPM label
        self.wpm_label = Label(self.container, width=8, text=f"WPM: {self.wpm}", foreground=LABEL_COLOR,
                               background=APP_BACKGROUND, font=LETTER_FONT,)
        self.wpm_label.grid(row=0, column=2)

        # Timer label
        self.timer_label = Label(self.container, width=14, text=f"Time left: {self.timer}", foreground=LABEL_COLOR,
                               background=APP_BACKGROUND, font=LETTER_FONT,)
        self.timer_label.grid(row=0, column=3)

        # Restart button
        self.restart_button = Button(self.container, text="🔁", command=self.restart)

        self.restart_button.config(fg=DIALOG_BOX_TEXT_COLOR, background=DIALOG_BOX_BACKGROUND, font=('', 20),
                                   padx=10, activebackground=DIALOG_BOX_TEXT_COLOR, activeforeground='#BBFBFF',
                                   borderwidth=0 )

        self.restart_button.grid(row=0, column=4)

        # Word Box
        self.text_box = Text(width=40, height=5, font=FONT, foreground=TEXT_COLOR, wrap='word',
                             background=TEXTBOX_AND_USERBOX_COLOR, padx=20, relief='solid')

        self.text_box.insert(END, chars=self.text,)
        self.text_box.config(state="disabled")

        self.text_box.tag_config('highlight_background', background=WORD_HIGHLIGHT_COLOR)

        self.text_box.tag_config('correct_word_highlight', foreground=CORRECT_WORD_HIGHLIGHT_COLOR)
        self.text_box.tag_config('wrong_word_highlight', foreground=WRONG_COLOR)

        self.text_box.tag_config('highlight_letter_correct', foreground=CORRECT_COLOR)
        self.text_box.tag_config('highlight_letter_wrong', foreground=WRONG_COLOR)

        self.word_list = self.text_box.get(1.0, END).replace('\n', '').split(' ')
        self.text_box.grid(row=2, column=1)

        # User Input
        self.user_text = Entry(width=20, font=FONT, fg=TEXT_COLOR, justify='center',
                               background=TEXTBOX_AND_USERBOX_COLOR,
                                highlightthickness=True, disabledbackground=USERBOX_DISABLE_COLOR)
        self.user_text.focus()
        self.user_text.grid(row=3, column=1, pady=5)

        # Highlighting the selected words.
        self.text_box.mark_set('current_word', 1.0)

        self.word_start = self.text_box.index('current_word')
        self.word_end = f"{self.word_start}+{len(self.word_list[0])}c"
        self.text_box.tag_add('highlight_background', self.word_start, self.word_end)

        # Check if any key is release.
        self.user_text.bind('<KeyRelease>', self.handle_key_release)

        # Keep root window alive
        self.root.mainloop()

    def resource_path(self, relative_path):
        """ Get absolute path to resource (for PyInstaller compatibility) """
        try:
            base_path = sys._MEIPASS  # PyInstaller temp path
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def dismiss(self):
        """This method is used for destroying the dialog box."""
        with open('./assets/text files/score.txt', 'w') as file:
            file.write(f"High Score: {self.cpm}")
        self.dlg.grab_release()
        self.dlg.destroy()

    def restart(self):
        """ To restart the game call this method."""
        self.dlg.grab_release()
        self.dlg.destroy()
        self.root.destroy()

        with open(self.txt_file, 'w') as file:
            file.write(f"High Score: {self.cpm}")
        self.__init__(self.typing_word)


    def handle_key_release(self, event):
        """This method is used to make timer start and calling the check and highlight method. """
        if self.first_time:
            self.count_down(self.timer)         # 🟢 First time only
            self.first_time = False     # 🔁 Disable future calls

        self.check_and_highlight(event) # 🔁 Every time


    def result_dialog_box(self):
        """ This is a custom dialog box for showing final result to the user. """

        message1 = f'(❁´◡`❁) Your score: {self.cpm} CPM(That is {self.wpm} WPM) 👈(⌒▽⌒)👉'
        self.dlg = Toplevel(self.root, padx=10, pady=10, background=DIALOG_BOX_BACKGROUND)

        result_message_label = Label(self.dlg, text=message1, pady=5, font=LETTER_FONT,
                                     fg=DIALOG_BOX_TEXT_COLOR, background=DIALOG_BOX_BACKGROUND)
        result_message_label.pack()

        if self.total_wrong_typed_word_list != self.total_attempted_word_list:
            
            message = (f'In reality, you typed {self.total_typed_word} CPM, '
                       f'but you made {self.total_wrong_typed_word}'
                       f'mistakes (out of {len(self.total_attempted_word_list)} words), '
                       f'\nwhich were not counted in the corrected scores.'
                       f'\n\nYour mistakes were:\n')

            real_message_label = Label(self.dlg, text=message, font=LETTER_FONT,
                                       background=DIALOG_BOX_BACKGROUND, fg=DIALOG_BOX_TEXT_COLOR)
            real_message_label.pack()

            corrected_word_list = []
            for i in range(0, len(self.total_attempted_word_list)):
                if self.total_attempted_word_list[i] != self.total_wrong_typed_word_list[i]:
                    corrected_word_list.append(f'Instead of "{self.total_attempted_word_list[i]}", '
                                               f'you typed "{self.total_wrong_typed_word_list[i]}".')

            choices_var = StringVar(value=corrected_word_list)
            list_of_words = Listbox(self.dlg, height=len(self.total_wrong_typed_word_list),
                                    listvariable=choices_var, justify='center', width=60,
                                    background=DIALOG_BOX_BACKGROUND, highlightthickness=False,
                                    disabledforeground=DIALOG_BOX_TEXT_COLOR, font=LETTER_FONT, borderwidth=0,
                                    state='disabled')
            list_of_words.pack(pady=5)

        else:
            message = f'\n😍 😍 🎉 \nGreate job you have typed all {self.wpm} words correctly!'
            real_message_label = Label(self.dlg, text=message, font=LETTER_FONT,
                                       background=DIALOG_BOX_BACKGROUND, fg=DIALOG_BOX_TEXT_COLOR)
            real_message_label.pack()
        container = Frame(self.dlg, borderwidth=0, background=DIALOG_BOX_BACKGROUND)
        container.pack(pady=10)

        ok_button = Button(container, text="Done", command=self.dismiss)
        ok_button.config(font=LETTER_FONT, fg=DIALOG_BOX_TEXT_COLOR, background=DIALOG_BOX_BACKGROUND,
                         activebackground='#DDF6D2', activeforeground='#4E71FF')
        ok_button.grid(row=0, column=0, padx=10)

        restart_button = Button(container, text="Restart", command=self.restart)
        restart_button.config(font=LETTER_FONT, fg=DIALOG_BOX_TEXT_COLOR, background=DIALOG_BOX_BACKGROUND,
                              activebackground='#CD5656', activeforeground='#BBFBFF')
        restart_button.grid(row=0, column=2, padx=10)

        self.dlg.protocol("WM_DELETE_WINDOW", self.dismiss)
        self.dlg.transient(self.root)  # dialog window is related to main
        self.dlg.wait_visibility()  # can't grab until window appears, so we wait
        self.dlg.grab_set()

    def count_down(self, count:int):
        """This a counter which count down to the count number."""
        self.timer = count
        self.timer_label.config(text=f"Time left: {count}")

        if self.timer > 0:
            self.root.after(1000, self.count_down, self.timer-1)
        else:
            self.user_text.config(state='disabled')
            self.result_dialog_box()

    def check_and_highlight(self, event):
        """This method selects current word and highlight the word."""

        typed_word = ''

        target_word = self.word_list[self.i]
        user_word = self.user_text.get()

        for j, letter in enumerate(user_word.strip()):
            index_letter = f"{self.word_start}+{j}c"
            typed_word += letter
            if j < len(target_word):
                if letter == target_word[j]:
                    self.text_box.tag_add('highlight_letter_correct', index_letter,
                                          f'{index_letter}+1c')
                else:
                    self.text_box.tag_add('highlight_letter_wrong', index_letter,
                                          f'{index_letter}+1c')

        if user_word.endswith(' ') and len(typed_word):

            self.cpm_label.config(text=f"Corrected CPM: {self.cpm}")
            self.wpm_label.config(text=f"WPM: {self.wpm}")
            self.user_text.delete(0, END)
            self.text_box.tag_remove('highlight_background', 1.0, END)

            self.total_attempted_word_list.append(target_word)
            self.total_wrong_typed_word_list.append(typed_word)

            self.total_typed_word += len(typed_word)

            if typed_word == target_word:
                self.cpm += len(target_word)
                self.wpm += 1
                self.text_box.tag_add('correct_word_highlight', self.word_start, self.word_end)
            else:
                self.total_wrong_typed_word += 1
                self.text_box.tag_add('wrong_word_highlight', self.word_start, self.word_end)

            if self.i < len(self.word_list)-1:
                self.i += 1

            if self.i < len(self.word_list):

                next_word = self.word_list[self.i]

                # Move to next word
                self.word_start = f"{self.word_end}+1c"
                self.word_end = f"{self.word_start}+{len(next_word)}c"

                self.text_box.mark_set('current_word', self.word_start)
                self.text_box.tag_add('highlight_background', self.word_start, self.word_end)
                self.text_box.tag_remove('highlight_letter_correct', 1.0, END)
                self.text_box.tag_remove('highlight_letter_wrong', 1.0, END)
                self.text_box.see(self.word_end)

            else:
                # End of word list
                self.user_text.config(state='disabled')




def main():
    app_ui = Ui(typing_text=typing_words)

if __name__ == "__main__":
    main()







