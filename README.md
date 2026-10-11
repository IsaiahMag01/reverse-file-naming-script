# Reverse File Numbering

A small Python script that reverses the numeric prefixes on files in a folder. It was built to fix media downloads where the numbering ran newest-to-oldest and needed to run oldest-to-newest.

## What It Does

Given a folder of files named like `1. Title.mp4`, `2. Title.mp4`, ... `N. Title.mp4`, the script flips the order so that:

| Before | After (50 files) |
|--------|------------------|
| `1. Newest video.mp4` | `50. Newest video.mp4` |
| `2. Next video.mp4` | `49. Next video.mp4` |
| `50. Oldest video.mp4` | `1. Oldest video.mp4` |

Only the leading number changes. The rest of each filename (including extra spaces and punctuation) is preserved exactly.

## Requirements

- Python 3.6 or newer
- No third-party packages

## Usage

1. Save `reverse_numbering.py` anywhere on your computer.
2. Open a terminal or command prompt.
3. **Preview first** (nothing is renamed):

   ```
   python reverse_numbering.py "C:\path\to\your\folder"
   ```

4. If the preview looks correct, **apply the changes**:

   ```
   python reverse_numbering.py "C:\path\to\your\folder" --apply
   ```

On macOS or Linux, use `python3` and a path such as `/Users/you/Videos/Series`.

## How It Works

1. Scans the folder (not subfolders) for files beginning with a number followed by a period, such as `12. `.
2. Finds the lowest and highest numbers present.
3. Calculates each file's new number as `highest + lowest - current`.
4. Renames in two passes, first to unique temporary names and then to the final names, so no file can overwrite another mid-process.

## Behavior Notes

- **Dry run by default.** Files are only renamed when `--apply` is included.
- **Gaps are handled.** If a number is missing (for example, a deleted video), the order is still correctly reversed based on the lowest and highest numbers found.
- **Zero-padding is preserved.** Files numbered `01.`, `02.` keep their padded format.
- **Unnumbered files are ignored.** Files without a leading `N. ` prefix, and subfolders, are left alone.

## Important: Run It Only Once

Running `--apply` a second time flips the numbering back to the original order. If you're unsure whether a folder has already been processed, run the preview first and check the output.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No files with a leading 'N. ' number found.` | Check that filenames start with a number and a period, e.g. `1. Title`. |
| `python` is not recognized | Install Python from python.org, or try `python3` / `py` instead. |
| Permission error on rename | Close any media player or downloader using the files, then try again. |

## Backup Tip

Before applying to a large folder, copy it somewhere safe. The rename is reliable, but a backup makes it trivial to recover if the result isn't what you expected.