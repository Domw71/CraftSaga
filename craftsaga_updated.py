import pygame
import random
import os
import time
import mysql.connector
import json
from mysql.connector import Error

pygame.init()

# Screen and grid setup
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
GRID_WIDTH, GRID_HEIGHT = 30, 22
TILE_SIZE = min(SCREEN_WIDTH // GRID_WIDTH, SCREEN_HEIGHT // GRID_HEIGHT)
WIDTH, HEIGHT = GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("CraftSaga")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
STEEL = (70, 130, 180)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (150, 150, 150)

# Fonts
TITLE_FONT = pygame.font.SysFont("Arial", int(TILE_SIZE * 1.2), bold=True)
BUTTON_FONT = pygame.font.SysFont("Arial", int(TILE_SIZE * 0.8), bold=True)
SMALL_FONT = pygame.font.SysFont("Arial", int(TILE_SIZE * 0.6))

# Define directories
TEXTURE_DIR = "data/textures"
ITEM_DIR = "data/items"
MONSTER_DIR = "data/monsters"
MAP_DIR = "data/maps"
STAT_DIR = "data/stats"
PLAYER_DIR = "data/player"
ARROW_DIR = "data/arrows"
NPC_DIR = "data/npcs"  # New: NPC directory

# Ensure directories exist
for directory in [TEXTURE_DIR, ITEM_DIR, MONSTER_DIR, MAP_DIR, STAT_DIR, PLAYER_DIR, ARROW_DIR, NPC_DIR]:
    os.makedirs(directory, exist_ok=True)

# Load textures/sprites
TEXTURES = {}
ITEMS = {}
MONSTER_SPRITES = {}
ARROW_SPRITES = {}
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

    item_files = ["Health_Box.png", "attack_pot.png"]
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

    arrow_files = ["left_arrow.png", "right_arrow.png"]
    for sprite in arrow_files:
        sprite_path = os.path.join(ARROW_DIR, sprite)
        if os.path.exists(sprite_path):
            ARROW_SPRITES[sprite] = pygame.transform.scale(pygame.image.load(sprite_path).convert_alpha(), (TILE_SIZE // 2, TILE_SIZE // 2))
        else:
            print(f"Warning: Arrow sprite '{sprite_path}' not found.")

    npc_files = ["roger.png"]  # New: Load NPC sprite
    for sprite in npc_files:
        sprite_path = os.path.join(NPC_DIR, sprite)
        if os.path.exists(sprite_path):
            NPC_SPRITES[sprite] = pygame.transform.scale(pygame.image.load(sprite_path).convert_alpha(), (TILE_SIZE, TILE_SIZE))
        else:
            print(f"Warning: NPC sprite '{sprite_path}' not found.")

    player_path = os.path.join(PLAYER_DIR, "player.png")
    PLAYER_SPRITE = pygame.transform.scale(pygame.image.load(player_path).convert_alpha(), (TILE_SIZE, TILE_SIZE)) if os.path.exists(player_path) else None

    menu_bg_path = os.path.join(TEXTURE_DIR, "menu_background.jpg")
    MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(menu_bg_path).convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT)) if os.path.exists(menu_bg_path) else None
except pygame.error as e:
    print(f"Texture load failed: {e}. Using colors.")
    MENU_BACKGROUND = None
    ARROW_SPRITES = {}
    NPC_SPRITES = {}

FALLBACK_TEXTURE = pygame.Surface((TILE_SIZE, TILE_SIZE))
FALLBACK_TEXTURE.fill(GREEN)

# Player and monster settings
player_speed = 0.2
monster_speed = 0.05
player_base_health = 100
player_base_attack = 10
player_base_defense = 5

# Player initial settings
INITIAL_HEALTH = 100
INITIAL_ATTACK = 10
INITIAL_STRENGTH = 10
INITIAL_DEFENSE = 10
INITIAL_LEVEL = 1
INITIAL_XP = 0
INITIAL_MONSTERS_KILLED = 0
INITIAL_ITEMS_COLLECTED = 0

# MySQL connection
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="Your Password",
            database="craftsaga"
        )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Database table creation
def create_tables():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                current_level INT DEFAULT 1,
                mutants_killed INT DEFAULT 0,
                items_collected INT DEFAULT 0,
                health INT DEFAULT 100,
                attack INT DEFAULT 10,
                defense INT DEFAULT 5,
                strength INT DEFAULT 10,
                level INT DEFAULT 1,
                xp INT DEFAULT 0,
                demons_killed INT DEFAULT 0,
                dragons_killed INT DEFAULT 0,
                killed_monsters TEXT,
                killed_monsters_details TEXT,
                collected_items_details TEXT,
                completed_levels TEXT,
                inventory_items TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS achievements (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player_id INT,
                achievement_name VARCHAR(255),
                completed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        # New table for quests
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quests (
                id INT AUTO_INCREMENT PRIMARY KEY,
                player_id INT,
                quest_id VARCHAR(255),
                completed BOOLEAN DEFAULT FALSE,
                FOREIGN KEY (player_id) REFERENCES players(id)
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print("Database tables verified/created.")

# Load map function
def load_map(filename):
    map_path = os.path.join(MAP_DIR, filename)
    grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    items = {}
    monsters = {}
    textures = {}
    npcs = {}  # New: Store NPC data
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
                npcs = data.get('npcs', {})  # Load NPCs with quests
    return grid, monsters, textures, items, npcs

class ChatBox:
    def __init__(self, x, y, width, height, max_lines=5):
        self.rect = pygame.Rect(x, y, width, height)
        self.messages = []  # List of (text, timer) tuples
        self.max_lines = max_lines
        self.font = SMALL_FONT
        self.line_height = self.font.get_linesize() + 5
        self.background_color = BLACK
        self.border_color = GRAY
        self.text_color = WHITE
        self.max_width = width - 20  # Account for 10px padding on each side

    def add_message(self, text, duration=300):  # Duration in frames (5 seconds at 60 FPS)
        # Split text into words
        words = text.split()
        current_line = ""
        wrapped_lines = []

        # Build lines that fit within max_width
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_surface = self.font.render(test_line, True, self.text_color)
            if test_surface.get_width() <= self.max_width:
                current_line = test_line
            else:
                if current_line:  # Add the previous line if it exists
                    wrapped_lines.append(current_line)
                current_line = word  # Start new line with current word

        # Add the last line if it exists
        if current_line:
            wrapped_lines.append(current_line)

        # Add each wrapped line as a message
        for line in wrapped_lines:
            self.messages.append((line, duration))
        
        # Trim excess messages beyond max_lines
        while len(self.messages) > self.max_lines:
            self.messages.pop(0)

    def update(self):
        # Decrease timers and remove expired messages
        self.messages = [(text, timer - 1) for text, timer in self.messages if timer > 0]

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)
        y_offset = self.rect.y + 10
        for text, _ in self.messages[-self.max_lines:]:  # Only draw up to max_lines
            text_surface = self.font.render(text, True, self.text_color)
            screen.blit(text_surface, (self.rect.x + 10, y_offset))
            y_offset += self.line_height
            if y_offset + self.line_height > self.rect.bottom:  # Stop if exceeding height
                break

class QuestBox:
    def __init__(self, x, y, width, height, max_lines=5):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_lines = max_lines
        self.font = SMALL_FONT
        self.line_height = self.font.get_linesize() + 5
        self.background_color = BLACK
        self.border_color = GRAY
        self.title_color = WHITE
        self.max_width = width - 20  # Padding

    def draw(self, screen, all_quests, active_quests, completed_quests, quest_items, current_level):
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)
        
        title_text = BUTTON_FONT.render("Quests", True, self.title_color)
        title_x = self.rect.x + (self.rect.width - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, self.rect.y + 10))
        
        y_offset = self.rect.y + title_text.get_height() + 20
        displayed_lines = 0
        
        level_quests = all_quests.get(current_level, {})
        if not level_quests:
            no_quests_text = self.font.render("No quests available.", True, WHITE)
            screen.blit(no_quests_text, (self.rect.x + 10, y_offset))
            return

        for quest_id, quest_data in level_quests.items():
            if displayed_lines >= self.max_lines:
                break
            
            # Determine the text to display
            if quest_id in completed_quests:
                # Completed quest: show item progress
                items_text = ", ".join(f"{item} ({count}/{target})" for item, target in quest_data["items"].items() 
                                      for count in [min(quest_items.get(item, 0), target)])
                text = items_text
            elif quest_data["accepted"]:
                # Accepted but not completed: show item progress
                items_text = ", ".join(f"{item} ({count}/{target})" for item, target in quest_data["items"].items() 
                                      for count in [min(quest_items.get(item, 0), target)])
                text = items_text
            else:
                # Not accepted: show prompt to talk to Roger
                text = "Talk to Roger (E) to accept quest (Y)"
            
            # Render the text
            text_surface = self.font.render(text, True, WHITE)
            while text_surface.get_width() > self.max_width and len(text) > 10:
                text = text[:-1]
                text_surface = self.font.render(text + "...", True, WHITE)
            
            # Determine color
            if quest_id in completed_quests:
                color = GREEN  # Completed
            elif quest_data["accepted"]:
                progress = sum(quest_items.get(item, 0) for item in quest_data["items"])
                color = GREEN if progress >= quest_data["target"] else RED  # Active: green if done, red if not
            else:
                color = RED  # Available but not accepted
            
            quest_surface = self.font.render(text, True, color)
            screen.blit(quest_surface, (self.rect.x + 10, y_offset))
            y_offset += self.line_height
            displayed_lines += 1

class Inventory:
    def __init__(self, x, y, width, height, grid_size=6):
        self.rect = pygame.Rect(x, y, width, height)
        self.grid_size = grid_size  # 6x6 grid
        self.cell_size = min(width // grid_size, height // grid_size)
        self.items = [[None for _ in range(grid_size)] for _ in range(grid_size)]  # 2D list for items
        self.background_color = BLACK
        self.border_color = GRAY
        self.font = SMALL_FONT

    def add_item(self, item_type):
        # Find the first empty slot in the grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.items[y][x] is None:
                    self.items[y][x] = {"type": item_type, "count": 1}
                    return True
                elif self.items[y][x]["type"] == item_type:
                    self.items[y][x]["count"] += 1
                    return True
        return False  # Inventory full

    def use_item(self, item_type):
        # Find and use the first instance of the item
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.items[y][x] and self.items[y][x]["type"] == item_type:
                    self.items[y][x]["count"] -= 1
                    if self.items[y][x]["count"] <= 0:
                        self.items[y][x] = None
                    return True
        return False  # No item found

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect, border_radius=5)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)

        title_text = BUTTON_FONT.render("Inventory", True, WHITE)
        title_x = self.rect.x + (self.rect.width - title_text.get_width()) // 2
        screen.blit(title_text, (title_x, self.rect.y + 10))

        grid_start_y = self.rect.y + title_text.get_height() + 20
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                cell_rect = pygame.Rect(
                    self.rect.x + x * self.cell_size,
                    grid_start_y + y * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )
                pygame.draw.rect(screen, LIGHT_GRAY, cell_rect, border_radius=2)
                pygame.draw.rect(screen, DARK_GRAY, cell_rect, 1, border_radius=2)
                if self.items[y][x]:
                    item_type = self.items[y][x]["type"]
                    count = self.items[y][x]["count"]
                    try:
                        screen.blit(
                            ITEMS.get(item_type),
                            (cell_rect.x + 5, cell_rect.y + 5)
                        )
                    except (NameError, KeyError):
                        pygame.draw.rect(screen, YELLOW, (cell_rect.x + 5, cell_rect.y + 5, self.cell_size - 10, self.cell_size - 10))
                    count_text = self.font.render(str(count), True, WHITE)
                    screen.blit(count_text, (cell_rect.right - count_text.get_width() - 2, cell_rect.bottom - count_text.get_height() - 2))
                
# Button and TextBox classes
class Button:
    def __init__(self, x, y, width, height, text, action=None, is_locked=False, is_completed=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = BUTTON_FONT.render(text, True, WHITE)
        self.action = action
        self.hovered = False
        self.is_locked = is_locked
        self.is_completed = is_completed  # New flag for completed state

    def draw(self, screen):
        shadow_rect = self.rect.move(5, 5)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=10)
        if self.is_completed:  # New condition for completed buttons
            color_top = GOLD if not self.hovered else (255, 235, 100)  # Bright gold to slightly muted gold
            color_bottom = (205, 175, 0) if not self.hovered else (185, 155, 50)  # Darker gold shades
        elif self.is_locked:  # Locked but not completed
            color_top = RED if not self.hovered else (200, 0, 0)
            color_bottom = (150, 0, 0) if not self.hovered else (100, 0, 0)
        else:  # Unlocked and not completed
            color_top = GREEN if not self.hovered else (0, 200, 0)
            color_bottom = (0, 150, 0) if not self.hovered else (0, 100, 0)
        for i in range(self.rect.height):
            alpha = i / self.rect.height
            color = tuple(int(color_top[j] * (1 - alpha) + color_bottom[j] * alpha) for j in range(3))
            pygame.draw.line(screen, color, (self.rect.x, self.rect.y + i), (self.rect.x + self.rect.width, self.rect.y + i))
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        text_rect = self.text.get_rect(center=self.rect.center)
        screen.blit(self.text, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update(self, pos):
        self.hovered = self.rect.collidepoint(pos)

class TextBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False

    def draw(self, screen):
        color = WHITE if self.active else GRAY
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=5)
        text_surface = SMALL_FONT.render(self.text if not self.active else self.text + "|", True, BLACK)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

# Game states
class GameState:
    MENU = 0
    LOGIN = 1
    REGISTER = 2
    PLAYING = 3
    PAUSED = 4
    GAME_OVER = 5
    HIGH_SCORES = 6
    CREDITS = 7
    UPDATES = 8
    CONTROLS = 9
    SELECT_LEVEL = 10
    ACHIEVEMENTS = 11

class CraftSagaGame:
    def __init__(self):
        self.state = GameState.MENU
        self.levels = [f"map_{i}.txt" for i in range(1, 11) if os.path.exists(os.path.join(MAP_DIR, f"map_{i}.txt"))]
        if not self.levels:
            raise FileNotFoundError("No maps found.")
        print(f"Found {len(self.levels)} levels: {self.levels}")
        self.current_level = 0
        self.player_id = None
        self.username = None
        self.player_health = None
        self.player_max_health = None
        self.player_attack = None
        self.player_attack_bonus = 0
        self.attack_bonus_timer = 0
        self.player_defense = None
        self.player_strength = None
        self.player_level = None
        self.player_xp = None
        self.mutants_killed = None
        self.items_collected = None
        self.demons_killed = None
        self.mutant_killed = None
        self.dragons_killed = None
        self.level_monsters_killed = 0
        self.level_items_collected = 0
        self.killed_monster_ids = set()
        self.collected_item_ids = set()
        self.unlocked_levels = 1
        self.completed_levels = set()
        self.achievement_message = None
        self.achievement_timer = 0
        self.textures = {}
        self.items_dict = {}
        self.xp_per_level = 5
        self.monster_kills = {"mutant.png": 0, "Demon.png": 0, "Dragon.png": 0}
        self.item_counts = {"Health_Box.png": 0, "attack_pot.png": 0}
        self.npcs = {}  # New: Store NPCs per level
        self.active_quests = {}  # New: {quest_id: {"progress": int, "target": int, "items": dict, "drop_sources": dict}}
        
        self.quest_items = {}  # New: {"seed": count}
        self.pending_quest = None  # New: Store pending quest acceptance
        self.all_quests = {}
        self.ACHIEVEMENTS_MAIN = 0
        self.ACHIEVEMENTS_MONSTERS = 1
        self.ACHIEVEMENTS_ITEMS = 2
        self.ach_sub_state = self.ACHIEVEMENTS_MAIN
        self.HIGH_SCORES_MAIN = 0
        self.HIGH_SCORES_DETAILS = 1
        self.high_score_sub_state = self.HIGH_SCORES_MAIN
        self.selected_player_stats = None

        chat_width = 400
        chat_height = 150
        objectives_width = 400
        objectives_height = 150
        quest_width = 400
        quest_height = 150
        inventory_width = 400  # Same width as quest box
        inventory_height = 400  # Enough for 6x6 grid with title
        objectives_x = SCREEN_WIDTH - objectives_width - 10
        objectives_y = 10
        chat_x = objectives_x
        chat_y = objectives_y + objectives_height + 10
        quest_x = chat_x  # Same x as chat box
        quest_y = chat_y + chat_height + 10  # Below chat box
        inventory_x = quest_x  # Same x as quest box
        inventory_y = quest_y + quest_height + 10  # Below quest box
        self.chat_box = ChatBox(chat_x, chat_y, chat_width, chat_height, max_lines=5)
        self.quest_box = QuestBox(quest_x, quest_y, quest_width, quest_height, max_lines=5)
        self.inventory = Inventory(inventory_x, inventory_y, inventory_width, inventory_height)  # New inventory

        self.levels_per_page = 5
        self.current_level_page = 0
        
        create_tables()

        button_width, button_height = 300, 60
        button_spacing = 20
        total_menu_height = 7 * (button_height + button_spacing) - button_spacing
        start_y = (SCREEN_HEIGHT - total_menu_height) // 2
        self.menu_buttons = [
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y, button_width, button_height, "Login/Register", lambda: setattr(self, 'state', GameState.LOGIN)),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + (button_height + button_spacing), button_width, button_height, "Credits", lambda: setattr(self, 'state', GameState.CREDITS)),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height, "Updates", lambda: setattr(self, 'state', GameState.UPDATES)),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 3 * (button_height + button_spacing), button_width, button_height, "Controls", lambda: setattr(self, 'state', GameState.CONTROLS)),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 4 * (button_height + button_spacing), button_width, button_height, "Select Level", lambda: self.select_level_action()),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 5 * (button_height + button_spacing), button_width, button_height, "High Scores", lambda: setattr(self, 'state', GameState.HIGH_SCORES)),
            Button(SCREEN_WIDTH // 2 - button_width // 2, start_y + 6 * (button_height + button_spacing), button_width, button_height, "Achievements", lambda: self.achievements_action()),
        ]
        self.back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back", lambda: setattr(self, 'state', GameState.MENU))
        self.login_boxes = [TextBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3, 200, 30), TextBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 60, 200, 30)]
        self.login_buttons = [
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 120, 200, 50, "Login", lambda: self.login_action()),
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 180, 200, 50, "Register", lambda: setattr(self, 'state', GameState.REGISTER)),
            self.back_button
        ]
        self.register_boxes = [TextBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3, 200, 30), TextBox(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 60, 200, 30)]
        self.register_buttons = [
            Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 120, 200, 50, "Register", lambda: self.register_action()),
            self.back_button
        ]
        self.load_level()

    def load_level(self):
        self.grid, monsters_stats, self.textures, self.items_dict, npcs_stats = load_map(self.levels[self.current_level])
        self.player_x, self.player_y = GRID_WIDTH / 2.0, GRID_HEIGHT / 2.0

        self.monsters = []
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 3:
                    key = f"{x},{y}"
                    if key in monsters_stats:
                        monster_data = monsters_stats[key]
                        monster = {
                            "x": x + 0.5,
                            "y": y + 0.5,
                            "sprite": monster_data.get("sprite", "mutant.png"),
                            "health": monster_data.get("health", (player_base_health * 2) + self.current_level * 50),
                            "max_health": monster_data.get("health", (player_base_health * 2) + self.current_level * 50),
                            "attack": monster_data.get("attack", (player_base_attack * 2) + self.current_level * 10),
                            "defense": monster_data.get("defense", (player_base_defense * 2) + self.current_level * 5),
                            "xp": monster_data.get("xp", 5),
                            "id": key,
                            "aggroed": False  # Ensure this is always set
                        }
                    else:
                        default_health = (player_base_health * 2) + self.current_level * 50
                        monster = {
                            "x": x + 0.5,
                            "y": y + 0.5,
                            "sprite": "mutant.png",
                            "health": default_health,
                            "max_health": default_health,
                            "attack": (player_base_attack * 2) + self.current_level * 10,
                            "defense": (player_base_defense * 2) + self.current_level * 5,
                            "xp": 5,
                            "id": key,
                            "aggroed": False  # Ensure this is always set
                        }
                    if monster["id"] not in self.killed_monster_ids:
                        self.monsters.append(monster)

        self.items = [(x + 0.5, y + 0.5, item_type) for y in range(GRID_HEIGHT) for x in range(GRID_WIDTH)
                      if f"{x},{y}" in self.items_dict and f"{x},{y}" not in self.collected_item_ids
                      for item_type in [self.items_dict[f"{x},{y}"]]]

        # Load NPCs
        self.npcs = {}
        if self.current_level not in self.all_quests:
            self.all_quests[self.current_level] = {}
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 7:  # NPC tile
                    key = f"{x},{y}"
                    if key in npcs_stats:
                        npc_data = npcs_stats[key]
                        self.npcs[key] = {
                            "x": x + 0.5,
                            "y": y + 0.5,
                            "sprite": npc_data.get("sprite", "roger.png"),
                            "quest": npc_data.get("quest", None)
                        }
                        if "quest" in npc_data and npc_data["quest"]:
                            quest_id = f"{self.current_level}_{key}"
                            if quest_id not in self.all_quests[self.current_level]:
                                self.all_quests[self.current_level][quest_id] = {
                                    "items": npc_data["quest"]["required_items"],
                                    "target": sum(npc_data["quest"]["required_items"].values()),
                                    "drop_sources": npc_data["quest"]["drop_sources"],
                                    "accepted": False
                                }
                    self.grid[y][x] = 1  # Reset NPC tile to walkable
        self.active_quests = {}
        for quest_id, quest_data in self.all_quests[self.current_level].items():
            if quest_data["accepted"] and quest_id not in self.completed_quests:
                self.active_quests[quest_id] = {
                    "progress": sum(self.quest_items.get(item, 0) for item in quest_data["items"]),
                    "target": quest_data["target"],
                    "items": quest_data["items"],
                    "drop_sources": quest_data["drop_sources"]
                }

        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x] == 6:
                    self.player_x, self.player_y = x + 0.5, y + 0.5
                    break
        self.grid = [[1 if cell in [3, 4, 6, 7] else cell for cell in row] for row in self.grid]
        self.level_monsters_killed = 0
        self.level_items_collected = 0
        self.active_quests = {}
        self.quest_items = {}
        self.quests = [
            {"text": f"Kill {len(self.monsters)} mutants", "progress": self.level_monsters_killed, "target": len(self.monsters)},
            {"text": f"Collect {len(self.items)} items", "progress": self.level_items_collected, "target": len(self.items)}
        ]
    def reset_game(self):
        self.player_health = max(100, min(self.player_max_health, self.player_health))
        self.attack_bonus_timer = 0
        self.player_attack_bonus = 0
        self.load_level()

    def login_action(self):
        self.login(self.login_boxes[0].text, self.login_boxes[1].text)

    def register_action(self):
        self.register(self.register_boxes[0].text, self.register_boxes[1].text)

    def logout(self):
        self.save_progress()
        self.player_id = None
        self.username = None
        self.unlocked_levels = 1
        self.inventory.items = [[None for _ in range(6)] for _ in range(6)]  # Clear inventory
        self.menu_buttons[0] = Button(SCREEN_WIDTH // 2 - 300 // 2, self.menu_buttons[0].rect.y, 300, 60, "Login/Register", lambda: setattr(self, 'state', GameState.LOGIN))
        self.state = GameState.MENU

    def save_progress(self):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            all_ids = list(self.killed_monster_ids) + list(self.collected_item_ids)
            inventory_json = json.dumps(self.inventory.items)  # Convert 6x6 grid to JSON
            cursor.execute("""
                UPDATE players SET current_level=%s, mutants_killed=%s, dragons_killed=%s, items_collected=%s,
                health=%s, attack=%s, defense=%s, strength=%s, level=%s, xp=%s, demons_killed=%s, 
                killed_monsters=%s, killed_monsters_details=%s, collected_items_details=%s, 
                completed_levels=%s, inventory_items=%s WHERE id=%s""",
                (self.current_level + 1, self.mutants_killed, self.dragons_killed, self.items_collected,
                 self.player_health, self.player_attack, self.player_defense, self.player_strength,
                 self.player_level, self.player_xp, self.demons_killed, json.dumps(all_ids),
                 json.dumps(self.monster_kills), json.dumps(self.item_counts), json.dumps(list(self.completed_levels)),
                 inventory_json, self.player_id))
            conn.commit()
            cursor.close()
            conn.close()
            print("Progress saved!")

    def login(self, username, password):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, current_level, mutants_killed, dragons_killed, items_collected, health, attack, defense, strength, level, xp, demons_killed, killed_monsters, killed_monsters_details, collected_items_details, completed_levels, inventory_items
                FROM players WHERE username=%s AND password=%s""", (username, password))
            result = cursor.fetchone()
            if result:
                self.player_id, self.current_level, self.mutants_killed, self.dragons_killed, self.items_collected, \
                self.player_health, self.player_attack, self.player_defense, self.player_strength, \
                self.player_level, self.player_xp, self.demons_killed, killed_monsters_json, \
                monster_details_json, item_details_json, completed_levels_json, inventory_json = result
                self.player_max_health = max(self.player_health, INITIAL_HEALTH)
                all_ids = set(json.loads(killed_monsters_json) if killed_monsters_json else [])
                self.killed_monster_ids = set()
                self.collected_item_ids = set()
                temp_monsters = []
                for y in range(GRID_HEIGHT):
                    for x in range(GRID_WIDTH):
                        if self.grid[y][x] == 3:
                            key = f"{x},{y}"
                            temp_monsters.append({"id": key})
                monster_ids = {m["id"] for m in temp_monsters}
                for id in all_ids:
                    if id in monster_ids:
                        self.killed_monster_ids.add(id)
                    else:
                        self.collected_item_ids.add(id)
                self.monster_kills = json.loads(monster_details_json) if monster_details_json else {"mutant.png": 0, "Demon.png": 0, "Dragon.png": 0}
                self.item_counts = json.loads(item_details_json) if item_details_json else {"Health_Box.png": 0, "attack_pot.png": 0}
                self.completed_levels = set(json.loads(completed_levels_json)) if completed_levels_json else set()
                self.inventory.items = json.loads(inventory_json) if inventory_json else [[None for _ in range(6)] for _ in range(6)]  # Load inventory
                # Load completed quests
                cursor.execute("SELECT quest_id FROM quests WHERE player_id=%s AND completed=1", (self.player_id,))
                self.completed_quests = {row[0] for row in cursor.fetchall()}
                self.unlocked_levels = max(self.unlocked_levels, self.current_level)
                self.current_level = 0
                self.level_monsters_killed = 0
                self.level_items_collected = 0
                self.reset_game()
                self.username = username
                self.menu_buttons[0] = Button(SCREEN_WIDTH // 2 - 300 // 2, self.menu_buttons[0].rect.y, 300, 60, "Logout", self.logout)
                self.state = GameState.SELECT_LEVEL
                if self.mutant_killed is None:
                    self.mutant_killed = 0
            cursor.close()
            conn.close()
        
    def register(self, username, password):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                self.player_health = INITIAL_HEALTH
                self.player_max_health = INITIAL_HEALTH
                self.player_attack = INITIAL_ATTACK
                self.player_defense = INITIAL_DEFENSE
                self.player_strength = INITIAL_STRENGTH
                self.player_level = INITIAL_LEVEL
                self.player_xp = INITIAL_XP
                self.mutants_killed = INITIAL_MONSTERS_KILLED
                self.demons_killed = INITIAL_MONSTERS_KILLED
                self.mutant_killed = INITIAL_MONSTERS_KILLED
                self.dragons_killed = INITIAL_MONSTERS_KILLED
                self.items_collected = INITIAL_ITEMS_COLLECTED
                self.killed_monster_ids = set()
                self.collected_item_ids = set()
                self.monster_kills = {"mutant.png": 0, "Demon.png": 0, "Dragon.png": 0}
                self.item_counts = {"Health_Box.png": 0, "attack_pot.png": 0}
                self.completed_levels = set()  # Initialize as empty set
                self.all_quests = {}
                self.completed_quests = set()

                cursor.execute("""
                    INSERT INTO players (username, password, health, attack, defense, strength, level, xp, demons_killed, mutants_killed, dragons_killed, items_collected, killed_monsters, killed_monsters_details, collected_items_details, completed_levels)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    (username, password, self.player_health, self.player_attack, self.player_defense,
                     self.player_strength, self.player_level, self.player_xp, self.demons_killed, self.mutants_killed, 
                     self.dragons_killed, self.items_collected, json.dumps([]), json.dumps(self.monster_kills), json.dumps(self.item_counts), json.dumps(list(self.completed_levels))))
                conn.commit()
                self.player_id = cursor.lastrowid
                self.username = username
                self.menu_buttons[0] = Button(SCREEN_WIDTH // 2 - 300 // 2, self.menu_buttons[0].rect.y, 300, 60, "Logout", self.logout)
                self.state = GameState.SELECT_LEVEL
                self.unlocked_levels = 1
                self.current_level = 0
                self.reset_game()
            except Error as e:
                print(f"Registration failed: {e}")
            cursor.close()
            conn.close()

    def show_achievement_popup(self, message):
        self.chat_box.add_message(message, duration=300)  # 15 seconds

    def check_level_up(self):
        required_xp = self.player_level * self.xp_per_level
        while self.player_xp >= required_xp:
            self.player_level += 1
            self.player_xp -= required_xp
            self.player_attack += 2
            self.player_defense += 1
            self.player_strength += 1
            self.player_max_health += 1
            self.player_health = self.player_max_health
            required_xp = self.player_level * self.xp_per_level
            self.chat_box.add_message(f"Level Up! Reached Level {self.player_level}", duration=300)  # 15 seconds

    def check_achievements(self):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            achievements = [
                ("Kill 10 Mutants", self.mutants_killed >= 10),
                ("Kill 20 Mutants", self.mutants_killed >= 20),
                ("Collect 30 Items", self.items_collected >= 30),
                ("Defeat Demon", self.demons_killed >= 1),
                ("Kill 2 Demons", self.demons_killed >= 2),
                ("Defeat Mutant", self.mutant_killed >= 1),
                ("Defeat a Dragon", self.dragons_killed >= 1),
            ]
            for name, condition in achievements:
                cursor.execute("SELECT id FROM achievements WHERE player_id=%s AND achievement_name=%s",
                               (self.player_id, name))
                if not cursor.fetchone() and condition:
                    cursor.execute("INSERT INTO achievements (player_id, achievement_name, completed) VALUES (%s, %s, %s)",
                                   (self.player_id, name, True))
                    self.show_achievement_popup(f"Congratulations! You have achieved {name}!")
            conn.commit()
            cursor.close()
            conn.close()
            
    def get_achievements(self):
        if not self.player_id:
            return []
        conn = connect_db()
        if not conn:
            return []
        cursor = conn.cursor()
        all_achievements = [
            ("Kill 10 Mutants", "Kill 10 mutants in total", self.mutants_killed >= 10),
            ("Kill 20 Mutants", "Kill 20 mutants in total", self.mutants_killed >= 20),
            ("Collect 30 Items", "Collect 30 items in total", self.items_collected >= 30),
            ("Reach Combat Level 3", "Reach level 3", self.player_level >= 3),
            ("Reach Combat Level 50", "Reach level 50", self.player_level >= 50),
            ("Defeat Demon", "Defeat a Demon monster", self.demons_killed >= 1),
            ("Kill 2 Demons", "Kill 2 Demon monsters", self.demons_killed >= 2),
            ("Defeat Mutant", "Defeat a mutant", self.mutant_killed >= 1),
            ("Defeat a Dragon", "Defeat a dragon", self.dragons_killed >= 1),
        ]
        cursor.execute("SELECT achievement_name FROM achievements WHERE player_id=%s", (self.player_id,))
        completed = {row[0] for row in cursor.fetchall()}
        achievements = []
        for name, description, condition in all_achievements:
            is_completed = name in completed or condition
            achievements.append({"name": name, "description": description, "completed": is_completed})
        cursor.close()
        conn.close()
        return achievements

    def get_high_scores(self):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username, current_level FROM players ORDER BY current_level DESC")
            scores = cursor.fetchall()
            cursor.close()
            conn.close()
            return scores
        return []

    def get_player_stats(self, username):
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mutants_killed, demons_killed, dragons_killed, health, attack, defense, strength, items_collected, killed_monsters_details, collected_items_details
                FROM players WHERE username=%s""", (username,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            if result:
                mutants_killed, demons_killed, dragons_killed, health, attack, defense, strength, items_collected, killed_monsters_json, collected_items_json = result
                monster_details = json.loads(killed_monsters_json) if killed_monsters_json else {"mutant.png": 0, "Demon.png": 0, "Dragon.png": 0}
                item_details = json.loads(collected_items_json) if collected_items_json else {"Health_Box.png": 0, "attack_pot.png": 0}
                return {
                    "username": username,
                    "mutants_killed": mutants_killed,
                    "demons_killed": demons_killed,
                    "dragons_killed": dragons_killed,
                    "health": health,
                    "attack": attack,
                    "defense": defense,
                    "strength": strength,
                    "items_collected": items_collected,
                    "monster_details": monster_details,
                    "item_details": item_details
                }
        return None
    
    def is_blocked(self, x, y):
        grid_x, grid_y = int(x), int(y)
        # Check if outside grid bounds
        if not (0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT):
            return True
        # Check if the texture is "boundary.jpg" or "water.jpg"
        key = f"{grid_x},{grid_y}"
        texture = self.textures.get(key, "boundary.jpg")  # Default to boundary.jpg if no texture specified
        return texture in ["boundary.jpg", "water.jpg"]

    def is_occupied(self, x, y, exclude_monster=None):
        if exclude_monster is None and abs(x - self.player_x) < 0.5 and abs(y - self.player_y) < 0.5:
            return False
        for monster in self.monsters:
            if monster != exclude_monster and abs(x - monster["x"]) < 0.5 and abs(y - monster["y"]) < 0.5:
                return True
        return False

    def attack_monster(self):
        for monster in self.monsters[:]:
            if abs(monster["x"] - self.player_x) < 0.5 and abs(monster["y"] - self.player_y) < 0.5:
                total_attack = self.player_attack + self.player_attack_bonus
                damage = max(0, total_attack * (1 + self.player_level * 0.1) - monster["defense"])
                monster["health"] -= damage
                print(f"Player attacked! Damage: {damage}, Monster HP: {monster['health']}")
                if monster["health"] <= 0:
                    monster_id = monster["id"]
                    sprite = monster.get("sprite", "mutant.png")
                    if monster_id not in self.killed_monster_ids:
                        self.killed_monster_ids.add(monster_id)
                        self.monster_kills[sprite] = self.monster_kills.get(sprite, 0) + 1
                        if sprite == "Demon.png":
                            self.demons_killed += 1
                        elif sprite == "mutant.png":
                            self.mutants_killed += 1
                            self.mutant_killed += 1
                        elif sprite == "Dragon.png":
                            self.dragons_killed += 1
                        # Drop quest items
                        for quest_id, quest in self.active_quests.items():
                            if sprite in quest["drop_sources"]:
                                item = quest["drop_sources"][sprite]
                                self.quest_items[item] = self.quest_items.get(item, 0) + 1
                                self.active_quests[quest_id]["progress"] = sum(self.quest_items.get(i, 0) for i in quest["items"])
                                self.chat_box.add_message(f"Collected {item}!", duration=300)
                    self.monsters.remove(monster)
                    self.level_monsters_killed += 1
                    self.player_xp += monster["xp"]
                    self.check_level_up()
                    for quest in self.quests:
                        if "mutants" in quest["text"].lower():
                            quest["progress"] = self.level_monsters_killed
                break

    def interact_with_npc(self):
        for key, npc in self.npcs.items():
            if abs(npc["x"] - self.player_x) < 0.5 and abs(npc["y"] - self.player_y) < 0.5:
                if "quest" in npc and npc["quest"]:
                    quest = npc["quest"]
                    quest_id = f"{self.current_level}_{key}"
                    if quest_id in self.completed_quests:
                        self.chat_box.add_message(quest["dialogue"]["complete"], duration=900)
                        return None
                    elif quest_id in self.active_quests and self.active_quests[quest_id]["progress"] >= self.active_quests[quest_id]["target"]:
                        self.chat_box.add_message(quest["dialogue"]["complete"], duration=900)
                        self.completed_quests.add(quest_id)
                        conn = connect_db()
                        if conn:
                            cursor = conn.cursor()
                            cursor.execute("""
                                INSERT INTO quests (player_id, quest_id, completed)
                                VALUES (%s, %s, %s)
                                ON DUPLICATE KEY UPDATE completed=%s
                            """, (self.player_id, quest_id, 1, 1))
                            conn.commit()
                            cursor.close()
                            conn.close()
                        del self.active_quests[quest_id]
                        for item, count in quest["required_items"].items():
                            self.quest_items[item] = max(0, self.quest_items.get(item, 0) - count)
                        self.save_progress()
                        return None
                    elif not self.all_quests[self.current_level][quest_id]["accepted"]:
                        self.chat_box.add_message(quest["dialogue"]["initial"], duration=900)
                        self.chat_box.add_message("Press Y to accept, N to decline", duration=900)
                        return {"quest_id": quest_id, "quest": quest, "npc_key": key}
                    else:
                        self.chat_box.add_message(quest["dialogue"]["in_progress"], duration=900)
                break
        return None

    def check_quests(self):
        for quest in self.quests:
            if "mutants" in quest["text"].lower():
                quest["progress"] = self.level_monsters_killed
            elif "items" in quest["text"].lower():
                quest["progress"] = self.level_items_collected

    def check_level_complete(self):
        # Check if all monsters are killed and items collected
        is_complete = len(self.monsters) == 0 and len(self.items) == 0
        # Only return True if the level hasn’t been completed yet
        return is_complete and self.current_level not in self.completed_levels

    def next_level(self):
        if self.current_level not in self.completed_levels:
            self.completed_levels.add(self.current_level)
            print(f"Level {self.current_level + 1} marked as completed.")
            
            # Show "Congratulations" message immediately
            self.chat_box.add_message(f"Congratulations! Level {self.current_level + 1} Completed!", duration=300)  # 1 second
            self.chat_box.update()  # Update timers
            screen.fill(BLACK)  # Clear screen
            self.chat_box.draw(screen)  # Draw message
            pygame.display.flip()  # Show it now
            pygame.time.wait(1000)  # Wait 1 second

            self.current_level += 1
            self.unlocked_levels = max(self.unlocked_levels, self.current_level + 1)
            self.save_progress()
            
            if self.current_level < len(self.levels):
                # Show "Loading" message immediately
                self.chat_box.add_message("Loading Next Level...", duration=300)  # 1 second
                self.chat_box.update()
                screen.fill(BLACK)
                self.chat_box.draw(screen)
                pygame.display.flip()
                pygame.time.wait(1000)  # Wait 1 second
                self.load_level()
            else:
                # Show "You Win" message immediately
                self.chat_box.add_message("You Win! All Levels Completed!", duration=300)  # 1 second
                self.chat_box.update()
                screen.fill(BLACK)
                self.chat_box.draw(screen)
                pygame.display.flip()
                pygame.time.wait(1000)  # Wait 1 second
                self.state = GameState.MENU

    def show_message(self, text, duration=1):
        screen.fill(BLACK)
        msg = TITLE_FONT.render(text, True, WHITE)
        screen.blit(msg, (SCREEN_WIDTH // 2 - msg.get_width() // 2, SCREEN_HEIGHT // 2 - msg.get_height() // 2))
        pygame.display.flip()
        time.sleep(duration)

    def select_level_action(self):
        if self.player_id:
            self.state = GameState.SELECT_LEVEL
        else:
            self.show_message("You must be logged in to select a level", 2)
            self.state = GameState.MENU

    def achievements_action(self):
        if self.player_id:
            self.state = GameState.ACHIEVEMENTS
            self.ach_sub_state = self.ACHIEVEMENTS_MAIN
        else:
            self.show_message("You must be logged in to view achievements", 2)
            self.state = GameState.MENU

    def set_level(self, level):
        print(f"Setting level to {level}")
        self.current_level = level
        self.reset_game()
        self.state = GameState.PLAYING

    def create_level_button(self, x, y, width, height, text, level_idx):
        is_completed = level_idx in self.completed_levels
        is_locked = level_idx >= self.unlocked_levels or is_completed  # Lock if beyond unlocked or completed
        if is_completed:
            text = f"Level {level_idx + 1} - Completed"
        elif is_locked:
            text = f"Level {level_idx + 1} - Locked"
        else:
            text = f"Level {level_idx + 1} - Unlocked"
        action = lambda: self.set_level(level_idx) if not is_locked else None
        return Button(x, y, width, height, text, action, is_locked, is_completed)  # Pass is_completed

    def run(self):
        running = True
        monster_attack_cooldown = 0
        clock = pygame.time.Clock()
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    if self.state == GameState.MENU:
                        for button in self.menu_buttons:
                            if button.clicked(pos) and button.action:
                                button.action()
                    elif self.state == GameState.LOGIN:
                        for box in self.login_boxes:
                            box.active = box.clicked(pos)
                        for button in self.login_buttons:
                            if button.clicked(pos) and button.action:
                                button.action()
                    elif self.state == GameState.REGISTER:
                        for box in self.register_boxes:
                            box.active = box.clicked(pos)
                        for button in self.register_buttons:
                            if button.clicked(pos) and button.action:
                                button.action()
                    elif self.state == GameState.PAUSED:
                        for button in self.pause_buttons:
                            if button.clicked(pos) and button.action:
                                button.action()
                    elif self.state == GameState.SELECT_LEVEL and self.player_id:
                        for i, button in enumerate(self.level_buttons):
                            level_idx = self.current_level_page * self.levels_per_page + i
                            if button.clicked(pos) and level_idx < self.unlocked_levels and button.action:
                                button.action()
                        if self.back_button.clicked(pos) and self.back_button.action:
                            self.back_button.action()
                        elif hasattr(self, 'arrow_left_rect') and self.arrow_left_rect.collidepoint(pos) and self.current_level_page > 0:
                            self.current_level_page -= 1
                        elif hasattr(self, 'arrow_right_rect') and self.arrow_right_rect.collidepoint(pos) and self.current_level_page < self.total_level_pages - 1:
                            self.current_level_page += 1
                    elif self.state == GameState.HIGH_SCORES:
                        back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back", 
                                            lambda: setattr(self, 'state', GameState.MENU) if self.high_score_sub_state == self.HIGH_SCORES_MAIN 
                                            else setattr(self, 'high_score_sub_state', self.HIGH_SCORES_MAIN))
                        if back_button.clicked(pos):
                            back_button.action()
                        elif hasattr(self, 'arrow_left_rect') and self.arrow_left_rect.collidepoint(pos) and self.high_score_page > 0:
                            self.high_score_page -= 1
                        elif hasattr(self, 'arrow_right_rect') and self.arrow_right_rect.collidepoint(pos) and self.high_score_page < self.total_pages - 1:
                            self.high_score_page += 1
                        elif self.high_score_sub_state == self.HIGH_SCORES_MAIN:
                            scores_per_page = 5
                            scores = self.get_high_scores()
                            start_idx = self.high_score_page * scores_per_page
                            end_idx = min(start_idx + scores_per_page, len(scores))
                            current_scores = scores[start_idx:end_idx]
                            table_width = SCREEN_WIDTH // 2
                            col_widths = [80, table_width - 180, 100]
                            row_height = 60
                            table_x = (SCREEN_WIDTH - table_width) // 2
                            table_y = SCREEN_HEIGHT // 4 + row_height
                            for i, (username, level) in enumerate(current_scores):
                                row_y = table_y + i * row_height
                                row_rect = pygame.Rect(table_x, row_y, table_width, row_height)
                                if row_rect.collidepoint(pos):
                                    self.selected_player_stats = self.get_player_stats(username)
                                    if self.selected_player_stats:
                                        self.high_score_sub_state = self.HIGH_SCORES_DETAILS
                                    break
                    elif self.state == GameState.ACHIEVEMENTS:
                        back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back", 
                                            lambda: setattr(self, 'state', GameState.MENU) if self.ach_sub_state == self.ACHIEVEMENTS_MAIN 
                                            else setattr(self, 'ach_sub_state', self.ACHIEVEMENTS_MAIN))
                        if back_button.clicked(pos):
                            back_button.action()
                        elif self.ach_sub_state == self.ACHIEVEMENTS_MAIN:
                            stats_y = SCREEN_HEIGHT // 4 + 60 * (5 + 1) + 50
                            monsters_button = Button(SCREEN_WIDTH // 2 - 320, stats_y, 300, 50, 
                                                    f"Monsters Killed: {self.mutants_killed + self.demons_killed + self.dragons_killed}", 
                                                    lambda: setattr(self, 'ach_sub_state', self.ACHIEVEMENTS_MONSTERS))
                            items_button = Button(SCREEN_WIDTH // 2 + 20, stats_y, 300, 50, 
                                                 f"Items Collected: {self.items_collected}", 
                                                 lambda: setattr(self, 'ach_sub_state', self.ACHIEVEMENTS_ITEMS))
                            if monsters_button.clicked(pos):
                                monsters_button.action()
                            elif items_button.clicked(pos):
                                items_button.action()
                            elif hasattr(self, 'arrow_left_rect') and self.arrow_left_rect.collidepoint(pos) and self.ach_page > 0:
                                self.ach_page -= 1
                            elif hasattr(self, 'arrow_right_rect') and self.arrow_right_rect.collidepoint(pos) and self.ach_page < self.total_pages - 1:
                                self.ach_page += 1
                    elif self.state == GameState.CREDITS:
                        if self.back_button.clicked(pos):
                            self.state = GameState.MENU
                    elif self.state == GameState.UPDATES:
                        if self.back_button.clicked(pos):
                            self.state = GameState.MENU
                    elif self.state == GameState.CONTROLS:
                        if self.back_button.clicked(pos):
                            self.state = GameState.MENU

                elif event.type == pygame.KEYDOWN:
                    if self.state in [GameState.LOGIN, GameState.REGISTER]:
                        active_box = next((box for box in (self.login_boxes if self.state == GameState.LOGIN else self.register_boxes) if box.active), None)
                        if active_box:
                            if event.key == pygame.K_BACKSPACE:
                                active_box.text = active_box.text[:-1]
                            elif event.key != pygame.K_RETURN:
                                active_box.text += event.unicode
                    elif self.state == GameState.PLAYING:
                        if event.key == pygame.K_p:
                            self.state = GameState.PAUSED
                            self.pause_buttons = [
                                Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4, 200, 50, "Resume", lambda: setattr(self, 'state', GameState.PLAYING)),
                                Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4 + 60, 200, 50, "Save", self.save_progress),
                                Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 4 + 120, 200, 50, "Main Menu", lambda: setattr(self, 'state', GameState.MENU)),
                            ]
                        elif event.key == pygame.K_SPACE:
                            self.attack_monster()
                        elif event.key == pygame.K_e:  # New: Interact with NPC
                            interaction = self.interact_with_npc()
                            if interaction:
                                self.pending_quest = interaction
                        elif event.key == pygame.K_y and hasattr(self, 'pending_quest'):
                            quest_id = self.pending_quest["quest_id"]
                            quest = self.pending_quest["quest"]
                            self.all_quests[self.current_level][quest_id]["accepted"] = True
                            self.active_quests[quest_id] = {
                                "progress": 0,
                                "target": sum(quest["required_items"].values()),
                                "items": quest["required_items"],
                                "drop_sources": quest["drop_sources"]
                            }
                            self.chat_box.add_message("Quest accepted!", duration=300)
                            del self.pending_quest
                        elif event.key == pygame.K_n:
                            self.chat_box.add_message("Quest declined.", duration=300)
                            del self.pending_quest
                        elif event.key == pygame.K_h:  # Use Health Box
                            if self.inventory.use_item("Health_Box.png"):
                                heal_amount = 50
                                self.player_health = min(self.player_max_health, self.player_health + heal_amount)
                                self.chat_box.add_message(f"Used Health Box! Healed {heal_amount} HP", duration=300)
                                print(f"Health Box used! Healed {heal_amount} HP, Player HP: {self.player_health}")
                            else:
                                self.chat_box.add_message("No Health Box in inventory!", duration=300)
                        elif event.key == pygame.K_r:  # Use Attack Potion
                            if self.inventory.use_item("attack_pot.png"):
                                self.player_attack_bonus = 5
                                self.attack_bonus_timer = 60 * 60  # 1 minute at 60 FPS
                                self.chat_box.add_message("Used Attack Potion! +5 Attack for 1 minute", duration=300)
                                print("Attack Potion used! +5 Attack for 1 minute")
                            else:
                                self.chat_box.add_message("No Attack Potion in inventory!", duration=300)

            self.chat_box.update()

            # Update buttons
            for button_group in [self.menu_buttons, self.login_buttons, self.register_buttons, getattr(self, 'pause_buttons', []), [self.back_button]]:
                for button in button_group:
                    button.update(mouse_pos)

            # Drawing (all your drawing code remains unchanged, just removing the pygame.quit() from here)
            if self.state == GameState.MENU:
                if MENU_BACKGROUND:
                    screen.blit(MENU_BACKGROUND, (0, 0))
                else:
                    screen.fill(BLACK)
                title = TITLE_FONT.render("CraftSaga", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 8))
                for button in self.menu_buttons:
                    button.draw(screen)
                if self.username:
                    username_text = SMALL_FONT.render(f"Logged in as: {self.username}", True, WHITE)
                    pygame.draw.rect(screen, BLACK, (10, 10, username_text.get_width() + 20, username_text.get_height() + 10), border_radius=5)
                    screen.blit(username_text, (20, 15))

            elif self.state == GameState.LOGIN:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Login", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 6))
                for box in self.login_boxes:
                    box.draw(screen)
                screen.blit(SMALL_FONT.render("Username", True, WHITE), (self.login_boxes[0].rect.x - 100, self.login_boxes[0].rect.y + 5))
                screen.blit(SMALL_FONT.render("Password", True, WHITE), (self.login_boxes[1].rect.x - 100, self.login_boxes[1].rect.y + 5))
                for button in self.login_buttons:
                    button.draw(screen)

            elif self.state == GameState.REGISTER:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Register", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 6))
                for box in self.register_boxes:
                    box.draw(screen)
                screen.blit(SMALL_FONT.render("Username", True, WHITE), (self.register_boxes[0].rect.x - 100, self.register_boxes[0].rect.y + 5))
                screen.blit(SMALL_FONT.render("Password", True, WHITE), (self.register_boxes[1].rect.x - 100, self.register_boxes[1].rect.y + 5))
                for button in self.register_buttons:
                    button.draw(screen)
                    
            elif self.state == GameState.PLAYING:
                # Clear the screen
                screen.fill(BLACK)

                # Handle player movement
                keys = pygame.key.get_pressed()
                new_x, new_y = self.player_x, self.player_y
                if keys[pygame.K_w]:
                    new_y -= player_speed
                if keys[pygame.K_s]:
                    new_y += player_speed
                if keys[pygame.K_a]:
                    new_x -= player_speed
                if keys[pygame.K_d]:
                    new_x += player_speed
                if not self.is_blocked(new_x, new_y) and not self.is_occupied(new_x, new_y):
                    self.player_x, self.player_y = new_x, new_y

                # Update monsters and handle their attacks
                monster_attack_cooldown = max(0, monster_attack_cooldown - 1)
                for monster in self.monsters:
                    dx = self.player_x - monster["x"]
                    dy = self.player_y - monster["y"]
                    distance = ((dx ** 2) + (dy ** 2)) ** 0.5  # Euclidean distance
                    if distance <= 2.0 and not monster["aggroed"]:
                        monster["aggroed"] = True  # Activate pursuit
                        print(f"Monster at ({monster['x']}, {monster['y']}) aggroed!")
                    if monster["aggroed"]:  # Chase indefinitely once aggroed
                        new_mx = monster["x"] + monster_speed * (dx / abs(dx)) if abs(dx) > 0.5 else monster["x"]
                        new_my = monster["y"] + monster_speed * (dy / abs(dy)) if abs(dy) > 0.5 else monster["y"]
                        if not self.is_blocked(new_mx, new_my) and not self.is_occupied(new_mx, new_my, exclude_monster=monster):
                            monster["x"], monster["y"] = new_mx, new_my
                    if abs(monster["x"] - self.player_x) <= 0.5 and abs(monster["y"] - self.player_y) <= 0.5:
                        if monster_attack_cooldown == 0:
                            damage = max(0, monster["attack"] - self.player_defense)
                            print(f"Monster attack: {monster['attack']}, Player defense: {self.player_defense}, Calculated damage: {damage}")
                            self.player_health -= damage
                            print(f"Monster attacked! Damage: {damage}, Player HP: {self.player_health}")
                            monster_attack_cooldown = 30
                        else:
                            print(f"Monster attack on cooldown: {monster_attack_cooldown}")

                # Update attack bonus timer
                if self.attack_bonus_timer > 0:
                    self.attack_bonus_timer -= 1
                    if self.attack_bonus_timer <= 0:
                        self.player_attack_bonus = 0
                        print("Attack boost expired!")

                # Handle item collection
                for item in self.items[:]:
                    if abs(item[0] - self.player_x) < 0.5 and abs(item[1] - self.player_y) < 0.5:
                        self.items.remove(item)
                        key = f"{int(item[0] - 0.5)},{int(item[1] - 0.5)}"
                        if key not in self.collected_item_ids:
                            self.collected_item_ids.add(key)
                            self.items_collected += 1
                            self.item_counts[item[2]] = self.item_counts.get(item[2], 0) + 1
                            print(f"Collected new item at {key}, Total: {self.items_collected}")
                            if self.inventory.add_item(item[2]):  # Add to inventory
                                item_name = "Health Box" if item[2] == "Health_Box.png" else "Attack Potion"
                                self.chat_box.add_message(f"{item_name} added to inventory!", duration=300)
                            else:
                                self.chat_box.add_message("Inventory full!", duration=300)
                        if key in self.items_dict:
                            del self.items_dict[key]
                        self.level_items_collected += 1
                        self.check_quests()  # Update quest progress
                        if item[2] == "Health_Box.png":
                            heal_amount = 50
                            self.player_health = min(self.player_max_health, self.player_health + heal_amount)
                            self.chat_box.add_message(f"Health Box Collected! Healed {heal_amount} HP", duration=300)
                            print(f"Health Box Collected! Healed {heal_amount} HP, Player HP: {self.player_health}")
                        elif item[2] == "attack_pot.png":
                            self.player_attack_bonus = 5
                            self.attack_bonus_timer = 60 * 60  # 1 minute at 60 FPS
                            self.chat_box.add_message("Attack Potion Collected! +5 Attack for 1 minute", duration=300)
                            print("Attack Potion Collected! +5 Attack for 1 minute")

                # Check for game over
                if self.player_health <= 0:
                    self.player_health = 100
                    conn = connect_db()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE players SET health=%s WHERE id=%s", (self.player_health, self.player_id))
                        conn.commit()
                        cursor.close()
                        conn.close()
                        print("Player health reset to 100 in database!")
                    self.save_progress()
                    self.chat_box.add_message("Game Over! Health restored to 100.")
                    self.show_message("Game Over")
                    self.state = GameState.GAME_OVER
                    return  # Exit early to avoid drawing this frame

                # Update game state
                self.check_quests()
                self.check_achievements()
                if self.check_level_complete():
                    self.next_level()

                # Draw the grid
                for y in range(GRID_HEIGHT):
                    for x in range(GRID_WIDTH):
                        rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        key = f"{x},{y}"
                        texture = self.textures.get(key, "boundary.jpg")
                        try:
                            screen.blit(TEXTURES.get(texture, FALLBACK_TEXTURE), rect)
                        except Exception as e:
                            print(f"Error rendering tile at ({x}, {y}): {e}")
                            pygame.draw.rect(screen, GREEN, rect)

                # Draw monsters with health bars
                for monster in self.monsters:
                    sprite = monster.get("sprite", "mutant.png")
                    mx, my = int(monster["x"] * TILE_SIZE - TILE_SIZE / 2), int(monster["y"] * TILE_SIZE - TILE_SIZE / 2)
                    try:
                        screen.blit(MONSTER_SPRITES.get(sprite, MONSTER_SPRITES.get("mutant.png")), (mx, my))
                    except (NameError, KeyError):
                        pygame.draw.rect(screen, BLUE, (mx, my, TILE_SIZE, TILE_SIZE))

                    # Monster health bar
                    health_bar_width, health_bar_height = TILE_SIZE, TILE_SIZE // 8
                    health_bar_x, health_bar_y = mx, my - TILE_SIZE // 2
                    max_health = monster.get("max_health", monster["health"])
                    health_fill_width = int(health_bar_width * max(0, monster["health"] / max_health))
                    pygame.draw.rect(screen, BLACK, (health_bar_x - 2, health_bar_y - 2, health_bar_width + 4, health_bar_height + 4))
                    pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
                    pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_fill_width, health_bar_height))

                    # Monster name
                    monster_name = sprite.split(".")[0].capitalize()
                    name_text = SMALL_FONT.render(monster_name, True, WHITE)
                    name_rect = name_text.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y - TILE_SIZE // 1.5))
                    pygame.draw.rect(screen, BLACK, name_rect.inflate(10, 10))
                    pygame.draw.rect(screen, GRAY, name_rect.inflate(10, 10), 2)
                    screen.blit(name_text, name_rect)

                # Draw items
                for ix, iy, item_type in self.items:
                    item_x, item_y = int(ix * TILE_SIZE - TILE_SIZE / 2), int(iy * TILE_SIZE - TILE_SIZE / 2)
                    item_rect = pygame.Rect(item_x - 5, item_y - 5, TILE_SIZE + 10, TILE_SIZE + 10)
                    pygame.draw.rect(screen, BLACK, item_rect)
                    pygame.draw.rect(screen, GRAY, item_rect, 2)
                    try:
                        screen.blit(ITEMS.get(item_type), (item_x, item_y))
                    except (NameError, KeyError):
                        pygame.draw.rect(screen, YELLOW, (item_x, item_y, TILE_SIZE, TILE_SIZE))
                    item_name = "Health Box" if item_type == "Health_Box.png" else "Attack Potion"
                    name_text = SMALL_FONT.render(item_name, True, WHITE)
                    name_rect = name_text.get_rect(center=(item_x + TILE_SIZE // 2, item_y - TILE_SIZE // 3))
                    pygame.draw.rect(screen, BLACK, name_rect.inflate(10, 10))
                    pygame.draw.rect(screen, GRAY, name_rect.inflate(10, 10), 2)
                    screen.blit(name_text, name_rect)

                # Draw NPCs
                for key, npc in self.npcs.items():
                    sprite = npc.get("sprite", "roger.png")
                    npc_x, npc_y = int(npc["x"] * TILE_SIZE - TILE_SIZE / 2), int(npc["y"] * TILE_SIZE - TILE_SIZE / 2)
                    try:
                        screen.blit(NPC_SPRITES.get(sprite, FALLBACK_TEXTURE), (npc_x, npc_y))
                    except (NameError, KeyError) as e:
                        print(f"Error rendering NPC at {key}: {e}")
                        pygame.draw.rect(screen, YELLOW, (npc_x, npc_y, TILE_SIZE, TILE_SIZE))
                    npc_name = sprite.split(".")[0].capitalize()
                    name_text = SMALL_FONT.render(npc_name, True, WHITE)
                    name_rect = name_text.get_rect(center=(npc_x + TILE_SIZE // 2, npc_y - TILE_SIZE // 3))
                    pygame.draw.rect(screen, BLACK, name_rect.inflate(10, 10))
                    pygame.draw.rect(screen, GRAY, name_rect.inflate(10, 10), 2)
                    screen.blit(name_text, name_rect)

                # Draw player with health bar
                px, py = int(self.player_x * TILE_SIZE - TILE_SIZE / 2), int(self.player_y * TILE_SIZE - TILE_SIZE / 2)
                try:
                    screen.blit(PLAYER_SPRITE, (px, py))
                except NameError:
                    pygame.draw.rect(screen, RED, (px, py, TILE_SIZE, TILE_SIZE))
                health_bar_width, health_bar_height = TILE_SIZE, TILE_SIZE // 8
                health_bar_x, health_bar_y = px, py - TILE_SIZE // 2
                health_fill_width = int(health_bar_width * max(0, self.player_health / self.player_max_health))
                pygame.draw.rect(screen, BLACK, (health_bar_x - 2, health_bar_y - 2, health_bar_width + 4, health_bar_height + 4))
                pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
                pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_fill_width, health_bar_height))

                # Draw player username
                if self.username:
                    username_text = SMALL_FONT.render(self.username, True, WHITE)
                    username_rect = username_text.get_rect(center=(health_bar_x + health_bar_width // 2, health_bar_y - TILE_SIZE // 1.5))
                    pygame.draw.rect(screen, BLACK, username_rect.inflate(10, 10))
                    pygame.draw.rect(screen, GRAY, username_rect.inflate(10, 10), 2)
                    screen.blit(username_text, username_rect)

                # Draw objectives
                objectives_width, objectives_height = 400, 150
                objectives_x, objectives_y = SCREEN_WIDTH - objectives_width - 10, 10
                pygame.draw.rect(screen, BLACK, (objectives_x, objectives_y, objectives_width, objectives_height), border_radius=5)
                pygame.draw.rect(screen, GRAY, (objectives_x, objectives_y, objectives_width, objectives_height), 2, border_radius=5)
                title_text = BUTTON_FONT.render("Objectives", True, WHITE)
                screen.blit(title_text, (objectives_x + (objectives_width - title_text.get_width()) // 2, objectives_y + 10))
                y_offset = objectives_y + title_text.get_height() + 20
                for quest in self.quests:
                    progress, target = quest["progress"], quest["target"]
                    text = f"{quest['text']} ({progress}/{target})"
                    color = GREEN if progress >= target else RED
                    quest_text = SMALL_FONT.render(text, True, color)
                    screen.blit(quest_text, (objectives_x + 15, y_offset))
                    y_offset += quest_text.get_height() + 10

                # Draw player stats
                    # Draw player stats
                attack_display = f"{self.player_attack}"
                if self.player_attack_bonus > 0:
                    attack_display += f" (+{self.player_attack_bonus})"
                stats = f"Health: {self.player_health}/{self.player_max_health}  Attack: {attack_display}  Defense: {self.player_defense}  Strength: {self.player_strength}  Level: {self.player_level}  XP: {self.player_xp}/{self.player_level * self.xp_per_level}"
                stats_text = SMALL_FONT.render(stats, True, WHITE)
                stats_rect = stats_text.get_rect()  # Get default rect first
                stats_rect.bottomleft = (10, SCREEN_HEIGHT - 10)  # Set bottomleft directly
                pygame.draw.rect(screen, BLACK, stats_rect.inflate(10, 10))
                pygame.draw.rect(screen, GRAY, stats_rect.inflate(10, 10), 2)
                screen.blit(stats_text, stats_rect)

                # Draw chat box
                self.chat_box.draw(screen)
                self.quest_box.draw(screen, self.all_quests, self.active_quests, self.completed_quests, self.quest_items, self.current_level)
                self.inventory.draw(screen)  # Draw inventory below quest box

                #if self.achievement_message and self.achievement_timer > 0:
                    #popup_text = TITLE_FONT.render(self.achievement_message, True, WHITE)
                    #popup_rect = popup_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    #pygame.draw.rect(screen, BLACK, (popup_rect.x - 10, popup_rect.y - 10, popup_rect.width + 20, popup_rect.height + 20))
                    #pygame.draw.rect(screen, GRAY, (popup_rect.x - 10, popup_rect.y - 10, popup_rect.width + 20, popup_rect.height + 20), 2)
                    #screen.blit(popup_text, popup_rect)
                    #self.achievement_timer -= 1
                    #if self.achievement_timer <= 0:
                        #self.achievement_message = None

            elif self.state == GameState.PAUSED:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Paused", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 6))
                for button in self.pause_buttons:
                    button.draw(screen)

            elif self.state == GameState.GAME_OVER:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Game Over", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2))
                pygame.display.flip()
                time.sleep(2)
                self.state = GameState.MENU

            elif self.state == GameState.HIGH_SCORES:
                screen.fill(BLACK)
                title = TITLE_FONT.render("High Scores", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 8))

                back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back", 
                                    lambda: setattr(self, 'state', GameState.MENU) if self.high_score_sub_state == self.HIGH_SCORES_MAIN 
                                    else setattr(self, 'high_score_sub_state', self.HIGH_SCORES_MAIN))
                back_button.update(mouse_pos)
                back_button.draw(screen)

                if self.high_score_sub_state == self.HIGH_SCORES_MAIN:
                    scores_per_page = 5
                    if not hasattr(self, 'high_score_page'):
                        self.high_score_page = 0
                    scores = self.get_high_scores()
                    self.total_pages = (len(scores) + scores_per_page - 1) // scores_per_page
                    start_idx = self.high_score_page * scores_per_page
                    end_idx = min(start_idx + scores_per_page, len(scores))
                    current_scores = scores[start_idx:end_idx]

                    table_width = SCREEN_WIDTH // 2
                    col_widths = [80, table_width - 180, 100]
                    row_height = 60
                    table_x = (SCREEN_WIDTH - table_width) // 2
                    table_y = SCREEN_HEIGHT // 4
                    headers = ["Rank", "Username", "Level"]
                    for col, (header, width) in enumerate(zip(headers, col_widths)):
                        pygame.draw.rect(screen, DARK_GRAY, (table_x + sum(col_widths[:col]), table_y - 5, width, row_height + 10), border_radius=5)
                        pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), table_y, width, row_height), border_radius=5)
                        screen.blit(SMALL_FONT.render(header, True, WHITE), (table_x + sum(col_widths[:col]) + width // 2 - SMALL_FONT.render(header, True, WHITE).get_width() // 2, table_y + 10))
                    for i, (username, level) in enumerate(current_scores):
                        rank = start_idx + i + 1
                        color = GOLD if rank == 1 else SILVER if rank == 2 else BRONZE if rank == 3 else WHITE
                        row_y = table_y + (i + 1) * row_height
                        for col, (text, width) in enumerate([(str(rank), col_widths[0]), (username, col_widths[1]), (str(level), col_widths[2])]):
                            pygame.draw.rect(screen, STEEL, (table_x + sum(col_widths[:col]), row_y, width, row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), row_y, width, row_height), 2, border_radius=5)
                            text_surface = SMALL_FONT.render(text, True, color)
                            screen.blit(text_surface, (table_x + sum(col_widths[:col]) + width // 2 - text_surface.get_width() // 2, row_y + 10))

                    total_table_height = row_height * (scores_per_page + 1)
                    arrow_left_pos = (table_x - 50, table_y + total_table_height // 2)
                    arrow_right_pos = (table_x + table_width + 10, table_y + total_table_height // 2)
                    if "left_arrow.png" in ARROW_SPRITES:
                        arrow_left = ARROW_SPRITES["left_arrow.png"] if self.high_score_page > 0 else pygame.transform.grayscale(ARROW_SPRITES["left_arrow.png"])
                        arrow_right = ARROW_SPRITES["right_arrow.png"] if self.high_score_page < self.total_pages - 1 else pygame.transform.grayscale(ARROW_SPRITES["right_arrow.png"])
                        screen.blit(arrow_left, arrow_left_pos)
                        screen.blit(arrow_right, arrow_right_pos)
                        self.arrow_left_rect = arrow_left.get_rect(topleft=arrow_left_pos)
                        self.arrow_right_rect = arrow_right.get_rect(topleft=arrow_right_pos)
                    else:
                        arrow_left = SMALL_FONT.render("<", True, WHITE if self.high_score_page > 0 else GRAY)
                        arrow_right = SMALL_FONT.render(">", True, WHITE if self.high_score_page < self.total_pages - 1 else GRAY)
                        screen.blit(arrow_left, arrow_left_pos)
                        screen.blit(arrow_right, arrow_right_pos)
                        self.arrow_left_rect = arrow_left.get_rect(topleft=arrow_left_pos)
                        self.arrow_right_rect = arrow_right.get_rect(topleft=arrow_right_pos)

                    page_text = SMALL_FONT.render(f"Page {self.high_score_page + 1}/{self.total_pages}", True, WHITE)
                    screen.blit(page_text, (SCREEN_WIDTH // 2 - page_text.get_width() // 2, table_y + total_table_height + 10))

                elif self.high_score_sub_state == self.HIGH_SCORES_DETAILS and self.selected_player_stats:
                    stats = self.selected_player_stats
                    title = TITLE_FONT.render(f"{stats['username']}'s Stats", True, WHITE)
                    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 5))

                    stat_list = [
                        ("Mutants Killed", str(stats["mutants_killed"])),
                        ("Demons Killed", str(stats["demons_killed"])),
                        ("Dragons Killed", str(stats["dragons_killed"])),
                        ("Health", str(stats["health"])),
                        ("Attack", str(stats["attack"])),
                        ("Strength", str(stats["strength"])),
                        ("Defense", str(stats["defense"])),
                        ("Items Collected", str(stats["items_collected"])),
                        ("Health Boxes", str(stats["item_details"].get("Health_Box.png", 0))),
                        ("Attack Potions", str(stats["item_details"].get("attack_pot.png", 0)))
                    ]

                    base_widths = [200, 150]
                    padding = 20
                    col_widths = base_widths[:]
                    for name, value in stat_list:
                        col_widths[0] = max(col_widths[0], SMALL_FONT.render(name, True, WHITE).get_width() + padding)
                        col_widths[1] = max(col_widths[1], SMALL_FONT.render(value, True, WHITE).get_width() + padding)
                    table_width = sum(col_widths)
                    row_height = 40
                    table_x = (SCREEN_WIDTH - table_width) // 2
                    table_height = row_height * (len(stat_list) + 1)
                    table_y = (SCREEN_HEIGHT - table_height) // 2

                    headers = ["Stat", "Value"]
                    for col, (header, width) in enumerate(zip(headers, col_widths)):
                        pygame.draw.rect(screen, DARK_GRAY, (table_x + sum(col_widths[:col]), table_y - 5, width, row_height + 10), border_radius=5)
                        pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), table_y, width, row_height), border_radius=5)
                        header_text = SMALL_FONT.render(header, True, WHITE)
                        screen.blit(header_text, (table_x + sum(col_widths[:col]) + width // 2 - header_text.get_width() // 2, table_y + 10))

                    for i, (name, value) in enumerate(stat_list):
                        row_y = table_y + (i + 1) * row_height
                        for col, (text, width) in enumerate([(name, col_widths[0]), (value, col_widths[1])]):
                            pygame.draw.rect(screen, STEEL, (table_x + sum(col_widths[:col]), row_y, width, row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), row_y, width, row_height), 2, border_radius=5)
                            text_surface = SMALL_FONT.render(text, True, WHITE)
                            screen.blit(text_surface, (table_x + sum(col_widths[:col]) + width // 2 - text_surface.get_width() // 2, row_y + 10))

            elif self.state == GameState.ACHIEVEMENTS:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Achievements", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 8))

                back_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 100, 200, 50, "Back", 
                                    lambda: setattr(self, 'state', GameState.MENU) if self.ach_sub_state == self.ACHIEVEMENTS_MAIN 
                                    else setattr(self, 'ach_sub_state', self.ACHIEVEMENTS_MAIN))
                back_button.update(mouse_pos)
                back_button.draw(screen)

                if self.ach_sub_state == self.ACHIEVEMENTS_MAIN:
                    ach_per_page = 5
                    if not hasattr(self, 'ach_page'):
                        self.ach_page = 0
                    achievements = self.get_achievements()
                    self.total_pages = (len(achievements) + ach_per_page - 1) // ach_per_page
                    start_idx = self.ach_page * ach_per_page
                    end_idx = min(start_idx + ach_per_page, len(achievements))
                    current_ach = achievements[start_idx:end_idx]

                    base_widths = [TILE_SIZE + 70, 350, 100]
                    padding = 10
                    col_widths = base_widths[:]
                    for ach in current_ach:
                        col_widths[0] = max(col_widths[0], SMALL_FONT.render(ach["name"], True, WHITE).get_width() + padding)
                        col_widths[1] = max(col_widths[1], SMALL_FONT.render(ach["description"], True, WHITE).get_width() + padding)
                        col_widths[2] = max(col_widths[2], SMALL_FONT.render("Unlocked", True, WHITE).get_width() + padding)
                    table_width = sum(col_widths)
                    row_height = 60
                    table_x = (SCREEN_WIDTH - table_width) // 2
                    table_y = SCREEN_HEIGHT // 4
                    headers = ["Achievement", "Description", "Status"]
                    for col, (header, width) in enumerate(zip(headers, col_widths)):
                        pygame.draw.rect(screen, DARK_GRAY, (table_x + sum(col_widths[:col]), table_y - 5, width, row_height + 10), border_radius=5)
                        pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), table_y, width, row_height), border_radius=5)
                        header_text = SMALL_FONT.render(header, True, WHITE)
                        screen.blit(header_text, (table_x + sum(col_widths[:col]) + width // 2 - header_text.get_width() // 2, table_y + 10))
                    for i, ach in enumerate(current_ach):
                        row_y = table_y + (i + 1) * row_height
                        status = "Unlocked" if ach["completed"] else "Locked"
                        color = GREEN if ach["completed"] else RED
                        for col, (text, width) in enumerate([(ach["name"], col_widths[0]), (ach["description"], col_widths[1]), (status, col_widths[2])]):
                            pygame.draw.rect(screen, STEEL, (table_x + sum(col_widths[:col]), row_y, width, row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), row_y, width, row_height), 2, border_radius=5)
                            text_surface = SMALL_FONT.render(text, True, color)
                            screen.blit(text_surface, (table_x + sum(col_widths[:col]) + width // 2 - text_surface.get_width() // 2, row_y + 10))

                    total_table_height = row_height * (ach_per_page + 1)
                    arrow_left_pos = (table_x - 50, table_y + total_table_height // 2)
                    arrow_right_pos = (table_x + table_width + 10, table_y + total_table_height // 2)
                    if "left_arrow.png" in ARROW_SPRITES:
                        arrow_left = ARROW_SPRITES["left_arrow.png"] if self.ach_page > 0 else pygame.transform.grayscale(ARROW_SPRITES["left_arrow.png"])
                        arrow_right = ARROW_SPRITES["right_arrow.png"] if self.ach_page < self.total_pages - 1 else pygame.transform.grayscale(ARROW_SPRITES["right_arrow.png"])
                        screen.blit(arrow_left, arrow_left_pos)
                        screen.blit(arrow_right, arrow_right_pos)
                        self.arrow_left_rect = arrow_left.get_rect(topleft=arrow_left_pos)
                        self.arrow_right_rect = arrow_right.get_rect(topleft=arrow_right_pos)
                    else:
                        arrow_left = SMALL_FONT.render("<", True, WHITE if self.ach_page > 0 else GRAY)
                        arrow_right = SMALL_FONT.render(">", True, WHITE if self.ach_page < self.total_pages - 1 else GRAY)
                        screen.blit(arrow_left, arrow_left_pos)
                        screen.blit(arrow_right, arrow_right_pos)
                        self.arrow_left_rect = arrow_left.get_rect(topleft=arrow_left_pos)
                        self.arrow_right_rect = arrow_right.get_rect(topleft=arrow_right_pos)

                    page_text = SMALL_FONT.render(f"Page {self.ach_page + 1}/{self.total_pages}", True, WHITE)
                    screen.blit(page_text, (SCREEN_WIDTH // 2 - page_text.get_width() // 2, table_y + total_table_height + 10))

                    stats_y = table_y + row_height * (ach_per_page + 1) + 50
                    button_width, button_height = 300, 50
                    monsters_button = Button(SCREEN_WIDTH // 2 - button_width - 20, stats_y, button_width, button_height, 
                                            f"Monsters Killed: {self.mutants_killed + self.demons_killed + self.dragons_killed}", 
                                            lambda: setattr(self, 'ach_sub_state', self.ACHIEVEMENTS_MONSTERS))
                    items_button = Button(SCREEN_WIDTH // 2 + 20, stats_y, button_width, button_height, 
                                         f"Items Collected: {self.items_collected}", 
                                         lambda: setattr(self, 'ach_sub_state', self.ACHIEVEMENTS_ITEMS))
                    monsters_button.update(mouse_pos)
                    items_button.update(mouse_pos)
                    monsters_button.draw(screen)
                    items_button.draw(screen)

                elif self.ach_sub_state == self.ACHIEVEMENTS_MONSTERS:
                    monster_list = list(self.monster_kills.items())
                    if not monster_list:
                        no_data_text = SMALL_FONT.render("No monsters killed yet.", True, WHITE)
                        screen.blit(no_data_text, (SCREEN_WIDTH // 2 - no_data_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    else:
                        base_widths = [TILE_SIZE + 70, 350, 100]
                        padding = 10
                        col_widths = base_widths[:]
                        for sprite, count in monster_list:
                            name = sprite.split(".")[0].capitalize()
                            col_widths[1] = max(col_widths[1], SMALL_FONT.render(name, True, WHITE).get_width() + padding)
                            col_widths[2] = max(col_widths[2], SMALL_FONT.render(str(count), True, WHITE).get_width() + padding)
                        table_width = sum(col_widths)
                        row_height = TILE_SIZE + 20
                        table_x = (SCREEN_WIDTH - table_width) // 2
                        table_height = row_height * (len(monster_list) + 1)
                        table_y = (SCREEN_HEIGHT - table_height) // 2

                        headers = ["Monster", "Name", "Qty"]
                        for col, (header, width) in enumerate(zip(headers, col_widths)):
                            pygame.draw.rect(screen, DARK_GRAY, (table_x + sum(col_widths[:col]), table_y - 5, width, row_height + 10), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), table_y, width, row_height), border_radius=5)
                            header_text = SMALL_FONT.render(header, True, WHITE)
                            screen.blit(header_text, (table_x + sum(col_widths[:col]) + width // 2 - header_text.get_width() // 2, table_y + 10))

                        for i, (sprite, count) in enumerate(monster_list):
                            row_y = table_y + (i + 1) * row_height
                            name = sprite.split(".")[0].capitalize()
                            pygame.draw.rect(screen, STEEL, (table_x, row_y, col_widths[0], row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x, row_y, col_widths[0], row_height), 2, border_radius=5)
                            screen.blit(MONSTER_SPRITES.get(sprite, FALLBACK_TEXTURE), (table_x + 10, row_y + 10))
                            pygame.draw.rect(screen, STEEL, (table_x + col_widths[0], row_y, col_widths[1], row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + col_widths[0], row_y, col_widths[1], row_height), 2, border_radius=5)
                            name_text = SMALL_FONT.render(name, True, WHITE)
                            screen.blit(name_text, (table_x + col_widths[0] + col_widths[1] // 2 - name_text.get_width() // 2, row_y + row_height // 2 - name_text.get_height() // 2))
                            pygame.draw.rect(screen, STEEL, (table_x + col_widths[0] + col_widths[1], row_y, col_widths[2], row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + col_widths[0] + col_widths[1], row_y, col_widths[2], row_height), 2, border_radius=5)
                            count_text = SMALL_FONT.render(str(count), True, WHITE)
                            screen.blit(count_text, (table_x + col_widths[0] + col_widths[1] + col_widths[2] // 2 - count_text.get_width() // 2, row_y + row_height // 2 - count_text.get_height() // 2))

                elif self.ach_sub_state == self.ACHIEVEMENTS_ITEMS:
                    item_list = list(self.item_counts.items())
                    if not item_list:
                        no_data_text = SMALL_FONT.render("No items collected yet.", True, WHITE)
                        screen.blit(no_data_text, (SCREEN_WIDTH // 2 - no_data_text.get_width() // 2, SCREEN_HEIGHT // 2))
                    else:
                        base_widths = [TILE_SIZE + 70, 350, 100]
                        padding = 10
                        col_widths = base_widths[:]
                        for sprite, count in item_list:
                            name = "Health Box" if sprite == "Health_Box.png" else "Attack Potion"
                            col_widths[1] = max(col_widths[1], SMALL_FONT.render(name, True, WHITE).get_width() + padding)
                            col_widths[2] = max(col_widths[2], SMALL_FONT.render(str(count), True, WHITE).get_width() + padding)
                        table_width = sum(col_widths)
                        row_height = TILE_SIZE + 20
                        table_x = (SCREEN_WIDTH - table_width) // 2
                        table_height = row_height * (len(item_list) + 1)
                        table_y = (SCREEN_HEIGHT - table_height) // 2

                        headers = ["Item", "Name", "Qty"]
                        for col, (header, width) in enumerate(zip(headers, col_widths)):
                            pygame.draw.rect(screen, DARK_GRAY, (table_x + sum(col_widths[:col]), table_y - 5, width, row_height + 10), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + sum(col_widths[:col]), table_y, width, row_height), border_radius=5)
                            header_text = SMALL_FONT.render(header, True, WHITE)
                            screen.blit(header_text, (table_x + sum(col_widths[:col]) + width // 2 - header_text.get_width() // 2, table_y + 10))

                        for i, (sprite, count) in enumerate(item_list):
                            row_y = table_y + (i + 1) * row_height
                            name = "Health Box" if sprite == "Health_Box.png" else "Attack Potion"
                            pygame.draw.rect(screen, STEEL, (table_x, row_y, col_widths[0], row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x, row_y, col_widths[0], row_height), 2, border_radius=5)
                            screen.blit(ITEMS.get(sprite, FALLBACK_TEXTURE), (table_x + 10, row_y + 10))
                            pygame.draw.rect(screen, STEEL, (table_x + col_widths[0], row_y, col_widths[1], row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + col_widths[0], row_y, col_widths[1], row_height), 2, border_radius=5)
                            name_text = SMALL_FONT.render(name, True, WHITE)
                            screen.blit(name_text, (table_x + col_widths[0] + col_widths[1] // 2 - name_text.get_width() // 2, row_y + row_height // 2 - name_text.get_height() // 2))
                            pygame.draw.rect(screen, STEEL, (table_x + col_widths[0] + col_widths[1], row_y, col_widths[2], row_height), border_radius=5)
                            pygame.draw.rect(screen, GRAY, (table_x + col_widths[0] + col_widths[1], row_y, col_widths[2], row_height), 2, border_radius=5)
                            count_text = SMALL_FONT.render(str(count), True, WHITE)
                            screen.blit(count_text, (table_x + col_widths[0] + col_widths[1] + col_widths[2] // 2 - count_text.get_width() // 2, row_y + row_height // 2 - count_text.get_height() // 2))

            elif self.state == GameState.CREDITS:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Credits", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 8))
                credits_text = [
                    "Game Design: Dom",
                    "Programming: Dom"
                ]
                for i, line in enumerate(credits_text):
                    text = SMALL_FONT.render(line, True, WHITE)
                    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4 + i * 40))
                self.back_button.draw(screen)

            elif self.state == GameState.UPDATES:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Updates", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 8))
                updates_text = [
                    "Version 1.0: Initial Release",
                    "Version 1.1: Added Achievements",
                    "Version 1.2: Fixed Item Collection Bug",
                    "Version 1.3: Added Inventory System",
                    "Version 1.4: Added Quest System"
                ]
                for i, line in enumerate(updates_text):
                    text = SMALL_FONT.render(line, True, WHITE)
                    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4 + i * 40))
                self.back_button.draw(screen)

            elif self.state == GameState.CONTROLS:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Controls", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 8))
                controls_text = [
                    "WASD: Move Player",
                    "Space: Attack",
                    "P: Pause",
                    "E: To start quest with roger Y/N",
                    "H: Heal when collected health potion",
                    "R: Increase strengh + 5 with strengh pot"
                ]
                for i, line in enumerate(controls_text):
                    text = SMALL_FONT.render(line, True, WHITE)
                    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 4 + i * 40))
                self.back_button.draw(screen)

            elif self.state == GameState.SELECT_LEVEL and self.player_id:
                screen.fill(BLACK)
                title = TITLE_FONT.render("Select Level", True, WHITE)
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 8))

                button_width, button_height = 300, 50
                button_spacing = 20
                total_height = self.levels_per_page * (button_height + button_spacing) - button_spacing
                start_y = (SCREEN_HEIGHT - total_height) // 2

                self.total_level_pages = (len(self.levels) + self.levels_per_page - 1) // self.levels_per_page
                start_idx = self.current_level_page * self.levels_per_page
                end_idx = min(start_idx + self.levels_per_page, len(self.levels))
                self.level_buttons = []

                for i, level_idx in enumerate(range(start_idx, end_idx)):
                    self.level_buttons.append(self.create_level_button(
                        SCREEN_WIDTH // 2 - button_width // 2,
                        start_y + i * (button_height + button_spacing),
                        button_width, button_height, "", level_idx
                    ))

                for button in self.level_buttons:
                    button.update(mouse_pos)
                    button.draw(screen)

                arrow_left_pos = (SCREEN_WIDTH // 2 - button_width // 2 - 50, start_y + total_height // 2)
                arrow_right_pos = (SCREEN_WIDTH // 2 + button_width // 2 + 10, start_y + total_height // 2)
                if "left_arrow.png" in ARROW_SPRITES:
                    arrow_left = ARROW_SPRITES["left_arrow.png"] if self.current_level_page > 0 else pygame.transform.grayscale(ARROW_SPRITES["left_arrow.png"])
                    arrow_right = ARROW_SPRITES["right_arrow.png"] if self.current_level_page < self.total_level_pages - 1 else pygame.transform.grayscale(ARROW_SPRITES["right_arrow.png"])
                else:
                    arrow_left = SMALL_FONT.render("<", True, WHITE if self.current_level_page > 0 else GRAY)
                    arrow_right = SMALL_FONT.render(">", True, WHITE if self.current_level_page < self.total_level_pages - 1 else GRAY)
                screen.blit(arrow_left, arrow_left_pos)
                screen.blit(arrow_right, arrow_right_pos)
                self.arrow_left_rect = arrow_left.get_rect(topleft=arrow_left_pos)
                self.arrow_right_rect = arrow_right.get_rect(topleft=arrow_right_pos)

                page_text = SMALL_FONT.render(f"Page {self.current_level_page + 1}/{self.total_level_pages}", True, WHITE)
                screen.blit(page_text, (SCREEN_WIDTH // 2 - page_text.get_width() // 2, start_y + total_height + 10))

                self.back_button.update(mouse_pos)
                self.back_button.draw(screen)
                #pygame.draw.rect(screen, RED, self.back_button.rect, 2)  # Debug outline

            pygame.display.flip()
            clock.tick(60)

        # Move pygame.quit() outside the loop
        pygame.quit()

def custom_bottomleft(x, y):
    def set_bottomleft(rect):
        rect.bottomleft = (x, y)
        return rect
    return set_bottomleft

if __name__ == "__main__":
    game = CraftSagaGame()
    game.run()

