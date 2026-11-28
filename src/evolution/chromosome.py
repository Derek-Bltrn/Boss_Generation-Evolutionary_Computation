from src.game.boss import BossConfig, MovementPattern


PROJECTILE_SPEEDS = (100, 140, 180, 220, 260, 300, 340, 380)

FIRE_INTERVAL_TICKS = (
    150, 132, 116, 102, 90, 78, 68, 60,
    52, 45, 39, 34, 29, 25, 20, 15,
)

MOVEMENT_PATTERNS: tuple[MovementPattern, ...] = (
    "zigzag", "horizontal", "vertical", "oval",
)
MOVEMENT_SPEEDS = (40, 55, 70, 90, 105, 120, 135, 150)

PROJECTILE_RADII = (4, 4.5, 5, 5.5, 6, 6.5, 7, 8)

BOSS_HEALTH_VALUES = (
    40, 50, 55, 60, 65, 70, 75, 80,
    85, 90, 95, 100, 105, 110, 115, 120,
)


def decode_attack_patterns(bits: str) -> tuple[int, int, int]:
    """Decode the three 3-bit attack genes from a nine-bit segment."""
    if len(bits) != 9 or any(bit not in "01" for bit in bits):
        raise ValueError("Attack genes must contain exactly nine binary digits.")

    patterns = (int(bits[:3], 2), int(bits[3:6], 2), int(bits[6:], 2))
    if len(set(patterns)) != 3:
        raise ValueError("Attack genes must encode three distinct attack IDs.")

    return patterns


def decode_projectile_count(bits: str) -> int:
    """Decode the four-bit projectile count gene into a count from 1 to 16."""
    if len(bits) != 4 or any(bit not in "01" for bit in bits):
        raise ValueError("The projectile count gene must contain exactly four binary digits.")

    return int(bits, 2) + 1


def decode_projectile_speed(bits: str) -> int:
    """Decode the three-bit projectile speed gene into pixels per second."""
    if len(bits) != 3 or any(bit not in "01" for bit in bits):
        raise ValueError("The projectile speed gene must contain exactly three binary digits.")

    return PROJECTILE_SPEEDS[int(bits, 2)]


def decode_fire_interval(bits: str) -> int:
    """Decode the four-bit firing cadence gene into ticks between shots."""
    if len(bits) != 4 or any(bit not in "01" for bit in bits):
        raise ValueError("The firing cadence gene must contain exactly four binary digits.")

    return FIRE_INTERVAL_TICKS[int(bits, 2)]


def decode_movement_pattern(bits: str) -> MovementPattern:
    """Decode the two-bit boss movement pattern gene."""
    if len(bits) != 2 or any(bit not in "01" for bit in bits):
        raise ValueError("The movement pattern gene must contain exactly two binary digits.")

    return MOVEMENT_PATTERNS[int(bits, 2)]


def decode_movement_speed(bits: str) -> int:
    """Decode the three-bit boss movement speed gene into pixels per second."""
    if len(bits) != 3 or any(bit not in "01" for bit in bits):
        raise ValueError("The movement speed gene must contain exactly three binary digits.")

    return MOVEMENT_SPEEDS[int(bits, 2)]


def decode_projectile_radius(bits: str) -> float:
    """Decode the three-bit boss projectile radius gene into pixels."""
    if len(bits) != 3 or any(bit not in "01" for bit in bits):
        raise ValueError("The projectile radius gene must contain exactly three binary digits.")

    return PROJECTILE_RADII[int(bits, 2)]


def decode_boss_health(bits: str) -> int:
    """Decode the four-bit boss health gene into hit points from 40 to 120."""
    if len(bits) != 4 or any(bit not in "01" for bit in bits):
        raise ValueError("The boss health gene must contain exactly four binary digits.")

    return BOSS_HEALTH_VALUES[int(bits, 2)]


def decode_chromosome(bits: str) -> BossConfig:
    """Decode a 32-bit chromosome into a playable boss configuration."""
    if len(bits) != 32:
        raise ValueError("A boss chromosome must contain exactly 32 binary digits.")

    return BossConfig(
        attack_patterns=decode_attack_patterns(bits[:9]),
        projectile_count=decode_projectile_count(bits[9:13]),
        projectile_speed=decode_projectile_speed(bits[13:16]),
        fire_interval=decode_fire_interval(bits[16:20]),
        movement_pattern=decode_movement_pattern(bits[20:22]),
        movement_speed=decode_movement_speed(bits[22:25]),
        projectile_radius=decode_projectile_radius(bits[25:28]),
        max_health=decode_boss_health(bits[28:]),
    )
