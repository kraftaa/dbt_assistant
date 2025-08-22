import os
import yaml

def build_knowledge(models_dir="models", exposures_dir="exposures"):
# def build_knowledge(models_dir="/Users/maria/Documents/GitHub/sparkle-dbt/models", exposures_dir="/Users/maria/Documents/GitHub/sparkle-dbt/models/gold"):
    knowledge = {"dbt_models": {}, "reports": {}}

    # Models
    for root, dirs, files in os.walk(models_dir):
        for f in files:
            if f.endswith(".sql"):
                path = os.path.join(root, f)
                name = os.path.splitext(f)[0]
                if "gold" in root:  # treat as report
                    knowledge["reports"][name] = {
                        "path": path,
                        "description": f"Report derived from gold model {name}"
                    }
                else:
                    knowledge["dbt_models"][name] = {
                        "path": path,
                        "description": f"DBT model located at {path}"
                    }

    # Exposures
    for root, dirs, files in os.walk(exposures_dir):
        for f in files:
            if f.endswith("exposures.yml") or f.endswith("exposures.yaml"):
                path = os.path.join(root, f)
                knowledge["reports"][os.path.splitext(f)[0]] = {
                    "path": path,
                    "description": f"Report/exposure defined in {path}"
                }

    return knowledge

# Save to yaml
knowledge = build_knowledge()
with open("dbt_knowledge.yaml", "w") as f:
    yaml.safe_dump(knowledge, f)
