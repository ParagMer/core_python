import json

class Task:
    def __init__(self, task_id, title, description, completed=False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.completed = completed

    def to_dict(self):
        """Convert the task object to a dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed
        }

    @classmethod
    def from_dict(cls, task_dict):
        """Create a task object from a dictionary."""
        return cls(
            task_dict['task_id'],
            task_dict['title'],
            task_dict['description'],
            task_dict['completed']
        )


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        try:
            with open(self.filename, 'r') as file:
                tasks_data = json.load(file)
                return [Task.from_dict(task) for task in tasks_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_tasks(self):
        """Save the tasks to the JSON file."""
        with open(self.filename, 'w') as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def create_task(self, title, description):
        """Create a new task."""
        task_id = len(self.tasks) + 1  # Simple incremental ID generation
        new_task = Task(task_id, title, description)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f"Task '{title}' created successfully.")

    def edit_task(self, task_id, title=None, description=None, completed=None):
        """Edit an existing task."""
        task = self.get_task_by_id(task_id)
        if task:
            if title: task.title = title
            if description: task.description = description
            if completed is not None: task.completed = completed
            self.save_tasks()
            print(f"Task {task_id} updated successfully.")
        else:
            print(f"Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        """Delete a task by its ID."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Task with ID {task_id} not found.")

    def get_task_by_id(self, task_id):
        """Retrieve a task by its ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def list_tasks(self):
        """List all tasks."""
        if not self.tasks:
            print("No tasks available.")
        for task in self.tasks:
            status = "Completed" if task.completed else "Pending"
            print(f"ID: {task.task_id} | Title: {task.title} | Status: {status}")
            
    def mark_task_complete(self, task_id):
        """Mark a task as complete."""
        task = self.get_task_by_id(task_id)
        if task:
            task.completed = True
            self.save_tasks()
            print(f"Task {task_id} marked as complete.")
        else:
            print(f"Task with ID {task_id} not found.")


# Main Program
def main():
    task_manager = TaskManager()

    while True:
        print("\n--- To-Do Task Manager ---")
        print("1. Create Task")
        print("2. Edit Task")
        print("3. Delete Task")
        print("4. List Tasks")
        print("5. Mark Task as Complete")
        print("6. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                title = input("Enter task title: ")
                description = input("Enter task description: ")
                task_manager.create_task(title, description)

            elif choice == 2:
                task_id = int(input("Enter task ID to edit: "))
                title = input("Enter new task title (leave blank to keep current): ")
                description = input("Enter new task description (leave blank to keep current): ")
                completed_input = input("Mark as completed? (y/n): ")
                completed = True if completed_input.lower() == 'y' else None
                task_manager.edit_task(task_id, title if title else None, description if description else None, completed)

            elif choice == 3:
                task_id = int(input("Enter task ID to delete: "))
                task_manager.delete_task(task_id)

            elif choice == 4:
                task_manager.list_tasks()

            elif choice == 5:
                task_id = int(input("Enter task ID to mark as complete: "))
                task_manager.mark_task_complete(task_id)

            elif choice == 6:
                print("Exiting the system...")
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
