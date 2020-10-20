from typing import TYPE_CHECKING

from ..core.notify_events import NotifyEventType
from ..core.utils import build_absolute_uri
from ..plugins.manager import get_plugins_manager
from . import events

if TYPE_CHECKING:
    from .models import ExportFile


def get_default_export_payload(export_file: "ExportFile") -> dict:
    user_id = export_file.user.id if export_file.user else None
    user_email = export_file.user.email if export_file.user else None
    app_id = export_file.app.id if export_file.app else None
    return {
        "user_id": user_id,
        "user_email": user_email,
        "app_id": app_id,
        "status": export_file.status,
        "message": export_file.message,
        "created_at": export_file.created_at,
        "updated_at": export_file.updated_at,
    }


def send_email_with_link_to_download_file(export_file: "ExportFile"):
    payload = get_default_export_payload(export_file)
    payload["csv_link"] = build_absolute_uri(export_file.content_file.url)

    manager = get_plugins_manager()
    manager.notify(NotifyEventType.CSV_PRODUCT_EXPORT_SUCCESS, payload)
    events.export_file_sent_event(export_file=export_file, user=export_file.user)


def send_export_failed_info(export_file: "ExportFile"):
    payload = get_default_export_payload(export_file)
    manager = get_plugins_manager()
    manager.notify(NotifyEventType.CSV_EXPORT_FAILED, payload)
    events.export_failed_info_sent_event(export_file=export_file, user=export_file.user)
