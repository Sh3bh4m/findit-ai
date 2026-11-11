# Security boundaries for this showcase

The original archives are **not** part of this repository. They contain environment configuration, client-specific deployment details and material inappropriate for public distribution.

The public code follows these basic practices:

- No live service URL, credential, token, private key, employee data or client content.
- Synthetic fixtures only; no customer screenshot or unredacted demonstration video.
- SQLite tables/columns are allowlisted and values are passed as parameters.
- Indexed semantic results are compared against current authorized source records.
- MCP example exposes synthetic read-only tools and no networked FileMaker endpoint.
- `.gitignore` excludes common secrets, databases, logs, archives and export formats; **ignore patterns are not a secret-scanning substitute**.

## Before any public release of real source

Obtain explicit written permission for intellectual property created in an employer/client context; review license obligations; verify every asset and dependency; scan both working files and Git history; keep credentials only in a secrets manager; rotate any credential already exposed. Source snapshots with `verify=False` TLS behavior or relaxed SSH host-key checks are not evidence of a hardened production deployment, and should be remediated in a separately authorized engineering task.

## No security warranty

This repository is educational and does not assert a production penetration-test, tenant-isolation audit, or compliance certification.

