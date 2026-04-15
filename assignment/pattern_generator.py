import maya.cmds as cmds

cmds.file(new=True, force=True)

def generate_pattern():
    """Generate a flower pattern:
    # Center sphere represents the flower core
    # Cylinders form petals in a cross shape
    # Cubes are the leaves 
    # Modulo is used to alternate petal size for variation"""

    # --- Configuration variables ---
    num_rows = 5
    num_cols = 5
    spacing = 3.0
           
    # Center of the grid
    center_row = num_rows // 2
    center_col = num_cols // 2

    # --- Create Shaders ---
    center_shader = cmds.shadingNode("lambert", asShader=True, name="centerMat")
    cmds.setAttr(center_shader + ".color", 1.0, 0.2, 0.5, type="double3") 

    petal_shader = cmds.shadingNode("lambert", asShader=True, name="petalMat")
    cmds.setAttr(petal_shader + ".color", 1.0, 0.8, 0.2, type="double3") 

    leaf_shader = cmds.shadingNode("lambert", asShader=True,name="leafMat")
    cmds.setAttr(leaf_shader + ".color", 0.2, 0.8, 0.3, type="double3") 

    # --- Nested loops to create the grid ---
    for row in range(num_rows):
        for col in range(num_cols):

            #Calculate position
            x_pos = col * spacing
            z_pos = row * spacing

            obj_name = f"flower_{row}_{col}"

            # Conditional logic (flower pattern)

            # Create a center object to be the focal point of the flower
            if row == center_row and col == center_col:
                obj = cmds.polySphere(name=obj_name, radius=1.2)[0]
                cmds.move(x_pos, 1.2, z_pos, obj)

                cmds.select(obj)
                cmds.hyperShade(assign=center_shader)

                print(f"{obj_name} is CENTER")
            
            # PETALS: cross shape to simulate petals extending from the center
            elif row == center_row or col == center_col:
                obj = cmds.polyCylinder(name=obj_name, radius=0.6, height=2.0)[0]
                cmds.move(x_pos, 1.0, z_pos, obj)

                #Alternate scale using modulo
                if col % 2 == 0:
                    cmds.scale(1, 1.5, 1, obj) # taller patels
                    print(f"{obj_name} is EVEN PETAL")
                else:
                    cmds.scale(1, 0.7, 1, obj) # shorter petals
                    print(f"{obj_name} is ODD PETAL")

                cmds.select(obj)
                cmds.hyperShade(assign=petal_shader)

            # LEAVES: cubes as background objects to act like leaves

            else:
                obj = cmds.polyCube(name=obj_name, width=1.2, height=1.2, depth=1.2)[0]
                cmds.move(x_pos, 0.6, z_pos, obj)
                
                # Alterante scale using modulo for irregular pattern
                if(row + col) % 2 == 0:
                    cmds.scale(1.2, 1.2, 1.2, obj)

                cmds.select(obj)
                cmds.hyperShade(assign=leaf_shader)

                print(f"{obj_name} is LEAF")



# ---------------------------------------------------------------------------
# Run the generator
# ---------------------------------------------------------------------------
generate_pattern()

# Frame everything in the viewport.
cmds.viewFit(allObjects=True)
print("Pattern generated successfully!")
