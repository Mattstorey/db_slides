from ete3 import Tree, TreeStyle, add_face_to_node, TextFace, NodeStyle

t1 = Tree("((((X,X),X),(((X,X),(X,X)),X)):3, ((Z,(Z,(Z,Z))), ((Z,Z),(Z,Z))):3):1;")

t_mislab = Tree("((((X,X),X),(((Y,X),(X,X)),X)):2, ((Y,((Y),(Y,Y))), ((Y,Y),(X,Y))):3):1;", name='Tree_mislab')
t_mislab_fix = Tree("((((X,X),X),(((X,X),(X,X)),X)):2, ((Y,((Y),(Y,Y))), ((Y,Y),(Y,Y))):3):1;", name='Tree_mislab_fix')

t_newspc = Tree("(((((X,X),(((X,(X,X)),X),(X,X)))):3, (((Y,(X,X)),(((Y,X),Y),(X,Y)))):2));",name='Tree_newspc')
t_newspc_fix = Tree("(((((X,X),(((X,(X,X)),X),(X,X)))):3, (((Y,(Y,Y)),(((Y,Y),Y),(Y,Y)))):2));",name='Tree_newspc_fix')

bare_tree = Tree("((((A:3,(X,X)):3,A):3,((((Y,Y),A),(A,Y)):4,(A,(A,A)):4):4):3, (A,(A,(Z,A):2):2):3):1;", name = "bare_tree")
bare_tree_filled = Tree("((((A:3,(X,X)):3,A):3,((((Y,Y),Y),(Y,Y)):4,(A,(A,A)):4):4):3, (A,(A,(Z,Z):2):2):3):1;", name = "bare_tree_filled")


trees = [t_mislab, t_mislab_fix, t_newspc, t_newspc_fix, bare_tree, bare_tree_filled]

def make_tree(t):
    ts = TreeStyle()

    ## make the tree in to a cladogram
    most_distant_leaf, tree_length = t.get_farthest_leaf()
    current_dist = 0
    for postorder, node in t.iter_prepostorder():
        if postorder:
            current_dist -= node.dist
        else:
            if node.is_leaf():
                node.dist += tree_length - (current_dist + node.dist)
            elif node.up: # node is internal
                current_dist += node.dist

    ## Rotate and color the lables 
    def rotation_layout(node):
        if node.is_leaf():
            if node.name == 'X':
                F = TextFace(node.name, tight_text=True,fgcolor='Blue')
                F.rotation = 90
                add_face_to_node(F, node, column=0, position="branch-right")
            elif node.name == 'Y':
                F = TextFace(node.name, tight_text=True, fgcolor='Red')
                F.rotation = 90
                add_face_to_node(F, node, column=0, position="branch-right")
            elif node.name == 'A':
                F = TextFace("")
                add_face_to_node(F, node, column=0, position="branch-right")
            else:
                F = TextFace(node.name, tight_text=True, fgcolor='Green')
                F.rotation = 90
                add_face_to_node(F, node, column=0, position="branch-right")


    ## Format the tree image
    nstyle = NodeStyle()
    nstyle["hz_line_type"] = 0
    nstyle["vt_line_color"] = "#ffffff"
    nstyle["hz_line_color"] = "#ffffff"
    nstyle["vt_line_width"] = 4
    nstyle["hz_line_width"] = 4
    nstyle["size"] = 0


    for n in t.traverse():
        n.set_style(nstyle)

    ## Set background
    t.img_style["bgcolor"] = "#2e3440"

    ## Tree 'shape'

    ts.min_leaf_separation = 20
    ts.show_leaf_name = False
    ts.layout_fn = rotation_layout
    ts.rotation = -90
    ts.show_scale = False

    #t.show(tree_style=ts)

    t.render(f"{t.name}.svg", tree_style=ts, dpi=900) 

for tree in trees:
    make_tree(tree)