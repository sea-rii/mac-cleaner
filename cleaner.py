from pathlib import Path
import os
import subprocess
import time

from rich.console import Console
from rich.table import Table
from rich.progress import track

from utils import format_size

console = Console()


class MacCleaner:
    def __init__(self, days_threshold: int = 30, large_file_min_mb: int = 500):
        # Settings
        self.days_threshold = days_threshold
        self.large_file_min_mb = large_file_min_mb

        # Stats
        self.total_freed = 0

        # Only user-level folders
        self.cache_paths = [
            Path.home() / "Library/Caches",
        ]

        self.log_paths = [
            Path.home() / "Library/Logs",
        ]

    # ---------- Utility methods ----------

    def folder_size(self, path: Path) -> int:
        """Return total size of all files in a folder tree."""
        if not path.exists():
            return 0

        size = 0
        for root, dirs, files in os.walk(path):
            for f in files:
                try:
                    size += (Path(root) / f).stat().st_size
                except (PermissionError, FileNotFoundError):
                    pass
        return size

    def total_size_of(self, paths: list[Path]) -> int:
        """Total size of a list of folders."""
        return sum(self.folder_size(p) for p in paths if p.exists())

    def _age_cutoff(self) -> float:
        """Timestamp; only delete things older than this."""
        return time.time() - self.days_threshold * 24 * 60 * 60

    def clear_folder_contents_age_based(self, root: Path) -> int:
        """
        Delete files inside a folder that are older than days_threshold.
        Recursively walks subfolders. Keeps the root folder itself.
        Returns total bytes freed.
        """
        if not root.exists():
            return 0

        freed = 0
        cutoff = self._age_cutoff()

        # Progress bar over top-level entries
        try:
            items = list(root.iterdir())
        except PermissionError:
            console.print(f"[yellow]Skipping (no permission to list):[/] {root}")
            return 0

        for item in track(items, description=f" Cleaning {root.name}..."):
            if item.is_dir():
                # Recurse into subfolder
                freed += self.clear_folder_contents_age_based(item)
                # Try to remove empty folder
                try:
                    item.rmdir()
                except OSError:
                    # Not empty / in use -> ignore
                    pass
            else:
                try:
                    mtime = item.stat().st_mtime
                    if mtime > cutoff:
                        # Too new → keep it
                        continue

                    size = item.stat().st_size
                    item.unlink()
                    freed += size
                except (PermissionError, FileNotFoundError):
                    pass
                except Exception as e:
                    console.print(f"[red]  Could not delete[/] {item}: {e}")

        return freed

    # ---------- Cleaning methods ----------

    def clear_caches(self):
        console.print("\n[bold cyan]🧹 Clearing Caches (age-based)...[/]")
        for folder in self.cache_paths:
            if folder.exists():
                console.print(f"[dim]Target:[/] {folder}")
                freed = self.clear_folder_contents_age_based(folder)
                self.total_freed += freed
                console.print(
                    f"[green]✔ Done[/] {folder} — freed [bold]{format_size(freed)}[/]"
                )
            else:
                console.print(f"[yellow]Skipping; does not exist:[/] {folder}")

    def clear_logs(self):
        console.print("\n[bold cyan]📄 Clearing Logs (age-based)...[/]")
        for folder in self.log_paths:
            if folder.exists():
                console.print(f"[dim]Target:[/] {folder}")
                freed = self.clear_folder_contents_age_based(folder)
                self.total_freed += freed
                console.print(
                    f"[green]✔ Done[/] {folder} — freed [bold]{format_size(freed)}[/]"
                )
            else:
                console.print(f"[yellow]Skipping; does not exist:[/] {folder}")

    def clear_trash(self):
        console.print("\n[bold cyan]🗑️ Asking Finder to empty Trash...[/]")

        try:
            # Don't crash if Finder refuses; just best-effort
            subprocess.run(
                ["osascript", "-e", 'tell application "Finder" to empty trash'],
                check=False,
            )
            console.print(
                "[green]✔ Request sent[/] — if Finder has permission, Trash should now be empty."
            )
        except Exception as e:
            console.print(f"[red]Could not ask Finder to empty Trash:[/] {e}")

    # ---------- Big File Radar ----------

    def find_large_files(self, roots: list[Path]):
        console.print(
            f"\n[bold magenta]🔍 Big File Radar[/] (>{self.large_file_min_mb} MB)"
        )

        min_bytes = self.large_file_min_mb * 1024 * 1024
        big_files: list[tuple[int, Path]] = []

        for root in roots:
            if not root.exists():
                console.print(f"[yellow]Skipping (not found):[/] {root}")
                continue

            console.print(f"[dim]Scanning:[/] {root}")
            for dirpath, dirs, files in os.walk(root):
                for name in files:
                    path = Path(dirpath) / name
                    try:
                        size = path.stat().st_size
                    except (PermissionError, FileNotFoundError):
                        continue

                    if size >= min_bytes:
                        big_files.append((size, path))

        if not big_files:
            console.print("[green]No files above threshold found. Nice! ✨[/]")
            return

        # Sort biggest first
        big_files.sort(reverse=True, key=lambda x: x[0])

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Size", justify="right")
        table.add_column("Path", overflow="fold")

        for size, path in big_files[:20]:
            table.add_row(format_size(size), str(path))

        console.print("\n[bold]Top 20 largest files found:[/]")
        console.print(table)

    # ---------- Dashboard ----------

    def show_dashboard(
        self,
        caches_before: int,
        caches_after: int,
        logs_before: int,
        logs_after: int,
    ):
        console.print("\n[bold blue]📊 Space Dashboard[/]")

        total_before = caches_before + logs_before
        total_after = caches_after + logs_after
        freed = max(0, total_before - total_after)

        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Category")
        table.add_column("Before")
        table.add_column("After")
        table.add_column("Freed")

        table.add_row(
            "Caches",
            format_size(caches_before),
            format_size(caches_after),
            format_size(max(0, caches_before - caches_after)),
        )
        table.add_row(
            "Logs",
            format_size(logs_before),
            format_size(logs_after),
            format_size(max(0, logs_before - logs_after)),
        )
        table.add_row(
            "[bold]Total[/]",
            format_size(total_before),
            format_size(total_after),
            format_size(freed),
        )

        console.print(table)
        console.print(
            f"\n[green]✨ Overall freed (this run):[/] [bold]{format_size(freed)}[/]"
        )
