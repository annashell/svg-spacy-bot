# svg-spacy-bot

This script initiates a Telegram bot that generates a syntactic dependency scheme for the given French sentences. To use the bot, type in a French text; the answer will be a .png picture scheme.

![image](https://github.com/user-attachments/assets/7343b98d-da3f-496c-bbf7-5995911c45a2)

Python 3.11 is required.
Used libraries:
1. telebot (for Telegram bot logic)
2. cairo (for SVG generation and converting SVG pictures to PNG)
3. spacy (for getting syntactic dependencies)
   
All the used libraries are listed in the requirements.txt file.

main.py includes the Telegram bot launch and its methods such as a welcoming message and message answer logic.
svg_generator.py includes 
  - a method for collecting syntactic dependencies (get_dependencies_for_text method)
  - a method for generating syntactic dependency scheme picture using cairo library (generate_svg_for_dep_dict)
    
More detailed information can be found inside the mentioned scripts.

To run the program:
1. Create a .env file with a string TG_TOKEN=%Your Telegram bot token% inside the svg-spacy-bot directory. To create a new TG bot and receive its token use @BotFather Telegram bot. 
2. Open CMD in the svg-spacy-bot directory
3. Run the command "python -m venv venv" to create a virtual environment
4. Run the command "venv\Scripts\activate.bat" to activate a virtual environment
5. Run "pip install -r requirements.txt" to install the package dependencies
6. Run the command "python main.py"

   
