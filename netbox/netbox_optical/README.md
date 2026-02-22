# NetBox Optical Plugin (Prototype)

> **Status:** Prototype / RFC — not for production use.
>
> This plugin is a working proof-of-concept for WDM (DWDM/CWDM) and optical-layer modeling in NetBox.
> It is intended for internal evaluation and feedback from domain experts.

## What This Plugin Does

NetBox Optical adds a set of models to NetBox that represent the **optical layer** — the
layer between physical cabling (which NetBox handles well) and logical/IP networking
(which NetBox also handles well). Today this middle layer is essentially absent from
the NetBox data model.

The plugin provides:

1. **Wavelength grids and channels** — Define standard or custom wavelength grids (ITU-T DWDM, CWDM, flex-grid) and their individual channels.
2. **Optical circuits (lightpaths)** — Model end-to-end wavelength services with ordered hops through physical interfaces, associated with a specific channel and optionally a tenant/customer.
3. **Multiplex groups** — Represent the internal MUX/DEMUX relationship where multiple client ports map to a single line port, with per-client-port channel assignments.

## Concepts

### Wavelength Grids and Channels

A **WavelengthGrid** represents a standardised or custom set of channel slots. For example:

- "ITU-T C-band 50 GHz" — the standard DWDM grid with ~80 channels
- "CWDM" — 18 channels at 20 nm spacing
- A custom grid for a specific vendor's equipment

Each grid contains **WavelengthChannel** entries that define the individual slots: a name
(e.g., "C21"), center frequency in GHz, center wavelength in nm, and optionally a channel
width for flex-grid allocations.

### Optical Circuits

An **OpticalCircuit** represents a lightpath — a wavelength service running end-to-end
across the network on a specific channel. It answers the question: *"This customer's
100G service is running on channel C21, and it traverses these interfaces on these devices
in this order."*

Each optical circuit has:
- A **channel** (which wavelength it uses)
- A **status** (planned, provisioning, active, decommissioning, decommissioned)
- An optional **tenant** (the customer or service owner)
- An ordered set of **hops** through device interfaces

An **OpticalCircuitHop** records a single stop in the lightpath. Each hop references a
specific interface on a device and includes a **port role** indicating whether the
interface is acting as a client port, line port, add port, drop port, or express
(pass-through) port at that point in the path.

### Multiplex Groups

A **MultiplexGroup** models the internal optical relationship within a MUX, DEMUX,
transponder, or ROADM where multiple client-side ports combine onto a single line-side
(network) port. This is the "many client ports → one line port" relationship that
NetBox currently cannot represent.

Each multiplex group has:
- A **device** (the MUX/DEMUX/transponder)
- A **line interface** (the aggregate network-side port)
- One or more **members** (client ports), each optionally assigned to a wavelength channel

This allows you to answer questions like:
- "Which client ports feed into this line port?"
- "What wavelength is assigned to each client port?"
- "How many channels are in use vs. available on this MUX?"

## Installation (for internal testing)

### 1. Enable the plugin

Add to your NetBox `configuration.py`:

```python
PLUGINS = [
    'netbox_optical',
]
```

### 2. Run migrations

```bash
cd netbox
python manage.py migrate netbox_optical
```

### 3. Restart NetBox

Restart the NetBox service. The plugin will appear as an "Optical" menu in the
navigation bar.

## API Endpoints

All models are exposed via the REST API at `/api/plugins/optical/`:

| Endpoint | Description |
|----------|-------------|
| `/api/plugins/optical/wavelength-grids/` | Wavelength grids (CRUD) |
| `/api/plugins/optical/wavelength-channels/` | Wavelength channels (CRUD) |
| `/api/plugins/optical/optical-circuits/` | Optical circuits / lightpaths (CRUD) |
| `/api/plugins/optical/optical-circuit-hops/` | Lightpath hops (CRUD) |
| `/api/plugins/optical/multiplex-groups/` | Multiplex groups (CRUD) |
| `/api/plugins/optical/multiplex-group-members/` | Multiplex group members (CRUD) |

## Testing Walkthrough

This walkthrough demonstrates the core functionality using a realistic scenario.

### Scenario: Modeling a 16-channel DWDM MUX with two active customer circuits

#### Step 1: Create a wavelength grid

```
POST /api/plugins/optical/wavelength-grids/
{
    "name": "ITU-T C-band 100 GHz",
    "grid_type": "dwdm-100ghz",
    "description": "Standard ITU-T DWDM C-band grid at 100 GHz spacing"
}
```

#### Step 2: Create channels on the grid

Create a few channels (in practice you'd create all ~40 for the 100 GHz grid):

```
POST /api/plugins/optical/wavelength-channels/
{
    "grid": <grid_id>,
    "name": "C21",
    "frequency_ghz": 192100.00,
    "wavelength_nm": 1560.6100
}
```

```
POST /api/plugins/optical/wavelength-channels/
{
    "grid": <grid_id>,
    "name": "C22",
    "frequency_ghz": 192200.00,
    "wavelength_nm": 1559.7900
}
```

#### Step 3: Create a multiplex group on a MUX device

Assuming you already have a device "MUX-SITE-A" with interfaces defined
(e.g., "Network 1" as the line port, "Client 1" through "Client 16" as client ports):

```
POST /api/plugins/optical/multiplex-groups/
{
    "name": "MUX-SITE-A Primary",
    "device": <device_id>,
    "line_interface": <network_1_interface_id>
}
```

#### Step 4: Add client ports to the multiplex group with channel assignments

```
POST /api/plugins/optical/multiplex-group-members/
{
    "group": <group_id>,
    "client_interface": <client_1_interface_id>,
    "channel": <c21_channel_id>
}
```

```
POST /api/plugins/optical/multiplex-group-members/
{
    "group": <group_id>,
    "client_interface": <client_2_interface_id>,
    "channel": <c22_channel_id>
}
```

#### Step 5: Create an optical circuit (lightpath)

```
POST /api/plugins/optical/optical-circuits/
{
    "name": "ACME-Corp-100G-East",
    "channel": <c21_channel_id>,
    "status": "active",
    "tenant": <acme_tenant_id>,
    "description": "ACME Corp 100G service, eastbound"
}
```

#### Step 6: Define the lightpath hops

```
POST /api/plugins/optical/optical-circuit-hops/
{"optical_circuit": <circuit_id>, "sequence": 1, "interface": <transponder_client_port>, "port_role": "client"}

POST /api/plugins/optical/optical-circuit-hops/
{"optical_circuit": <circuit_id>, "sequence": 2, "interface": <mux_client_1>, "port_role": "client"}

POST /api/plugins/optical/optical-circuit-hops/
{"optical_circuit": <circuit_id>, "sequence": 3, "interface": <mux_network_1>, "port_role": "line"}

POST /api/plugins/optical/optical-circuit-hops/
{"optical_circuit": <circuit_id>, "sequence": 4, "interface": <remote_demux_network_1>, "port_role": "line"}

POST /api/plugins/optical/optical-circuit-hops/
{"optical_circuit": <circuit_id>, "sequence": 5, "interface": <remote_demux_client_1>, "port_role": "drop"}
```

You can now:
- View the optical circuit to see its full hop-by-hop path
- View the multiplex group to see which channels are in use
- Query optical circuits by tenant to find all of ACME Corp's wavelength services
- Query optical circuit hops by interface to find what lightpaths traverse a given port

## What This Prototype Does NOT Cover (Yet)

These are identified as important but deferred to keep the MVP focused:

- **ROADM routing logic** — Modeling how ROADMs route specific wavelengths between degrees
- **Flex-grid spectrum management** — Tracking contiguous spectral blocks
- **OTN sub-wavelength multiplexing** — Modeling services multiplexed within a wavelength
- **Optical engineering parameters** — Span loss, launch power, OSNR, link budgets
- **Impact analysis** — Computing blast radius of fiber cuts or equipment failures
- **Optical/DWDM interface types** — Requires core NetBox changes (new InterfaceType choices)
- **L1 adjacencies** — Splitters, taps, TX/RX asymmetry, broadcast topology, photonic cross-connects

## Data Model Diagram

```
┌─────────────────┐
│ WavelengthGrid  │
│─────────────────│
│ name            │
│ grid_type       │
│ description     │
└────────┬────────┘
         │ 1:N
         ▼
┌──────────────────┐        ┌──────────────────────┐
│ WavelengthChannel│◄───────│ MultiplexGroupMember  │
│──────────────────│        │──────────────────────│
│ name             │        │ client_interface ─────┼──► dcim.Interface
│ frequency_ghz    │        │ channel (optional)    │
│ wavelength_nm    │        └──────────┬───────────┘
│ width_ghz        │                   │ N:1
└────────┬─────────┘                   ▼
         │                  ┌──────────────────────┐
         │                  │ MultiplexGroup        │
         │                  │──────────────────────│
         │                  │ name                  │
         │                  │ device ───────────────┼──► dcim.Device
         │                  │ line_interface ───────┼──► dcim.Interface
         │                  └──────────────────────┘
         │ 1:N
         ▼
┌──────────────────┐
│ OpticalCircuit   │
│──────────────────│
│ name             │
│ status           │
│ tenant ──────────┼──► tenancy.Tenant
│ description      │
└────────┬─────────┘
         │ 1:N
         ▼
┌──────────────────┐
│ OpticalCircuitHop│
│──────────────────│
│ sequence         │
│ interface ───────┼──► dcim.Interface
│ port_role        │
└──────────────────┘
```

## Feedback Requested

We are looking for feedback on:

1. **Model completeness** — Are these the right objects? Are we missing fields?
2. **Naming** — Do "OpticalCircuit", "MultiplexGroup", etc. make sense to optical engineers?
3. **Workflow** — Does the create-grid → create-channels → create-mux → create-circuit flow feel natural?
4. **Port roles** — Are client/line/add/drop/express the right set?
5. **What's most urgently missing** from the deferred list?
