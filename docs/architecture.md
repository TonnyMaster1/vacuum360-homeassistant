# Architecture

This project uses a two-layer architecture.

## Layer 1 - Python library

The Python library is responsible for communicating with the 360 cloud.

Responsibilities:

- Login
- Authentication
- Robot discovery
- Send commands
- Read robot state
- Read maps
- Decode protocol data

This layer must not depend on Home Assistant.

## Layer 2 - Home Assistant integration

The Home Assistant integration is responsible for exposing the robot inside Home Assistant.

Responsibilities:

- Config Flow
- Vacuum entity
- Sensors
- Selects
- Buttons
- Services
- Diagnostics
- Repairs

This layer uses the Python library.

## Why this architecture?

Separating the cloud library from the Home Assistant integration makes the project easier to maintain, test, and reuse.