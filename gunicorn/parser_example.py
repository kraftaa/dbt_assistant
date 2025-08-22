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
    columns = set()

    for select_expr in parsed.expressions:
        if isinstance(select_expr, exp.Alias):
            # Prefer alias name
            columns.add(select_expr.alias)
        elif isinstance(select_expr, exp.Column):
            columns.add(select_expr.name)

    columns = list(columns)
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
                    "path": path,
                    "description": f"DBT model located at {path}",
                    **parsed_info
                    }
            else:
                # Skip everything else, e.g. schema.yml
                continue
    return knowledge

def export_knowledge(knowledge, output_file="models_and_reports.yaml"):
    with open(output_file, "w") as f:
        yaml.safe_dump(knowledge, f, sort_keys=False)

# --- run ---

if __name__ == "__main__":
    knowledge = ("models")
    export_knowledge(knowledge)
    print("Knowledge extracted and saved to models_and_reports.yaml")

