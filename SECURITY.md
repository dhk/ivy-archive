# Security and private data

Do not report secrets, personal data, or sensitive archive content in a public issue. Use GitHub's private vulnerability-reporting channel if it is enabled for this repository; otherwise contact the maintainer privately through a previously established channel and share only the minimum necessary detail.

Ivy's `visibility` field classifies content but does not enforce access. Never commit private, sensitive, or unreviewed material to a public repository. Keep sensitive content in an access-controlled repository, use least-privilege credentials, and maintain an encrypted or equivalently protected backup.

Before contributing, inspect staged changes and generated registries for credentials, personal paths, private names, and content copied from another archive. If a credential is exposed, revoke or rotate it immediately; deleting the working-tree file is not enough because Git history and forks may retain it.

Security fixes should preserve the public repository as the authority for generic schemas and tooling. Do not solve a private-data incident by copying those authorities into a private repository.
