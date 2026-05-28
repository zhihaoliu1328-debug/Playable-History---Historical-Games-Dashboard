# Playable History

This Streamlit dashboard is a digital humanities data visualization project about historical video games. Instead of asking whether games are historically accurate, it asks what kind of historical agency games make playable.

The project maps a curated corpus of historical video games between two interpretive poles:

- **Command/control history:** warfare, strategy, empire, management, politics, diplomacy
- **Lived/experiential history:** society, culture, narrative, place, open-world exploration, embodied experience

## Project Structure

```text
historical-games-dashboard/
|-- app.py
|-- requirements.txt
|-- README.md
|-- data/
|   |-- raw_games_dataset.csv
|   `-- cleaned_games_playable_history.csv
`-- writeup/
```

## How to Run

Install the required packages:

```bash
python -m pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app.py
```

## Requirements

The dashboard uses only:

- streamlit
- pandas
- plotly

## Data

The dashboard uses `data/cleaned_games_playable_history.csv`, a curated exploratory corpus of historical video games. Game metadata, themes, and source links were collected from MobyGames.com. During cleaning, those themes were grouped into interpretive categories for this project.

Important fields include:

- `title`
- `release_year`
- `main_genre`
- `rating`
- `command_control_score`
- `lived_experience_score`
- `historical_play_type`
- interpretive tag columns such as `has_warfare`, `has_strategy_system`, `has_society_culture`, and `has_narrative_adventure`

The score columns are built from interpretive Boolean tags:

- `command_control_score` counts warfare, strategy/system, management/economy, empire/expansion, and politics/diplomacy tags.
- `lived_experience_score` counts society/culture, narrative/adventure, and open world/sandbox tags.

## Dashboard Visualizations

1. **Playable History Grid**  
   A bubble grid that places games by command/control score and lived/experiential score. Bubble size shows how many games share a score combination, hover text shows specific titles, and an optional release-year animation shows how the corpus accumulates over time.

2. **Historical Game Themes: Experiential vs Command**  
   A diverging bar chart that contrasts command/control modes with lived/experiential modes. The chart includes a percentage/count toggle that changes how the balance is measured.

3. **Genre Orientation Plot**  
   A dumbbell chart showing whether each genre tends to lean toward command/control or lived/experiential forms of play. Controls allow sorting, minimum genre size filtering, and genre highlighting.

4. **Ratings as Reception Clue**  
   A compact rating visualization that treats ratings as reception context, not as proof of quality or causation.

## Method Note

This is a curated exploratory corpus, not a random sample of all historical video games. The tags are interpretive categories created during data cleaning. The dashboard is intended as a digital humanities argument built through corpus creation, metadata cleaning, interpretive categorization, and visual storytelling.

## Collaboration Statement

This project used ChatGPT/Codex as a coding and design assistant for Streamlit implementation, visualization structure, debugging, and README revision. The research question, dataset direction, interpretive framing, and final project decisions remain the author's responsibility.
