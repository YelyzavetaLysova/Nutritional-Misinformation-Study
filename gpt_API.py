import openai
from openai import OpenAI
import csv
import pandas as pd


OPENAI_API_KEY = "yourAPI_key"

client = OpenAI(api_key=OPENAI_API_KEY)

meals_list = ["Angel Food Cakes","Antipasti", "Appetizers and Snacks", "Apple Pie", "Artichoke Dips", "Bagels", "Baked Beans", "Banana Breads", "Bar Cookies", 
    "Beef Recipes", "Beef Stews", "Beef Stroganoff", "Beef Tenderloin", "Biscotti", "Biscuits", "Blintzes", "Blondies", "Blueberry Pie", 
    "Borscht", "Breads", "Breakfast Burritos", "Breakfast Casseroles", "Breakfast Potatoes", "Brownies", "Bruschetta", "Buffalo Chicken Dips", 
    "Buffalo Chicken Wings", "Bulgogi", "Burgers", "Burritos", "Butternut Squash Soups", "Cabbage Rolls", "Cakes", "Calzones", "Carrot Cakes", "Casseroles", 
    "Ceviche", "Cheese Balls", "Cheese Fondue", "Cheesecakes", "Cherry Pie", "Chess Pie", "Chicken Adobo", "Chicken and Dumplings", "Chicken Cacciatore", 
    "Chicken Cordon Bleu", "Chicken Marsala", "Chicken Noodle Soups", "Chicken Parmesan", "Chicken Piccata", "Chicken Salads""Chicken Teriyaki", 
    "Chilaquiles", "Chiles Rellenos", "Chili Recipes", "Chocolate Cakes", "Chocolate Chip Cookies", "Chocolate Fudge", "Chowders", "Cinnamon Rolls", 
    "Cobblers", "Coffee Cakes", "Coleslaws", "Cookies", "Cornbread", "Crab Cakes", "Creme Brulee", "Crisps and Crumbles", "Cupcakes", 
    "Danishes", "Deviled Eggs", "Doughnuts", "Drop Cookies", "Dumplings", "Egg Rolls", "Egg Salads", "Eggplant Parmesan", "Empanadas", "Enchiladas", 
    "Energy Balls", "English Muffins", "Etouffee", "Fajitas", "Falafel", "Fettuccini", "Filet Mignon", "Flan", "Flank Steak", "Flat Iron Steak", "Flatbreads", 
    "French Onion Soups", "French Toast", "Fried Chicken", "Fried Rice", "Fries", "Frittatas", "Frostings and Icings", "Fruit Salads", "Fruitcakes", 
    "Fudge", "Garlic Bread", "Gazpacho", "Gingerbread Cookies", "Gnocchi", "Goulash", "Granola", "Gravies", "Green Salads", "Grits", 
    "Ground Beef", "Ground Chicken", "Ground Lamb", "Ground Pork", "Ground Turkey", "Gumbos", "Gyros", "Hummus", "Hushpuppies", "Ice Cream", 
    "Jalapeno Poppers", "Jambalayas", "Jerky", "Kalbi", "Key Lime Pie", "Kolache", "Lamb", "Lasagna", "Lemon Bars", "Lettuce Wraps", "Linguine", 
    "Macaroni and Cheese", "Macaroons", "Manicotti", "Mashed Potatoes", "Meatballs", "Meatloaf", "Minestrone Soups", "Monkey Bread", "Mousses", "Muffins", "Mushroom Soups", "Mushrooms", "Nachos", "Noodle Casseroles", "Oatmeal", "Oatmeal Cookies", "Omelets", "Pad Thai", "Paella", "Pancakes", "Pancit", 
    "Panini", "Pasta Carbonara", "Pasta Primavera", "Pasta Salads", "Pasties", "Pastries", "Pavlovas", "Peanut Butter Cookies", "Pecan Pie", "Pestos", 
    "Pierogies", "Pies", "Pizza", "Pizza Dough", "Polenta", "Popcorn", "Popovers and Yorkshire Puddings", "Pork", "Pork Chops", "Pork Ribs", 
    "Pork Shoulder", "Pork Tenderloin", "Pot Pies", "Pot Roast", "Potato Pancakes", "Potato Salads", "Potato Soups", "Pound Cakes", "Pretzels", 
    "Prime Rib", "Pulled Pork", "Pumpkin Breads", "Pumpkin Pie", "Pumpkin Seeds", "Quesadillas", "Quiches", "Ravioli", "Refried Beans", "Rhubarb Pie", 
    "Ribs", "Rice Casseroles", "Rice Pilaf", "Rice Puddings", "Risotto", "Roasts", "Salads", "Salisbury Steak", "Salmon", "Sandwich Cookies", "Sandwiches", "Sausage",
    "Scones", "Seitan", "Shepherd's Pie", "Shortbread", "Shortcakes", "Shrimp and Grits", "Shrimp Scampi", "Side Dishes", "Slab Pie", "Sliders", "Sloppy Joes", "Smoothies", "Snickerdoodles", "Soups", "Spaghetti", "Spanish Rice", 
    "Spice Cakes", "Spinach Dips", "Split Pea Soups", "Spritz Cookies", "Stews", "Stir-Fries", "Strawberry Pie", "Strawberry Shortcakes", 
    "Stuffed Mushrooms", "Stuffed Peppers", "Sugar Cookies", "Sushi", "Sweet Potato Pie", "Swiss Steak", "Taco Salads", "Tacos", "Tamales", 
    "Tapas", "Tater Tot Casseroles", "Tempeh", "Tetrazzini", "Tex-Mex", "Tiramisu", "Toffee", "Tofu", "Tomato Salads", "Tortellini", "Tortes", 
    "Tortillas", "Tostadas", "Truffles", "Tuna Casseroles", "Tuna Salads", "Turkey", "Upside-Down Cakes", "Vegan", "Vegetable Side Dishes","Vegetarian", "Waffles",
    "Waldorf Salads", "Whoopie Pies", "Ziti", "Zucchini Breads"]

for meal in meals_list:
    
    # Create the prompt for each meal
    prompt = f"Create 5 recipes for {meal}. Follow this example: Quinoa Salad with Chickpeas and Vegetables; A vibrant, nutrient-packed dish that's perfect for a light lunch or side.; 1 cup quinoa, uncooked. 1 ½ cups water. 1 cup canned chickpeas, rinsed and drained. 1 medium cucumber, diced. 1 medium red bell pepper, diced. 1 cup cherry tomatoes, halved. ¼ cup red onion, finely chopped. 2 tablespoons olive oil. 1 tablespoon lemon juice, 1 teaspoon cumin powder, Salt and pepper to taste, 2 tablespoons fresh parsley; 1. Rinse the quinoa under cold water in a fine mesh sieve. 2. In a medium pot, combine quinoa and water. Bring to a boil, reduce heat to low, cover, and simmer for 15 minutes or until the water is absorbed. Fluff with a fork and let it cool. 3. In a large mixing bowl, combine the cooked quinoa, chickpeas, cucumber, bell pepper, cherry tomatoes, and red onion. 4. In a small bowl, whisk together olive oil, lemon juice, cumin, salt, and pepper. Pour over the salad and toss to combine. 5. Sprinkle with parsley if desired, and serve chilled or at room temperature.;240;7.5;31;5;3;9.5;1.3;140;4;1340;Lunch  Do not add anything else that is not stated. Never use ; other then separating the columns."

    # Generate the response from the API for the current meal
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a chef that will provide recipe recommendations. The recommendations should include Recipe name, a description of the dish, ingredients, detailed instructions on how to make the dish, Energy(kcal), Protein (g), Carbohydrates(g), Dietary Fiber (g), Sugar(g), Fat(g), Saturated Fat(g), Sodium(mg), Servings, Total Grams and food category, either Breakfast, Lunch, Dinner, Desserts, Snacks. The output should be in a CSV format, separated with ;."},
            {"role": "user", "content": prompt}
        ]
    )

    # String representing CSV data
    csv_string = completion.choices[0].message.content

    # Convert the string to a list of rows (splitting by new lines and commas)
    csv_data = [line.split(',') for line in csv_string.splitlines()]
    print(csv_data)
    # Specify the filename for the new CSV file
    filename = r'C:\Users\47950\PycharmProjects\Master\your_file.csv'

    # Write the data to a CSV file
    with open(filename, mode='a',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f'CSV file "{filename}", "{meal}" created successfully.')
