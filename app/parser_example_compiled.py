import os
import yaml
import sqlglot
from sqlglot import parse_one, exp

def resolve_table_name(expr):
    # resolve {{ ref(...) }} -> transform.*, {{ source(...) }} -> schema.table
    name = expr.sql()
    if "{{ ref(" in name:
        ref_name = name.split("'")[1]
        return f"transform.{ref_name}"
    elif "{{ source(" in name:
        parts = name.replace("{{ source(", "").replace(") }}", "").split(",")
        schema = parts[0].strip("' \"")
        table = parts[1].strip("' \"")
        return f"{schema}.{table}"
    return name

def strip_schema(full_name):
    return full_name.split('.')[-1].replace('"', '')
def extract_info(sql_text):
    parsed = parse_one(sql_text, read="postgres")
    # columns = [c.sql() for c in parsed.find_all(exp.Column)]
    columns = []

    for alias in parsed.find_all(exp.Alias):
        expr_str = alias.this.sql()   # full expression including array indexing
        alias_name = alias.alias       # AS name
        columns.append(f"{expr_str} AS {alias_name}")

    print(columns)

    # columns = set()
    #
    # for select_expr in parsed.expressions:
    #     if isinstance(select_expr, exp.Alias):
    #         # Prefer alias name
    #         columns.add(select_expr.alias)
    #     elif isinstance(select_expr, exp.Column):
    #         columns.add(select_expr.name)
    #
    # columns = list(columns)
    tables = [strip_schema(resolve_table_name(t)) for t in parsed.find_all(exp.Table)
              if t.name.lower() != "transformed_data"
              and "__dbt_tmp" not in t.name.lower() ]
    conditions = [w.sql() for w in parsed.find_all(exp.Where)]
    lineage_start = tables[0] if tables else None
    return {
        "columns": columns,
        "tables": tables,
        "conditions": conditions,
        "lineage_start": lineage_start
    }

def build_knowledge(models_dir="models"):
    knowledge = {}
    # Parse models
    for root, dirs, files in os.walk(models_dir):
        print(dirs)
        dirs[:] = [d for d in dirs if d not in ("local", "v1", "schema.yml")]
        for f in files:
            if f.endswith(".sql"):
                path = os.path.join(root, f)
                name = os.path.splitext(f)[0]
                with open(path) as file:
                    sql_text = file.read()
                parsed_info = extract_info(sql_text)
                knowledge[name] = {
                    "type": "dbt_model",
                    "path": path,
                    "description": f"DBT model located at {path}",
                    **parsed_info
                }
    # Parse exposures
    exposures_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dbt_project/exposures.yml"))
    if os.path.exists(exposures_path):
        print(f"Found exposures file: {exposures_path}")
        with open(exposures_path) as f:
            exposures_yaml = yaml.safe_load(f)
        exposures = exposures_yaml.get("exposures", [])
        for exposure in exposures:
            if not isinstance(exposure, dict):
                continue
            name = exposure.get("name")
            if not name:
                continue
            knowledge[name] = {
                "type": "exposure",
                "url": exposure.get("url"),
                "description": exposure.get("description"),
                "maturity": exposure.get("maturity"),
                "depends_on": exposure.get("depends_on"),
                "owner": exposure.get("owner"),
            }
    else:
        print(f"Exposures file not found at: {exposures_path}")
    return knowledge

def export_knowledge(knowledge, output_file="models_and_reports.yaml"):
    with open(output_file, "w") as f:
        yaml.safe_dump(knowledge, f, sort_keys=False)

# --- run ---
# dbt compile --profiles-dir config --target dev
if __name__ == "__main__":
    # Build knowledge from all model directories
    base_models_dir = "../dbt_project/target/compiled/dbt_project/models"
    
    print("🔍 Building knowledge base from dbt models...")
    print(f"📁 Looking in: {base_models_dir}")
    
    # Check if the directory exists
    if not os.path.exists(base_models_dir):
        print(f"❌ Error: Models directory not found at {base_models_dir}")
        print("💡 Make sure to run 'dbt compile' first in your dbt_project directory")
        exit(1)
    
    # Build knowledge from all model layers
    knowledge = {}
    
    # Process each model layer (bronze, silver, gold)
    for layer in ["bronze", "silver", "gold"]:
        layer_path = os.path.join(base_models_dir, layer)
        if os.path.exists(layer_path):
            print(f"📂 Processing {layer} models...")
            layer_knowledge = build_knowledge(layer_path)
            knowledge.update(layer_knowledge)
            print(f"✅ Found {len(layer_knowledge)} {layer} models")
        else:
            print(f"⚠️  {layer} directory not found, skipping...")
    
    # Parse exposures
    exposures_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dbt_project/exposures.yml"))
    if os.path.exists(exposures_path):
        print(f"📊 Found exposures file: {exposures_path}")
        with open(exposures_path) as f:
            exposures_yaml = yaml.safe_load(f)
        exposures = exposures_yaml.get("exposures", [])
        for exposure in exposures:
            if not isinstance(exposure, dict):
                continue
            name = exposure.get("name")
            if not name:
                continue
            knowledge[name] = {
                "type": "exposure",
                "url": exposure.get("url"),
                "description": exposure.get("description"),
                "maturity": exposure.get("maturity"),
                "depends_on": exposure.get("depends_on"),
                "owner": exposure.get("owner"),
            }
        print(f"✅ Found {len(exposures)} exposures")
    else:
        print(f"⚠️  Exposures file not found at: {exposures_path}")
    
    # Export the complete knowledge base
    output_file = "models_and_reports.yaml"
    export_knowledge(knowledge, output_file)
    
    print(f"\n🎉 Knowledge base built successfully!")
    print(f"📊 Total items: {len(knowledge)}")
    print(f"📁 Models: {len([k for k, v in knowledge.items() if v.get('type') == 'dbt_model'])}")
    print(f"📊 Exposures: {len([k for k, v in knowledge.items() if v.get('type') == 'exposure'])}")
    print(f"💾 Saved to: {output_file}")

