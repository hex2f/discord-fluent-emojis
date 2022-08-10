import json
import os
import sys
from PIL import Image
from tqdm import tqdm

if not os.path.exists("./twemoji"):
  print('Cloning twemoji from github...')
  os.system("git clone https://github.com/discord/twemoji")

if not os.path.exists("./fluentui-emoji"):
  print('Cloning fluentui-emoji from github...')
  os.system("git clone https://github.com/microsoft/fluentui-emoji")

if os.path.exists("./discord_fluent"):
  print('Removing existing discord_fluent folder...')
  os.system("rm -rf ./discord_fluent")

print('Creating discord_fluent folder...')
os.system("cp -r ./twemoji ./discord_fluent")

print('Patching fluentui-emoji into twemoji...')

def patch(source_file, svg, unicode):
  filename = ""
  try:
    directory = f"/{'Color' if svg else '3D'}"
    filename = os.listdir(source_file + directory)[0]
  except:
    directory = f"/Default/{'Color' if svg else '3D'}"
    filename = os.listdir(source_file + directory)[0]
  if filename is not None:
    if svg:
      # copy f"{source_file + directory}/{filename}" to f"discord_fluent/assets/svg/{unicode}.svg"
      with open(source_file + directory + "/" + filename, "r") as f:
        data = f.read()
      with open(f"./discord_fluent/assets/svg/{unicode}.svg", "w") as f:
        f.write(data)
    else:
      image = Image.open(f'./{source_file + directory}/{filename}')
      image = image.resize((72, 72))
      image.save(f'./discord_fluent/assets/72x72/{unicode}.png')

for asset_name in tqdm(os.listdir('fluentui-emoji/assets')):
  try:
    with open(f'fluentui-emoji/assets/{asset_name}/metadata.json', 'r') as f:
      data = json.load(f)
      # TODO: Skintone support
      unicode = data['unicode'].split(' ')[0]
      if os.path.exists(f"./twemoji/assets/72x72/{data['unicode']}.png"):
        patch(f'fluentui-emoji/assets/{asset_name}', False, unicode)
        patch(f'fluentui-emoji/assets/{asset_name}', True, unicode)
  except Exception as e:
    print("failed to patch emoji:", e)
    pass
