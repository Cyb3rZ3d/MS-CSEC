import random
from typing import List

import numpy as np
import pandas as pd


# ---------------------------
# CONFIG
# ---------------------------

CSV_PATH = r"C:\Users\rubva\GitHub\MS-CSEC\PowerBall ML\lottotexas.csv"

WHITE_MIN, WHITE_MAX = 1, 69
SPECIAL_MIN, SPECIAL_MAX = 1, 26
PLAYS_PER_MODE = 2  # number of tickets per scenario


# ---------------------------
# UTILITIES
# ---------------------------

def is_prime(n: int) -> bool:
    """Simple primality test for small n."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    r = int(n ** 0.5)
    for k in range(3, r + 1, 2):
        if n % k == 0:
            return False
    return True


def sample_uniform_whites(allowed_numbers: np.ndarray, k: int = 5) -> List[int]:
    """Uniform sampling of k unique white balls from allowed_numbers."""
    sample = random.sample(allowed_numbers.tolist(), k)
    sample.sort()
    return sample


def sample_uniform_special(allowed_numbers: np.ndarray) -> int:
    """Uniform sampling of one special ball from allowed_numbers."""
    return int(random.choice(allowed_numbers.tolist()))


def sample_whites_with_even_odd(
    allowed_numbers: np.ndarray,
    k: int = 5,
    max_tries: int = 50
) -> List[int]:
    """
    Sample k unique whites from allowed_numbers, enforcing that the
    resulting set has at least one even and one odd.
    """
    nums = allowed_numbers.tolist()
    last = None
    for _ in range(max_tries):
        sample = random.sample(nums, k)
        sample.sort()
        last = sample
        odds = sum(1 for x in sample if x % 2 == 1)
        evens = k - odds
        if odds > 0 and evens > 0:
            return sample
    # fallback if constraint can't be satisfied within max_tries
    return last


def least_used_pool(
    counts: np.ndarray,
    all_numbers: np.ndarray,
    present_mask: np.ndarray,
    needed: int
) -> np.ndarray:
    """
    Build a pool of numbers corresponding to the smallest nonzero counts,
    accumulating until we have at least 'needed' numbers.
    """
    # Filter to numbers that actually appear (count > 0)
    pos_mask = (present_mask & (counts > 0))
    if not pos_mask.any():
        # No numbers present; just return whatever present_mask gives
        return all_numbers[present_mask]

    pos_counts = counts[pos_mask]
    unique_counts = sorted(set(pos_counts))
    selected_mask = np.zeros_like(present_mask, dtype=bool)

    for c in unique_counts:
        selected_mask |= ((counts == c) & pos_mask)
        if selected_mask.sum() >= needed:
            break

    pool = all_numbers[selected_mask]
    if pool.size == 0:
        # fallback to all present numbers
        pool = all_numbers[present_mask]
    return pool


def format_ticket(whites: List[int], special: int) -> str:
    whites_str = " ".join(f"{w:02d}" for w in whites)
    return f"{whites_str} | SP {special:02d}"


# ---------------------------
# DATA LOADING & COUNTS
# ---------------------------

def normalize_history(csv_path: str) -> pd.DataFrame:
    """
    Load and normalize Lotto Texas CSV in this format (NO header row):

        Game Name, Month, Day, Year, Num1, Num2, Num3, Num4, Num5, Num6
    """
    df_raw = pd.read_csv(
        csv_path,
        header=None,
        names=[
            "game_name",
            "month",
            "day",
            "year",
            "num1",
            "num2",
            "num3",
            "num4",
            "num5",
            "num6",
        ],
    )

    date_series = pd.to_datetime(
        {
            "year": df_raw["year"].astype(int),
            "month": df_raw["month"].astype(int),
            "day": df_raw["day"].astype(int),
        },
        errors="coerce",
    )

    normalized_rows = []
    for idx, row in df_raw.iterrows():
        date = date_series.iloc[idx]
        if pd.isna(date):
            continue

        game_name = str(row["game_name"]).strip()

        whites = [
            int(row["num1"]),
            int(row["num2"]),
            int(row["num3"]),
            int(row["num4"]),
            int(row["num5"]),
        ]
        special = int(row["num6"])

        normalized_rows.append(
            {
                "date": date,
                "game_name": game_name,
                "w1": whites[0],
                "w2": whites[1],
                "w3": whites[2],
                "w4": whites[3],
                "w5": whites[4],
                "special": special,
            }
        )

    return pd.DataFrame(normalized_rows)


def build_frequency_counts(df: pd.DataFrame):
    """
    Build raw frequency counts for white and special numbers
    across the full Powerball ranges (1–69, 1–26).
    """
    white_counts = np.zeros(WHITE_MAX, dtype=float)      # index 0 -> number 1
    special_counts = np.zeros(SPECIAL_MAX, dtype=float)  # index 0 -> number 1

    white_cols = ["w1", "w2", "w3", "w4", "w5"]

    for _, row in df.iterrows():
        for c in white_cols:
            w = int(row[c])
            if WHITE_MIN <= w <= WHITE_MAX:
                white_counts[w - 1] += 1

        s = int(row["special"])
        if SPECIAL_MIN <= s <= SPECIAL_MAX:
            special_counts[s - 1] += 1

    white_numbers = np.arange(WHITE_MIN, WHITE_MAX + 1, dtype=int)
    special_numbers = np.arange(SPECIAL_MIN, SPECIAL_MAX + 1, dtype=int)

    return white_numbers, white_counts, special_numbers, special_counts


# ---------------------------
# GROUP 1: THEORETICAL POWERBALL RANGE (NO CSV RESTRICTION)
# ---------------------------

def group1_random_full(white_numbers, special_numbers):
    print("\n--- Group 1: Theoretical Powerball Range (no CSV restriction) ---")
    # 1) Random numbers
    print("\n1) Random numbers")
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(white_numbers, k=5)
        sp = sample_uniform_special(special_numbers)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 2) Random even and odd numbers (ensure both even & odd in whites)
    print("\n2) Random even and odd numbers (whites must include both)")
    for i in range(PLAYS_PER_MODE):
        whites = sample_whites_with_even_odd(white_numbers, k=5)
        sp = sample_uniform_special(special_numbers)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 3) Random prime and even numbers (numbers that are prime OR even)
    print("\n3) Random prime and even numbers (prime OR even)")
    white_mask = np.array(
        [is_prime(n) or (n % 2 == 0) for n in white_numbers], dtype=bool
    )
    special_mask = np.array(
        [is_prime(n) or (n % 2 == 0) for n in special_numbers], dtype=bool
    )
    white_pool = white_numbers[white_mask]
    special_pool = special_numbers[special_mask]
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(white_pool, k=5)
        sp = sample_uniform_special(special_pool)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 4) Random prime and odd numbers (prime OR odd)
    print("\n4) Random prime and odd numbers (prime OR odd)")
    white_mask = np.array(
        [is_prime(n) or (n % 2 == 1) for n in white_numbers], dtype=bool
    )
    special_mask = np.array(
        [is_prime(n) or (n % 2 == 1) for n in special_numbers], dtype=bool
    )
    white_pool = white_numbers[white_mask]
    special_pool = special_numbers[special_mask]
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(white_pool, k=5)
        sp = sample_uniform_special(special_pool)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 5) Random prime numbers only
    print("\n5) Random prime numbers only")
    white_mask = np.array([is_prime(n) for n in white_numbers], dtype=bool)
    special_mask = np.array([is_prime(n) for n in special_numbers], dtype=bool)
    white_pool = white_numbers[white_mask]
    special_pool = special_numbers[special_mask]
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(white_pool, k=5)
        sp = sample_uniform_special(special_pool)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")


# ---------------------------
# GROUP 2: ONLY USING NUMBERS THAT APPEAR IN THE CSV
# ---------------------------

def group2_csv_based(
    white_numbers,
    white_counts,
    special_numbers,
    special_counts,
):
    print("\n--- Group 2: Using ONLY numbers that appear in the CSV ---")

    white_present_mask = white_counts > 0
    special_present_mask = special_counts > 0

    white_from_csv = white_numbers[white_present_mask]
    special_from_csv = special_numbers[special_present_mask]

    # Helper: filter pool by condition, fallback to unfiltered pool if too small
    def filtered_pool(pool_numbers, cond_mask, min_needed):
        sub = pool_numbers[cond_mask]
        if sub.size >= min_needed:
            return sub
        return pool_numbers  # fallback

    # 1) Random - Select any numbers within the CSV
    print("\n1) Random - Select any numbers within the CSV")
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(white_from_csv, k=5)
        sp = sample_uniform_special(special_from_csv)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 2) Random even and odd numbers (whites must include both parity)
    print("\n2) Random even and odd numbers (CSV; whites must include both)")
    for i in range(PLAYS_PER_MODE):
        whites = sample_whites_with_even_odd(white_from_csv, k=5)
        sp = sample_uniform_special(special_from_csv)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 3) Random prime and even numbers (CSV; prime OR even)
    print("\n3) Random prime and even numbers (CSV; prime OR even)")
    w_mask_pe = np.array(
        [is_prime(n) or (n % 2 == 0) for n in white_from_csv], dtype=bool
    )
    s_mask_pe = np.array(
        [is_prime(n) or (n % 2 == 0) for n in special_from_csv], dtype=bool
    )
    w_pool_pe = filtered_pool(white_from_csv, w_mask_pe, min_needed=5)
    s_pool_pe = filtered_pool(special_from_csv, s_mask_pe, min_needed=1)
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(w_pool_pe, k=5)
        sp = sample_uniform_special(s_pool_pe)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 4) Random prime and odd numbers (CSV; prime OR odd)
    print("\n4) Random prime and odd numbers (CSV; prime OR odd)")
    w_mask_po = np.array(
        [is_prime(n) or (n % 2 == 1) for n in white_from_csv], dtype=bool
    )
    s_mask_po = np.array(
        [is_prime(n) or (n % 2 == 1) for n in special_from_csv], dtype=bool
    )
    w_pool_po = filtered_pool(white_from_csv, w_mask_po, min_needed=5)
    s_pool_po = filtered_pool(special_from_csv, s_mask_po, min_needed=1)
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(w_pool_po, k=5)
        sp = sample_uniform_special(s_pool_po)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 5) Random prime numbers (CSV; prime only)
    print("\n5) Random prime numbers (CSV; prime only)")
    w_mask_p = np.array([is_prime(n) for n in white_from_csv], dtype=bool)
    s_mask_p = np.array([is_prime(n) for n in special_from_csv], dtype=bool)
    w_pool_p = filtered_pool(white_from_csv, w_mask_p, min_needed=5)
    s_pool_p = filtered_pool(special_from_csv, s_mask_p, min_needed=1)
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(w_pool_p, k=5)
        sp = sample_uniform_special(s_pool_p)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # ------- LEAST-USED VARIANTS -------

    # Precompute least-used pools (no extra filters yet)
    least_white_pool = least_used_pool(
        white_counts,
        white_numbers,
        white_present_mask,
        needed=5,
    )
    least_special_pool = least_used_pool(
        special_counts,
        special_numbers,
        special_present_mask,
        needed=1,
    )

    # 6) Random - least used numbers
    print("\n6) Random - least used numbers (CSV)")
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(least_white_pool, k=5)
        sp = sample_uniform_special(least_special_pool)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 7) Random - least used even and odd numbers (whites must include both)
    print("\n7) Random - least used even and odd numbers (CSV; whites both parity)")
    for i in range(PLAYS_PER_MODE):
        whites = sample_whites_with_even_odd(least_white_pool, k=5)
        sp = sample_uniform_special(least_special_pool)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 8) Random - least used prime and even numbers (prime OR even)
    print("\n8) Random - least used prime and even numbers (CSV; prime OR even)")
    lw_mask_pe = np.array(
        [is_prime(n) or (n % 2 == 0) for n in least_white_pool], dtype=bool
    )
    ls_mask_pe = np.array(
        [is_prime(n) or (n % 2 == 0) for n in least_special_pool], dtype=bool
    )
    lw_pool_pe = filtered_pool(least_white_pool, lw_mask_pe, min_needed=5)
    ls_pool_pe = filtered_pool(least_special_pool, ls_mask_pe, min_needed=1)
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(lw_pool_pe, k=5)
        sp = sample_uniform_special(ls_pool_pe)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 9) Random - least used prime and odd numbers (prime OR odd)
    print("\n9) Random - least used prime and odd numbers (CSV; prime OR odd)")
    lw_mask_po = np.array(
        [is_prime(n) or (n % 2 == 1) for n in least_white_pool], dtype=bool
    )
    ls_mask_po = np.array(
        [is_prime(n) or (n % 2 == 1) for n in least_special_pool], dtype=bool
    )
    lw_pool_po = filtered_pool(least_white_pool, lw_mask_po, min_needed=5)
    ls_pool_po = filtered_pool(least_special_pool, ls_mask_po, min_needed=1)
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(lw_pool_po, k=5)
        sp = sample_uniform_special(ls_pool_po)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")

    # 10) Random - least prime numbers
    print("\n10) Random - least prime numbers (CSV; prime only)")
    lw_mask_p = np.array([is_prime(n) for n in least_white_pool], dtype=bool)
    ls_mask_p = np.array([is_prime(n) for n in least_special_pool], dtype=bool)
    lw_pool_p = filtered_pool(least_white_pool, lw_mask_p, min_needed=5)
    ls_pool_p = filtered_pool(least_special_pool, ls_mask_p, min_needed=1)
    for i in range(PLAYS_PER_MODE):
        whites = sample_uniform_whites(lw_pool_p, k=5)
        sp = sample_uniform_special(ls_pool_p)
        print(f"Play {i+1}: {format_ticket(whites, sp)}")


# ---------------------------
# MAIN FUNCTION
# ---------------------------

def main():
    df = normalize_history(CSV_PATH)
    white_numbers, white_counts, special_numbers, special_counts = build_frequency_counts(df)

    print(f"Using data from {df['date'].min().date()} to {df['date'].max().date()}")

    # Group 1: full theoretical ranges, no CSV restriction
    group1_random_full(white_numbers, special_numbers)

    # Group 2: only using numbers that actually appear in the CSV
    group2_csv_based(
        white_numbers,
        white_counts,
        special_numbers,
        special_counts,
    )


# ---------------------------
# ENTRY POINT
# ---------------------------

if __name__ == "__main__":
    main()
