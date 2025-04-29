from PyQt5.QtCore import QObject, QRunnable, QThreadPool, pyqtSignal

class WorkerSignals(QObject):
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
    finished = pyqtSignal()

class Task(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self):
        result = self.fn(*self.args, **self.kwargs, progress_callback=self.signals.progress)
        self.signals.result.emit(result)
        self.signals.finished.emit()

class TaskRunner:
    # Central thread pool manager
    
    def __init__(self):
        self.pool = QThreadPool.globalInstance()

    def submit(self, fn, *args, **kwargs) -> Task:
        task = Task(fn, *args, **kwargs)
        self.pool.start(task)
        return task
