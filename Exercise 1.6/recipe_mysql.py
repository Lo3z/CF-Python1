import mysql.connector

conn = mysql.connector.connect(
  host='localhost',
  user='cf-python',
  passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute('''
CREATE TABLE IF NOT EXISTS Recipes (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(50),
  ingredients VARCHAR(255),
  cooking_time INT,
  difficulty VARCHAR(20)
);
''')

def create_recipe(conn, cursor):
  name = str(input("Enter the name of the recipe: "))
  cooking_time = int(input("Enter the cooking time (in minutes): "))
  ingredients = list(input("Enter the ingredients: ").split(', '))
  difficulty = calculate_difficulty(cooking_time, ingredients)

  ingredients_str = ", ".join(ingredients)

  cursor.execute('''
  INSERT INTO Recipes (
    name, ingredients, cooking_time, difficulty)
    VALUES (%s, %s, %s, %s)
  ''', (name, ingredients_str, cooking_time, difficulty))

  conn.commit()

def calculate_difficulty(cooking_time, ingredients):
  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = "Easy"
  elif cooking_time < 10 and len(ingredients) >= 4:
    difficulty = "Medium"
  elif cooking_time >= 10 and len(ingredients) < 4:
    difficulty = "Intermediate"
  elif cooking_time >= 10 and len(ingredients) >= 4: 
    difficulty = "Hard"
  return difficulty

def search_recipe(conn, cursor):
  all_ingredients = []

  cursor.execute("SELECT ingredients FROM Recipes")
  results = cursor.fetchall()

  for row in results:
    ingredient_string = row[0]
    ingredient_split = [i.strip() for i in ingredient_string.split(',')]
    for ingredient in ingredient_split:
      if ingredient not in all_ingredients:
        all_ingredients.append(ingredient)

  print("Available ingredients: ")
  print("-------------------------")
  for idx, ingredient in enumerate(all_ingredients, 1):
    print(f"{idx}. {ingredient}")
  
  choice = int(input("Choose an ingredient by number: "))
  search_ingredient = all_ingredients[choice - 1]
  print(f"You selected: {search_ingredient}")

  cursor.execute(
    'SELECT name FROM Recipes WHERE ingredients LIKE %s',
    ('%' + search_ingredient + '%',)
  )
  results = cursor.fetchall()
  print("Search complete!")
  print("Search results: ")
  print("----------------")
  for row in results: 
    print(row[0])

def update_recipe(conn, cursor):
  cursor.execute("SELECT id, name FROM Recipes")
  results = cursor.fetchall()

  print("Available recipes: ")
  print("----------------------")
  for idx, row in enumerate(results, 1):
    print(f"{idx}. {row[1]}")

  update_choice = ''
  choice = int(input("Choose a recipe to update by number: "))
  search_recipe = results[choice - 1]
  print(f"You selected: {search_recipe[1]}.")

  print("What would you like to update?")
  print("--------------------------------")
  print("1. Name")
  print("2. Cooking Time (in minutes)")
  print("3. Ingredients")
  update_choice = input("Your choice: ")

  if update_choice == '1':
    update_name = str(input("Enter the new name for the recipe: "))
    cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (update_name, search_recipe[0]))

    conn.commit()
    print("Update complete!")
  elif update_choice == '2':
    update_cooking_time = int(input("Enter the new cooking time for the recipe: "))
    cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (update_cooking_time, search_recipe[0]))

    cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (search_recipe[0],))
    row = cursor.fetchone()
    current_ingredients = row[0].split(', ')
    update_difficulty = calculate_difficulty(update_cooking_time, current_ingredients)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (update_difficulty, search_recipe[0]))

    conn.commit()
    print("Update complete!")
  elif update_choice == '3':
    update_ingredients = list(input("Enter the new ingredients: ").split(', '))
    update_ingredients_str = ", ".join(update_ingredients)
    cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (update_ingredients_str, search_recipe[0]))

    cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (search_recipe[0],))
    row = cursor.fetchone()
    current_cooking_time = row[0]
    update_difficulty = calculate_difficulty(current_cooking_time, update_ingredients)
    cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (update_difficulty, search_recipe[0]))

    conn.commit()
    print("Update complete!")

def delete_recipe(conn, cursor):
  cursor.execute("SELECT id, name FROM Recipes")
  results = cursor.fetchall()

  print("Available recipes: ")
  print("----------------------")
  for idx, row in enumerate(results, 1):
    print(f"{idx}. {row[1]}")

  choice = int(input("Choose a recipe to delete by number: "))
  delete_recipe = results[choice - 1]
  print(f"{delete_recipe[1]} will be deleted...")

  cursor.execute("DELETE FROM Recipes WHERE id = %s", (delete_recipe[0],))
  print("Recipe was deleted.")
  conn.commit()

def main_menu(conn, cursor):
  choice = ''
  while(choice != 'quit'):
    print("Main Menu")
    print("-----------------------------")
    print("What would you like to do? Pick a choice!")
    print("1. Create Recipe")
    print("2. Search Recipe")
    print("3. Update Recipe")
    print("4. Delete Recipe")
    print("Type 'quit' to exit the program.")
    choice = input("Your choice: ")

    if choice == '1':
      create_recipe(conn, cursor)
    elif choice == '2':
      search_recipe(conn, cursor)
    elif choice == '3':
      update_recipe(conn, cursor)
    elif choice == '4':
      delete_recipe(conn, cursor)
  
  conn.commit()
  conn.close()
  print("Goodbye!")

main_menu(conn, cursor)