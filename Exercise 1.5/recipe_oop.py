class Recipe(object):

  all_ingredients = []

  def __init__(self, name, ingredients, cooking_time):
    self.name = name
    self.ingredients = ingredients
    self.cooking_time = cooking_time
    self.difficulty = None
  
  def get_name(self):
    return self.name
  
  def set_name(self):
    self.name = name
  
  def get_cooking_time(self):
    return self.cooking_time
  
  def set_cooking_time(self):
    self.cooking_time = cooking_time
  
  def add_ingredients(self, *ingredients):
    for ingredient in ingredients:
      self.ingredients.append(ingredient)
    self.update_all_ingredients()
  
  def get_ingredients(self):
    return self.ingredients

  def calculate_difficulty(self):
    if self.cooking_time < 10 and len(self.ingredients) < 4:
      self.difficulty = "Easy"
    elif self.cooking_time < 10 and len(self.ingredients) >= 4:
      self.difficulty = "Medium"
    elif self.cooking_time >= 10 and len(self.ingredients) < 4:
      self.difficulty = "Intermediate"
    elif self.cooking_time >= 10 and len(self.ingredients) >= 4: 
      self.difficulty = "Hard"

  def get_difficulty(self):
    if self.difficulty is None:
      self.calculate_difficulty()
      return self.difficulty
    else:
      return self.difficulty

  def search_ingredient(self, ingredient):
    if ingredient in self.ingredients:
      return True
    else:
      return False
  
  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      if ingredient not in Recipe.all_ingredients:
        Recipe.all_ingredients.append(ingredient)

  def __str__(self):
    output = str("\n"+str(self.name) +"\n" + 30*'-' + '\nIngredients: ' + str(self.ingredients) + '\nCooking Time (in minutes): ' + str(self.cooking_time) + '\nDifficulty: ' + str(self.difficulty))
    return output

  def recipe_search(data, search_term):
    print("\nSearch results for " + str(search_term) +": ")
    for recipe in data:
      if recipe.search_ingredient(search_term):
        print(recipe)

tea = Recipe(
  "Tea",
  ["Leaves", "Sugar", "Water"],
  5,
)
tea.calculate_difficulty()
print(tea)

coffee = Recipe(
  "Coffee",
  ["Coffee Grounds", "Sugar", "Water"],
  5,
)
coffee.calculate_difficulty()
print(coffee)

cake = Recipe(
  "Cake",
  ["Sugar", "Butter", "Eggs", "Vanilla Extract", "Flour", "Baking Powder", "Milk"],
  50
)
cake.calculate_difficulty()
print(cake)

banana_smoothie = Recipe(
  "Banana Smoothie",
  ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"],
  5
)
banana_smoothie.calculate_difficulty()
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

Recipe.recipe_search(recipes_list, "Water")
Recipe.recipe_search(recipes_list, "Sugar")
Recipe.recipe_search(recipes_list, "Bananas")