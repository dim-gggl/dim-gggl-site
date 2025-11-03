#!/usr/bin/env python
"""
Interactive script to review and update technology proficiency levels.
Run with: python manage.py shell < scripts/update_proficiency.py
Or: python scripts/update_proficiency.py
"""
import os
import sys
import django

# Setup Django environment if running standalone
if __name__ == "__main__":
    # Add the project root to the path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_dimitri.settings")

    # Disable cache to avoid Redis connection issues during updates
    os.environ["DISABLE_CACHE"] = "1"

    django.setup()

from django.db.models.signals import post_save, post_delete
from projects.models import Technology
from projects.signals import invalidate_sidebar_cache


def get_star_display(level):
    """Return a visual star rating."""
    return "★" * level + "☆" * (5 - level)


def get_color_code(level):
    """Return color code based on proficiency level."""
    colors = {
        1: "\033[91m",  # Red
        2: "\033[93m",  # Yellow
        3: "\033[94m",  # Blue
        4: "\033[96m",  # Cyan
        5: "\033[92m",  # Green
    }
    return colors.get(level, "\033[0m")


def reset_color():
    """Reset terminal color."""
    return "\033[0m"


def display_technology(tech, index):
    """Display technology info with formatting."""
    color = get_color_code(tech.proficiency)
    stars = get_star_display(tech.proficiency)

    print(f"\n{color}{'=' * 60}{reset_color()}")
    print(f"{color}[{index}] {tech.name.upper()}{reset_color()}")
    print(f"{color}{'=' * 60}{reset_color()}")
    print(f"  Category:    {tech.category}")
    print(f"  Current:     {stars} ({tech.proficiency}/5)")
    print(f"  Icon:        {tech.icon or 'None'}")
    print(f"  Color:       {tech.color}")
    print(f"  Projects:    {tech.projects.count()}")


def get_valid_input(prompt, valid_options):
    """Get and validate user input."""
    while True:
        response = input(prompt).strip().lower()
        if response in valid_options:
            return response
        print(f"❌ Invalid input. Please enter one of: {', '.join(valid_options)}")


def update_proficiency_interactive():
    """Main interactive function to review and update proficiency levels."""
    # Disconnect signals to avoid Redis connection issues during batch updates
    print("\n⚙️  Temporarily disabling cache invalidation signals...")
    post_save.disconnect(invalidate_sidebar_cache, sender=Technology)
    post_delete.disconnect(invalidate_sidebar_cache, sender=Technology)

    technologies = Technology.objects.all().order_by("category", "name")
    total = technologies.count()

    if total == 0:
        print("❌ No technologies found in the database.")
        # Reconnect signals before returning
        post_save.connect(invalidate_sidebar_cache, sender=Technology)
        post_delete.connect(invalidate_sidebar_cache, sender=Technology)
        return

    print("\n" + "=" * 60)
    print("🎯 TECHNOLOGY PROFICIENCY UPDATE TOOL")
    print("=" * 60)
    print(f"\n📊 Found {total} technologies to review\n")
    print("Commands:")
    print("  1-5: Set proficiency level")
    print("  s:   Skip this technology")
    print("  q:   Quit and save changes")
    print("  v:   View all technologies summary")
    print("=" * 60)

    updated_count = 0
    skipped_count = 0

    for index, tech in enumerate(technologies, 1):
        display_technology(tech, f"{index}/{total}")

        # Get user action
        action = get_valid_input(
            "\n➡️  Action [1-5/s/q/v]: ",
            ["1", "2", "3", "4", "5", "s", "skip", "q", "quit", "v", "view"],
        )

        # Handle view command
        if action in ["v", "view"]:
            print("\n" + "=" * 60)
            print("📋 TECHNOLOGIES SUMMARY")
            print("=" * 60)
            for t in technologies:
                stars = get_star_display(t.proficiency)
                print(f"  {t.name:<30} {stars} ({t.proficiency}/5) - {t.category}")
            print("=" * 60)

            # Ask again for this technology
            action = get_valid_input(
                f"\n➡️  Action for {tech.name} [1-5/s/q]: ",
                ["1", "2", "3", "4", "5", "s", "skip", "q", "quit"],
            )

        # Handle quit command
        if action in ["q", "quit"]:
            print(f"\n✅ Quitting. Updated: {updated_count}, Skipped: {skipped_count}")
            break

        # Handle skip command
        if action in ["s", "skip"]:
            print(f"⏭️  Skipped {tech.name}")
            skipped_count += 1
            continue

        # Handle proficiency update
        new_level = int(action)
        old_level = tech.proficiency

        if new_level != old_level:
            tech.proficiency = new_level
            tech.save()
            new_stars = get_star_display(new_level)
            print(f"✅ Updated {tech.name}: {old_level}/5 → {new_level}/5 {new_stars}")
            updated_count += 1
        else:
            print(f"➖ No change for {tech.name}")
            skipped_count += 1

    # Reconnect signals
    print("\n⚙️  Reconnecting cache invalidation signals...")
    post_save.connect(invalidate_sidebar_cache, sender=Technology)
    post_delete.connect(invalidate_sidebar_cache, sender=Technology)

    # Final summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    print(f"  Total technologies:  {total}")
    print(f"  Updated:             {updated_count}")
    print(f"  Skipped:             {skipped_count}")
    print(f"  Reviewed:            {updated_count + skipped_count}/{total}")
    print("=" * 60 + "\n")

    # Show final distribution
    print("🎯 PROFICIENCY DISTRIBUTION:")
    for level in range(1, 6):
        count = technologies.filter(proficiency=level).count()
        stars = get_star_display(level)
        bar = "█" * count
        print(f"  {stars} ({level}/5): {bar} {count}")
    print("=" * 60 + "\n")

    # Manual cache invalidation (will work if Redis is running)
    try:
        from django.core.cache import cache

        cache.delete("project_list_sidebar_data")
        print("✅ Cache invalidated successfully")
    except Exception as e:
        print(f"⚠️  Could not invalidate cache (Redis not running?): {e}")
        print("   Cache will be refreshed automatically when Redis is available.")


if __name__ == "__main__":
    try:
        update_proficiency_interactive()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Changes up to this point have been saved.")
        # Ensure signals are reconnected even on interrupt
        try:
            post_save.connect(invalidate_sidebar_cache, sender=Technology)
            post_delete.connect(invalidate_sidebar_cache, sender=Technology)
            print("✅ Signals reconnected")
        except Exception:
            pass
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        # Ensure signals are reconnected even on error
        try:
            post_save.connect(invalidate_sidebar_cache, sender=Technology)
            post_delete.connect(invalidate_sidebar_cache, sender=Technology)
            print("✅ Signals reconnected")
        except Exception:
            pass
        sys.exit(1)
