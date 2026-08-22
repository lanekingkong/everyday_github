#!/usr/bin/env python3
"""
Cryptographic Password Generator
XKCD-style passphrases + high-entropy random passwords with strength estimation.
"""
import secrets
import math
import os


WORDLIST_PATH = os.path.join(os.path.dirname(__file__), "wordlist.txt")

# Default wordlist (EFF large wordlist)
DEFAULT_WORDS = [
    "apple", "banana", "carrot", "dolphin", "elephant", "flamingo", "guitar",
    "harmony", "island", "jungle", "kayak", "lantern", "mountain", "napkin",
    "october", "penguin", "quartz", "rocket", "sunset", "tornado", "umbrella",
    "violet", "walnut", "xenon", "yogurt", "zebra", "anchor", "breeze",
    "cactus", "diamond", "emerald", "forest", "galaxy", "horizon", "icicle",
    "jasper", "koala", "lemon", "mango", "nebula", "orchid", "pepper",
    "quicksand", "rainbow", "sapphire", "thunder", "universe", "voyager",
    "whistle", "acorn", "badge", "cabin", "dagger", "eagle", "falcon",
    "garden", "helmet", "igloo", "jigsaw", "kitten", "llama", "magnet",
    "noodle", "oasis", "pearl", "quiver", "raccoon", "shamrock", "tulip",
    "ukulele", "viper", "walrus", "acrobat", "bonfire", "crystal", "dragon",
    "echo", "feather", "glacier", "hedge", "insect", "jupiter", "karate",
    "lotus", "marble", "nutmeg", "onyx", "puzzle", "quasar", "robin",
    "saddle", "trophy", "urchin", "velvet", "willow", "zeppelin", "aurora",
    "blizzard", "comet", "dusk", "ember", "frost", "gale", "haven",
]


def load_wordlist():
    if os.path.exists(WORDLIST_PATH):
        with open(WORDLIST_PATH, "r") as f:
            return [w.strip() for w in f if w.strip() and not w.startswith("#")]
    return DEFAULT_WORDS


def passphrase(num_words: int = 4, separator: str = "-", capitalize: bool = False) -> str:
    """Generate an XKCD-style passphrase using random words."""
    words = load_wordlist()
    chosen = [secrets.choice(words) for _ in range(num_words)]
    if capitalize:
        chosen = [w.capitalize() for w in chosen]
    return separator.join(chosen)


def random_password(length: int = 20, include_special: bool = True) -> str:
    """Generate a high-entropy random password."""
    import string
    alphabet = string.ascii_letters + string.digits
    if include_special:
        alphabet += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def estimate_entropy(password: str, method: str = "passphrase") -> dict:
    """Estimate password strength in bits of entropy and crack time."""
    if method == "passphrase":
        wordlist_size = len(load_wordlist())
        num_words = len(password.split("-"))
        entropy = num_words * math.log2(wordlist_size)
    else:
        import string
        pool = 0
        for charset, name in [
            (string.ascii_lowercase, "lower"),
            (string.ascii_uppercase, "upper"),
            (string.digits, "digits"),
            ("!@#$%^&*()-_=+[]{}|;:,.<>?", "special"),
        ]:
            if any(c in password for c in charset):
                pool += len(charset)
        entropy = len(password) * math.log2(max(pool, 1))

    # Crack time estimates (1 billion guesses/sec for online, 1 trillion for offline)
    seconds_online = 2 ** entropy / 1e9
    seconds_offline = 2 ** entropy / 1e12

    def format_time(seconds):
        if seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.0f} min"
        elif seconds < 86400:
            return f"{seconds/3600:.0f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.0f} days"
        elif seconds < 3153600000:
            return f"{seconds/31536000:.0f} years"
        else:
            return f"{seconds/31536000/1e9:.1f}B years"

    return {
        "entropy_bits": round(entropy, 1),
        "crack_online": format_time(seconds_online),
        "crack_offline": format_time(seconds_offline),
        "strength": (
            "🔴 Weak" if entropy < 40 else
            "🟡 Fair" if entropy < 60 else
            "🟢 Strong" if entropy < 90 else
            "🟣 Very Strong"
        ),
    }


if __name__ == "__main__":
    print("🔐 Password Generator\n")

    for words in [3, 4, 5, 6]:
        pp = passphrase(num_words=words, separator="-")
        est = estimate_entropy(pp, "passphrase")
        print(f"  {est['strength']} ({words} words): {pp}")
        print(f"       Entropy: {est['entropy_bits']} bits | Online: {est['crack_online']} | Offline: {est['crack_offline']}\n")

    print("─" * 55)
    print("Random passwords:\n")

    for length in [12, 16, 20, 24]:
        pw = random_password(length)
        est = estimate_entropy(pw, "random")
        print(f"  {est['strength']} ({length} chars): {pw}")
        print(f"       Entropy: {est['entropy_bits']} bits | Online: {est['crack_online']}\n")
