# PIXM - Performance Information Exchange Model

![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)
![Status](https://img.shields.io/badge/Status-Prototype-orange)
![Standard](https://img.shields.io/badge/Domain-Aviation-blue)

## Overview

**PIXM (Performance Information Exchange Model)** is the next-generation open standard for the exchange of aircraft performance data. 

PIXM leverages modern data modeling technologies (XML/XSD, GML, Python) to provide a type-safe, validating, and extensible framework for performance data. It is designed to support the needs of aircraft performance data users and generators across the industry and intended for the benefit of aviation as a whole.

This repository houses the primary data model, including XML Schemas (XSD), Python reference implementations, and other utilities as determined by and at the discretion of the PIXM Change Control Board.

---

## Repository Structure

```text
.
├── schemas/                # The core PIXM XML Schema Definition files (XSD)
│   ├── PIXM_Features.xsd   # Main feature definitions (Aircraft, Engines, etc.)
│   ├── PIXM_DataTypes.xsd  # Fundamental types (Speed, Weight, Temperature)
│   ├── PIXM_Codelists.xsd  # Enumerated values (controlled vocabulary)
│   └── ...
├── examples/               # Sample PIXM datasets (Takeoff, Landing)
├── docs/                   # Specification documentation and UML diagrams
└── README.md
```

---

## Licensing & Intellectual Property

The PIXM Core Schema, Utilities, and reference implementations in this repository are released under the Apache License, Version 2.0.

**Why Apache 2.0?**
The use of the Apache 2.0 license is intended to foster the widest possible adoption of PIXM across the aviation ecosystem. We understand that aircraft performance data is critical, safety-sensitive, and commercially valuable. This licensing model was chosen to ensure legal certainty for PIXM users across the spectrum of aviation.

Key benefits of this license for PIXM adopters include:

* Commercial Friendly: You can freely use PIXM schemas and libraries inside proprietary, closed-source software (such as commercial EFBs, Flight Planning Systems, or OEM performance tools). PIXM does not force you to open-source any proprietary application code.

* Explicit Patent Grant: The Apache 2.0 license includes a patent grant clause. This ensures that any contributor to the PIXM standard grants you a license to use their contribution.

* Interoperability: This license is compatible with the vast majority of open-source and commercial software stacks used in aviation IT (Java, Python, .NET, C++, etc.).

**Note on Proprietary Data:**
While the structure (the PIXM Data Model) defined here is open, the content generated or exchanged using PIXM remains the intellectual property of the data originator (e.g., the Aircraft OEM, Airline, or Vendor), subject to their specific data use agreements.
