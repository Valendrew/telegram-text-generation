class Counter:
    def __init__(self, threshold: int = 10) -> None:
        self.count = 0
        self.threshold = threshold

    def change_threshold(self, threshold: int):
        self.threshold = threshold

    def check_threshold(self) -> bool:
        return self.count >= self.threshold

    def increase_count(self):
        self.count += 1

    def reset_count(self):
        self.count = 0
