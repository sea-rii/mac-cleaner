from pathlib import Path

from cleaner import MacCleaner, console


def main():
    cleaner = MacCleaner(
        days_threshold=30,      # delete cache/log files older than 30 days
        large_file_min_mb=500,  # Big File Radar threshold
    )

    while True:
        console.print("\n[bold green]🍏 Mac Cleaner — by Siri[/]")
        console.print(
            "[dim]Age-based cleaning · Big File Radar · Space dashboard[/]\n"
        )

        console.print("Choose an option:")
        console.print("  [cyan]1)[/] Clean caches (age-based)")
        console.print("  [cyan]2)[/] Clean logs (age-based)")
        console.print("  [cyan]3)[/] Empty Trash (via Finder)")
        console.print("  [cyan]4)[/] Big File Radar (Downloads / Desktop / Movies)")
        console.print("  [cyan]5)[/] FULL CLEAN + dashboard")
        console.print("  [cyan]6)[/] Exit")

        choice = input("\nYour choice: ").strip()

        if choice == "1":
            cleaner.clear_caches()

        elif choice == "2":
            cleaner.clear_logs()

        elif choice == "3":
            cleaner.clear_trash()

        elif choice == "4":
            roots = [
                Path.home() / "Downloads",
                Path.home() / "Desktop",
                Path.home() / "Movies",
            ]
            cleaner.find_large_files(roots)

        elif choice == "5":
            # Measure before
            caches_before = cleaner.total_size_of(cleaner.cache_paths)
            logs_before = cleaner.total_size_of(cleaner.log_paths)

            # Clean
            cleaner.clear_caches()
            cleaner.clear_logs()
            cleaner.clear_trash()

            # Measure after
            caches_after = cleaner.total_size_of(cleaner.cache_paths)
            logs_after = cleaner.total_size_of(cleaner.log_paths)

            cleaner.show_dashboard(
                caches_before, caches_after, logs_before, logs_after
            )

        elif choice == "6":
            console.print("\n[dim]Bye! Your Mac feels lighter already. ✨[/]\n")
            break

        else:
            console.print("[red]Invalid option.[/] Try again.")


if __name__ == "__main__":
    main()
