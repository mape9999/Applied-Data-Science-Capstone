


# Redefining the flowchart using Graphviz
flowchart = graphviz.Digraph(format='png', graph_attr={'rankdir': 'TB'})

# Start Node
flowchart.node("Start", shape="ellipse", style="filled", fillcolor="lightblue")

# Web Scraping
flowchart.node("Fetch Wikipedia Page", shape="parallelogram", style="filled", fillcolor="lightgrey")
flowchart.node("Parse HTML with BeautifulSoup", shape="box", style="filled", fillcolor="lightyellow")

# Extract Data
flowchart.node("Find All Tables", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Extract Column Names", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Initialize Data Dictionary", shape="parallelogram", style="filled", fillcolor="lightgrey")
flowchart.node("Iterate Through Rows", shape="box", style="filled", fillcolor="lightyellow")
flowchart.node("Extract Relevant Data Fields", shape="box", style="filled", fillcolor="lightyellow")

# Data Cleaning
flowchart.node("Clean & Format Data", shape="box", style="filled", fillcolor="lightcoral")

# DataFrame Construction
flowchart.node("Create Pandas DataFrame", shape="parallelogram", style="filled", fillcolor="lightgrey")

# Data Export
flowchart.node("Save to CSV", shape="parallelogram", style="filled", fillcolor="lightblue")
flowchart.node("Convert to HTML Table", shape="parallelogram", style="filled", fillcolor="lightblue")

# End Node
flowchart.node("End", shape="ellipse", style="filled", fillcolor="lightblue")

# Define the edges between nodes
flowchart.edge("Start", "Fetch Wikipedia Page")
flowchart.edge("Fetch Wikipedia Page", "Parse HTML with BeautifulSoup")
flowchart.edge("Parse HTML with BeautifulSoup", "Find All Tables")
flowchart.edge("Find All Tables", "Extract Column Names")
flowchart.edge("Extract Column Names", "Initialize Data Dictionary")
flowchart.edge("Initialize Data Dictionary", "Iterate Through Rows")
flowchart.edge("Iterate Through Rows", "Extract Relevant Data Fields")
flowchart.edge("Extract Relevant Data Fields", "Clean & Format Data")
flowchart.edge("Clean & Format Data", "Create Pandas DataFrame")
flowchart.edge("Create Pandas DataFrame", "Save to CSV")
flowchart.edge("Save to CSV", "Convert to HTML Table")
flowchart.edge("Convert to HTML Table", "End")

# Render and display the flowchart
flowchart_path = "/mnt/data/web_scraping_flowchart"
flowchart.render(flowchart_path)

# Return the path of the generated flowchart image
flowchart_path + ".png"