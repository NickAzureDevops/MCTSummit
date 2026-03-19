Open GitHub Issue 
* Show a real feature request for your project, e.g.:“Add AI study plan generator endpoint.”
* Highlight user story and acceptance criteria.

2. Generate Speckit Spec
* Use Speckit to generate a structured spec for the feature.
* Show the actual spec file in spec.md.
* Highlight sections: Purpose, Inputs/Outputs, Error handling.

3. Implement in VS Code
* Open VS Code.
* Open the spec file.
* Create or show app.py or ui.py.
* Paste the spec as a comment at the top.
* Use Copilot to generate the function/class for the AI study plan generator.
* Refine Copilot’s suggestions to match the spec.

4. Generate Tests 
* Create or show test file (e.g., test_app.py).
* Use Copilot Chat:“Generate unit tests for the AI study plan generator based on the Speckit spec.”
* Run tests and show results.

5. GitHub SDK Automation
* Show update_pr_description.py.
* Use Copilot to generate/update a script that reads the Speckit spec and updates the PR description.
* Run the script and show the PR update in GitHub.

6. Create Pull Request & CI/CD 
* Push branch and open PR.
* Show PR template, Copilot summary, Speckit spec link, and GitHub SDK automation.
* Open GitHub Actions to show tests and build running.

7. Close the Loop 
* Return to the original issue.
* Show the workflow: Issue → Spec → Code → Tests → Automation → PR → CI → Merge.
