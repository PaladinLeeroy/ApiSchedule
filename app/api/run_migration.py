import sys
import os
# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.api.migrations.update_schedule_templates import upgrade as upgrade_schedule_templates
from app.api.migrations.add_full_semester import upgrade as upgrade_full_semester

if __name__ == '__main__':
    print("Starting migrations...")
    upgrade_schedule_templates()
    upgrade_full_semester()
    print("Migrations completed successfully!") 