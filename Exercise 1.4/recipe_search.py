import pickle

def display_recipe(recipe):
  print("Recipe: ", recipe['name'])
  print("--------------------")
  print("Cooking time (minutes): ", recipe['cooking_time'])
  print("Ingredients: ", recipe['ingredients'])
  print("Difficulty: ", recipe['difficulty'])

def search_ingredient(data):
  all_ingredients = data["all_ingredients"]
  recipes_list = data["recipes_list"]

  for index, ingredient in enumerate(all_ingredients):
    print(f"Index {index}: {ingredient}")
  
  try:
    user_index = int(input("enter the number of the ingredient: "))
    ingredient_searched = all_ingredients[user_index]
  except ValueError:
    print("Input is invalid.")
  else:
    for recipe in recipes_list:
      if ingredient_searched in recipe['ingredients']:
        print(recipe)

filename = input("Enter the filename where you've stored your recipe data: ")

try:
  with open(filename, 'rb') as my_file:
    data = pickle.load(my_file)
except FileNotFoundError:
  print("File does not exist.")
else:
  search_ingredient(data)