# Test Fixtures

Fixtures used by tests must be deterministic, minimal, synthetic, and safe to publish.

Never place credentials, private data, production configuration, or large generated dependency trees in this directory.

When a fixture encodes a bug, document the expected invariant in the test that consumes it.
