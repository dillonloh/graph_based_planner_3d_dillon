import yaml

stream = open(r'C:\Users\lohdi\Desktop\graph_planner_3d\graph_based_planner_3d_dillon\images\YAML62.yaml', 'r')
x = yaml.safe_load(stream)

print(x)