# Documentation Generation Workflow Update

## Summary of Changes

This update modifies the GitHub Actions workflow (`documentation_agent.yml`) responsible for automatically generating documentation based on code changes.  The primary change involves adding permissions to allow the workflow to push updated documentation back to the repository and simplifying the passing of the code diff to the documentation generation script.


## New Features / Fixes

* **Added write permissions for the `contents` API:** The workflow now includes a `permissions` block explicitly granting write access to the repository's contents. This is crucial for the workflow to successfully commit and push the generated documentation.
* **Simplified `generate_docs.py` execution:** The method of passing the code diff (`git diff`) to the `generate_docs.py` script has been streamlined.  The diff is now directly passed as an environment variable, removing the need for command-line argument handling.


## How to Use

This update does not introduce any new user-facing functions or components.  The improvement is solely within the internal workflow of the documentation generation process.  The `generate_docs.py` script remains unchanged in terms of its usage; it continues to receive the code diff via the `CODE_DIFF` environment variable.  No code example is needed for users.  The expected behavior remains:  pushing code changes triggers the workflow, which generates and commits updated documentation.
