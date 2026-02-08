import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecowatch.settings')
django.setup()

from django_q.models import Schedule
from django.utils import timezone

name = 'Fetch Air Quality every 10 min'
s, created = Schedule.objects.get_or_create(
    name=name,
    defaults={
        'func': 'django.core.management.call_command',
        'args': '"fetch_air_quality"',
        'schedule_type': 'I',
        'minutes': 10,
        'next_run': timezone.now()
    }
)

if not created:
    s.schedule_type = 'I'
    s.minutes = 10
    s.save()

print(f"Schedule '{name}' status:")
print(f"- Created: {created}")
print(f"- Next run: {s.next_run}")
print(f"- Schedule type: {s.schedule_type}")
print(f"- Intervals (min): {s.minutes}")
print(f"- Total schedules: {Schedule.objects.count()}")
