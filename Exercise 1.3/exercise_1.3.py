recipes_list = []
ingredients_list = []

def take_recipe():
  global name
  global cooking_time
  global ingredients
  global recipe

  name = str(input("Enter the name of the recipe: "))
  cooking_time = int(input("Enter the cooking time (in minutes): "))
  ingredients = list(input("Enter the ingredients: ").split(', '))
  recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}

n = int(input("How many recipes would you like to enter? "))

for i in range(n):
  take_recipe()
  for ingredient in ingredients:
    if ingredient not in ingredients_list:
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

for recipe in recipes_list:
  print("Recipe: ", recipe['name'])
  print("Cooking time (minutes): ", recipe['cooking_time'])
  print("Ingredients:")
  for ingredient in ingredients:
    print(ingredient)
  if cooking_time < 10 and len(ingredients) < 4:
    difficulty = "Easy"
    print("Difficulty: Easy")
  elif cooking_time < 10 and len(ingredients) >= 4:
    difficulty = "Medium"
    print("Difficulty: Medium")
  elif cooking_time >= 10 and len(ingredients) < 4:
    difficulty = "Intermediate"
    print("Difficulty: Intermediate")
  elif cooking_time >= 10 and len(ingredients) >= 4: 
    difficulty = "Hard"
    print("Difficulty: Hard")
  print("---")

list.sort(ingredients_list)
print("Ingredients Available Across All Recipes")
print("----------------------------------------")
for ingredient in ingredients_list:
  print(ingredient)