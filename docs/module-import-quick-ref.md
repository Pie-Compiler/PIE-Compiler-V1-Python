# Module Import Paths - Quick Reference

## Syntax Options

| Syntax | Description | Example |
|--------|-------------|---------|
| `import module;` | Standard import (searches default paths) | `import http;` |
| `import module as alias;` | Import with alias | `import http as web;` |
| `import module from "path";` | Import from custom path | `import util from "./Utils/";` |
| `import module from "path" as alias;` | Custom path + alias | `import util from "./lib/" as u;` |

## Path Types

| Path Type | Example | Description |
|-----------|---------|-------------|
| Relative (same dir) | `"./"`  | Current directory |
| Relative (subdir) | `"./Utils/"` | Subdirectory |
| Relative (parent) | `"../"` | Parent directory |
| Absolute | `"/opt/modules/"` | Absolute filesystem path |

## Examples

### Basic Import
```pie
import UserModule from "./";
import util from "./Utils/";

string remark = UserModule.remarks(85.5);
int sum = util.add(10, 20);
```

### With Aliases
```pie
import UserModule from "./modules/" as user;
import utilities from "./lib/" as utils;

string result = user.processData();
int value = utils.calculate(42);
```

### Mixed Imports
```pie
// Standard library module
import http;

// Custom path modules  
import config from "./config/";
import helpers from "../shared/";

// Use them together
string response = http.get("https://api.example.com");
string apiKey = config.getApiKey();
string formatted = helpers.format(response);
```

## Default Search Order (without custom path)

1. Standard library (`stdlib/`)
2. Source file directory
3. Current working directory
4. User-defined paths (`-I` flag)

## With Custom Path

When you specify `from "path"`, only that path is searched - the default search is bypassed.

## Quick Tips

✅ Use relative paths for project modules
✅ Keep module names descriptive
✅ Organize modules by functionality
✅ Document module dependencies
❌ Avoid deeply nested paths
❌ Avoid absolute paths (not portable)
