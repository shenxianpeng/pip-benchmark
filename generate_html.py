import os
import json

benchmark_dir = ".benchmarks"
output_dir = ".benchmarks/html"
os.makedirs(output_dir, exist_ok=True)

index_lines = ["<h1>Benchmark Results</h1><ul>"]

for filename in sorted(os.listdir(benchmark_dir)):
    if filename.endswith(".json"):
        with open(os.path.join(benchmark_dir, filename)) as f:
            data = json.load(f)
        html_file = filename.replace(".json", ".html")
        with open(os.path.join(output_dir, html_file), "w") as out:
            out.write(f"<h1>{filename}</h1><pre>{json.dumps(data, indent=2)}</pre>")
        index_lines.append(f'<li><a href="{html_file}">{filename}</a></li>')

index_lines.append("</ul>")
with open(os.path.join(output_dir, "index.html"), "w") as idx:
    idx.write("\n".join(index_lines))

print(f"Results written to {output_dir}")
