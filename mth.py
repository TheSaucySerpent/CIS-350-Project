# Import the NetworkX library
import networkx as nx

# Import matplotlib for graph visualization
import matplotlib.pyplot as plt

# Create an empty graph object
G = nx.Graph()

a = {"a" : 0 ,  "b" :  25 , "c" : 17 , "d" : 34 , "e" : 19}
b = {"a" : 25 , "b" :  0 ,  "c" : 23 , "d" : 18 , "e" : 31}
c = {"a" : 17 , "b" :  23 , "c" : 0 ,  "d" : 24 , "e" : 16}
d = {"a" : 34 , "b" :  18 , "c" : 24 , "d" : 0 ,  "e" : 29}
e = {"a" : 19 , "b" :  31 , "c" : 16 , "d" : 29 , "e" : 0}

li = [a,b,c,d,e]

def get_smallest_value(d):
    # Remove keys with value 0 and find the minimum among the rest
    return min(val for val in d.values() if val != 0)

# Finding smallest value in each dictionary
min_a = get_smallest_value(a)
min_b = get_smallest_value(b)
min_c = get_smallest_value(c)
min_d = get_smallest_value(d)
min_e = get_smallest_value(e)

print("Smallest value in 'a':", min_a)
print("Smallest value in 'b':", min_b)
print("Smallest value in 'c':", min_c)
print("Smallest value in 'd':", min_d)
print("Smallest value in 'e':", min_e)


# Draw the tree
pos = nx.spring_layout(G, seed=42)  # positions for all nodes
nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, font_size=18)

# Show the plot
# plt.show()
