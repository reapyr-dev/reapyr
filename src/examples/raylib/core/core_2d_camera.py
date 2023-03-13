"""

raylib [core] example - 2d camera

"""

import raylib

# Definitions
# ------------------------------------------------------------------------------------
MAX_BUILDINGS = 100


# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# Program main entry point
# ------------------------------------------------------------------------------------
def main():
    # Initialization
    # ------------------------------------------------------------------------------------
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 450

    raylib.InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 2d camera")

    player = raylib.Rectangle(400, 280, 40, 40)
    buildings = []
    build_colors = []

    spacing = 0

    for i in range(MAX_BUILDINGS):
        buildings.append(raylib.Rectangle())
        buildings[i].width = raylib.GetRandomValue(50, 200)
        buildings[i].height = raylib.GetRandomValue(100, 800)
        buildings[i].y = SCREEN_HEIGHT - 130.0 - buildings[i].height
        buildings[i].x = -6000.0 + spacing

        spacing += buildings[i].width
        build_colors.append(raylib.Color())
        build_colors[i] = raylib.Color(raylib.GetRandomValue(200, 240), raylib.GetRandomValue(200, 240), raylib.GetRandomValue(200, 250), 255)

    camera = raylib.Camera2D(raylib.Vector2(player.x + 20.0, player.y + 20.0), raylib.Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0), 0.0, 1.0)

    raylib.SetTargetFPS(60)  # Set our game to run at 60 frames-per-second
    # ------------------------------------------------------------------------------------

    # Main game loop
    while not raylib.WindowShouldClose():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        # Player movement
        if raylib.IsKeyDown(raylib.KEY_RIGHT): player.x += 2
        if raylib.IsKeyDown(raylib.KEY_LEFT): player.x -= 2

        # Camera target follows player
        camera.target = raylib.Vector2(player.x + 20, player.y + 20)

        # Camera rotation controls
        if raylib.IsKeyDown(raylib.KEY_A):
            camera.rotation -= 1
        elif raylib.IsKeyDown(raylib.KEY_S):
            camera.rotation += 1

        # Limit camera rotation to 80 degrees (-40 to 40)
        if camera.rotation > 40:
            camera.rotation = 40
        elif camera.rotation < -40:
            camera.rotation = -40

        # Camera zoom controls
        camera.zoom += raylib.GetMouseWheelMove() * 0.05

        if camera.zoom > 3.0:
            camera.zoom = 3.0
        elif camera.zoom < 0.1:
            camera.zoom = 0.1

        # Camera reset (zoom and rotation)
        if raylib.IsKeyPressed(raylib.KEY_R):
            camera.zoom = 1.0
            camera.rotation = 0.0
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        raylib.BeginDrawing()

        raylib.ClearBackground(raylib.RAYWHITE)

        raylib.BeginMode2D(camera)

        raylib.DrawRectangle(-6000, 320, 13000, 8000, raylib.DARKGRAY)

        for i in range(MAX_BUILDINGS): raylib.DrawRectangleRec(buildings[i], build_colors[i])

        raylib.DrawRectangleRec(player, raylib.RED)

        raylib.DrawLine(int(camera.target.x), -SCREEN_HEIGHT * 10, int(camera.target.x), SCREEN_HEIGHT * 10, raylib.GREEN)
        raylib.DrawLine(-SCREEN_WIDTH * 10, int(camera.target.y), SCREEN_WIDTH * 10, int(camera.target.y), raylib.GREEN)

        raylib.EndMode2D()

        raylib.DrawText("SCREEN AREA", 640, 10, 20, raylib.RED)

        raylib.DrawRectangle(0, 0, SCREEN_WIDTH, 5, raylib.RED)
        raylib.DrawRectangle(0, 5, 5, SCREEN_HEIGHT - 10, raylib.RED)
        raylib.DrawRectangle(SCREEN_WIDTH - 5, 5, 5, SCREEN_HEIGHT - 10, raylib.RED)
        raylib.DrawRectangle(0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5, raylib.RED)

        raylib.DrawRectangle(10, 10, 250, 113, raylib.Fade(raylib.SKYBLUE, 0.5))
        raylib.DrawRectangleLines(10, 10, 250, 113, raylib.BLUE)

        raylib.DrawText("Free 2d camera controls:", 20, 20, 10, raylib.BLACK)
        raylib.DrawText("- Right/Left to move Offset", 40, 40, 10, raylib.DARKGRAY)
        raylib.DrawText("- Mouse Wheel to Zoom in-out", 40, 60, 10, raylib.DARKGRAY)
        raylib.DrawText("- A / S to Rotate", 40, 80, 10, raylib.DARKGRAY)
        raylib.DrawText("- R to reset Zoom and Rotation", 40, 100, 10, raylib.DARKGRAY)

        raylib.EndDrawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # ----------------------------------------------------------------------------------
    raylib.CloseWindow()  # Close window and OpenGL context
    # ----------------------------------------------------------------------------------


# Execute the main function
if __name__ == '__main__':
    main()
