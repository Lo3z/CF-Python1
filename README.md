# Recipe App (Command Line Version)

This project should allow users to create and mofidy recipes with ignredients, cooking times, and difficulty parameters. 
All input and output for this app will take place in the command line/powershell. 


## Key Features

- Create and manage recipes on a locally hosted MySQL database. 
- Option to search for recipes that contain a specific set of ingredients. 
- Automatically rates each recipe by their difficulty level.
- Display more details on each recipe if the user prompts it, such as the incredits, cook time, and difficulty. 

## Structure for Recipes

- We will be using Dictionaries as the primary structure for each recipe, as we have multiple keys to work with for each recipe (name, cooking time, and ingredients). A dictionary would allow us to store values for these keys and these values can be lists as well, which works well for the ingredients key.
- We will be using a List as the primary structure for our "all_recipes" data, since we can easily append new recipes, and delete existing recipes from the list. 
