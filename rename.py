""" Python 3 code to rename multiple
 files in a directory or folder"""
import os


# Function to rename multiple files
def main(start: int, end: int, filetype: str) -> None:
    """Removes start charachters and end characters from all files in a directory
    use only on files of same type"""
    # Destination Folder
    folder = "CSV_files"
    for filename in os.listdir(folder):
        drc = f"{folder}/{filename[start:end]}{filetype}"
        src = f"{folder}/{filename}"
        os.rename(src, drc)


# Driver Code
if __name__ == "__main__":

    # Calling main() function
    main()
