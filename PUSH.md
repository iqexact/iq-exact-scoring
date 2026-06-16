# First push to GitHub

Repository: https://github.com/iqexact/iq-exact-scoring

```powershell
cd "d:\IQ тесты\iq-exact-scoring"
git init
git remote add origin https://github.com/iqexact/iq-exact-scoring.git
git add .
git status
git commit -m "Initial release: IQ Exact scoring methodology (norms v0)"
git branch -M main
git push -u origin main
```

Then on GitHub: **Releases → New release → Tag `norms-v0`** (title: `Norms v0`, paste from CHANGELOG).

## Verify locally before push

```powershell
python reference/score.py
python scripts/verify_result.py --raw 17 --norms v0
```

## Regenerate JSON after norm changes

```powershell
python "d:\IQ тесты\product\scripts\export_github_scoring.py"
```
