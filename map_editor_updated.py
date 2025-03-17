import pygame
import os
import json

# Initialize Pygame
pygame.init()

# Get the screen resolution
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h

# Grid settings
GRID_WIDTH, GRID_HEIGHT = 30, 22
TILE_SIZE = min(SCREEN_WIDTH // GRID_WIDTH, (SCREEN_HEIGHT - 100) // GRID_HEIGHT)
WIDTH, HEIGHT = GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE + 100

# Set up the display (maximized)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("CraftSaga Map Editor")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)
GOLD = (255, 215, 0)

# Load fonts
TITLE_FONT = pygame.font.SysFont("Arial", int(TILE_SIZE * 1.2), bold=True)
BUTTON_FONT = pygame.font.SysFont("Arial", int(TILE_SIZE * 0.8), bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", int(TILE_SIZE * 0.6))
MAP_FONT = pygame.font.SysFont("Arial", int(TILE_SIZE * 0.4))

# Define directories
TEXTURE_DIR = "data/textures"
ITEM_DIR = "data/items"
MONSTER_DIR = "data/monsters"
MAP_DIR = "data/maps"
STAT_DIR = "data/stats"
PLAYER_DIR = "data/player"
NPC_DIR = "data/npcs"  # New: NPC directory

# Ensure directories exist
for directory in [TEXTURE_DIR, ITEM_DIR, MONSTER_DIR, MAP_DIR, STAT_DIR, PLAYER_DIR, NPC_DIR]:
    os.makedirs(directory, exist_ok=True)

# Load textures/sprites with fallback
TEXTURES = {}
ITEMS = {}
MONSTER_SPRITES = {}
NPC_SPRITES = {}  # New: NPC sprites
try:
    texture_files = ["grass.jpg", "dirt.jpg", "water.jpg", "lava.jpg", "boundary.jpg", "FieldsTile_01.png", "FieldsTile_02.png", "FieldsTile_03.png", "FieldsTile_04.png", "FieldsTile_05.png", "FieldsTile_06.png", "FieldsTile_07.png",
                     "FieldsTile_08.png", "FieldsTile_09.png", "FieldsTile_10.png", "FieldsTile_11.png", "FieldsTile_12.png", "FieldsTile_13.png", "FieldsTile_14.png", "FieldsTile_05.png", "FieldsTile_16.png", "FieldsTile_17.png",
                     "FieldsTile_18.png", "FieldsTile_19.png", "FieldsTile_20.png", "FieldsTile_21.png", "FieldsTile_22.png", "FieldsTile_23.png", "FieldsTile_24.png", "FieldsTile_25.png", "FieldsTile_26.png", "FieldsTile_27.png",
                     "FieldsTile_28.png", "FieldsTile_28.png", "FieldsTile_30.png", "FieldsTile_31.png", "FieldsTile_32.png", "FieldsTile_33.png", "FieldsTile_34.png", "FieldsTile_35.png", "FieldsTile_36.png", "FieldsTile_37.png",
                     "Tile_03.png", "Tile_04.png", "Tile_05.png", "Tile_06.png", "Tile_07.png", "Tile_08.png", "Tile_09.png", "Tile_10.png", "Tile_11.png", "Tile_12.png", "Tile_13.png", "Tile_20.png"]
    for tex in texture_files:
        tex_path = os.path.join(TEXTURE_DIR, tex)
        if os.path.exists(tex_path):
            TEXTURES[tex] = pygame.transform.scale(pygame.image.load(tex_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        else:
            print(f"Warning: Texture file '{tex_path}' not found.")

    item_files = ["Health_Box.png", "attack_pot.png", "door.png"]
    for item in item_files:
        item_path = os.path.join(ITEM_DIR, item)
        if os.path.exists(item_path):
            ITEMS[item] = pygame.transform.scale(pygame.image.load(item_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        else:
            print(f"Warning: Item file '{item_path}' not found.")

    monster_files = ["mutant.png", "Demon.png", "Dragon.png"]
    for sprite in monster_files:
        sprite_path = os.path.join(MONSTER_DIR, sprite)
        if os.path.exists(sprite_path):
            MONSTER_SPRITES[sprite] = pygame.transform.scale(pygame.image.load(sprite_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        else:
            print(f"Warning: Monster sprite '{sprite_path}' not found.")

    npc_files = ["roger.png"]  # New: Load NPC sprite
    for sprite in npc_files:
        sprite_path = os.path.join(NPC_DIR, sprite)
        if os.path.exists(sprite_path):
            NPC_SPRITES[sprite] = pygame.transform.scale(pygame.image.load(sprite_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        else:
            print(f"Warning: NPC sprite '{sprite_path}' not found.")

    player_path = os.path.join(PLAYER_DIR, "player.png")
    if os.path.exists(player_path):
        PLAYER_SPRITE = pygame.transform.scale(pygame.image.load(player_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
    else:
        print("Warning: Player sprite 'player.png' not found.")
        PLAYER_SPRITE = pygame.Surface((TILE_SIZE, TILE_SIZE))
        PLAYER_SPRITE.fill(RED)

    menu_bg_path = os.path.join(TEXTURE_DIR, "menu_background.jpg")
    if os.path.exists(menu_bg_path):
        MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(menu_bg_path).convert_alpha(), (SCREEN_WIDTH, 100))
    else:
        print("Warning: Menu background 'menu_background.jpg' not found.")
        MENU_BACKGROUND = None
except pygame.error as e:
    print(f"Texture load failed: {e}. Using colors.")

# Fallback surface for missing textures
FALLBACK_TEXTURE = pygame.Surface((TILE_SIZE, TILE_SIZE))
FALLBACK_TEXTURE.fill(GREEN)

# Enhanced Button class
class Button:
    def __init__(self, x, y, width, height, text, value=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_surface = BUTTON_FONT.render(text, True, WHITE)
        self.text = text
        self.value = value
        self.action = action
        self.hovered = False
        self.selected = False

    def draw(self, screen):
        shadow_rect = self.rect.move(5, 5)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=10)
        color_top = GREEN if self.selected else (LIGHT_GRAY if not self.hovered else GREEN)
        color_bottom = DARK_GRAY if self.selected else (GRAY if not self.hovered else DARK_GRAY)
        for i in range(self.rect.height):
            alpha = i / self.rect.height
            color = tuple(int(color_top[j] * (1 - alpha) + color_bottom[j] * alpha) for j in range(3))
            pygame.draw.line(screen, color, (self.rect.x, self.rect.y + i), (self.rect.x + self.rect.width, self.rect.y + i))
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        screen.blit(self.text_surface, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)

# Text input class
class TextInput:
    def __init__(self, x, y, width, height, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.label = label
        self.active = False

    def draw(self, screen):
        color = WHITE if self.active else GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        display_text = f"{self.label}: {self.text}" if self.text or self.active else self.label
        text_surface = SMALL_FONT.render(display_text + ("|" if self.active else ""), True, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# New: Quest setup class for NPCs
class QuestSetup:
    def __init__(self):
        self.active = False
        self.dialogue_inputs = [
            TextInput(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3, 400, 30, "Initial Dialogue"),
            TextInput(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3 + 40, 400, 30, "In Progress Dialogue"),
            TextInput(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3 + 80, 400, 30, "Complete Dialogue")
        ]
        self.item_input = TextInput(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3 + 120, 200, 30, "Item Name")
        self.amount_input = TextInput(SCREEN_WIDTH // 2 + 10, SCREEN_HEIGHT // 3 + 120, 50, 30, "Qty")
        self.drop_input = TextInput(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 3 + 160, 400, 30, "Drop Source (e.g., mutant.png)")
        self.confirm_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 200, 200, 50, "Confirm", action=self.confirm)
        self.quest_data = None

    def confirm(self):
        item_name = self.item_input.text or "seed"
        amount = int(self.amount_input.text) if self.amount_input.text.isdigit() else 1
        drop_source = self.drop_input.text or "mutant.png"
        self.quest_data = {
            "dialogue": {
                "initial": self.dialogue_inputs[0].text or "Can you help me?",
                "in_progress": self.dialogue_inputs[1].text or "Any progress?",
                "complete": self.dialogue_inputs[2].text or "Thanks!"
            },
            "required_items": {item_name: amount},
            "drop_sources": {drop_source: item_name}
        }
        self.active = False

    def draw(self, screen):
        for input_box in self.dialogue_inputs + [self.item_input, self.amount_input, self.drop_input]:
            input_box.draw(screen)
        self.confirm_button.draw(screen)

# Updated load_map to include NPCs
def load_map(filename):
    map_path = os.path.join(MAP_DIR, filename)
    grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    items = {}
    monsters = {}
    textures = {}
    npcs = {}  # New: Load NPCs
    if os.path.exists(map_path):
        with open(map_path, 'r') as f:
            grid = [[int(char) for char in line.strip()] for line in f.readlines()]
        stats_file = os.path.join(STAT_DIR, filename.replace('.txt', '_stats.json'))
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                data = json.load(f)
                monsters = data.get('monsters', {})
                textures = data.get('textures', {})
                items = data.get('items', {})
                npcs = data.get('npcs', {})  # Load NPC data
    return grid, monsters, textures, items, npcs

# Updated save_map to include NPCs
def save_map(filename, grid, monsters, textures, items, npcs):
    map_path = os.path.join(MAP_DIR, filename)
    with open(map_path, 'w') as f:
        for row in grid:
            f.write(''.join(map(str, row)) + '\n')
    stats_file = os.path.join(STAT_DIR, filename.replace('.txt', '_stats.json'))
    with open(stats_file, 'w') as f:
        json.dump({'monsters': monsters, 'textures': textures, 'items': items, 'npcs': npcs}, f, indent=2)
    print(f"Saved to {map_path} and {stats_file}")

# Updated place_on_grid to handle NPCs
def place_on_grid(grid, monsters, textures, items, npcs, x, y, selected_tool, selected_texture, inputs, quest_data=None):
    if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
        key = f"{x},{y}"
        if selected_tool == 6:  # Player
            for gy in range(GRID_HEIGHT):
                for gx in range(GRID_WIDTH):
                    if grid[gy][gx] == 6:
                        grid[gy][gx] = 1
            grid[y][x] = 6
            items.pop(key, None)
            monsters.pop(key, None)
            npcs.pop(key, None)
        elif selected_tool == 3:  # Monster
            grid[y][x] = 3
            monsters[key] = {
                "sprite": selected_texture,
                "health": int(inputs[0].text or 50),
                "max_health": int(inputs[0].text or 50),
                "attack": int(inputs[1].text or 10),
                "defense": int(inputs[2].text or 5),
                "xp": int(inputs[3].text or 4)
            }
            items.pop(key, None)
            npcs.pop(key, None)
        elif selected_tool in [1, 2, 5]:  # Texture
            grid[y][x] = selected_tool
            textures[key] = selected_texture
            if grid[y][x] not in [1, 2, 5]:
                monsters.pop(key, None)
                items.pop(key, None)
                npcs.pop(key, None)
        elif selected_tool == 4:  # Item
            items[key] = selected_texture
            if key not in textures:
                textures[key] = "grass.jpg"
            if grid[y][x] not in [1, 2, 5]:
                grid[y][x] = 1
                monsters.pop(key, None)
                npcs.pop(key, None)
        elif selected_tool == 7:  # New: NPC
            grid[y][x] = 7
            npcs[key] = {
                "sprite": selected_texture,
                "quest": quest_data if quest_data else None
            }
            items.pop(key, None)
            monsters.pop(key, None)
            if key not in textures:
                textures[key] = "grass.jpg"
        elif selected_tool == 0:  # Empty
            if key in items:
                items.pop(key)
            elif key in monsters:
                monsters.pop(key)
                grid[y][x] = 1
            elif key in npcs:  # New: Remove NPC
                npcs.pop(key)
                grid[y][x] = 1
            elif grid[y][x] == 6:
                grid[y][x] = 1
            else:
                textures.pop(key, None)
                grid[y][x] = 1

def map_editor(start_map=1):
    grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    monsters = {}
    textures = {}
    items = {}
    npcs = {}  # New: Store NPCs
    running = True
    selected_tool = None
    selected_texture = "grass.jpg"
    selected_sprite_pos = None
    selected_monster_key = None
    mousedown = False
    current_map = f"map_{start_map}.txt"

    # Sprite grid setup
    SPRITE_GRID_WIDTH = 13
    SPRITE_GRID_HEIGHT = GRID_HEIGHT
    SPRITE_GRID_X = GRID_WIDTH * TILE_SIZE + 10
    SPRITE_GRID_Y = 100
    sprite_grid = [[None for _ in range(SPRITE_GRID_WIDTH)] for _ in range(SPRITE_GRID_HEIGHT)]
    sprite_items = {
        "item": [(item, 4) for item in ITEMS.keys()],
        "player": [("player.png", 6)],
        "monster": [(sprite, 3) for sprite in MONSTER_SPRITES.keys()],
        "texture": [(tex, 1 if "grass" in tex else 2 if "dirt" in tex else 5) for tex in TEXTURES.keys()],
        "map": [(f"map_{i}.txt", None) for i in range(1, 11) if os.path.exists(os.path.join(MAP_DIR, f"map_{i}.txt"))] + [("New", None)],
        "npc": [(sprite, 7) for sprite in NPC_SPRITES.keys()]  # New: NPC category
    }

    # Default monster stats for pre-filling inputs
    default_monster_stats = {
        "mutant.png": {"health": "50", "attack": "8", "defense": "1", "xp": "4"},
        "Demon.png": {"health": "100", "attack": "19", "defense": "1", "xp": "2"},
        "Dragon.png": {"health": "100", "attack": "22", "defense": "5", "xp": "4"}
    }

    # Menu bar layout
    button_width, button_height = 150, 40
    button_spacing = 20
    total_width = 8 * button_width + 7 * button_spacing  # Updated for new NPC button
    start_x = (SCREEN_WIDTH - total_width - (SPRITE_GRID_WIDTH * TILE_SIZE + 20)) // 2
    buttons = [
        Button(start_x, 10, button_width, button_height, "Map", None, lambda: load_sprite_grid(sprite_grid, "map")),
        Button(start_x + button_width + button_spacing, 10, button_width, button_height, "Item", 4, lambda: load_sprite_grid(sprite_grid, "item")),
        Button(start_x + 2 * (button_width + button_spacing), 10, button_width, button_height, "Player", 6, lambda: load_sprite_grid(sprite_grid, "player")),
        Button(start_x + 3 * (button_width + button_spacing), 10, button_width, button_height, "Monster", 3, lambda: load_sprite_grid(sprite_grid, "monster")),
        Button(start_x + 4 * (button_width + button_spacing), 10, button_width, button_height, "Texture", 1, lambda: load_sprite_grid(sprite_grid, "texture")),
        Button(start_x + 5 * (button_width + button_spacing), 10, button_width, button_height, "NPC", 7, lambda: load_sprite_grid(sprite_grid, "npc")),  # New: NPC button
        Button(start_x + 6 * (button_width + button_spacing), 10, button_width, button_height, "Empty", 0),
        Button(start_x + 7 * (button_width + button_spacing), 10, button_width, button_height, "Save", -1, lambda: save_map(current_map, grid, monsters, textures, items, npcs))
    ]

    # Inputs for monster stats
    input_width = 150
    inputs_start_x = start_x
    inputs = [
        TextInput(inputs_start_x, 60, input_width, 30, "Health"),
        TextInput(inputs_start_x + input_width + button_spacing, 60, input_width, 30, "Attack"),
        TextInput(inputs_start_x + 2 * (input_width + button_spacing), 60, input_width, 30, "Defense"),
        TextInput(inputs_start_x + 3 * (input_width + button_spacing), 60, input_width, 30, "XP")
    ]

    # Initialize inputs with default stats for mutant
    current_monster = "mutant.png"
    for i, (key, value) in enumerate(default_monster_stats[current_monster].items()):
        inputs[i].text = value

    if os.path.exists(os.path.join(MAP_DIR, current_map)):
        grid, monsters, textures, items, npcs = load_map(current_map)
        selected_texture = "grass.jpg"

    quest_setup = QuestSetup()  # New: Quest setup UI

    def load_sprite_grid(sprite_grid, category):
        nonlocal selected_sprite_pos
        for y in range(SPRITE_GRID_HEIGHT):
            for x in range(SPRITE_GRID_WIDTH):
                sprite_grid[y][x] = None
        items_list = sprite_items[category]
        for i, (sprite, value) in enumerate(items_list):
            y = i // SPRITE_GRID_WIDTH
            x = i % SPRITE_GRID_WIDTH
            if y < SPRITE_GRID_HEIGHT:
                sprite_grid[y][x] = (sprite, value)
        for button in buttons:
            button.selected = (button.text.lower() == category)
        selected_sprite_pos = None

    clock = pygame.time.Clock()
    while running:
        mouse_pos = pygame.mouse.get_pos()
        shift_pressed = pygame.key.get_mods() & pygame.KMOD_SHIFT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                mousedown = True

                # Handle buttons
                for button in buttons:
                    if button.clicked((mx, my)):
                        if button.action:
                            button.action()
                            if button.value == -1:  # Save
                                save_map(current_map, grid, monsters, textures, items, npcs)
                                sprite_items["map"] = [(f"map_{i}.txt", None) for i in range(1, 11) if os.path.exists(os.path.join(MAP_DIR, f"map_{i}.txt"))] + [("New", None)]
                                start_map += 1
                                current_map = f"map_{start_map}.txt"
                                grid, monsters, textures, items, npcs = load_map(current_map) if os.path.exists(os.path.join(MAP_DIR, current_map)) else ([[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)], {}, {}, {}, {})
                        else:
                            selected_tool = button.value
                        break

                # Handle sprite grid clicks
                if mx >= SPRITE_GRID_X and my >= SPRITE_GRID_Y:
                    sprite_x = (mx - SPRITE_GRID_X) // TILE_SIZE
                    sprite_y = (my - SPRITE_GRID_Y) // TILE_SIZE
                    if 0 <= sprite_x < SPRITE_GRID_WIDTH and 0 <= sprite_y < SPRITE_GRID_HEIGHT:
                        sprite = sprite_grid[sprite_y][sprite_x]
                        if sprite:
                            sprite_name, sprite_value = sprite
                            selected_sprite_pos = (sprite_x, sprite_y)
                            if sprite_name == "New":
                                start_map = 1
                                while os.path.exists(os.path.join(MAP_DIR, f"map_{start_map}.txt")) and start_map <= 10:
                                    start_map += 1
                                if start_map <= 10:
                                    current_map = f"map_{start_map}.txt"
                                    grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
                                    monsters = {}
                                    textures = {}
                                    items = {}
                                    npcs = {}
                                    sprite_items["map"] = [(f"map_{i}.txt", None) for i in range(1, 11) if os.path.exists(os.path.join(MAP_DIR, f"map_{i}.txt"))] + [("New", None)]
                                    load_sprite_grid(sprite_grid, "map")
                                else:
                                    print("Maximum map limit (10) reached.")
                            elif sprite_name.endswith(".txt"):
                                current_map = sprite_name
                                grid, monsters, textures, items, npcs = load_map(current_map)
                                selected_monster_key = None
                            else:
                                selected_tool = sprite_value
                                selected_texture = sprite_name
                                if selected_tool == 3:
                                    current_monster = selected_texture
                                    for i, (key, value) in enumerate(default_monster_stats[current_monster].items()):
                                        inputs[i].text = value
                            mousedown = False

                # Handle grid clicks
                if my > 100 and mx < GRID_WIDTH * TILE_SIZE:
                    x, y = mx // TILE_SIZE, (my - 100) // TILE_SIZE
                    key = f"{x},{y}"
                    if shift_pressed and selected_tool is not None:
                        if selected_tool == 7:  # New: NPC with quest setup
                            quest_setup.active = True
                            while quest_setup.active:
                                for sub_event in pygame.event.get():
                                    if sub_event.type == pygame.QUIT:
                                        running = False
                                        quest_setup.active = False
                                    elif sub_event.type == pygame.MOUSEBUTTONDOWN:
                                        for input_box in quest_setup.dialogue_inputs + [quest_setup.item_input, quest_setup.amount_input, quest_setup.drop_input]:
                                            input_box.active = input_box.clicked(sub_event.pos)
                                        if quest_setup.confirm_button.clicked(sub_event.pos):
                                            quest_setup.confirm()
                                    elif sub_event.type == pygame.KEYDOWN:
                                        for input_box in quest_setup.dialogue_inputs + [quest_setup.item_input, quest_setup.amount_input, quest_setup.drop_input]:
                                            if input_box.active:
                                                if sub_event.key == pygame.K_BACKSPACE:
                                                    input_box.text = input_box.text[:-1]
                                                elif sub_event.key != pygame.K_RETURN:
                                                    input_box.text += sub_event.unicode
                                screen.fill(BLACK)
                                quest_setup.draw(screen)
                                pygame.display.flip()
                                clock.tick(60)
                            place_on_grid(grid, monsters, textures, items, npcs, x, y, selected_tool, selected_texture, inputs, quest_setup.quest_data)
                        else:
                            place_on_grid(grid, monsters, textures, items, npcs, x, y, selected_tool, selected_texture, inputs)
                            selected_monster_key = key if selected_tool == 3 else None
                            if selected_monster_key and selected_monster_key in monsters:
                                for i, key in enumerate(["health", "attack", "defense", "xp"]):
                                    inputs[i].text = str(monsters[selected_monster_key][key])
                    elif grid[y][x] == 3 and key in monsters:
                        selected_monster_key = key
                        for i, key in enumerate(["health", "attack", "defense", "xp"]):
                            inputs[i].text = str(monsters[selected_monster_key][key])

                # Handle text input clicks
                for input_box in inputs:
                    if input_box.clicked((mx, my)):
                        input_box.active = True
                    else:
                        input_box.active = False

            elif event.type == pygame.MOUSEBUTTONUP:
                mousedown = False
            elif event.type == pygame.MOUSEMOTION and mousedown and shift_pressed:
                mx, my = event.pos
                if my > 100 and mx < GRID_WIDTH * TILE_SIZE and selected_tool is not None and selected_tool not in [3, 6, 7]:
                    x, y = mx // TILE_SIZE, (my - 100) // TILE_SIZE
                    place_on_grid(grid, monsters, textures, items, npcs, x, y, selected_tool, selected_texture, inputs)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif any(input_box.active for input_box in inputs):
                    active_input = next(input_box for input_box in inputs if input_box.active)
                    if event.key == pygame.K_BACKSPACE:
                        active_input.text = active_input.text[:-1]
                    elif event.key in [pygame.K_RETURN, pygame.K_KP_ENTER]:
                        active_input.active = False
                        if selected_monster_key and selected_monster_key in monsters:
                            monsters[selected_monster_key].update({
                                "health": int(inputs[0].text or 50),
                                "max_health": int(inputs[0].text or 50),
                                "attack": int(inputs[1].text or 10),
                                "defense": int(inputs[2].text or 5),
                                "xp": int(inputs[3].text or 4)
                            })
                    elif event.unicode.isdigit():
                        active_input.text += event.unicode

        # Update button hover states
        for button in buttons:
            button.update(mouse_pos)

        screen.fill(BLACK)
        if MENU_BACKGROUND:
            screen.blit(MENU_BACKGROUND, (0, 0))
        else:
            for i in range(100):
                alpha = i / 100
                color = tuple(int(DARK_GRAY[j] * (1 - alpha) + LIGHT_GRAY[j] * alpha) for j in range(3))
                pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))
            title = TITLE_FONT.render("Map Editor", True, WHITE)
            offset = 200
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2 + offset, 10))

        # Draw main grid with highlight for selected monster
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = (x * TILE_SIZE, y * TILE_SIZE + 100, TILE_SIZE, TILE_SIZE)
                key = f"{x},{y}"
                try:
                    texture = textures.get(key, "boundary.jpg")
                    screen.blit(TEXTURES.get(texture, FALLBACK_TEXTURE), rect)

                    if grid[y][x] == 3:
                        sprite = monsters.get(key, {}).get("sprite", selected_texture)
                        screen.blit(MONSTER_SPRITES.get(sprite, FALLBACK_TEXTURE), rect)
                        if key == selected_monster_key:
                            pygame.draw.rect(screen, GOLD, rect, 3)
                    elif grid[y][x] == 6:
                        screen.blit(PLAYER_SPRITE, rect)
                    elif grid[y][x] == 7:  # New: Draw NPCs
                        sprite = npcs.get(key, {}).get("sprite", selected_texture)
                        screen.blit(NPC_SPRITES.get(sprite, FALLBACK_TEXTURE), rect)
                    elif key in items:
                        item_sprite = items.get(key, "Health_Box.png")
                        screen.blit(ITEMS.get(item_sprite, FALLBACK_TEXTURE), rect)
                except (NameError, KeyError) as e:
                    print(f"Error drawing tile at {x},{y}: {e}")
                    pygame.draw.rect(screen, GREEN, rect)
                    if grid[y][x] == 3:
                        pygame.draw.rect(screen, BLUE, rect)
                    elif grid[y][x] == 6:
                        pygame.draw.rect(screen, RED, rect)
                    elif grid[y][x] == 7:  # New: Fallback for NPC
                        pygame.draw.rect(screen, YELLOW, rect)
                    if key in items:
                        pygame.draw.rect(screen, YELLOW, rect)

        # Draw sprite grid
        for y in range(SPRITE_GRID_HEIGHT):
            for x in range(SPRITE_GRID_WIDTH):
                rect = (SPRITE_GRID_X + x * TILE_SIZE, SPRITE_GRID_Y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, GRAY, rect, 1)
                sprite = sprite_grid[y][x]
                if sprite:
                    sprite_name, _ = sprite
                    if sprite_name in TEXTURES:
                        screen.blit(TEXTURES.get(sprite_name, FALLBACK_TEXTURE), rect)
                    elif sprite_name in ITEMS:
                        screen.blit(ITEMS.get(sprite_name, FALLBACK_TEXTURE), rect)
                    elif sprite_name in MONSTER_SPRITES:
                        screen.blit(MONSTER_SPRITES.get(sprite_name, FALLBACK_TEXTURE), rect)
                    elif sprite_name in NPC_SPRITES:  # New: Draw NPC sprites
                        screen.blit(NPC_SPRITES.get(sprite_name, FALLBACK_TEXTURE), rect)
                    elif sprite_name == "player.png":
                        screen.blit(PLAYER_SPRITE, rect)
                    elif sprite_name.endswith(".txt") or sprite_name == "New":
                        text_surface = MAP_FONT.render(sprite_name, True, WHITE)
                        text_rect = text_surface.get_rect(center=(rect[0] + TILE_SIZE // 2, rect[1] + TILE_SIZE // 2))
                        pygame.draw.rect(screen, DARK_GRAY, rect)
                        screen.blit(text_surface, text_rect)
                if selected_sprite_pos and selected_sprite_pos == (x, y):
                    pygame.draw.rect(screen, GOLD, rect, 3)

        # Draw UI
        for button in buttons:
            button.draw(screen)
        for input_box in inputs:
            input_box.draw(screen)

        # Hint text
        hint = SMALL_FONT.render("V1.03 - Hold Shift + Click/Drag to Place, Click to Select Monster, Shift + Click NPC for Quest", True, WHITE)
        screen.blit(hint, (10, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    start_map = 1
    while os.path.exists(os.path.join(MAP_DIR, f"map_{start_map}.txt")) and start_map <= 10:
        start_map += 1
    if start_map > 10:
        print("All maps (1-10) already exist. Loading editor for map_1.txt.")
        start_map = 1
    map_editor(start_map)
