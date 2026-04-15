"""
DIGM 131 - Assignment 2: Procedural Pattern Generator
======================================================

OBJECTIVE:
    Use loops and conditionals to generate a repeating pattern of 3D objects
    in Maya. You will practice nested loops, conditional logic, and
    mathematical positioning.

REQUIREMENTS:
    1. Use a nested loop (a loop inside a loop) to create a grid or pattern
       of objects.
    2. Include at least one conditional (if/elif/else) that changes an
       object's properties (type, size, color, or position offset) based
       on its row, column, or index.
    3. Generate at least 25 objects total (e.g., a 5x5 grid).
    4. Comment every major block of code explaining your logic.

GRADING CRITERIA:
    - [25%] Nested loop correctly generates a grid/pattern of objects.
    - [25%] Conditional logic visibly changes object properties based on
            position or index.
    - [20%] At least 25 objects are generated.
    - [15%] Code is well-commented with clear explanations.
    - [15%] Pattern is visually interesting and intentional.

TIPS:
    - A 5x5 grid gives you 25 objects. A 6x6 grid gives you 36.
    - Use the loop variables (row, col) to calculate X and Z positions.
    - The modulo operator (%) is great for alternating patterns:
          if col % 2 == 0:    # every other column
    - You can vary: primitive type, height, width, position offset, etc.

COMMENT HABITS (practice these throughout the course):
    - Add a comment before each logical section explaining its purpose.
    - Use inline comments sparingly and only when the code is not obvious.
    - Keep comments up to date -- if you change the code, update the comment.
"""

import maya.cmds as cmds

# Clear the scene.
cmds.file(new=True, force=True)


def generate_pattern():
    """Generate a procedural pattern of objects using nested loops.

    This function should:
        1. Define variables for rows, columns, and spacing.
        2. Use a nested for-loop to iterate over rows and columns.
        3. Inside the loop, use a conditional to vary object properties.
        4. Create and position each object.
    """
    # --- Configuration variables ---
    num_rows = 5        # Number of rows in the pattern.
    num_cols = 5        # Number of columns in the pattern.
    spacing = 3.0       # Distance between object centers.

    # TODO: Create a nested loop that iterates over rows and columns.
    #
    # HINT -- your loop structure should look something like this:
    #
    #   for row in range(num_rows):
    #       for col in range(num_cols):
    #           # Calculate position
    #           x_pos = col * spacing
    #           z_pos = row * spacing
    #
    #           # TODO: Add a conditional here that changes something
    #           # based on row, col, or (row + col).
    #           # For example:
    #           #   if (row + col) % 2 == 0:
    #           #       create a cube
    #           #   else:
    #           #       create a sphere
    #
    #           # TODO: Create the object using cmds.polyCube(), etc.
    #
    #           # TODO: Position the object using cmds.move().
    #
    #           # TODO: (Optional) Vary the scale using cmds.scale().

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
