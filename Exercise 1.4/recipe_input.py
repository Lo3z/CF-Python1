import pickle

recipes_list = []
all_ingredients = []

def take_recipe():
  global name
  global cooking_time
  global ingredients
  global recipe
  global difficulty

  name = str(input("Enter the name of the recipe: "))
  cooking_time = int(input("Enter the cooking time (in minutes): "))
  ingredients = list(input("Enter the ingredients: ").split(', '))
  difficulty = calc_difficulty()
  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients, 'difficulty': difficulty}

  print(recipe)

def calc_difficulty():

  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = "Easy"
  elif cooking_time < 10 and len(ingredients) >= 4:
    difficulty = "Medium"
  elif cooking_time >= 10 and len(ingredients) < 4:
    difficulty = "Intermediate"
  elif cooking_time >= 10 and len(ingredients) >= 4: 
    difficulty = "Hard"
  return difficulty
  
filename = input("Enter the filename where you will store your recipe: ")

try:
  with open(filename, 'rb') as my_file:
    data = pickle.load(my_file)
except FileNotFoundError: 
  print("File does not exist. Creating file...")
  data = {
    "recipes_list": [],
    "all_ingredients": []
  }
except:
  print("Something went wrong. Creating file...")
  data = {
    "recipes_list": [],
    "all_ingredients": []
  }
else: 
  print("File loaded successfully.")
  my_file.close()
finally: 
  recipes_list = data['recipes_list']
  all_ingredients = data['all_ingredients']
  print("Process complete.")

n = int(input("How many recipes would you like to enter? "))

for i in range(n):
  take_recipe()
  for ingredient in ingredients:
    if ingredient not in all_ingredients:
      all_ingredients.append(ingredient)
  recipes_list.append(recipe)

data = { 
  "recipes_list": recipes_list, 
  "all_ingredients": all_ingredients
}

with open(filename, 'wb') as my_file:
  pickle.dump(data, my_file)