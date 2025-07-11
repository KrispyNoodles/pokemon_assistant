# 🧠 Pokémon Assistant Wiki
## 📌 Overview
Pokémon Assistant is a multi-agent system powered by LangGraph and LangChain. It helps users identify Pokémon and choose the most effective move during battle using natural language queries or images.

## 🎮 Demo
![POKEMON-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/815f2858-a963-4c15-9bce-ef4d62223354)

## 🧩 Architecture
Agents:
- Supervisor Agent: Delegates tasks to sub-agents based on user query.
- Pokemon Identifier Agent: Identifies Pokémon (from name/image) and retrieves their type.
- Pokemon Decision Move Agent: Determines the most effective move based on Pokémon type.

<img width="676" height="249" alt="output" src="https://github.com/user-attachments/assets/a78bca38-b973-4e4f-ac85-914fbdf2d7c3" />

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






