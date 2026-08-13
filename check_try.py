import glob, re
files = glob.glob('src/native/managed/cdac/Microsoft.Diagnostics.DataContractReader.Legacy/*.cs')
for file in files:
    with open(file, 'r') as f:
        content = f.read()
    
    matches = re.finditer(r'^[ \t]*int\s+I[A-Za-z0-9_]+\.[A-Za-z0-9_]+\s*\([^)]*\)', content, re.MULTILINE)
    for match in matches:
        start_idx = match.end()
        # Find the next method or end of file
        next_match = re.search(r'^[ \t]*int\s+I[A-Za-z0-9_]+\.[A-Za-z0-9_]+', content[start_idx:], re.MULTILINE)
        end_idx = start_idx + next_match.start() if next_match else len(content)
        
        body = content[start_idx:end_idx]
        
        # We only care if it has some substantial code and no catch.
        # If it just returns HResults.E_NOTIMPL, it's fine.
        if 'catch (' not in body and 'E_NOTIMPL' not in body and 'CanFallback' not in body:
            # Let's see what it does
            lines = body.strip().split('\n')
            if len(lines) > 5:
                print(f"File: {file}")
                print(f"Method: {match.group(0)}")
                print(f"Body: {body.strip()[:200]}")
                print("---")
