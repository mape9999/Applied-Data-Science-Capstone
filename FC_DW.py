# Redefining the flowchart using Graphviz for Exploratory Data Analysis (EDA) and Training Label Assignment
flowchart = graphviz.Digraph(format='png', graph_attr={'rankdir': 'TB'})

# Start Node
flowchart.node("Start", shape="ellipse", style="filled", fillcolor="lightblue")

# Load Data
flowchart.node("Load Dataset", shape="parallelogram", style="filled", fillcolor="lightgrey")

# Exploratory Data Analysis (EDA)
flowchart.node("Check Missing Values", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Check Data Types", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Count Launches per Site", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Count Orbits", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Analyze Landing Outcomes", shape="box", style="filled", fillcolor="lightyellow")

# Define Training Labels
flowchart.node("Define Bad Outcomes", shape="diamond", style="filled", fillcolor="lightgreen")
flowchart.node("Create Landing Class", shape="box", style="filled", fillcolor="lightgreen")
flowchart.node("Assign Class Labels", shape="box", style="filled", fillcolor="lightgreen")

# Analyze Landing Performance
flowchart.node("Count Landing Failures", shape="box", style="filled", fillcolor="lightcoral")
flowchart.node("Calculate Success Rate", shape="box", style="filled", fillcolor="lightcoral")

# Data Export
flowchart.node("Save to CSV", shape="parallelogram", style="filled", fillcolor="lightblue")

# End Node
flowchart.node("End", shape="ellipse", style="filled", fillcolor="lightblue")

# Define the edges between nodes
flowchart.edge("Start", "Load Dataset")
flowchart.edge("Load Dataset", "Check Missing Values")
flowchart.edge("Check Missing Values", "Check Data Types")
flowchart.edge("Check Data Types", "Count Launches per Site")
flowchart.edge("Count Launches per Site", "Count Orbits")
flowchart.edge("Count Orbits", "Analyze Landing Outcomes")
flowchart.edge("Analyze Landing Outcomes", "Define Bad Outcomes")
flowchart.edge("Define Bad Outcomes", "Create Landing Class", label="Bad Outcomes Identified")
flowchart.edge("Create Landing Class", "Assign Class Labels")
flowchart.edge("Assign Class Labels", "Count Landing Failures")
flowchart.edge("Count Landing Failures", "Calculate Success Rate")
flowchart.edge("Calculate Success Rate", "Save to CSV")
flowchart.edge("Save to CSV", "End")

# Render and display the flowchart
flowchart_path = "/mnt/data/eda_training_labels_flowchart"
flowchart.render(flowchart_path)

# Return the path of the generated flowchart image
flowchart_path + ".png"