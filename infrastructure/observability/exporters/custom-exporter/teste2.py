import toml

config = toml.load("config.toml")

for key in config.items():
    print(key)
