"""
PIE Module Resolver
Handles module discovery, loading, and dependency resolution.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Any


class ModuleResolver:
    """
    Resolves and loads PIE modules from the standard library and user paths.
    
    Search order:
    1. Standard library (stdlib/)
    2. User-defined paths (via -I flag or PIEPATH environment variable)
    3. Current directory
    """
    
    def __init__(self, stdlib_path: Optional[Path] = None, user_paths: Optional[List[str]] = None):
        """
        Initialize the module resolver.
        
        Args:
            stdlib_path: Path to standard library (defaults to <project>/stdlib)
            user_paths: Additional paths to search for modules
        """
        # Determine stdlib path (relative to this file's location)
        if stdlib_path is None:
            # Go up from src/frontend/module_resolver.py to project root, then to stdlib
            project_root = Path(__file__).parent.parent.parent
            stdlib_path = project_root / 'stdlib'
        
        self.stdlib_path = Path(stdlib_path)
        self.user_paths = [Path(p) for p in (user_paths or [])]
        self.loaded_modules: Dict[str, 'ModuleInfo'] = {}  # Cache loaded modules
        
        # Add current directory to search paths
        self.user_paths.append(Path.cwd())
    
    def resolve_module(self, module_name: str, source_file_dir: Optional[Path] = None) -> 'ModuleInfo':
        """
        Resolve a module name to its file path and metadata.
        
        Args:
            module_name: Name of the module (e.g., 'http' or 'std.math')
            source_file_dir: Directory of the file doing the import (for relative imports)
        
        Returns:
            ModuleInfo object containing module metadata and paths
        
        Raises:
            ModuleNotFoundError: If module cannot be found
            ModuleError: If module is invalid (missing files, bad metadata, etc.)
        """
        # Check if already loaded
        if module_name in self.loaded_modules:
            return self.loaded_modules[module_name]
        
        # Convert module name to path (e.g., 'std.math' -> 'std/math')
        module_path_parts = module_name.split('.')
        
        # Try standard library first (directory-based modules with module.json)
        module_path = self.stdlib_path.joinpath(*module_path_parts)
        if module_path.exists() and module_path.is_dir():
            return self._load_module(module_path, module_name)
        
        # Try user paths (directory-based modules)
        for user_path in self.user_paths:
            module_path = user_path.joinpath(*module_path_parts)
            if module_path.exists() and module_path.is_dir():
                return self._load_module(module_path, module_name)
        
        # Try user-defined .pie file modules (single file, no module.json)
        # Search order: source file dir -> user paths -> current dir
        search_dirs = []
        if source_file_dir:
            search_dirs.append(source_file_dir)
        search_dirs.extend(self.user_paths)
        
        for search_dir in search_dirs:
            pie_file = search_dir / f"{module_name}.pie"
            if pie_file.exists() and pie_file.is_file():
                return self._load_pie_module(pie_file, module_name)
        
        # Module not found
        raise ModuleNotFoundError(
            f"Module '{module_name}' not found in:\n"
            f"  - Standard library: {self.stdlib_path}\n"
            f"  - User paths: {', '.join(str(p) for p in self.user_paths)}\n"
            f"  - Source directory: {source_file_dir if source_file_dir else 'N/A'}"
        )
    
    def _load_module(self, module_path: Path, module_name: str) -> 'ModuleInfo':
        """
        Load module metadata and PIE interface file (stdlib-style module).
        
        Args:
            module_path: Path to the module directory
            module_name: Name of the module
        
        Returns:
            ModuleInfo object
        
        Raises:
            ModuleError: If module is invalid
        """
        # Load module.json
        metadata_file = module_path / 'module.json'
        if not metadata_file.exists():
            raise ModuleError(
                f"Module '{module_name}' is missing module.json in {module_path}"
            )
        
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        except json.JSONDecodeError as e:
            raise ModuleError(
                f"Module '{module_name}' has invalid module.json: {e}"
            )
        
        # Validate metadata
        self._validate_metadata(metadata, module_name)
        
        # Determine PIE interface file name (last part of module name)
        module_path_parts = module_name.split('.')
        pie_filename = module_path_parts[-1]
        pie_file = module_path / f'{pie_filename}.pie'
        
        # PIE file is optional for some modules (pure C modules)
        pie_file_exists = pie_file.exists()
        
        # Create module info
        module_info = ModuleInfo(
            name=module_name,
            path=module_path,
            pie_file=pie_file if pie_file_exists else None,
            metadata=metadata,
            is_user_module=False
        )
        
        # Cache the module
        self.loaded_modules[module_name] = module_info
        
        return module_info
    
    def _load_pie_module(self, pie_file: Path, module_name: str) -> 'ModuleInfo':
        """
        Load a user-defined .pie module (single file, no module.json).
        
        Args:
            pie_file: Path to the .pie file
            module_name: Name of the module
        
        Returns:
            ModuleInfo object
        
        Note:
            User-defined modules don't have module.json files.
            Their exports will be determined by parsing the .pie file
            and finding functions with the 'export' keyword.
        """
        # Create minimal metadata for user module
        metadata = {
            'name': module_name,
            'version': '1.0.0',
            'description': f'User-defined module: {module_name}',
            'exports': {
                'functions': [],  # Will be populated during semantic analysis
                'types': []
            }
        }
        
        # Create module info
        module_info = ModuleInfo(
            name=module_name,
            path=pie_file.parent,
            pie_file=pie_file,
            metadata=metadata,
            is_user_module=True
        )
        
        # Cache the module
        self.loaded_modules[module_name] = module_info
        
        return module_info
    
    def _validate_metadata(self, metadata: Dict[str, Any], module_name: str):
        """
        Validate module metadata structure.
        
        Args:
            metadata: Parsed module.json content
            module_name: Name of the module
        
        Raises:
            ModuleError: If metadata is invalid
        """
        required_fields = ['name', 'version', 'description']
        for field in required_fields:
            if field not in metadata:
                raise ModuleError(
                    f"Module '{module_name}' metadata missing required field: {field}"
                )
        
        # Validate name matches
        if metadata['name'] != module_name.split('.')[-1]:
            raise ModuleError(
                f"Module '{module_name}' metadata name mismatch: "
                f"expected '{module_name.split('.')[-1]}', got '{metadata['name']}'"
            )
        
        # Validate exports structure if present
        if 'exports' in metadata:
            exports = metadata['exports']
            if 'functions' in exports and not isinstance(exports['functions'], list):
                raise ModuleError(
                    f"Module '{module_name}' exports.functions must be a list"
                )
            if 'types' in exports and not isinstance(exports['types'], list):
                raise ModuleError(
                    f"Module '{module_name}' exports.types must be a list"
                )
    
    def get_module_c_sources(self, module_name: str) -> List[Path]:
        """
        Get list of C source files for a module.
        
        Args:
            module_name: Name of the module
        
        Returns:
            List of absolute paths to C source files
        """
        module_info = self.loaded_modules.get(module_name)
        if not module_info:
            return []
        
        c_bindings = module_info.metadata.get('c_bindings', {})
        sources = c_bindings.get('sources', [])
        
        # Convert to absolute paths (relative to project src/runtime/ directory)
        project_root = Path(__file__).parent.parent.parent
        runtime_dir = project_root / 'src' / 'runtime'
        
        return [runtime_dir / src for src in sources]
    
    def get_module_libraries(self, module_name: str) -> List[str]:
        """
        Get list of libraries to link for a module.
        
        Args:
            module_name: Name of the module
        
        Returns:
            List of library names (without -l prefix)
        """
        module_info = self.loaded_modules.get(module_name)
        if not module_info:
            return []
        
        c_bindings = module_info.metadata.get('c_bindings', {})
        return c_bindings.get('libraries', [])
    
    def get_all_loaded_modules(self) -> Dict[str, 'ModuleInfo']:
        """Get all currently loaded modules."""
        return self.loaded_modules.copy()


class ModuleInfo:
    """
    Information about a loaded module.
    """
    
    def __init__(self, name: str, path: Path, pie_file: Optional[Path], metadata: Dict[str, Any], is_user_module: bool = False):
        self.name = name
        self.path = path
        self.pie_file = pie_file
        self.metadata = metadata
        self.is_user_module = is_user_module  # True for .pie modules, False for stdlib modules
    
    def __repr__(self):
        module_type = "user" if self.is_user_module else "stdlib"
        return f"ModuleInfo(name='{self.name}', path={self.path}, type={module_type})"
    
    def get_exports(self) -> Dict[str, Any]:
        """Get module exports (functions and types)."""
        return self.metadata.get('exports', {})
    
    def get_functions(self) -> List[Dict[str, str]]:
        """Get list of exported functions."""
        return self.get_exports().get('functions', [])
    
    def get_types(self) -> List[Dict[str, str]]:
        """Get list of exported types."""
        return self.get_exports().get('types', [])
    
    def get_c_bindings(self) -> Dict[str, Any]:
        """Get C bindings information."""
        return self.metadata.get('c_bindings', {})


class ModuleNotFoundError(Exception):
    """Raised when a module cannot be found."""
    pass


class ModuleError(Exception):
    """Raised when a module is invalid or has errors."""
    pass


# Example usage and testing
if __name__ == "__main__":
    # Test the module resolver
    resolver = ModuleResolver()
    
    try:
        # Try to load http module
        http_module = resolver.resolve_module('http')
        print(f"Loaded module: {http_module}")
        print(f"Functions: {len(http_module.get_functions())}")
        print(f"Types: {len(http_module.get_types())}")
        
        # Try to load json module
        json_module = resolver.resolve_module('json')
        print(f"\nLoaded module: {json_module}")
        print(f"Functions: {len(json_module.get_functions())}")
        
        # Print module functions
        print("\nHTTP Module Functions:")
        for func in http_module.get_functions():
            print(f"  - {func['name']}: {func['signature']}")
        
        print("\nJSON Module Functions:")
        for func in json_module.get_functions()[:5]:  # First 5
            print(f"  - {func['name']}: {func['signature']}")
        
    except (ModuleNotFoundError, ModuleError) as e:
        print(f"Error: {e}")
