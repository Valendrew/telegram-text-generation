from .utils.Counter import Counter

commands = ["generate", "threshold"]
thresholds = {"low": 30, "normal": 20, "high": 10}
counter = Counter(thresholds["normal"])

from textgen.bot import (
    generate_sentence,
    increase_counter,
    set_threshold,
    threshold_message,
)
