# Module Import Path Feature - Test Suite

## Test Cases

### Test 1: Relative Path - Same Directory
```pie
import UserModule from "./testFiles/";
```
**Expected:** Module loads successfully from testFiles/UserModule.pie

### Test 2: Relative Path - Subdirectory  
```pie
import util from "./testFiles/Utils/";
```
**Expected:** Module loads successfully from testFiles/Utils/util.pie

### Test 3: Standard Import (No Path)
```pie
import http;
```
**Expected:** Searches stdlib, current dir, etc.

### Test 4: Import with Alias
```pie
import UserModule from "./testFiles/" as user;
```
**Expected:** Module accessible via `user.functionName()`

### Test 5: Custom Path + Alias
```pie
import util from "./testFiles/Utils/" as u;
```
**Expected:** Module accessible via `u.functionName()`

### Test 6: Parent Directory (from nested file)
```pie
import shared from "../";
```
**Expected:** Loads module from parent directory

### Test 7: Error - Module Not Found
```pie
import NonExistent from "./wrong/path/";
```
**Expected:** Clear error message with attempted paths

### Test 8: Error - Invalid Path
```pie
import Module from "./does/not/exist/";
```
**Expected:** Error indicating path doesn't exist

## Verification

All test cases passed! ✅

- ✅ Relative paths work correctly
- ✅ Subdirectory imports work
- ✅ Custom paths override default search
- ✅ Aliases work with custom paths
- ✅ Error messages are clear and helpful
- ✅ Backward compatible with standard imports
