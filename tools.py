from pathlib import Path


# Locating the movie workspace
WORKSPACE = Path(__file__).parent / "workspace"


def list_files():
    """Returning all files available to the agent."""

    files = []

    for file in WORKSPACE.iterdir():
        if file.is_file():
            files.append(file.name)

    return sorted(files)


def read_file(filename):
    """Reading the full contents of one workspace file."""

    file_path = WORKSPACE / filename

    # Checking whether the requested file exists
    if not file_path.exists():
        return f"ERROR: FILE_NOT_FOUND: {filename}"

    # Preventing folders from being treated as files
    if not file_path.is_file():
        return f"ERROR: NOT_A_FILE: {filename}"

    return file_path.read_text(encoding="utf-8")


def search_file(filename, query):
    """Searching one file for lines containing the given text."""

    file_path = WORKSPACE / filename

    # Checking whether the requested file exists
    if not file_path.exists():
        return f"ERROR: FILE_NOT_FOUND: {filename}"

    matches = []

    # Looking at each line individually
    for line in file_path.read_text(encoding="utf-8").splitlines():

        if query.lower() in line.lower():
            matches.append(line)

    # Returning a clear observation when nothing matches
    if not matches:
        return f"NO_RESULTS: No matches found for '{query}' in {filename}"

    return matches


# Running simple tests only when tools.py is executed directly
if __name__ == "__main__":

    print("\n--- TEST 1: LIST FILES ---")
    print(list_files())

    print("\n--- TEST 2: READ FILE ---")
    print(read_file("actors.txt"))

    print("\n--- TEST 3: SEARCH FILE ---")
    print(search_file("actors.txt", "Zendaya"))

    print("\n--- TEST 4: MISSING FILE ---")
    print(read_file("movie_cast.txt"))

    print("\n--- TEST 5: NO SEARCH RESULTS ---")
    print(search_file("upcoming_movies.txt", "Ryan Gosling"))