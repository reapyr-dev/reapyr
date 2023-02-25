import raylib
print(raylib.__file__)
raylib.InitWindow(800, 600, "title")
raylib.SetTargetFPS(60)

while not raylib.WindowShouldClose():
    raylib.BeginDrawing()
    raylib.ClearBackground(raylib.Color(255, 255, 255, 255))
    raylib.DrawText("You created your first window!", 190, 200, 20, raylib.Color(111, 111, 111, 255))
    raylib.EndDrawing()

raylib.CloseWindow()