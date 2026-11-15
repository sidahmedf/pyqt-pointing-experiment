# PyQt Pointing Experiment — Interactive Cursor Techniques & Controlled Evaluation

**PyQt Pointing Experiment** is an end-to-end Human-Computer Interaction (HCI) research and benchmarking suite built with **Python (PyQt5)** and **R**. It implements three classic target-acquisition techniques (**Standard Cursor**, **Bubble Cursor**, and **Rope Cursor**), provides an automated multi-trial controlled experiment harness, and includes a full statistical analysis pipeline in R Markdown across 7 participants ($5{,}040$ logged trials).

---

## Repository Structure

The monorepo is organized into three cohesive modules that can either be run independently or executed together as a complete experimental pipeline:

```text
pyqt-pointing-experiment/
├── pointing-techniques/     # Module 1: Standalone PyQt5 cursor simulations (Normal, Bubble, Rope)
├── controlled-experiment/   # Module 2 (Hero): Multi-trial experiment harness, target generator & CSV logger
│   └── TP1/                 # Isolated widget snapshot used by the experiment runner
└── statistical-analysis/    # Module 3: Data consolidation scripts & R Markdown statistical evaluation
    ├── logs.Rmd             # R Markdown analysis source (ANOVA, Fitts's Law / speed-accuracy)
    ├── logs.pdf             # Pre-rendered PDF report (with visible R source code)
    ├── logs.html            # Pre-rendered interactive HTML report (collapsible sections)
    └── data.csv             # Consolidated dataset (7 participants × 720 trials = 5,040 rows)
```

---

## 1. Pointing Techniques (`pointing-techniques/`)

Implements and compares three 2D target-selection cursors in **PyQt5**:

* **Normal Cursor (`NormalCursor`):** Standard point cursor; selection occurs only when the physical cursor intersects the target radius ($d \le r$).
* **Bubble Cursor (`BubbleCursor`):** Area cursor that dynamically resizes its activation radius to always encompass the closest target, maximizing effective target width in sparse regions.
* **Rope Cursor (`RopeCursor`):** Subclass of `BubbleCursor` that overrides `paint()` to render a visual tether ("rope") connecting the pointer to the closest target rather than drawing an enclosing circle.

### Running Standalone Mode

```bash
cd pointing-techniques
pip install PyQt5
python main.py
```

*(Ensure `src_tp_bubble.csv` is present in the working directory.)*

#### Switching Cursor Techniques
Edit `pointing-techniques/main.py` and `pointing-techniques/BubbleWidget.py` to toggle between the three modes:

| `main.py` Widget | `BubbleWidget.py` Cursor | Active Technique |
| :--- | :--- | :--- |
| `BubbleWidget()` | `BubbleCursor` | **Bubble Cursor** (Default) |
| `BubbleWidget()` | `RopeCursor` | **Rope Cursor** |
| `NormalWidget()` | *(N/A)* | **Normal Cursor** |

---

## 2. Controlled Experiment Harness (`controlled-experiment/`) — *Main Pipeline*

Automates within-subject controlled experiments comparing **Bubble**, **Rope**, and **Normal** cursors across varying target densities and sizes, logging reaction times and error counts to CSV.

### Experimental Design

| Factor | Levels |
| :--- | :--- |
| **Techniques** | `Bubble`, `Rope`, `Normal` |
| **Target Densities** | `30`, `90` distractors |
| **Target Sizes** | `8 px`, `18 px` |
| **Repetitions** | `3` blocks per condition |
| **Trials per Repetition** | `20` target acquisitions ($720$ trials per participant) |

### Step 1 — Generate Target & Sequence Files

Generate the CSV target layouts and trial sequences for all four density/size combinations:

```bash
cd controlled-experiment

python generate_files.py -n 30 -s 8 -m 10
python generate_files.py -n 30 -s 18 -m 10
python generate_files.py -n 90 -s 8 -m 10
python generate_files.py -n 90 -s 18 -m 10
```

This outputs `targets_<density>_<size>.csv` and `sequence_<density>_<size>.csv` in the directory.

### Step 2 — Launch the Experiment Runner

```bash
python MainExp.py
```

*(Note: Always launch via `MainExp.py`, which binds the pointing widgets to `XPManager`; `main.py` is kept for configuration-dialog testing only.)*

1. Enter the **Participant ID**, select the **Technique** (`Bubble` / `Rope` / `Normal`), and set the number of **Repetitions**.
2. Complete the highlighted red target sequence.
3. Results are automatically exported to `results/user_<id>_<technique>_<timestamp>.csv`.

---

## 3. Statistical Analysis & R Reports (`statistical-analysis/`)

Consolidates raw participant logs and evaluates movement time (`Time_ms`) and error rates (`Errors`) across cursor techniques, target densities, and target sizes.

### View Pre-Rendered Reports (No R Installation Required)

GitHub natively renders PDFs directly in the browser—click **`statistical-analysis/logs.pdf`** in the file tree above to inspect all statistical tests, plots, and R source code, or open `statistical-analysis/logs.html` locally for an interactive view.

### Reproducing the Analysis in RStudio

1. Install [R](https://cran.r-project.org/) and [RStudio](https://posit.co/download/rstudio-desktop/).
2. Open `statistical-analysis/TP LOGS.Rproj` in RStudio.
3. Open `logs.Rmd` and click **Knit** (or run chunks interactively).

### Dataset Schema (`data.csv`)

```csv
User, Technique, Density, Size, Repetition, Target_ID, Timestamp, Errors, Time_ms
```

*(Optional)* To rebuild `data.csv` from raw participant folders (`data final/1/` through `data final/7/`):
1. Run `python merge.py` inside each participant folder to produce `merged_user_X.csv`.
2. Run `python create_csv.py` inside `data final/` to validate and merge all $7 \times 720 = 5{,}040$ rows into `data.csv`.