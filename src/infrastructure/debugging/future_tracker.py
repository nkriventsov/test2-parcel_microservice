import asyncio

# Список для хранения всех Future и Task
all_futures = []


class TrackedFuture(asyncio.Future):
    """
    Класс для отслеживания всех созданных Future.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_futures.append(self)

    def __repr__(self):
        return (
            f"<TrackedFuture id={id(self)} done={self.done()} "
            f"result={self.result() if self.done() else None} "
            f"exception={self.exception() if self.done() else None} "
            f"loop={self.get_loop()}>"
        )


class TrackedTask(asyncio.Task):
    """
    Класс для отслеживания всех созданных Task.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_futures.append(self)

    def __repr__(self):
        return (
            f"<TrackedTask id={id(self)} name={self.get_name()} "
            f"done={self.done()} "
            f"result={self.result() if self.done() else None} "
            f"exception={self.exception() if self.done() else None} "
            f"loop={self.get_loop()}>"
        )

def get_all_futures_and_tasks():
    """
    Возвращает список всех Future и Task.
    """
    return all_futures


