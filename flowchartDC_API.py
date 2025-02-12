
# FLOWCHART Data Collection Process for Falcon 9 Rocket Analysis
import matplotlib.pyplot as plt
import graphviz

flowchart = graphviz.Digraph(format='png', graph_attr={'rankdir': 'TB'})

# Start Node
flowchart.node("Start", shape="ellipse", style="filled", fillcolor="lightblue")

# Data Collection
flowchart.node("Fetch SpaceX API Data", shape="parallelogram", style="filled", fillcolor="lightgrey")

# Data Processing Steps
flowchart.node("Extract Rocket Details", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Extract Launch Site Details", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Extract Payload Data", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Extract Core Data", shape="box", style="filled", fillcolor="lightyellow")

# Data Wrangling
flowchart.node("Normalize JSON to DataFrame", shape="parallelogram", style="filled", fillcolor="lightgrey")
flowchart.node("Filter Data (Single Core, Single Payload)", shape="box", style="filled", fillcolor="lightcoral")
flowchart.node("Convert Date Format", shape="box", style="filled", fillcolor="lightcoral")
flowchart.node("Filter Falcon 9 Launches", shape="box", style="filled", fillcolor="lightcoral")

# Missing Data Handling
flowchart.node("Check for Missing Values", shape="diamond", style="filled", fillcolor="lightgreen")
flowchart.node("Replace Missing Payload Mass with Mean", shape="box", style="filled", fillcolor="lightgreen")

# Data Export
flowchart.node("Save to CSV", shape="parallelogram", style="filled", fillcolor="lightblue")
flowchart.node("Convert to HTML Table", shape="parallelogram", style="filled", fillcolor="lightblue")

# End Node
flowchart.node("End", shape="ellipse", style="filled", fillcolor="lightblue")

# Define the edges between nodes
flowchart.edge("Start", "Fetch SpaceX API Data")
flowchart.edge("Fetch SpaceX API Data", "Extract Rocket Details")
flowchart.edge("Fetch SpaceX API Data", "Extract Launch Site Details")
flowchart.edge("Fetch SpaceX API Data", "Extract Payload Data")
flowchart.edge("Fetch SpaceX API Data", "Extract Core Data")

flowchart.edge("Extract Rocket Details", "Normalize JSON to DataFrame")
flowchart.edge("Extract Launch Site Details", "Normalize JSON to DataFrame")
flowchart.edge("Extract Payload Data", "Normalize JSON to DataFrame")
flowchart.edge("Extract Core Data", "Normalize JSON to DataFrame")

flowchart.edge("Normalize JSON to DataFrame", "Filter Data (Single Core, Single Payload)")
flowchart.edge("Filter Data (Single Core, Single Payload)", "Convert Date Format")
flowchart.edge("Convert Date Format", "Filter Falcon 9 Launches")
flowchart.edge("Filter Falcon 9 Launches", "Check for Missing Values")

flowchart.edge("Check for Missing Values", "Replace Missing Payload Mass with Mean", label="Yes")
flowchart.edge("Check for Missing Values", "Save to CSV", label="No")
flowchart.edge("Replace Missing Payload Mass with Mean", "Save to CSV")

flowchart.edge("Save to CSV", "Convert to HTML Table")
flowchart.edge("Convert to HTML Table", "End")

# Render and display the flowchart
flowchart_path = "/mnt/data/data_collection_flowchart"
flowchart.render(flowchart_path)

# Return the path of the generated flowchart image
flowchart_path + ".png"