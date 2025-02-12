import matplotlib.pyplot as plt
import graphviz

# Define the flowchart structure
flowchart = graphviz.Digraph(format='png')
flowchart.attr(size='10')

# Start
flowchart.node('Start', 'Start', shape='oval')

# EDA and Data Preparation
flowchart.node('EDA', 'Perform EDA\n(Dataset: dataset_part_2.csv)', shape='parallelogram')
flowchart.node('ClassCol', 'Create "Class" column\n(Standardize & Split Data)', shape='parallelogram')

# Model Training and Hyperparameter Tuning
flowchart.node('TrainTestSplit', 'Split into Training & Test Data', shape='parallelogram')
flowchart.node('SVM', 'Train SVM Model\n(GridSearchCV)', shape='parallelogram')
flowchart.node('Tree', 'Train Decision Tree\n(GridSearchCV)', shape='parallelogram')
flowchart.node('LR', 'Train Logistic Regression\n(GridSearchCV)', shape='parallelogram')
flowchart.node('KNN', 'Train KNN\n(GridSearchCV)', shape='parallelogram')

# Performance Evaluation
flowchart.node('Eval', 'Evaluate Models\n(Confusion Matrix, Accuracy)', shape='parallelogram')

# Best Model Selection
flowchart.node('BestModel', 'Select Best Model\n(Highest Accuracy)', shape='parallelogram')

# End
flowchart.node('End', 'End', shape='oval')

# Define edges
flowchart.edge('Start', 'EDA')
flowchart.edge('EDA', 'ClassCol')
flowchart.edge('ClassCol', 'TrainTestSplit')
flowchart.edge('TrainTestSplit', 'SVM')
flowchart.edge('TrainTestSplit', 'Tree')
flowchart.edge('TrainTestSplit', 'LR')
flowchart.edge('TrainTestSplit', 'KNN')

flowchart.edge('SVM', 'Eval')
flowchart.edge('Tree', 'Eval')
flowchart.edge('LR', 'Eval')
flowchart.edge('KNN', 'Eval')

flowchart.edge('Eval', 'BestModel')
flowchart.edge('BestModel', 'End')

# Render and display the flowchart
flowchart_path = "/mnt/data/ml_pipeline_flowchart"
flowchart.render(flowchart_path)

# Display the flowchart
from IPython.display import display
from PIL import Image

display(Image.open(flowchart_path + ".png"))
