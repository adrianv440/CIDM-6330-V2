import csv
from pathlib import Path

from django.core.files import File
from django.db.models.signals import post_save

from .models import Bookmark


from .models import Bookmark

# Define a hypothetical messagebus and commands for domain events, similar to your allocation system


class MessageBus:
    @staticmethod
    def handle(command, unit_of_work):
        # Implement handling logic
        pass


class Commands:
    @staticmethod
    def CreateBatch(batch_id, sku, quantity, eta):
        # Command for creating a batch
        pass

    @staticmethod
    def Allocate(order_id, sku, quantity):
        # Command for allocating stock to an order
        pass


class FakeUnitOfWork:
    # Simulated unit of work
    def __init__(self):
        self.products = {}
        self.committed = False

    def commit(self):
        self.committed = True

# Define the receiver function for saving bookmarks to log


@receiver(post_save, sender=Bookmark)
def log_bookmark_to_csv(sender, instance, **kwargs):
    print("Bookmark was saved, logging to CSV.")
    file_path = Path(__file__).resolve().parent / "logs" / "bookmark_log.csv"
    with open(file_path, "a+", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            instance.id,
            instance.title,
            instance.url,
            instance.notes,
            instance.date_added.strftime('%Y-%m-%d %H:%M:%S')
        ])

    # Simulate a message bus handling
    uow = FakeUnitOfWork()
    MessageBus.handle(Commands.CreateBatch(
        "batch1", instance.title, 100, None), uow)
    result = MessageBus.handle(
        Commands.Allocate("o1", instance.title, 10), uow)
