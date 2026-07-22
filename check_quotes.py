content = open('financial_assistant.py', 'r', encoding='utf-8').read()
lines = content.split('\n')
for i, line in enumerate(lines):
    if '""" """,' in line or '""" """,' in line:
        print(f'Line {i+1}: {line[:100]}')