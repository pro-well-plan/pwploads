# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [v0.2.3] - 2020-12-17
### Added
- Load case: displacement to gas

## [v0.2.2] - 2020-12-08
### Added
- Bending stress due to wellbore trajectory

## [v0.2.0] - 2020-12-04
### Added
- Load limits for connections

## [v0.1.3] - 2020-11-06
### Changed
- Load case: green cement pressure test

## [v0.1.2] - 2020-11-04
### Fixed
- Load cases didn't reach axial, burst, collapse.

## [v0.1.1] - 2020-11-02
### Added
- Structure
- External pressure profile (Burst)
- Burst cases: 
  - fracture at shoe with gas gradient above
  - fraction of BHP at WH
  - gas kick profile
  - pressure test: one or more fluids behind the casing
  - production with packer: regular or depleted zone
  - production without packer: regular or depleted zone
  - stimulation
  - fluid storage: one or two fluids behind the casing. regular or depleted zone. 
- Internal and External pressure profiles (Collapse)
- Collapse cases:
  - Losses during drilling
  - Plug cementation: one or more fluids behind the casing
  - DST: partial or full evacuation
  - Production: full evacuation
  - Injection: partial or full evacuation
- Axial forces:
  - Weight in air
  - Buoyancy
  - Pressure testing
  - Pick-up
  - Thermal
  - Balloning
  - Shock load
- Cases: 
  - Running
  - Pulling
  - Cementation
  - Green cement
- API limits
- Triaxial design factor
### Changed
- Fluid density units: sg

## [v0.0.1] - 2020-08-01
Initial version
