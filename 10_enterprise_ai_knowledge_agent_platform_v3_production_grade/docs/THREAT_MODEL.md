# Threat Model

Primary threats include prompt injection in documents, secret extraction, unauthorized API use, unsafe SQL generation, poisoned indexes, malicious file uploads, and citation fabrication. Controls include untrusted-content treatment, source allowlists, extension limits, API-key authentication, read-only allowlisted SQL templates, index manifests and hashes, non-root containers, secret injection, and explicit abstention.
