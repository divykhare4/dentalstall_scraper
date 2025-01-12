from app.logger import logger


class NotificationBase:
    def notify(self, new_count: int, updated_count: int):
        """Notify about the scraping results - this should be overridden by subclasses"""
        raise NotImplementedError(
            "The 'notify' method must be implemented by subclasses."
        )


class LogBasedNotification(NotificationBase):
    def notify(self, new_count: int, updated_count: int):
        """Log the result of the notification"""
        logger.info(
            f"NOTIFICATION_LOGGED: {new_count} new products scraped and {updated_count} products updated."
        )


class EmailBasedNotification(NotificationBase):
    def notify(self, new_count: int, updated_count: int, recipient_email: str):
        """Notify via email"""
        # Email sending logic should be placed here
        logger.info(
            f"Email notification sent to {recipient_email}: {new_count} new products scraped and {updated_count} products updated."
        )


class SMSBasedNotification(NotificationBase):
    def notify(self, new_count: int, updated_count: int, recipient_phone: str):
        """Notify via SMS"""
        # SMS sending logic should be implemented here
        logger.info(
            f"SMS notification sent to {recipient_phone}: {new_count} new products scraped and {updated_count} products updated."
        )
