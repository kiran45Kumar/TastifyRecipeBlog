with open('data.json', 'rb') as f:
    raw = f.read()

# Force save as UTF-8
with open('data_fixed.json', 'w', encoding='utf-8') as f:
    f.write(raw.decode('utf-8', errors='ignore'))  # ignore corrupt bytes