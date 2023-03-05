"""

raylib [core] example - 2d camera

"""

from raylib import *

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

    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "raylib [core] example - 2d camera")

    player = Rectangle(400, 280, 40, 40)
    buildings = []
    build_colors = []

    spacing = 0

    for i in range(MAX_BUILDINGS):
        buildings.append(Rectangle())
        buildings[i].width = GetRandomValue(50, 200)
        buildings[i].height = GetRandomValue(100, 800)
        buildings[i].y = SCREEN_HEIGHT - 130.0 - buildings[i].height
        buildings[i].x = -6000.0 + spacing

        spacing += buildings[i].width
        build_colors.append(Color())
        build_colors[i] = Color(GetRandomValue(200, 240), GetRandomValue(200, 240), GetRandomValue(200, 250), 255)

    camera = Camera2D()
    camera.target = Vector2(player.x + 20.0, player.y + 20.0)
    camera.offset = Vector2(SCREEN_WIDTH / 2.0, SCREEN_HEIGHT / 2.0)
    camera.rotation = 0.0
    camera.zoom = 1.0

    SetTargetFPS(60)  # Set our game to run at 60 frames-per-second
    # ------------------------------------------------------------------------------------

    # Main game loop
    while not WindowShouldClose():  # Detect window close button or ESC key
        # Update
        # ----------------------------------------------------------------------------------
        # Player movement
        if IsKeyDown(KEY_RIGHT): player.x += 2
        if IsKeyDown(KEY_LEFT): player.x -= 2

        # Camera target follows player
        camera.target = Vector2(player.x + 20, player.y + 20)

        # Camera rotation controls
        if IsKeyDown(KEY_A):
            camera.rotation -= 1
        elif IsKeyDown(KEY_S):
            camera.rotation += 1

        # Limit camera rotation to 80 degrees (-40 to 40)
        if camera.rotation > 40:
            camera.rotation = 40
        elif camera.rotation < -40:
            camera.rotation = -40

        # Camera zoom controls
        camera.zoom += GetMouseWheelMove() * 0.05

        if camera.zoom > 3.0:
            camera.zoom = 3.0
        elif camera.zoom < 0.1:
            camera.zoom = 0.1

        # Camera reset (zoom and rotation)
        if IsKeyPressed(KEY_R):
            camera.zoom = 1.0
            camera.rotation = 0.0
        # ----------------------------------------------------------------------------------

        # Draw
        # ----------------------------------------------------------------------------------
        BeginDrawing()

        ClearBackground(RAYWHITE)

        BeginMode2D(camera)

        DrawRectangle(-6000, 320, 13000, 8000, DARKGRAY)

        for i in range(MAX_BUILDINGS): DrawRectangleRec(buildings[i], build_colors[i])

        DrawRectangleRec(player, RED)

        DrawLine(int(camera.target.x), -SCREEN_HEIGHT * 10, int(camera.target.x), SCREEN_HEIGHT * 10, GREEN)
        DrawLine(-SCREEN_WIDTH * 10, int(camera.target.y), SCREEN_WIDTH * 10, int(camera.target.y), GREEN)

        EndMode2D()

        DrawText("SCREEN AREA", 640, 10, 20, RED)

        DrawRectangle(0, 0, SCREEN_WIDTH, 5, RED)
        DrawRectangle(0, 5, 5, SCREEN_HEIGHT - 10, RED)
        DrawRectangle(SCREEN_WIDTH - 5, 5, 5, SCREEN_HEIGHT - 10, RED)
        DrawRectangle(0, SCREEN_HEIGHT - 5, SCREEN_WIDTH, 5, RED)

        DrawRectangle(10, 10, 250, 113, Fade(SKYBLUE, 0.5))
        DrawRectangleLines(10, 10, 250, 113, BLUE)

        DrawText("Free 2d camera controls:", 20, 20, 10, BLACK)
        DrawText("- Right/Left to move Offset", 40, 40, 10, DARKGRAY)
        DrawText("- Mouse Wheel to Zoom in-out", 40, 60, 10, DARKGRAY)
        DrawText("- A / S to Rotate", 40, 80, 10, DARKGRAY)
        DrawText("- R to reset Zoom and Rotation", 40, 100, 10, DARKGRAY)

        EndDrawing()
        # ----------------------------------------------------------------------------------

    # De-Initialization
    # ----------------------------------------------------------------------------------
    CloseWindow()  # Close window and OpenGL context
    # ----------------------------------------------------------------------------------


# Execute the main function
if __name__ == '__main__':
    main()
