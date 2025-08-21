import os
import glob
import yaml

def load_dbt_models(project_path):
    models = {}
    for sql_file in glob.glob(os.path.join(project_path, "models/**/*.sql"), recursive=True):
        name = os.path.splitext(os.path.basename(sql_file))[0]
        with open(sql_file, "r") as f:
            sql = f.read()
        models[name] = {"description": f"SQL model at {sql_file}", "sql": sql}
    return models

def load_exposures(exposures_file):
    with open(exposures_file, "r") as f:
        data = yaml.safe_load(f)
    exposures = {}
    for exp in data.get("exposures", []):
        name = exp["name"]
        exposures[name] = {
            "description": exp.get("description", ""),
            "depends_on": exp.get("depends_on", []),
        }
    return exposures

def build_knowledge(project_path, exposures_file):
    models = load_dbt_models(project_path)
    reports = load_exposures(exposures_file)
    return {"dbt_models": models, "reports": reports}

def export_models_and_reports(knowledge, output_file="models_and_reports.yaml"):
    with open(output_file, "w") as f:
        yaml.safe_dump(knowledge, f, sort_keys=False)

