"""Django management command to update technology proficiency levels interactively."""
from django.core.management.base import BaseCommand
from django.db.models.signals import post_save, post_delete

from projects.models import Technology
from projects.signals import invalidate_sidebar_cache


class Command(BaseCommand):
    """Interactive command to review and update technology proficiency levels."""
    
    help = 'Interactively update technology proficiency levels'

    def get_star_display(self, level):
        """Return a visual star rating."""
        return "★" * level + "☆" * (5 - level)

    def get_color_code(self, level):
        """Return color code based on proficiency level."""
        colors = {
            1: "\033[91m",  # Red
            2: "\033[93m",  # Yellow
            3: "\033[94m",  # Blue
            4: "\033[96m",  # Cyan
            5: "\033[92m",  # Green
        }
        return colors.get(level, "\033[0m")

    def reset_color(self):
        """Reset terminal color."""
        return "\033[0m"

    def display_technology(self, tech, index):
        """Display technology info with formatting."""
        color = self.get_color_code(tech.proficiency)
        stars = self.get_star_display(tech.proficiency)
        
        self.stdout.write(f"\n{color}{'=' * 60}{self.reset_color()}")
        self.stdout.write(f"{color}[{index}] {tech.name.upper()}{self.reset_color()}")
        self.stdout.write(f"{color}{'=' * 60}{self.reset_color()}")
        self.stdout.write(f"  Category:    {tech.category}")
        self.stdout.write(f"  Current:     {stars} ({tech.proficiency}/5)")
        self.stdout.write(f"  Icon:        {tech.icon or 'None'}")
        self.stdout.write(f"  Color:       {tech.color}")
        self.stdout.write(f"  Projects:    {tech.projects.count()}")

    def get_valid_input(self, prompt, valid_options):
        """Get and validate user input."""
        while True:
            response = input(prompt).strip().lower()
            if response in valid_options:
                return response
            self.stdout.write(
                self.style.ERROR(
                    f"Invalid input. Please enter one of: {', '.join(valid_options)}"
                )
            )

    def handle(self, *args, **options):
        """Execute the command."""
        # Disconnect signals to avoid Redis connection issues during batch updates
        self.stdout.write("⚙️  Temporarily disabling cache invalidation signals...")
        post_save.disconnect(invalidate_sidebar_cache, sender=Technology)
        post_delete.disconnect(invalidate_sidebar_cache, sender=Technology)
        
        technologies = Technology.objects.all().order_by('category', 'name')
        total = technologies.count()
        
        if total == 0:
            self.stdout.write(self.style.ERROR("No technologies found in the database."))
            # Reconnect signals before returning
            post_save.connect(invalidate_sidebar_cache, sender=Technology)
            post_delete.connect(invalidate_sidebar_cache, sender=Technology)
            return
        
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("🎯 TECHNOLOGY PROFICIENCY UPDATE TOOL")
        self.stdout.write("=" * 60)
        self.stdout.write(f"\n📊 Found {total} technologies to review\n")
        self.stdout.write("Commands:")
        self.stdout.write("  1-5: Set proficiency level")
        self.stdout.write("  s:   Skip this technology")
        self.stdout.write("  q:   Quit and save changes")
        self.stdout.write("  v:   View all technologies summary")
        self.stdout.write("=" * 60)
        
        updated_count = 0
        skipped_count = 0
        
        try:
            for index, tech in enumerate(technologies, 1):
                self.display_technology(tech, f"{index}/{total}")
                
                # Get user action
                action = self.get_valid_input(
                    f"\n➡️  Action [1-5/s/q/v]: ",
                    ["1", "2", "3", "4", "5", "s", "skip", "q", "quit", "v", "view"]
                )
                
                # Handle view command
                if action in ["v", "view"]:
                    self.stdout.write("\n" + "=" * 60)
                    self.stdout.write("📋 TECHNOLOGIES SUMMARY")
                    self.stdout.write("=" * 60)
                    for t in technologies:
                        stars = self.get_star_display(t.proficiency)
                        self.stdout.write(f"  {t.name:<30} {stars} ({t.proficiency}/5) - {t.category}")
                    self.stdout.write("=" * 60)
                    
                    # Ask again for this technology
                    action = self.get_valid_input(
                        f"\n➡️  Action for {tech.name} [1-5/s/q]: ",
                        ["1", "2", "3", "4", "5", "s", "skip", "q", "quit"]
                    )
                
                # Handle quit command
                if action in ["q", "quit"]:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"\n✅ Quitting. Updated: {updated_count}, Skipped: {skipped_count}"
                        )
                    )
                    break
                
                # Handle skip command
                if action in ["s", "skip"]:
                    self.stdout.write(f"⏭️  Skipped {tech.name}")
                    skipped_count += 1
                    continue
                
                # Handle proficiency update
                new_level = int(action)
                old_level = tech.proficiency
                
                if new_level != old_level:
                    tech.proficiency = new_level
                    tech.save()
                    new_stars = self.get_star_display(new_level)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"✅ Updated {tech.name}: {old_level}/5 → {new_level}/5 {new_stars}"
                        )
                    )
                    updated_count += 1
                else:
                    self.stdout.write(f"➖ No change for {tech.name}")
                    skipped_count += 1
        
        except KeyboardInterrupt:
            self.stdout.write(
                self.style.WARNING(
                    "\n\n⚠️  Interrupted by user. Changes up to this point have been saved."
                )
            )
        
        finally:
            # Reconnect signals
            self.stdout.write("\n⚙️  Reconnecting cache invalidation signals...")
            post_save.connect(invalidate_sidebar_cache, sender=Technology)
            post_delete.connect(invalidate_sidebar_cache, sender=Technology)
        
        # Final summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("📊 FINAL SUMMARY")
        self.stdout.write("=" * 60)
        self.stdout.write(f"  Total technologies:  {total}")
        self.stdout.write(f"  Updated:             {updated_count}")
        self.stdout.write(f"  Skipped:             {skipped_count}")
        self.stdout.write(f"  Reviewed:            {updated_count + skipped_count}/{total}")
        self.stdout.write("=" * 60 + "\n")
        
        # Show final distribution
        self.stdout.write("🎯 PROFICIENCY DISTRIBUTION:")
        for level in range(1, 6):
            count = technologies.filter(proficiency=level).count()
            stars = self.get_star_display(level)
            bar = "█" * count
            self.stdout.write(f"  {stars} ({level}/5): {bar} {count}")
        self.stdout.write("=" * 60 + "\n")
        
        # Manual cache invalidation (will work if Redis is running)
        try:
            from django.core.cache import cache
            cache.delete('project_list_sidebar_data')
            self.stdout.write(self.style.SUCCESS("✅ Cache invalidated successfully"))
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f"⚠️  Could not invalidate cache (Redis not running?): {e}"
                )
            )
            self.stdout.write("   Cache will be refreshed automatically when Redis is available.")

