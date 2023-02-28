
# *******************************************************************************************
# *
# *   raylib [textures] example - Bunnymark
# *
# *   Example originally created with raylib 1.6, last time updated with raylib 2.5
# *
# *   Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
# *   BSD-like license that allows static linking with closed source software
# *
# *   Copyright (c) 2014-2023 Ramon Santamaria (@raysan5)
# *
# 
# ********************************************************************************************

# Adapted by stu for Shedskin python compiler

import raylib

MAX_BUNNIES = 500000    # 50K bunnies limit

# This is the maximum amount of elements (quads) per batch
# NOTE: This value is defined in [rlgl] module and can be changed there
MAX_BATCH_ELEMENTS = 8192

# Just a tad faster to use this instead of raylib.Vector2
# In a real game, likely float access isn't a bottleneck
# So it may be more convenient to use the raylib.Vector2
class vec2:
    def __init__(self) -> None:
        self.x=0.0
        self.y=0.0

class Bunny:
    def __init__(self) -> None:
        self.position = vec2()
        self.speed = vec2()
        self.color = raylib.Color()

#------------------------------------------------------------------------------------
# Program main entry point
#------------------------------------------------------------------------------------

def bunnyMain():
    # Initialization
    #--------------------------------------------------------------------------------------
    screenWidth = 800   #1920
    screenHeight = 450  #1080

    raylib.InitWindow(screenWidth, screenHeight, "Bunnymark - Raylib + Shedskin version");
    #raylib.ToggleFullscreen()
    # Load bunny texture
    texBunny = raylib.LoadTexture("resources/wabbit_alpha.png");

    bunnies = []        #(Bunny *)malloc(MAX_BUNNIES*sizeof(Bunny));    # Bunnies array
    for i in range(MAX_BUNNIES):
        bunnies.append(Bunny())

    bunniesCount = 0           # Bunnies counter

    raylib.SetTargetFPS(60);               # Set our game to run at 60 frames-per-second
    #--------------------------------------------------------------------------------------

    # Main game loop
    while not raylib.WindowShouldClose():    # Detect window close button or ESC key
        # Update
        #----------------------------------------------------------------------------------
        if raylib.IsMouseButtonDown(0):
            # Create more bunnies
            for i in range(10000):
                if bunniesCount < MAX_BUNNIES:
                    pos = raylib.GetMousePosition()
                    bunnies[bunniesCount].position.x = pos.x
                    bunnies[bunniesCount].position.y = pos.y
                    bunnies[bunniesCount].speed.x = raylib.GetRandomValue(-250, 250)/60.0
                    bunnies[bunniesCount].speed.y = raylib.GetRandomValue(-250, 250)/60.0
                    bunnies[bunniesCount].color = raylib.Color(raylib.GetRandomValue(50, 240),
                                                       raylib.GetRandomValue(80, 240),
                                                       raylib.GetRandomValue(100, 240), 255 )
                    bunniesCount += 1
            print("Bunnies:", bunniesCount, bunnies[bunniesCount-1].speed.x, bunnies[bunniesCount-1].speed.y)

        # Update bunnies
        for i in range(bunniesCount):
            
            bunny = bunnies[i]
            bunny.position.x += bunny.speed.x
            bunny.position.y += bunny.speed.y

            if (((bunny.position.x + texBunny.width/2) > screenWidth) or
                ((bunny.position.x + texBunny.width/2) < 0)): bunny.speed.x *= -1
            if (((bunny.position.y + texBunny.height/2) >screenHeight) or
                ((bunny.position.y + texBunny.height/2 - 40) < 0)): bunny.speed.y *= -1
        
        #----------------------------------------------------------------------------------
        # Draw
        #----------------------------------------------------------------------------------
        raylib.BeginDrawing()

        raylib.ClearBackground(raylib.RAYWHITE)

        for i in range(bunniesCount):
            # NOTE: When internal batch buffer limit is reached (MAX_BATCH_ELEMENTS),
            # a draw call is launched and buffer starts being filled again;
            # before issuing a draw call, updated vertex data from internal CPU buffer is send to GPU...
            # Process of sending data is costly and it could happen that GPU data has not been completely
            # processed for drawing while new data is tried to be sent (updating current in-use buffers)
            # it could generates a stall and consequently a frame drop, limiting the number of drawn bunnies
            bunny = bunnies[i]
            #raylib.DrawTexture(texBunny, bunny.position.x, bunny.position.y, bunny.color)  
            raylib.DrawTexture(texBunny,  bunny.position.x, bunny.position.y, bunny.color)  

        raylib.DrawRectangle(0, 0, screenWidth, 40, raylib.BLACK)
        raylib.DrawText("bunnies: " + str(bunniesCount), 120, 10, 20, raylib.GREEN)
        raylib.DrawText("batched draw calls: " + str(1 + int(bunniesCount/MAX_BATCH_ELEMENTS)), 320, 10, 20, raylib.MAROON)

        raylib.DrawFPS(10, 10)

        raylib.EndDrawing()

    #----------------------------------------------------------------------------------   
    # De-Initialization
    #--------------------------------------------------------------------------------------

    raylib.UnloadTexture(texBunny)    # Unload bunny texture

    raylib.CloseWindow();              # Close window and OpenGL context
    #--------------------------------------------------------------------------------------

bunnyMain()
