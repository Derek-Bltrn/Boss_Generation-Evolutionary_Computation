# Boss Generation - Evolutionary Computation

A 2D video game project that uses evolutionary computation to automatically generate and balance boss fights through genetic algorithms.

## Overview

Balancing boss difficulty is a common challenge in video game development. Different combinations of attack patterns, projectile speeds, firing rates, and movement behaviors can produce significantly different gameplay experiences.

This project explores the use of a **genetic algorithm** to discover boss configurations that achieve a target win rate of **70% against a simulated casual player**.

Instead of manually adjusting each parameter, the algorithm explores a large search space of possible configurations through selection, crossover, and mutation.

## How It Works

The game features a top-down 2D shooter where a player faces a single-phase boss in a combat encounter lasting up to **60 seconds**.

Each boss is represented by a **32-bit binary chromosome** encoding 10 configurable characteristics, including:

- Attack pattern and projectile count
- Projectile speed and firing rate
- Attack spread and accuracy
- Boss movement pattern and speed
- Attack warning time
- Boss health

To evaluate a configuration, a simulated player attempts to defeat the boss across **100 independent combat simulations**.

The genetic algorithm aims to discover multiple viable boss configurations with a win rate close to 70%, rather than identifying a single optimal design.

## Evolutionary Approach

The proposed genetic algorithm uses:

| Component | Method |
|---|---|
| Representation | 32-bit binary chromosome |
| Selection | Tournament selection (k = 3) |
| Crossover | Uniform crossover by genes |
| Mutation | Bit-flip mutation |
| Replacement | Generational with elitism |
| Fitness | Proximity to a 70% win rate |

The evolutionary approach will be compared against random search and hill climbing to evaluate its effectiveness.

## Technologies

- **Python** — Game logic, simulation, and evolutionary algorithms
- **Pygame** — 2D game visualization and player interaction
- **Git & GitHub** — Version control and project management

## Documentation

Detailed information about the project's design, implementation, methodology, experiments, and results is available in the project documentation.

**[View Project Documentation](https://docs.google.com/document/d/YOUR_DOCUMENT_ID/edit)**

## Project Goals

- Develop a functional 2D boss fight.
- Implement an accelerated combat simulation without graphical rendering.
- Create a simulated player with consistent characteristics.
- Evaluate boss difficulty through repeated combat simulations.
- Apply genetic algorithms to automatically balance boss configurations.
- Compare evolutionary optimization against baseline search methods.
- Analyze the diversity and performance of the generated bosses.

## License

This project is developed for educational purposes as part of the Evolutionary Computation course.