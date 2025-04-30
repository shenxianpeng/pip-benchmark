import os
import json
from html import escape

benchmark_dir = ".benchmarks"
output_dir = os.path.join(benchmark_dir, "html")
os.makedirs(output_dir, exist_ok=True)

index_lines = [
    "<!DOCTYPE html>",
    "<html><head><meta charset='utf-8'><title>Benchmark Results</title></head><body>",
    "<h1>Benchmark Results</h1><ul>"
]

def generate_table(benchmarks):
    rows = [
        "<table border='1' cellpadding='5'><tr><th>Name</th><th>Mean (s)</th><th>StdDev (s)</th><th>Rounds</th><th>Ops/sec</th></tr>"
    ]
    for bench in benchmarks:
        name = escape(bench.get("fullname", bench.get("name", "N/A")))
        mean = f"{bench['stats']['mean']:.6f}"
        stddev = f"{bench['stats']['stddev']:.6f}"
        rounds = bench['stats'].get("rounds", "-")
        ops = f"{1.0 / bench['stats']['mean']:.2f}" if bench['stats']['mean'] else "-"
        rows.append(f"<tr><td>{name}</td><td>{mean}</td><td>{stddev}</td><td>{rounds}</td><td>{ops}</td></tr>")
    rows.append("</table>")
    return "\n".join(rows)

for root, _, files in os.walk(benchmark_dir):
    for filename in sorted(files):
        if filename.endswith(".json") and not root.startswith(output_dir):
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, benchmark_dir)
            html_file = rel_path.replace(os.sep, "_").replace(".json", ".html")
            output_path = os.path.join(output_dir, html_file)

            try:
                with open(full_path, "r") as f:
                    data = json.load(f)
            except Exception as e:
                print(f"Failed to parse {full_path}: {e}")
                continue

            benchmarks = data.get("benchmarks", [])

            with open(output_path, "w") as f:
                f.write(f"<h1>{escape(rel_path)}</h1>\n")
                if benchmarks:
                    f.write(generate_table(benchmarks))
                else:
                    f.write("<p>No benchmark data found.</p>")

            index_lines.append(f'<li><a href="{html_file}">{rel_path}</a></li>')

index_lines.append("</ul></body></html>")
with open(os.path.join(output_dir, "index.html"), "w") as f:
    f.write("\n".join(index_lines))
print(f"HTML files generated in {output_dir}")
