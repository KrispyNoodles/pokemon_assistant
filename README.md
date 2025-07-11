# 🧠 Pokémon Assistant Wiki
## 📌 Overview
Pokémon Assistant is a multi-agent system powered by LangGraph and LangChain. It helps users identify Pokémon and choose the most effective move during battle using natural language queries or images.

## 🎮 Demo
![POKEMON-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/2b1ce883-5998-437d-a9bb-06da290402de)

## 🧩 Architecture
Agents:
- Supervisor Agent: Delegates tasks to sub-agents based on user query.
- Pokemon Identifier Agent: Identifies Pokémon (from name/image) and retrieves their type.
- Pokemon Decision Move Agent: Determines the most effective move based on Pokémon type.

<img width="676" height="249" alt="output" src="https://github.com/user-attachments/assets/fb158374-156b-46af-a596-439aecb6d36a" />


## ⚙️ Setup
1. Install dependencies
``` python
pip install -r requirements.txt
```

2. Create .env
``` python
API_KEY=your_openai_api_key
ENDPOINT=https://your_azure_endpoint
MODEL=gpt-4o
```

3. Run the app on `main.ipynb`

## 📁 Dataset Used from Kaggle
[Pokedex Dataset](https://www.kaggle.com/datasets/brdata/complete-pokemon-dataset-gen-iiv):
Complete Pokemon Dataset(Gen I - VII) → Used for Pokémon metadata such as type and stats.

[Pokemon Moves Dataset](https://www.kaggle.com/datasets/thiagoamancio/full-pokemons-and-moves-datasets):
Full Pokémons and Moves Datasets → Used for retrieving move types and effectiveness.






