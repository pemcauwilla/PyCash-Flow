class Observer:
    def update(self, data=None):
        raise NotImplementedError("Update method must be implemented!")

class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, data=None) -> None:
        for observer in self._observers:
            observer.update(data)