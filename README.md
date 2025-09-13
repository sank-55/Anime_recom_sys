# Anime Recommender Streamlit App
#### generate poster of recommended shows along with a brief overview from the wikipidea and it is styled using external CSS

Some of Snapshots of the UI
<img width="1353" height="602" alt="Screenshot 2025-09-09 234521" src="https://github.com/user-attachments/assets/cd970670-3187-4f7d-ab82-a1b95b63f2ee" />


In recommendation .....
<img width="1352" height="602" alt="Screenshot 2025-09-09 233300" src="https://github.com/user-attachments/assets/414bb619-0620-4f03-adda-fa5b25c41edd" />
<img width="1344" height="618" alt="Screenshot 2025-09-09 233338" src="https://github.com/user-attachments/assets/2e9500da-ff51-465b-9b6c-0727bbdd6ba5" />

Surprise ME ** Special Feature
For various insighfull EDA visit anime.ipynb file 

See Live: https://smart-anime-recommendation-system-sank-55.streamlit.app


[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Repo](https://img.shields.io/badge/github-sank--55/Anime_recom_streamlit_app-ff69b4)](https://github.com/sank-55/Anime_recom_streamlit_app)

---

## Overview

This repository is a lightweight **Anime Recommender** implemented with a Streamlit front-end. It combines collaborative filtering and TF–IDF content features (title/synopsis/genres) to provide personalized recommendations. The repository contains the app script, sample datasets (`anime.csv`, `rating.csv`), and example notebooks used for exploration and model experiments.

> I gathered file-level information from the original repository `sank-55/Anime_recom_streamlit_app` on GitHub (see **Resources** at the end). citeturn0view0

---

## What’s in this repo

* `app.py` — Streamlit app entry point (UI + recommendation endpoints).
* `anime.csv` — Anime metadata (used for TF–IDF and display).
* `rating.csv` — User–anime ratings used for collaborative filtering.
* `anime.ipynb`, `aime_recom.ipynb` — Jupyter notebooks containing EDA, experiments and model prototyping.
* `anime_recommender.zip` — Packaged version of supporting scripts/data (if included by the repo author).
* `README.md`, `LICENSE` — Project documentation and MIT license.

---

## Quickstart (run locally)

**Prerequisites**

* Python 3.8+
* `pip` or `conda`

1. Clone the repository

```bash
git clone https://github.com/sank-55/Anime_recom_streamlit_app.git
cd Anime_recom_streamlit_app
```

2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS / Linux
venv\\Scripts\\activate  # Windows
```

3. Install dependencies

```bash
pip install -r requirements.txt
# If requirements.txt is not present, install the common packages:
# pip install streamlit pandas numpy scikit-learn scipy joblib
```

4. Run the Streamlit app

```bash
streamlit run app.py
```

Open the URL shown by Streamlit (typically `http://localhost:8501`) to use the recommender UI.

---

## Data & Preprocessing

* The included `anime.csv` provides anime metadata used to build TF–IDF vectors (title, genre, synopsis if available).
* `rating.csv` contains historical user ratings used to train collaborative filtering models (item-based, user-based or matrix factorization).

If you want to use your own dataset, replace these CSVs or modify the data-loading block in `app.py`/notebooks.

---

## How the recommender works (high level)

1. **TF–IDF content module**: Build TF–IDF vectors from anime metadata (title + synopsis + genres). Compute cosine similarity between anime items to provide content-based candidates.
2. **Collaborative filtering**: Use rating history to predict user-item scores (neighborhood-based or matrix factorization). This captures user preference patterns.
3. **Hybrid scoring**: Combine the CF predicted score and content-similarity score with a weight `alpha`:

```
final_score = alpha * cf_score + (1 - alpha) * content_score
```

Tune `alpha` on validation data to balance personalization and content-similarity.

---

## Files to look at (recommended)

* `app.py` — See how the UI calls preprocessing, TF–IDF, CF, and the hybrid scoring. Modify this file to change behavior or expose new parameters.
* `anime.ipynb`, `aime_recom.ipynb` — Useful for inspecting data distributions, TF–IDF examples and offline evaluation experiments.
* `anime_recommender.zip` — If present, inspect for additional helper scripts and model files.

---

#### pickle file is used to store the vector information after ceating various no. of vectors bagging 

## Extending & Improving

* **Add model persistence**: Save trained CF models and vectorizers with `joblib` and load them in `app.py` to avoid re-training every run.
* **Hyperparameter tuning**: Tune CF factors, neighborhood sizes, and TF–IDF n-gram ranges.
* **Cold-start strategies**: Use additional metadata (studio, tags) or popularity priors for brand-new users/items.
* **Scalability**: Switch TF–IDF to `scikit-learn`'s sparse matrices and use ANN libraries (Faiss/Annoy) for fast nearest neighbors on large catalogs.

---

## Troubleshooting & Tips

* If the Streamlit app fails to start, ensure `streamlit` is installed and run `streamlit hello` to verify installation.
* If recommendations are slow, precompute TF–IDF matrices and CF predictions and load them at runtime.
* Verify that `anime.csv` and `rating.csv` have the correct column names expected in `app.py` (open `app.py` and check the CSV load lines).

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Add tests and documentation
4. Push and open a pull request

---

## License

This project uses the **MIT License**. See `LICENSE` in the repository.

---

## Resources

* Original repository listing (files inspected): `sank-55/Anime_recom_streamlit_app` on GitHub. citeturn0view0

---

If you’d like, I can now:

* commit this README to the repository (I can generate a ready-to-paste `README.md`),
* extract `requirements.txt` by scanning `app.py` & notebooks and building a dependency list, or
* open and summarize `app.py` and the notebooks to add targeted usage examples and API endpoints to this README.
