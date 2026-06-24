from __future__ import annotations

import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path as FilePath
import shutil

from .graph_data import Node, Path

RESULT_DIR = FilePath("result-mmdc")


def render_mermaid(mst_paths, kruskal_steps, mode="result", open_output=True):
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    mmd_path = RESULT_DIR / f"{timestamp}.mmdc"
    svg_path = RESULT_DIR / f"{timestamp}.svg"

    diagram = build_mermaid_diagram(mst_paths, kruskal_steps, mode=mode)
    mmd_path.write_text(diagram, encoding="utf-8")

    command = _resolve_mmdc_command()
    if command is None:
        raise FileNotFoundError(
            "Mermaid CLI was not found. Expected 'mmdc.cmd', 'mmdc', or 'mmdc.ps1' in PATH."
        )

    subprocess.run([command, "-i", str(mmd_path), "-o", str(svg_path)], check=True)

    if open_output:
        webbrowser.open(svg_path.resolve().as_uri())

    return mmd_path, svg_path


def build_mermaid_diagram(mst_paths, kruskal_steps, mode="result"):
    if mode == "process":
        return _build_process_diagram(kruskal_steps)
    return _build_result_diagram(mst_paths)


def _build_result_diagram(mst_paths):
    lines = ["flowchart LR", ""]
    lines.extend(_build_graph_subgraph("result", "MST Result", mst_paths, mst_paths))
    return "\n".join(lines) + "\n"


def _build_process_diagram(kruskal_steps):
    lines = ["flowchart LR", ""]
    lines.extend(_build_graph_subgraph("a", "Base Rooute", Path.get_sorted_paths(), []))
    lines.append("")
    lines.extend(_build_sorted_path_subgraph("b", Path.get_sorted_paths()))
    lines.append("")

    accepted_anchor = "b"
    step_letters = []

    for index, step in enumerate(kruskal_steps, start=1):
        step_key = _index_to_letters(index + 2)
        step_letters.append((step_key, step))
        title = f"KRUSKAL - step {index}"
        if step["accepted"]:
            active_edges = step["mst_snapshot"]
            if index == _last_accepted_index(kruskal_steps):
                title += " - MST"
        else:
            active_edges = step["mst_snapshot"]
            title += " - CYCLE"

        lines.extend(
            _build_graph_subgraph(
                step_key,
                title,
                Path.get_sorted_paths(),
                active_edges,
            )
        )
        lines.append("")

    lines.append("a --> b")

    for step_key, step in step_letters:
        lines.append(f"{accepted_anchor} --> {step_key}")
        if step["accepted"]:
            accepted_anchor = step_key

    return "\n".join(lines) + "\n"


def _build_graph_subgraph(prefix, title, all_paths, active_paths):
    active_edges = {
        tuple(sorted(path._path))
        for path in active_paths
    }
    lines = [f'subgraph {prefix}["{title}"]']

    for order, node_id in enumerate(sorted(Node._self_map), start=1):
        lines.append(f"{prefix}_n{order}(({_mermaid_node_label(node_id)}))")

    lines.append("")

    for path in all_paths:
        node1, node2 = path._path
        edge = tuple(sorted((node1, node2)))
        style = "---" if edge in active_edges else "-.-"
        lines.append(
            f"{prefix}_n{_node_order(node1)} {style}|{path.distance}| {prefix}_n{_node_order(node2)}"
        )

    lines.append("end")
    return lines


def _build_sorted_path_subgraph(prefix, sorted_paths):
    lines = [f'subgraph {prefix}["Sorted Path"]']

    for index, path in enumerate(sorted_paths, start=1):
        node1, node2 = path._path
        lines.append(
            f'{prefix}_{index}["{_mermaid_node_label(node1)} <--> {_mermaid_node_label(node2)} = {path.distance}"]'
        )
        if index < len(sorted_paths):
            lines.append("-->")

    lines.append("end")
    return lines


def _node_order(node_id):
    return sorted(Node._self_map).index(node_id) + 1


def _mermaid_node_label(node_id):
    return _index_to_letters(_node_order(node_id) - 1)


def _index_to_letters(index):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    current = index

    while True:
        result = alphabet[current % 26] + result
        current = current // 26 - 1
        if current < 0:
            return result


def _last_accepted_index(steps):
    accepted_indexes = [index for index, step in enumerate(steps, start=1) if step["accepted"]]
    return accepted_indexes[-1] if accepted_indexes else 0


def _resolve_mmdc_command():
    for candidate in ("mmdc.cmd", "mmdc", "mmdc.ps1"):
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None
