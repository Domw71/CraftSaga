Just learning python had fun making a little game and a map editor. 


Create new folder CraftSaga extract data.rar to the new file this contains all textures, sprites ect.. 

File Structure

CraftSaga/
├── data/
│   ├── arrows
│   ├── items
│   ├── maps
│   ├── monsters
│   ├── npcs
│   ├── player
│   ├── stats
│   ├── textures
├── craftsaga_updated.py
├── map_editor_updated.py

Change the database credentials to yours in craftsaga_updated.py

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

Run craftsaga_updated.py 
click login/register > register this will log you in once account is created 
you have got highscores, achievments and select level each time you complete a level it will become completed and next level will become unlocked.


-to make new levels load map_editor_updated.py click map and start making new map goto textures and lay the floor by clicking texture and holding shift + click to add to map area (boundary.jpg and water.png are boundarys so player cant walk on them. 
once you have made your map add player by clicking player and adding to map (shift + click)

- add monster doing the same you can edit there health attack defence and xp by clicking in the boxes to edit the stats then press enter to set it 
- adding quest click on npc add it to map you will be prompted to add dialogue item name and monster item name can be whatever monster is eiter Demon, Dragon or mutant.png 
