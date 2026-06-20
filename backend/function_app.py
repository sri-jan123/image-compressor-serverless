from app_instance import app


# Import all trigger files so decorators are registered

import triggers.upload_image
import triggers.process_image
import triggers.get_history
import triggers.get_image_status
import triggers.download_image
