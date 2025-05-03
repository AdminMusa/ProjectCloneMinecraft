from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random, os, json
from math import floor
import subprocess

app = Ursina()

CHUNK_SIZE = 16
current_chunk_coords = None
terrain_blocks = []
CHUNK_FOLDER = 'Chunks'

if not os.path.exists(CHUNK_FOLDER):
    os.makedirs(CHUNK_FOLDER)

textures = {
    '1': load_texture('grass.png'),
    '2': load_texture('stone.png'),
    '3': load_texture('wood.png'),
    '4': load_texture('leaves.png'),
    '5': load_texture('bedrock.png'),
    '6': load_texture('brick.png'),
    '7': load_texture('coal ore.png'),
    '8': load_texture('diamond ore.png'),
    '9': load_texture('furnace.png'),
    'm': load_texture('obsidian.png'),
    'n': load_texture('sand.png'),
    'b': load_texture('sandstone.png'),
    'v': load_texture('stoneBricks.png'),
    'c': load_texture('tnt.png'),
    'x': load_texture('woodenplanks.png'),
    'z': load_texture('craftingTable.png')
}

sky = Sky(texture='Sky0.png')

current_block = '1'

# Text label
block_label = Text(text="Current Block: Grass", position=(0.5, 0.45), origin=(0.5, 0.5), scale=2)

# Block icon at bottom center
current_block_icon = Entity(
    parent=camera.ui,
    model='quad',
    texture=textures[current_block],
    scale=(0.1, 0.1),
    position=(0, -0.45)
)

inventory = []
inventory_display = None
inventory_open = False

def input(key):
    global current_block
    if key in textures:
        current_block = key

        block_names = {
            '1': "Grass",
            '2': "Stone",
            '3': "Wood",
            '4': "Leaves",
            '5': "Bedrock",
            '6': "Brick",
            '7': "Coal Ore",
            '8': "Diamond Ore",
            '9': "Furnace",
            'm': "Obsidian",
            'n': "Sand",
            'b': "Sandstone",
            'v': "Stone Bricks",
            'c': "TNT",
            'x': "Wooden Planks",
            'z': "CraftingTable"
        }

        block_label.text = f"Current Block: {block_names.get(current_block, 'Unknown')}"
        current_block_icon.texture = textures[current_block]

class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=textures['1'], is_terrain=False):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            texture=texture,
            color=color.white,
            highlight_color=color.lime
        )
        self.is_terrain = is_terrain
        self.texture_id = [k for k,v in textures.items() if v==texture][0]

    def input(self, key):
        global current_block
        if self.hovered:
            if key == 'left mouse down':
                Voxel(position=self.position + mouse.normal, texture=textures[current_block])
            if key == 'right mouse down' and not self.is_terrain:
                destroy(self)

def save_chunk(cx, cz, block_data):
    filename = f"{CHUNK_FOLDER}/chunk_x{cx}_z{cz}.json"
    with open(filename, 'w') as f:
        json.dump(block_data, f)

def load_chunk(cx, cz):
    filename = f"{CHUNK_FOLDER}/chunk_x{cx}_z{cz}.json"
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return None

def generate_chunk(cx, cz):
    print(f'Loading chunk {cx}, {cz}')
    chunk_data = load_chunk(cx, cz)
    block_data = []

    if chunk_data:
        for data in chunk_data:
            pos = tuple(data['pos'])
            tex = textures[data['type']]
            block = Voxel(position=pos, texture=tex, is_terrain=False)
            terrain_blocks.append(block)
    else:
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                world_x = cx * CHUNK_SIZE + x
                world_z = cz * CHUNK_SIZE + z
                block = Voxel(position=(world_x, 0, world_z), texture=textures['1'], is_terrain=True)
                terrain_blocks.append(block)
                block_data.append({'pos': [world_x, 0, world_z], 'type': '1'})

        save_chunk(cx, cz, block_data)

def unload_chunk():
    print('Unloading terrain blocks')
    for block in terrain_blocks:
        destroy(block)
    terrain_blocks.clear()

player = FirstPersonController()

def update():
    global current_chunk_coords
    player_chunk_x = floor(player.x / CHUNK_SIZE)
    player_chunk_z = floor(player.z / CHUNK_SIZE)
    new_coords = (player_chunk_x, player_chunk_z)

    if new_coords != current_chunk_coords:
        if current_chunk_coords is not None:
            unload_chunk()
        generate_chunk(*new_coords)
        current_chunk_coords = new_coords

app.run()

subprocess.run(['python', 'luach.py'])
