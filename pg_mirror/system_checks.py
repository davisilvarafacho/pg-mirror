"""
System checks module for PostgreSQL client tools verification.

This module provides functions to check if PostgreSQL client tools
(pg_dump, pg_restore, psql) are installed and accessible in the system.

Supports Linux, macOS, and Windows platforms.
"""

import platform
import shutil
import subprocess
import sys
from typing import Any, Dict, Optional, Tuple


class SystemCheckError(Exception):
    """Exception raised when system checks fail."""
    pass


def get_os_info() -> Dict[str, str]:
    """
    Get operating system information.
    
    Returns:
        Dictionary with OS name, version, and architecture
    """
    return {
        "system": platform.system(),  # Linux, Darwin, Windows
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "platform": platform.platform()
    }


def check_command_exists(command: str) -> Tuple[bool, Optional[str]]:
    """
    Check if a command exists in the system PATH.
    
    Args:
        command: Command name to check (e.g., 'pg_dump')
    
    Returns:
        Tuple of (exists: bool, path: str or None)
    """
    path = shutil.which(command)
    return (path is not None, path)


def get_command_version(command: str) -> Optional[str]:
    """
    Get version of a command.
    
    Args:
        command: Command name to check version
    
    Returns:
        Version string or None if failed
    """
    try:
        result = subprocess.run(
            [command, "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            # Return first line of output (usually contains version)
            return result.stdout.strip().split('\n')[0]
        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def check_postgresql_tools() -> Dict[str, Dict[str, Any]]:
    """
    Check if all required PostgreSQL client tools are installed.
    
    Returns:
        Dictionary with status of each tool:
        {
            'pg_dump': {'installed': bool, 'path': str, 'version': str},
            'pg_restore': {'installed': bool, 'path': str, 'version': str},
            'psql': {'installed': bool, 'path': str, 'version': str}
        }
    """
    tools = ['pg_dump', 'pg_restore', 'psql']
    results = {}
    
    for tool in tools:
        exists, path = check_command_exists(tool)
        version = get_command_version(tool) if exists else None
        
        results[tool] = {
            'installed': exists,
            'path': path,
            'version': version
        }
    
    return results


def get_installation_instructions() -> Dict[str, str]:
    """
    Get installation instructions for PostgreSQL client tools based on OS.
    
    Returns:
        Dictionary with installation commands for current OS
    """
    system = platform.system()
    
    instructions = {
        "Linux": {
            "debian": "sudo apt-get update && sudo apt-get install postgresql-client",
            "ubuntu": "sudo apt-get update && sudo apt-get install postgresql-client",
            "fedora": "sudo dnf install postgresql",
            "rhel": "sudo yum install postgresql",
            "centos": "sudo yum install postgresql",
            "arch": "sudo pacman -S postgresql",
            "generic": "Install postgresql-client package using your distribution's package manager"
        },
        "Darwin": {
            "homebrew": "brew install postgresql",
            "macports": "sudo port install postgresql-client",
            "generic": "brew install postgresql (requires Homebrew)"
        },
        "Windows": {
            "installer": "Download from: https://www.postgresql.org/download/windows/",
            "chocolatey": "choco install postgresql",
            "scoop": "scoop install postgresql",
            "generic": "Download installer from https://www.postgresql.org/download/windows/"
        }
    }
    
    return instructions.get(system, {"generic": "Visit https://www.postgresql.org/download/"})


def verify_system_requirements(verbose: bool = False) -> bool:
    """
    Verify all system requirements are met.
    
    Args:
        verbose: If True, print detailed information
    
    Returns:
        True if all requirements are met, False otherwise
    
    Raises:
        SystemCheckError: If critical requirements are missing
    """
    os_info = get_os_info()
    tools_status = check_postgresql_tools()
    
    if verbose:
        print("=" * 60)
        print("System Information:")
        print("=" * 60)
        print(f"OS: {os_info['system']} {os_info['release']}")
        print(f"Platform: {os_info['platform']}")
        print(f"Machine: {os_info['machine']}")
        print()
        print("=" * 60)
        print("PostgreSQL Client Tools:")
        print("=" * 60)
    
    all_installed = True
    missing_tools = []
    
    for tool, status in tools_status.items():
        if verbose:
            if status['installed']:
                print(f"✓ {tool:<12} : {status['version']}")
                print(f"  Path: {status['path']}")
            else:
                print(f"✗ {tool:<12} : NOT FOUND")
        
        if not status['installed']:
            all_installed = False
            missing_tools.append(tool)
    
    if not all_installed:
        if verbose:
            print()
            print("=" * 60)
            print("Installation Instructions:")
            print("=" * 60)
            instructions = get_installation_instructions()
            for method, command in instructions.items():
                print(f"\n{method.upper()}:")
                print(f"  {command}")
            print()
        
        error_msg = f"Missing required PostgreSQL client tools: {', '.join(missing_tools)}"
        raise SystemCheckError(error_msg)
    
    if verbose:
        print()
        print("=" * 60)
        print("✓ All system requirements met!")
        print("=" * 60)
        print()
    
    return True


def print_installation_help():
    """
    Print detailed installation help for PostgreSQL client tools.
    """
    os_info = get_os_info()
    system = os_info['system']
    
    print("=" * 60)
    print("PostgreSQL Client Tools Installation Guide")
    print("=" * 60)
    print()
    print(f"Detected OS: {system} {os_info['release']}")
    print()
    print("Required tools: pg_dump, pg_restore, psql")
    print()
    
    instructions = get_installation_instructions()
    
    print("Installation Options:")
    print("-" * 60)
    for method, command in instructions.items():
        print(f"\n{method.upper()}:")
        print(f"  {command}")
    
    print()
    print("=" * 60)
    print("After installation, verify with:")
    print("  pg_dump --version")
    print("  pg_restore --version")
    print("  psql --version")
    print("=" * 60)


def check_python_version(min_version: Tuple[int, int] = (3, 8)) -> bool:
    """
    Check if Python version meets minimum requirements.
    
    Args:
        min_version: Minimum required version as tuple (major, minor)
    
    Returns:
        True if version is sufficient
    
    Raises:
        SystemCheckError: If Python version is too old
    """
    current = sys.version_info[:2]
    
    if current < min_version:
        raise SystemCheckError(
            f"Python {min_version[0]}.{min_version[1]}+ required. "
            f"Current version: {current[0]}.{current[1]}"
        )
    
    return True


if __name__ == "__main__":
    """Run system checks when module is executed directly."""
    print("Running pg-mirror system checks...\n")
    
    try:
        # Check Python version
        check_python_version()
        print(f"✓ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print()
        
        # Check PostgreSQL tools
        verify_system_requirements(verbose=True)
        
    except SystemCheckError as e:
        print(f"\n✗ System check failed: {e}\n")
        print_installation_help()
        sys.exit(1)
