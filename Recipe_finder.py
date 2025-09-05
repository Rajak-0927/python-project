from tkinter import Tk, Label, Entry, Button, Text, END, Canvas
from PIL import Image, ImageTk
import tkinter.font as tkFont  # Import the font module
import requests
from io import BytesIO
import webbrowser

# API details
API_KEY = '11d06c59eefb43b0a77d59e51d85ce11'  # Replace with your valid Spoonacular API key
BASE_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# App constants
WINDOW_TITLE = "Recipe Finder"
RECIPE_IMAGE_SIZE = (300, 200)
BG_COLOR = "#9FE2BF"
BTN_COLOR = "#00796b"


class RecipeApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.window = Tk()
        self.window.title(WINDOW_TITLE)

        # Start maximized
        self.window.state("zoomed")

        # Detect screen width and height
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Load and resize background image
        try:
            bg_image = Image.open(r"C:\Users\Admin\OneDrive\Desktop\project\Food Shot18 .jpeg.jpg")  
            bg_image = bg_image.resize((screen_width, screen_height))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
        except Exception as e:
            print("Error loading background image:", e)
            self.bg_photo = None

        # Create canvas
        self.canvas = Canvas(self.window, width=screen_width, height=screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Display background image
        if self.bg_photo:
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        # Define custom fonts
        font_title = tkFont.Font(family="Roboto", size=32, weight="bold")
        font_label = tkFont.Font(family="Helvetica", size=14, weight="bold")
        font_entry = tkFont.Font(family="Helvetica", size=12)
        font_button = tkFont.Font(family="Helvetica", size=12, weight="bold")
        font_text = tkFont.Font(family="Helvetica", size=12)

        # Title label
        self.title_label = Label(self.window, text="Explore Tastes, Create Memories", font=font_title, bg=BG_COLOR, fg="white")
        self.title_label.place(relx=0.5, y=50, anchor="center")

        # Search label
        self.label = Label(self.window, text="Enter Ingredients (comma-separated):", bg=BG_COLOR, fg="black", font=font_label)
        self.label.place(relx=0.5, y=200, anchor="center")

        # Entry box
        self.entry = Entry(self.window, width=50, font=font_entry)
        self.entry.place(relx=0.5, y=240, anchor="center")

        # Search button
        self.search_button = Button(self.window, text="Search", command=self.search_recipes, bg=BTN_COLOR, fg="white", font=font_button)
        self.search_button.place(relx=0.5, y=270, anchor="center")  

        # Result display
        self.result_text = Text(self.window, height=10, width=50, wrap='word', bg="#f1f8e9", font=font_text)
        self.result_text.place(relx=0.5, y=370, anchor="center")

        # Image holder
        self.image_label = Label(self.window, bg=BG_COLOR)
        self.image_label.place(relx=0.5, y=600, anchor="center")

    def search_recipes(self):
        ingredients = self.entry.get()
        if not ingredients:
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, "Please enter some ingredients.")
            return

        # Clear previous results
        self.result_text.delete(1.0, END)
        self.image_label.config(image='')

        # API request
        params = {
            'apiKey': self.api_key,
            'ingredients': ingredients,
            'number': 1
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()  # Raise an error for failed requests
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.result_text.insert(END, f"Error fetching recipes: {e}")
            return

        # Display result
        if data:
            recipe = data[0]
            title = recipe['title']
            image_url = recipe['image']
            recipe_id = recipe['id']

            self.result_text.insert(END, f"Recipe: {title}\n")
            self.result_text.insert(END, "Click here to view the recipe.")

            # Display image
            self.display_image(image_url)

            # Bind a function to open the recipe URL dynamically
            def open_recipe(event):
                url = f"https://spoonacular.com/recipes/{title.replace(' ', '-').lower()}-{recipe_id}"
                webbrowser.open(url)

            # Get position for the tag to dynamically link the text
            start_index = self.result_text.index("end-1c linestart")  # Position of last inserted text
            end_index = self.result_text.index("end-1c lineend")  # End position of the text

            self.result_text.tag_add("recipe_link", start_index, end_index)
            self.result_text.tag_config("recipe_link", foreground="blue", underline=1)
            self.result_text.tag_bind("recipe_link", "<Button-1>", open_recipe)

        else:
            self.result_text.insert(END, "No recipes found for the given ingredients.")

    def display_image(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            img_data = Image.open(BytesIO(response.content))
            img_data = img_data.resize(RECIPE_IMAGE_SIZE)
            photo = ImageTk.PhotoImage(img_data)

            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep reference to prevent garbage collection

        except Exception as e:
            print("Error loading image:", e)

    def run(self):
        self.window.mainloop()

# Run the app
if __name__ == "__main__":
    app = RecipeApp(API_KEY)
    app.run()
