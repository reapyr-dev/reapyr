


import raylib

raylib.InitWindow(800, 600, "title")
raylib.SetTargetFPS(60)

while not raylib.WindowShouldClose():
    raylib.BeginDrawing()
    raylib.ClearBackground(raylib.Color(255, 255, 255, 255))
    raylib.DrawText("You created your first GUI element!", 190, 200, 20, raylib.Color(111, 111, 111, 255))
    raylib.GuiButton(raylib.Rectangle( 190, 255, 125, 30 ), "Hello RayGuiButton!")
    raylib.EndDrawing()

raylib.CloseWindow()