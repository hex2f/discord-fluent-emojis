import json
import os
from tqdm import tqdm
from PIL import Image

if os.path.exists("./discord_fluent"):
  print('Removing existing discord_fluent folder...')
  os.system("rm -rf ./discord_fluent")

print('Creating discord_fluent folder...')
os.system("cp -r ./twemoji ./discord_fluent")


flags = {
  '1f3fb': 'Light',
  '1f3fc': 'Medium-Light',
  '1f3fd': 'Medium',
  '1f3fe': 'Medium-Dark',
  '1f3ff': 'Dark'
}

print('Patching twemoji...')
for asset_name in tqdm(os.listdir('fluentui-emoji/assets')):
  try:
    with open(f'fluentui-emoji/assets/{asset_name}/metadata.json', 'r') as f:
      data = json.load(f)
      variations = []
      if 'unicodeSkintones' in data:
        for variation in data['unicodeSkintones']:
          key = ' '.join(variation.split(' ')[1:])
          flag = flags[key] if key in flags else 'Default'
          variations.append({ 'unicode': '-'.join(variation.split(' ')), 'child_path': f'{flag}/'  })
      else:
        variations.append({ 'unicode': '-'.join(data['unicode'].split(' ')), 'child_path': '' })
      for variation in variations:
        if os.path.exists(f"./twemoji/assets/72x72/{variation['unicode']}.png"):
          # Copy 3D
          file_name = os.listdir(f"./fluentui-emoji/assets/{asset_name}/{variation['child_path']}3D")[0]
          image = Image.open(f'./fluentui-emoji/assets/{asset_name}/{variation["child_path"]}3D/{file_name}')
          image72 = image.resize((72, 72))
          image72.save(f'./discord_fluent/assets/72x72/{variation["unicode"]}.png')
          # Copy SVG
          file_name = os.listdir(f"./fluentui-emoji/assets/{asset_name}/{variation['child_path']}3D")[0]
          with open(f'./fluentui-emoji/assets/{asset_name}/{variation["child_path"]}3D/{file_name}', 'rb') as f:
            svg = f.read()
          with open(f'./discord_fluent/assets/svg/{variation["unicode"]}.svg', 'wb') as f:
            f.write(svg)
      

  except Exception as e:
    print('failed to patch emoji:', e)
    pass

with open('./discord_fluent/package.json', 'r') as f:
  data = json.load(f)
  data['name'] = 'discord-fluent-emoji'
  data['description'] = 'Twemoji patched for Fluent UI Emoji for Discord'
  data['version'] = '1.1.0'
  data['files'] = [
    "dist/twemoji*.js",
    "dist/svg/*.svg",
    "dist/72x72/*.png",
    "index.d.ts"
  ]
  with open('./discord_fluent/package.json', 'w') as f2:
    json.dump(data, f2, indent=2)