import re

content = open("src/native/managed/cdac/Microsoft.Diagnostics.DataContractReader.Legacy/SOSDacImpl.cs").read()
# Let's extract TraverseEHInfo, TraverseLoaderHeap, TraverseModuleMap, TraverseRCWCleanupList, TraverseVirtCallStubHeap
methods = ["TraverseEHInfo", "TraverseLoaderHeap", "TraverseModuleMap", "TraverseRCWCleanupList", "TraverseVirtCallStubHeap"]

for method in methods:
    print(method)
    match = re.search(r'int ISOSDacInterface\.' + method + r'\(.+?^    }', content, re.MULTILINE | re.DOTALL)
    if match:
        body = match.group(0)
        # Check if callback is invoked inside the method while holding the lock
        lock_idx = body.find("using ComInterfaceLock comLockScope = new(_apiLock);")
        callback_idx = -1
        if "TraverseEHInfo" in method:
            callback_idx = body.find("pCallback(")
        elif "TraverseLoaderHeap" in method:
            callback_idx = body.find("TraverseLoaderHeapCore(")
        elif "TraverseModuleMap" in method:
            callback_idx = body.find("pCallback(")
        elif "TraverseRCWCleanupList" in method:
            callback_idx = body.find("pCallback(")
        elif "TraverseVirtCallStubHeap" in method:
            callback_idx = body.find("TraverseLoaderHeapCore(")
            
        print(f"Lock at: {lock_idx}")
        print(f"Callback at: {callback_idx}")
        print("---")
        
