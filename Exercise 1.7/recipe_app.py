from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy import or_

engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Recipe(Base):
  __tablename__ = "final_recipes"
  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(50))
  ingredients = Column(String(255))
  cooking_time = Column(Integer)
  difficulty = Column(String(20))

  def __repr__(self):
    return "<Recipe ID: " + str(self.id) + "-" + self.name + "-" + self.difficulty + ">"
  
  def __str__(self):
    return (
      "Recipe Name: " + self.name + 
      "\n----------" + 
      "\nIngredients: " + self.ingredients + 
      "\nCooking time (in minutes): " + str(self.cooking_time) +
      "\nDifficulty: " + self.difficulty
    )

  def calculate_difficulty(self):
    ingredient_list = self.return_ingredients_as_list()

    if self.cooking_time < 10 and len(ingredient_list) < 4:
      self.difficulty = "Easy"
    elif self.cooking_time < 10 and len(ingredient_list) >= 4:
      self.difficulty = "Medium"
    elif self.cooking_time >= 10 and len(ingredient_list) < 4:
      self.difficulty = "Intermediate"
    elif self.cooking_time >= 10 and len(ingredient_list) >= 4: 
      self.difficulty = "Hard"
  
  def return_ingredients_as_list(self):
    if self.ingredients == "":
      return []
    else:
      return self.ingredients.split(", ")

Base.metadata.create_all(engine)

def create_recipe():
  # Name Validation
  while True:
    name = input("Enter the name of the recipe: ")
    if len(name) > 50:
      print("Name too long, max 50 characters.")
    elif not name.replace(" ", "").isalnum():
      print("Name can only contain letters and numbers.")
    else: 
      break

  # Cooking Time Validation
  while True:
    cooking_time = input("Enter the cooking time (in minutes): ")
    if not cooking_time.isnumeric():
      print("Cooking time can only be numbers.")
    else:
      break

  ingredients = []
  num_ingredients = int(input("How many ingredients would you like to enter? "))

  for i in range(num_ingredients):
    ingredients.append(input("Enter an ingredient: "))
  
  ingredients_str = ", ".join(ingredients)

  recipe = Recipe(
    name = name,
    ingredients = ingredients_str,
    cooking_time = int(cooking_time),
    difficulty = ""
  )

  recipe.calculate_difficulty()

  session.add(recipe)
  session.commit()
  print("Recipe created successfully!")

def view_all_recipes():
  recipe_list = session.query(Recipe).all()

  if not recipe_list:
    print("No recipes found in the database.")
    # return None

  for recipe in recipe_list:
    print(recipe)
    print()
  
def search_by_ingredients():
  if session.query(Recipe).count() == 0:
    print("No recipes found in the database.")
    # return None
  
  results = session.query(Recipe.ingredients).all()
  all_ingredients = []

  for row in results:
    ingredient_split = [i.strip() for i in row[0].split(', ')]
    for ingredient in ingredient_split:
      if ingredient not in all_ingredients:
        all_ingredients.append(ingredient)

  print("Available ingredients: ")
  print("-------------------------")
  for idx, ingredient in enumerate(all_ingredients, 1):
    print(f"{idx}. {ingredient}")

  user_input = input("Choose ingredient(s) by number (separate multiple with spaces): ")
  try:
    choices = [int(x) for x in user_input.split()]
  except ValueError:
    print("Invalid input. Please enter numbers only.")
    # return None
  
  if any(c < 1 or c > len(all_ingredients) for c in choices):
    print("One or more selected numbers are invalid.")
    # return None

  search_ingredients = [all_ingredients[c - 1] for c in choices]
  print(f"You selected: {', '.join(search_ingredients)}")

  conditions = []

  for ingredient in search_ingredients:
    like_term = f"%{ingredient}%"
    conditions.append(Recipe.ingredients.like(like_term))

  results = session.query(Recipe).filter(or_(*conditions)).all()

  if not results:
    print("No recipes found with the chosen ingredients.")
    # return None
  
  print("Search results:")
  print("----------------")
  for recipe in results:
    print(recipe)
  print("Search complete!")

def edit_recipe():
  if session.query(Recipe).count() == 0:
    print("No recipes found in the database.")
    # return None
  
  results = session.query(Recipe.id, Recipe.name).all()

  print("Available Recipes:")
  print("-------------------------")
  for recipe_id, name in results:
    print(f"{recipe_id}. {name}")

  try:
    recipe_id = int(input("Enter the ID of the recipe to edit: "))
  except ValueError:
    print("Invalid input.")
    # return None
  
  recipe_to_edit = session.query(Recipe).filter_by(id=recipe_id).first()

  if not recipe_to_edit:
    print("Recipe not found.")
    # return None

  print("What would you like to update?")
  print("--------------------------------")
  print(f"1. Name: {recipe_to_edit.name}")
  print(f"2. Cooking Time: {recipe_to_edit.cooking_time}")
  print(f"3. Ingredients: {recipe_to_edit.ingredients}")
  choice = input("Your choice: ")

  if choice == '1':
    update_name = input("Enter the new name for the recipe: ")
    if len(update_name) > 50:
      print("Name too long.")
      # return None

    recipe_to_edit.name = update_name

  elif choice == '2':
    update_cooking_time = input("Enter the new cooking time for the recipe: ")
    if not update_cooking_time.isnumeric():
      print("Invalid cooking time.")
      # return None

    recipe_to_edit.cooking_time = int(update_cooking_time)

  elif choice == '3':
    ingredients = []
    count = input("How many ingredients? ")
    if not count.isnumeric():
      print("Invalid number.")
      # return None

    for i in range(int(count)):
      ingredients.append(input("Enter ingredient: "))

    recipe_to_edit.ingredients = ", ".join(ingredients)
  
  else:
    print("Invalid choice.")
    # return None
  
  recipe_to_edit.calculate_difficulty()
  session.commit()
  print("Recipe updated successfully!")

def delete_recipe():
  if session.query(Recipe).count() == 0:
    print("No recipes found in the database.")
    # return None
  
  results = session.query(Recipe.id, Recipe.name).all()

  print("Available Recipes:")
  print("-------------------------")
  for recipe_id, name in results:
    print(f"{recipe_id}. {name}")

  try:
    recipe_id = int(input("Enter the ID of the recipe to delete: "))
  except ValueError:
    print("Invalid input.")
    # return None
  
  recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).first()

  if recipe_to_delete is None:
    print("No recipe found with that ID.")
    return

  delete_confirm = input(f"Are you sure you want to delete {recipe_to_delete.name}? (Yes/No) ")

  if delete_confirm == "Yes" or "yes" or "Y" or "y":
    session.delete(recipe_to_delete)
    session.commit()
    print("Recipe deleted.")
  elif delete_confirm == "No" or "no" or "N" or "n":
    print("Delete cancelled.")
    # return None
  else:
    print("Invalid choice.")
    # return None

def main_menu():
  choice = ''
  while(choice != 'quit'):
    print("Main Menu")
    print("-----------------------------")
    print("What would you like to do? Pick a choice!")
    print("1. Create Recipe")
    print("2. View Recipes")
    print("3. Search Recipe")
    print("4. Update Recipe")
    print("5. Delete Recipe")
    print("Type 'quit' to exit the program.")
    choice = input("Your choice: ")

    if choice == '1':
      create_recipe()
    elif choice == '2':
      view_all_recipes()
    elif choice == '3':
      search_by_ingredients()
    elif choice == '4':
      edit_recipe()
    elif choice == '5':
      delete_recipe()
    else:
      print("Invalid choice.")
  
  session.commit()
  session.close()
  engine.dispose()
  print("Goodbye!")

main_menu()