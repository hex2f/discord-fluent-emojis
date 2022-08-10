import os

if not os.path.exists("./twemoji"):
  print('Cloning twemoji from github...')
  os.system("git clone https://github.com/discord/twemoji")

if not os.path.exists("./fluentui-emoji"):
  print('Cloning fluentui-emoji from github...')
  os.system("git clone https://github.com/microsoft/fluentui-emoji")
