from tkinter import Tk, ttk, Listbox, Variable, SINGLE, VERTICAL, N, W, E, S, StringVar, messagebox, simpledialog

from database.operations import create_task, get_tasks, remove_task, edit_task


class MainForm(Tk):
    def __init__(self):
        super().__init__()
        self.title('Todo app')
        self.geometry("840x640")
        self.wm_maxsize(840, 640)
        self.wm_minsize(840, 640)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=30)

        self.title_label = ttk.Label(self, text='Daily tasks', font=('Arial', 28))
        self.title_label.grid(column=0, row=0)

        self.tools_frame = ttk.Frame(self, padding=(10, 10, 10, 10))
        self.tools_frame.grid(column=0, row=1)

        self.task_caption = StringVar()
        self.task_entry = ttk.Entry(self.tools_frame, textvariable=self.task_caption)
        self.task_entry.grid(column=0, row=0, sticky=(N, S, W, E))

        self.add_button = ttk.Button(self.tools_frame, text='Add', command=self.add_button_click)
        self.add_button.grid(column=1, row=0, padx=10)
        self.remove_button = ttk.Button(self.tools_frame, text='Remove', command=self.remove_button_click)
        self.remove_button.grid(column=2, row=0, padx=10)
        self.edit_button = ttk.Button(self.tools_frame, text='Edit', command=self.edit_button_click)
        self.edit_button.grid(column=3, row=0, padx=10)

        self.tasks_list = get_tasks()
        self.tasks_list_var = Variable(value=self.tasks_list)
        self.tasks_lb = Listbox(self, listvariable=self.tasks_list_var, selectmode=SINGLE)
        self.tasks_lb.grid(column=0, row=2, sticky=(E, W, N, S))
        self.bind('<<ListboxSelect>>', self.task_selected)

        self.lb_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.tasks_lb.yview)
        self.tasks_lb.config(yscrollcommand=self.lb_scrollbar.set)
        self.lb_scrollbar.grid(column=1, row=2, sticky=(N, S, W))

    def add_button_click(self):
        value = self.task_caption.get().strip()
        if value:
            task = create_task(value)
            if task:
                self.tasks_list = get_tasks()
                self.tasks_list_var.set(self.tasks_list)
                self.task_caption.set('')
            else:
                messagebox.showerror('Error', 'The task already exists')
        else:
            messagebox.showerror('Error', 'The field is empty')

    def remove_button_click(self):
        value = self.task_caption.get()
        if value:
            result = remove_task(value)
            if result:
                self.tasks_list = get_tasks()
                self.tasks_list_var.set(self.tasks_list)
                selected_item_id = self.tasks_lb.curselection()
                if selected_item_id:
                    self.task_caption.set(self.tasks_lb.get(selected_item_id))
            else:
                messagebox.showerror('Error', 'Task with this name does not exist')
        else:
            messagebox.showerror('Error', 'The element was not selected')

    def edit_button_click(self):
        val = self.task_caption.get()
        if val in self.tasks_list:
            new_val = simpledialog.askstring('Edit element', f'Editing element "{val}"', initialvalue=val)
            new_val = new_val.strip()
            if new_val:
                if new_val not in self.tasks_list:
                    if edit_task(val, new_val):
                        self.task_caption.set(new_val.strip())
                        self.tasks_list = get_tasks()
                        self.tasks_list_var.set(self.tasks_list)
                    else:
                        messagebox.showerror('Error', 'Task with this name does not exist')
                else:
                    messagebox.showerror('Error', f'Task with name {new_val} already exists')
        else:
            messagebox.showerror('Error', 'Task with this name does not exist')

    def task_selected(self, event):
        if self.tasks_list_var.get():
            selected_item_id = self.tasks_lb.curselection()
            if selected_item_id:
                self.task_caption.set(self.tasks_lb.get(selected_item_id))
