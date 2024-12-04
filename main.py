import tkinter as tk
from tkinter import messagebox, ttk

# Sample data: list of 15 people with their cost and capability
people = [
    {"name": "Alice", "cost": 200, "capability": 7},
    {"name": "Bob", "cost": 450, "capability": 9},
    {"name": "Charlie", "cost": 300, "capability": 6},
    {"name": "David", "cost": 400, "capability": 8},
    {"name": "Eve", "cost": 250, "capability": 5},
    {"name": "Frank", "cost": 350, "capability": 7},
    {"name": "Grace", "cost": 400, "capability": 6},
    {"name": "Hannah", "cost": 320, "capability": 8},
    {"name": "Ivy", "cost": 280, "capability": 5},
    {"name": "Jack", "cost": 420, "capability": 9},
    {"name": "Kara", "cost": 310, "capability": 7},
    {"name": "Leo", "cost": 360, "capability": 8},
    {"name": "Mia", "cost": 240, "capability": 5},
    {"name": "Nina", "cost": 410, "capability": 9},
    {"name": "Oscar", "cost": 370, "capability": 6}
]

class TeamAllocator:
    def __init__(self, master):
        self.master = master
        master.title("Team Allocator")

        self.teams_count = tk.IntVar(value=3)
        self.team_labels = []
        self.person_listboxes = []
        self.allocated_people = set()
        self.selected_people_per_team = {}

        self.create_widgets()

    def create_widgets(self):
        # Input for number of teams
        ttk.Label(self.master, text="Number of Teams:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
        team_entry = ttk.Entry(self.master, width=5, textvariable=self.teams_count)
        team_entry.grid(row=0, column=1, padx=10, pady=5)

        # Button to create team labels and person dropdowns
        create_teams_button = ttk.Button(self.master, text="Create Teams", command=self.create_team_widgets)
        create_teams_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_team_widgets(self):
        num_teams = self.teams_count.get()

        # If the number of teams is different, recreate all widgets
        if len(self.team_labels) != num_teams:
            for label in self.team_labels:
                label.destroy()
            for listbox in self.person_listboxes:
                listbox.destroy()

            self.team_labels.clear()
            self.person_listboxes.clear()
            self.selected_people_per_team.clear()
            self.allocated_people.clear()  # Clear allocated people

            # Create labels and dropdowns for each team
            for i in range(num_teams):
                ttk.Label(self.master, text=f"Team {i+1}").grid(row=3 + 2 * i, column=0, padx=10, pady=5, sticky=tk.W)
                self.team_labels.append(f"Team {i+1}")

                # Create a listbox for selecting people
                listbox = tk.Listbox(self.master, selectmode=tk.MULTIPLE, width=30)
                for person in people:
                    if person["name"] not in self.allocated_people:
                        listbox.insert(tk.END, person["name"])
                listbox.grid(row=3 + 2 * i, column=1, padx=10, pady=5)
                self.person_listboxes.append(listbox)

        else:
            # Update the options in each listbox
            for i, listbox in enumerate(self.person_listboxes):
                current_selections = [listbox.get(idx) for idx in listbox.curselection()]
                listbox.delete(0, tk.END)
                for person in people:
                    if person["name"] not in self.allocated_people or person["name"] in current_selections:
                        listbox.insert(tk.END, person["name"])
                # Restore the previous selection
                for name in current_selections:
                    idx = listbox.get(0, tk.END).index(name)
                    listbox.selection_set(idx)

        # Button to allocate teams
        allocate_teams_button = ttk.Button(self.master, text="Allocate Teams", command=self.allocate_teams)
        allocate_teams_button.grid(row=3 + 2 * num_teams, column=0, columnspan=2, pady=10)

    def allocate_teams(self):
        self.allocated_people.clear()  # Clear previously allocated people
        team_allocations = {}
        for i, listbox in enumerate(self.person_listboxes):
            selected_indices = listbox.curselection()
            selected_names = [listbox.get(idx) for idx in selected_indices]
            
            # Update allocated people
            self.allocated_people.update(selected_names)
            
            # Store the selected names for each team
            self.selected_people_per_team[f"Team {i+1}"] = selected_names

        messagebox.showinfo("Team Allocation", f"{self.selected_people_per_team}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TeamAllocator(root)
    root.mainloop()
