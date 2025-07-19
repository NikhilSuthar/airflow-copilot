# 🤝 Contributing to Airflow Copilot

We welcome contributions of all kinds — new tools, bug fixes, documentation improvements, and more. Follow the steps below to get started:

---


## 🛠️ Development Workflow

1. **Fork the Repository**  
   → Create a feature branch using the convention: `feat/your-feature-name`

2. **Run Code Quality Checks**  
   Ensure your code passes pre-commit hooks and style checks:
   ```bash
   pre-commit run -a
   ```
   > Includes: `black`, `isort`, `flake8`, and `mypy`.

3. **Run Tests**  
   Make sure all tests pass before opening a PR:
   ```bash
   pytest -q
   ```

4. **Open a Pull Request**  
   Submit your PR and make sure all CI checks pass. Use a clear title and description. Link related issues if applicable.

---

## 💡 Tips

- Small, focused PRs are easier to review.
- Write meaningful commit messages.
- Add tests for new features or bug fixes when possible.
- For major features, consider opening a discussion or issue first.

Thanks for helping improve Airflow Copilot! 🚀
