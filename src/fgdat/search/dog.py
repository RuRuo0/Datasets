from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print("modified: {}".format(event.src_path))


if __name__ == "__main__":
    path = "F:/FormalGeo/data/formalized-problems"
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
