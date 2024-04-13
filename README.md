# cintel-06-custom
Module 6 Costum Cintel Project

In this project, we dive into 2023 WTA match data through a csv file

## Create and activate a local virtual environment in .venv.
    py -m venv .venv
    .\.venv\Scripts\Activate

## Install your dependencies into your .venv (pandas and pyarrow) and freeze into your requirements.txt. 
    py -m pip install faicons pandas pyarrow plotly scipy shiny shinylive shinywidgets 
    py -m pip install –-upgrade pip
    py -m pip freeze > requirements.txt

## Load data
    app_dir = Path(__file__).parent
    matches_df = pd.read_csv(app_dir / "wta_proj_matches_2023.csv", dtype={"person_id": str})