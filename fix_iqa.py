import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from monitoring.models import Reading

def fix_missing_iqa():
    readings = Reading.objects.filter(iqa__isnull=True)
    count = readings.count()
    print(f"Found {count} readings with missing IQA.")
    
    updated = 0
    for r in readings:
        if r.pm25 is not None:
            # Simple formula: PM2.5 * 2 (as used in sync script)
            r.iqa = int(r.pm25 * 2)
            r.save()
            updated += 1
            
    print(f"Updated {updated} readings.")

if __name__ == "__main__":
    fix_missing_iqa()
